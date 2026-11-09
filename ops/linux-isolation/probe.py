"""Negative probes never read bytes from excluded paths or signal host processes."""
import errno
import json
import os
from pathlib import Path
import resource
import socket
import subprocess as sp
from guard import require_sandbox

require_sandbox()
checks = {}
home = Path.home()
marker = json.loads(Path('/run/whereis-isolation.json').read_text())
checks['uid_home_preserved'] = os.getuid() == marker['uid'] and str(home) == marker['home']
for namespace, inode in marker['namespaces'].items():
    checks['private_' + namespace] = os.stat('/proc/self/ns/' + namespace).st_ino != inode
status = dict(row.split(':', 1) for row in Path('/proc/self/status').read_text().splitlines() if ':' in row)
checks['no_new_privileges'] = status['NoNewPrivs'].strip() == '1'
checks['capabilities_zero'] = int(status['CapEff'].strip(), 16) == int(status['CapPrm'].strip(), 16) == 0
for label, path in {
    'crm_path': home / 'crm-remisiones-veterinarias',
    'shared_gh': home / '.config/gh', 'shared_ssh': home / '.ssh',
    'system_bus': Path('/run/dbus/system_bus_socket'),
    'user_bus': Path('/run/user') / str(os.getuid()) / 'bus',
    'host_canary': home / '.local/state/whereis-programador/host-canary',
    'host_sysfs': Path('/sys/fs/cgroup'),
}.items():
    checks['excluded_' + label] = not path.exists()
checks['no_credentials_in_environment'] = not any(any(t in k for t in ('TOKEN', 'API_KEY', 'SSH_AUTH_SOCK', 'DBUS_SESSION')) for k in os.environ)
for label, path in [('repo', home / 'whereis/AGENTS.md'), ('control', Path(__file__).parent / 'sandbox.py')]:
    try:
        fd = os.open(path, os.O_WRONLY)  # Do not write or truncate.
    except OSError as exc:
        checks[label + '_readonly'] = exc.errno in (errno.EROFS, errno.EACCES)
    else:
        os.close(fd)
        checks[label + '_readonly'] = False
test = Path('/tmp/write-test')
test.write_text('synthetic')
checks['private_tmp_write'] = test.read_text() == 'synthetic'
checks['tmpfs_bounded'] = os.statvfs('/tmp').f_blocks * os.statvfs('/tmp').f_frsize <= 32 * 1024**2
checks['home_bounded'] = os.statvfs(home).f_blocks * os.statvfs(home).f_frsize <= 96 * 1024**2
checks['file_limit'] = resource.getrlimit(resource.RLIMIT_FSIZE)[0] == 16 * 1024**2
checks['core_disabled'] = resource.getrlimit(resource.RLIMIT_CORE)[0] == 0
canary = marker['canary']
try:
    os.kill(canary['pid'], 0)  # Existence check only; no signal is sent.
except ProcessLookupError:
    checks['host_pid_hidden'] = True
else:
    checks['host_pid_hidden'] = False
for label, family, address in [('host_tcp_socket', socket.AF_INET, ('127.0.0.1', canary['tcp_port'])),
                                ('host_unix_socket', socket.AF_UNIX, canary['unix']),
                                ('host_abstract_socket', socket.AF_UNIX, '\0' + canary['abstract'])]:
    sock = socket.socket(family); sock.settimeout(0.2)
    try:
        sock.connect(address)
    except OSError:
        checks[label + '_hidden'] = True
    else:
        checks[label + '_hidden'] = False
    finally:
        sock.close()
for label, command in [('new_userns', ['unshare', '-Ur', 'true']), ('sudo', ['sudo', '-n', 'true'])]:
    checks[label + '_rejected'] = sp.run(command, stdout=sp.DEVNULL, stderr=sp.DEVNULL).returncode != 0
for host in ('127.0.0.1', '169.254.169.254', '10.0.0.1', '1.1.1.1'):
    sock = socket.socket()
    sock.settimeout(0.2)
    try:
        sock.connect((host, 443))
    except OSError:
        checks['network_denied_' + host] = True
    else:
        checks['network_denied_' + host] = False
    finally:
        sock.close()
print(json.dumps(checks, sort_keys=True))
failed = [name for name, passed in checks.items() if not passed]
print('ISOLATION_PROBE', len(checks) - len(failed), 'PASS', len(failed), 'FAIL', failed)
raise SystemExit(bool(failed))
