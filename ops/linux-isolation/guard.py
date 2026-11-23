"""Reject accidental legacy entry outside the verified namespace tree."""
import json
import os
from pathlib import Path


def require_sandbox():
    marker = Path("/run/whereis-isolation.json")
    if not marker.is_file():
        raise RuntimeError("WHEREIS requires the mandatory sandbox launcher")
    host = json.loads(marker.read_text())
    for name, inode in host["namespaces"].items():
        if os.stat(f"/proc/self/ns/{name}").st_ino == inode:
            raise RuntimeError("Host namespace retained: " + name)
    status = dict(row.split(":", 1) for row in Path("/proc/self/status").read_text().splitlines() if ":" in row)
    if status["NoNewPrivs"].strip() != "1" or int(status["CapEff"].strip(), 16) or int(status["CapPrm"].strip(), 16):
        raise RuntimeError("Unexpected sandbox privileges")
    if os.getuid() != host["uid"] or os.environ.get("HOME") != host["home"]:
        raise RuntimeError("Unexpected sandbox identity")
    if Path("/sys").exists() and list(Path("/sys").iterdir()):
        raise RuntimeError("Host sysfs exposed")
