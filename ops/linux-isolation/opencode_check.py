"""Initialize isolated metadata and verify agent discovery without inference."""
import json
import os
import subprocess as sp
import time
from guard import require_sandbox

require_sandbox()
result = sp.run([os.environ['OPENCODE'], 'debug', 'config'], capture_output=True, text=True, timeout=20)
if result.returncode:
    raise SystemExit(1)
# V2 metadata initialization is asynchronous. An exit-0 empty list is not readiness.
deadline = time.monotonic() + 40
while time.monotonic() < deadline:
    result = sp.run([os.environ['OPENCODE'], 'debug', 'agents'], capture_output=True, text=True, timeout=10)
    if result.returncode:
        raise SystemExit(1)
    matches = sum(agent.get('name') == 'whereis-programador' for agent in json.loads(result.stdout))
    if matches == 1:
        print('AGENT_EXACT_MATCHES', matches)
        raise SystemExit(0)
    if matches > 1:
        raise SystemExit(1)
    time.sleep(0.25)
print('AGENT_DISCOVERY_NOT_READY')
raise SystemExit(1)
