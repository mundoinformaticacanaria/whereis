"""Runner integration: own credentials, generic engine invocation and optimistic heartbeat."""
import base64
import json
import os
from pathlib import Path
import subprocess as sp
from engine import instance, credential_environment
from heartbeat import Heartbeat, Conflict, HeartbeatBlocked

CONFIG = Path.home() / '.config/whereis-programador'
LOG = 'repos/mundoinformaticacanaria/whereis/contents/docs/logs/programador-linux.log'


def api(arguments, payload=None):
    command = ['gh', 'api', LOG, *arguments]
    result = sp.run(command, input=json.dumps(payload) if payload is not None else None,
                    capture_output=True, text=True, timeout=30, close_fds=True)
    if result.returncode:
        if 'HTTP 409' in result.stderr: raise Conflict()
        raise HeartbeatBlocked('Heartbeat API failure; no response or credentials logged')
    return json.loads(result.stdout)


def read_log():
    result = api(['-f', 'ref=ops/logs', '--method', 'GET'])
    return base64.b64decode(result['content']).decode(), result['sha']


def write_log(text, sha):
    api(['--method', 'PUT', '--input', '-'], {'message': 'ops: PROGRAMADOR-LINUX heartbeat',
        'branch': 'ops/logs', 'sha': sha, 'content': base64.b64encode(text.encode()).decode()})


heartbeat = Heartbeat(read_log, write_log)


def invoke_engine(prompt, output):
    values = instance(CONFIG / 'instance.env')
    profiles = json.loads(Path(__file__).with_name('provider-profiles.json').read_text())
    env = dict(os.environ)
    env.update(credential_environment(values, profiles, CONFIG / 'auth/provider.json'))
    command = [values['OPENCODE'], 'run', '--standalone', '--agent', values['AGENT'],
               '--model', values['MODEL'], '--format', 'json', prompt]
    with output.open('w') as stream:
        result = sp.run(command, cwd=values['REPO_DIR'], env=env, stdout=stream, stderr=sp.STDOUT,
                        timeout=int(values['MODEL_TIMEOUT']), close_fds=True)
    if result.returncode:
        raise RuntimeError('Engine failure; private recovery retained')
    texts = []
    for row in output.read_text().splitlines():
        try:
            event = json.loads(row)
        except json.JSONDecodeError:
            continue
        if event.get('type') == 'text': texts.append(event.get('part', {}).get('text', ''))
    return '\n'.join(texts)
