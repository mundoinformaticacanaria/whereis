"""Unauthenticated TLS smoke; never accesses a model completion endpoint."""
import json
import subprocess as sp
from guard import require_sandbox
from egress import APPROVED

require_sandbox()
base = ['curl', '--silent', '--show-error', '--head', '--noproxy', '*', '--proto', '=https',
        '--proto-redir', '=https', '--tlsv1.2', '--connect-timeout', '3', '--max-time', '8']
results = {}
for host in APPROVED:
    target = host + ':443:127.0.0.' + str(APPROVED.index(host) + 2) + ':8443'
    result = sp.run(base + ['--connect-to', target, 'https://' + host + '/'], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    results['tls_' + host] = result.returncode == 0
    print('TLS_RESULT', host, result.returncode)
# Certificate hostname verification must remain active through the fixed relay.
result = sp.run(base + ['--connect-to', 'example.invalid:443:127.0.0.2:8443', 'https://example.invalid/'],
                stdout=sp.DEVNULL, stderr=sp.DEVNULL)
results['wrong_certificate_rejected'] = result.returncode == 60
for host in ('example.invalid', '169.254.169.254', '127.0.0.1', '10.0.0.1'):
    result = sp.run(base + ['https://' + host + '/'], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    results['unapproved_' + host] = result.returncode != 0
print('NETWORK_SMOKE ' + json.dumps(results, sort_keys=True))
raise SystemExit(not all(results.values()))
