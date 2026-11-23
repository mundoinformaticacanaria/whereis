"""Fixed-destination systemd relays. Python coordinates; it never forwards traffic."""
import ipaddress
import os
from pathlib import Path
import signal
import socket
import subprocess as sp
import time
from urllib.parse import urlsplit

APPROVED = ("api.github.com", "github.com", "openrouter.ai")
PROXY = "/usr/lib/systemd/systemd-socket-proxyd"
ACTIVATE = "/usr/bin/systemd-socket-activate"


def endpoint(url):
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.hostname not in APPROVED or parsed.username is not None
            or parsed.password is not None or parsed.port not in (None, 443) or parsed.fragment):
        raise ValueError("Unapproved HTTPS destination")
    return parsed.hostname


def public_pins(host, resolver=socket.getaddrinfo):
    if host not in APPROVED:
        raise ValueError("Unapproved hostname")
    records = resolver(host, 443, type=socket.SOCK_STREAM)
    addresses = {row[4][0] for row in records}
    if not addresses or any(not ipaddress.ip_address(address).is_global
                            or ipaddress.ip_address(address).is_multicast
                            or ipaddress.ip_address(address).is_reserved for address in addresses):
        raise ValueError("DNS returned a local/private/special destination")
    ipv4 = sorted(address for address in addresses if ipaddress.ip_address(address).version == 4)
    if not ipv4:
        raise ValueError("No validated IPv4 pin available")
    return ipv4[0]  # Numeric target is pinned for the lifetime of this relay.


class Relay:
    def __init__(self, host, directory, resolver=socket.getaddrinfo):
        self.host = endpoint("https://" + host)
        self.pin = public_pins(host, resolver)
        self.path = Path(directory) / (str(APPROVED.index(host)) + ".sock")
        self.process = None

    def start(self):
        if self.path.exists() or not Path(PROXY).is_file():
            raise RuntimeError("Relay preconditions failed")
        command = [ACTIVATE, "--listen=" + str(self.path), PROXY, "--connections-max=8", self.pin + ":443"]
        self.process = sp.Popen(command, stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL,
                                close_fds=True, start_new_session=True)
        for _ in range(100):
            if self.process.poll() is not None:
                raise RuntimeError("Standard fixed relay failed")
            if self.path.exists():
                return
            time.sleep(0.01)
        self.close()
        raise RuntimeError("Standard fixed relay timeout")

    def close(self):
        if self.process is None or self.process.poll() is not None:
            return
        os.killpg(self.process.pid, signal.SIGTERM)
        try:
            self.process.wait(timeout=2)
        except sp.TimeoutExpired:
            os.killpg(self.process.pid, signal.SIGKILL)
            self.process.wait()


def inside_relays():
    """High ports need no capabilities; real Git/GH compatibility remains a separate gate."""
    processes = []
    for index, host in enumerate(APPROVED, 2):
        command = [ACTIVATE, "--listen=127.0.0." + str(index) + ":8443",
                   PROXY, "--connections-max=8", "/run/whereis-egress/" + str(APPROVED.index(host)) + ".sock"]
        processes.append(sp.Popen(command, stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL, close_fds=True))
    for _ in range(100):
        ready = True
        if any(process.poll() is not None for process in processes):
            raise RuntimeError('Private relay startup failed')
        for index in range(2, len(APPROVED) + 2):
            try:
                with socket.create_connection(('127.0.0.' + str(index), 8443), timeout=0.05):
                    pass
            except OSError:
                ready = False
        if ready:
            break
        time.sleep(0.01)
    else:
        raise RuntimeError('Private relay readiness timeout')
    command = ["/usr/bin/python3", str(Path(__file__).with_name("network_verify.py"))]
    os.execv(command[0], command)


if __name__ == "__main__":
    inside_relays()
