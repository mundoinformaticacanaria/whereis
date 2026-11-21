"""Apply only a fully tested WHEREIS candidate; keep real execution fail-closed."""
import ast
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess as sp
from engine import instance

HERE = Path(__file__).resolve().parent
HOME = Path.home()
STATE = HOME / '.local/state/whereis-programador'
TARGET = HOME / '.local/libexec/whereis-programador'
CONFIG = HOME / '.config/whereis-programador'
QWEN = 'openrouter/qwen/qwen3.8-27b:free'
INSTALL = ('sandbox.py','guard.py','engine.py','heartbeat.py','runner_support.py','review.py',
           'egress.py','network_verify.py','opencode_check.py','probe.py','provider-profiles.json',
           'configure-model','github-review')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic(path, content, mode=0o600):
    temporary = path.with_name(path.name + '.isolation-new')
    with temporary.open('xb') as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.chmod(mode)
    temporary.replace(path)


def preconditions():
    from sandbox import private_path
    for path in (CONFIG, TARGET, STATE, HOME / 'whereis'):
        private_path(path, True)
    backup = Path((STATE / 'isolation-backup-path').read_text().strip())
    if backup.parent != STATE / 'backups' or backup.is_symlink():
        raise RuntimeError('Unexpected recovery point')
    manifest = json.loads((backup / 'manifest.json').read_text())
    for path in (CONFIG / 'instance.env', TARGET / 'review.py', TARGET / 'github-review', TARGET / 'configure-model'):
        private_path(path)
        key = str(path.relative_to(HOME))
        if digest(path) != manifest[key]['sha256'] or digest(backup / 'files' / key) != manifest[key]['sha256']:
            raise RuntimeError('Concurrent change or invalid backup; no overwrite')
    if instance(CONFIG / 'instance.env')['MODEL'] != QWEN:
        raise RuntimeError('Current Qwen selector changed')
    return backup


def validate():
    for path in HERE.glob('*.py'):
        ast.parse(path.read_text())
    sp.run(['bash','-n',str(HERE/'github-review')],check=True)
    sp.run(['python3','-m','unittest','discover','-s',str(HERE),'-p','test_*.py','-q'],check=True)
    for mode in ('probe','selftest','agents','tls-smoke'):
        result = sp.run(['python3',str(HERE/'sandbox.py'),'--offline',mode],capture_output=True,text=True)
        (HERE/(mode+'-release.output')).write_text(result.stdout+result.stderr)
        print('PREINSTALL',mode,result.returncode,flush=True)
        if result.returncode:
            raise RuntimeError('Candidate validation failed: '+mode)


def main():
    os.umask(0o077)
    preconditions()
    validate()
    with (STATE/'review.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        backup = preconditions()  # Recheck after every test and immediately before mutations.
        values = instance(CONFIG/'instance.env')
        values.pop('OPENROUTER_ENV',None)
        values['GH_CONFIG_DIR'] = str(CONFIG/'gh')
        values['PROVIDER_CREDENTIAL_FILE'] = str(CONFIG/'auth/provider.json')
        for path in (CONFIG/'gh',CONFIG/'auth'):
            if path.exists() and (path.is_symlink() or not path.is_dir()):
                raise RuntimeError('Unexpected dedicated authentication directory')
            path.mkdir(mode=0o700,exist_ok=True)
        # A partial installation must remain stopped, rather than restore an unsafe entry.
        atomic(TARGET/'github-review',b'#!/bin/sh\necho "WHEREIS BLOCKED: isolation installation incomplete" >&2\nexit 78\n')
        for name in INSTALL:
            if name != 'github-review': atomic(TARGET/name,(HERE/name).read_bytes())
        atomic(CONFIG/'instance.env',(''.join(k+'='+v+'\n' for k,v in values.items())).encode())
        policy = sp.run(['git','-C',str(HOME/'whereis'),'show','origin/main:docs/logs/README.md'],
                        check=True,capture_output=True).stdout
        # Adopt only after code, exact-byte policy tests and actual integration tests pass.
        atomic(STATE/'heartbeat-policy.sha256',(hashlib.sha256(policy).hexdigest()+'\n').encode())
        atomic(TARGET/'github-review',(HERE/'github-review').read_bytes())
        manifest = {name:digest(TARGET/name) for name in INSTALL}
        atomic(STATE/'isolation-installed.json',json.dumps({'files':manifest,'real_execution':'BLOCKED',
            'backup_verified':True,'qwen_preserved':values['MODEL']==QWEN},indent=2).encode())
        assert values['MODEL'] == QWEN
        print('APPLIED_WHEREIS_FILES',len(INSTALL),'BACKUP_RETAINED','QWEN_PRESERVED','REAL_EXECUTION_BLOCKED')


if __name__ == '__main__':main()
