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
    if not addresses or any(not ipaddress.ip_address(address).is_global for address in addresses):
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
    """Bind private loopback HTTPS, then remove capabilities before the test program."""
    for index, host in enumerate(APPROVED, 2):
        command = [ACTIVATE, "--listen=127.0.0." + str(index) + ":443",
                   "/usr/bin/setpriv", "--bounding-set=-all", "--inh-caps=-all", "--ambient-caps=-all",
                   "--no-new-privs", PROXY, "--connections-max=8", "/run/whereis-egress/" + str(APPROVED.index(host)) + ".sock"]
        sp.Popen(command, stdin=sp.DEVNULL, stdout=sp.DEVNULL, stderr=sp.DEVNULL, close_fds=True)
    command = ["/usr/bin/setpriv", "--bounding-set=-all", "--inh-caps=-all", "--ambient-caps=-all",
               "--no-new-privs", "/usr/bin/python3", str(Path(__file__).with_name("network_verify.py"))]
    os.execv(command[0], command)


if __name__ == "__main__":
    inside_relays()
