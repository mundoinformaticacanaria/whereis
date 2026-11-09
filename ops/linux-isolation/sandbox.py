#!/usr/bin/env python3
"""Mandatory WHEREIS entry. Offline integration is available; real execution is gated."""
import json
import os
from pathlib import Path
import resource
import signal
import stat
import subprocess as sp
import sys
import tempfile
import uuid

HOME = Path.home()
CONTROL = Path(__file__).resolve().parent
CONFIG = HOME / ".config/whereis-programador"
REPO = HOME / "whereis"
NAMESPACES = ("user", "pid", "mnt", "ipc", "net", "uts", "cgroup")
MODES = ("probe", "selftest", "version", "paths", "config", "agents", "tls-smoke")
LIMITS = {"memory.max": "335544320", "memory.swap.max": "0", "pids.max": "48"}


def private_path(path, directory=False):
    meta = path.lstat()
    if path.is_symlink() or meta.st_uid != os.getuid():
        raise RuntimeError("Unexpected path owner/link")
    if directory != stat.S_ISDIR(meta.st_mode) or (not directory and meta.st_nlink != 1):
        raise RuntimeError("Unexpected path type/link count")
    for parent in path.parents:
        if parent.is_symlink():
            raise RuntimeError("Symlink ancestor rejected")


def verify_scope():
    cgroup = Path("/sys/fs/cgroup") / Path("/proc/self/cgroup").read_text().strip().split("::", 1)[1].lstrip("/")
    observed = {key: (cgroup / key).read_text().strip() for key in (*LIMITS, "cpu.max")}
    if any(observed[k] != v for k, v in LIMITS.items()):
        raise RuntimeError("Required cgroup limits unavailable")
    quota, period = observed["cpu.max"].split()
    if quota == "max" or int(quota) / int(period) > 0.25:
        raise RuntimeError("CPU limit unavailable")
    print("WHEREIS_CGROUP_VERIFIED " + json.dumps(observed), flush=True)


def bubblewrap(mode, temporary, relay_directory=None):
    from engine import instance
    values = instance(CONFIG / "instance.env")
    if values["IDENTITY"] != "PROGRAMADOR-LINUX" or values["REPOSITORY"] != "mundoinformaticacanaria/whereis":
        raise RuntimeError("Wrong instance")
    if values["REPO_DIR"] != str(REPO):
        raise RuntimeError("Unexpected repository path")
    binary = Path(values["OPENCODE"])
    if binary != HOME / ".opencode/bin/opencode":
        raise RuntimeError("Unreviewed shared binary path")
    private_path(CONTROL, True)
    private_path(CONFIG, True)
    private_path(REPO, True)
    marker = {"uid": os.getuid(), "home": str(HOME),
              "namespaces": {n: os.stat("/proc/self/ns/" + n).st_ino for n in NAMESPACES}}
    (temporary / "marker.json").write_text(json.dumps(marker))
    hosts = "127.0.0.1 localhost\n::1 localhost\n"
    if mode == "tls-smoke":
        from egress import APPROVED
        hosts += ''.join(f"127.0.0.{index} {host}\n" for index, host in enumerate(APPROVED, 2))
    (temporary / "hosts").write_text(hosts)
    (temporary / "resolv.conf").write_text("nameserver 127.0.0.1\noptions attempts:1 timeout:1\n")
    (temporary / "passwd").write_text(f"{HOME.name}:x:{os.getuid()}:{os.getgid()}:WHEREIS:{HOME}:/bin/bash\n")
    (temporary / "group").write_text(f"{HOME.name}:x:{os.getgid()}:\n")
    (temporary / "nsswitch.conf").write_text("passwd: files\ngroup: files\nhosts: files dns\n")
    args = ["/usr/bin/bwrap", "--unshare-all", "--disable-userns", "--assert-userns-disabled",
            "--die-with-parent", "--new-session", "--cap-drop", "ALL", "--clearenv",
            "--hostname", "whereis-offline", "--proc", "/proc", "--dev", "/dev",
            "--size", str(8 * 1024**2), "--tmpfs", "/dev/shm",
            "--size", str(32 * 1024**2), "--tmpfs", "/tmp",
            "--size", str(96 * 1024**2), "--tmpfs", str(HOME)]
    for path in ("/usr",):
        args += ["--ro-bind", path, path]
    for path in ("/bin", "/sbin", "/lib", "/lib64"):
        source = Path(path)
        if source.is_symlink():
            args += ["--symlink", os.readlink(source), path]
        elif source.exists():
            args += ["--ro-bind", path, path]
    for name in ("hosts", "resolv.conf", "passwd", "group", "nsswitch.conf"):
        args += ["--ro-bind", str(temporary / name), "/etc/" + name]
    for path in ("/etc/ssl/certs", "/etc/ca-certificates.conf", "/etc/os-release", "/usr/share/zoneinfo"):
        if Path(path).exists():
            args += ["--ro-bind", path, path]
    args += ["--ro-bind", str(temporary / "marker.json"), "/run/whereis-isolation.json",
             "--ro-bind", str(CONTROL), str(CONTROL),
             "--ro-bind", str(REPO), str(REPO),
             "--ro-bind", str(binary), str(binary)]
    for directory in (".local/state/whereis-programador/logs", ".local/state/whereis-programador/recovery",
                      ".local/share/whereis-programador", ".cache/whereis-programador",
                      ".config/whereis-programador/gh", ".config/whereis-programador/xdg/opencode",
                      ".local/state/whereis-programador/workdir/.opencode"):
        args += ["--dir", str(HOME / directory)]
    config = CONFIG / "xdg/opencode"
    for src, dest in ((CONFIG / "instance.env", CONFIG / "instance.env"),
                      (config / "opencode.json", config / "opencode.json"),
                      (config / "agents", config / "agents"),
                      (config / "agents", HOME / ".local/state/whereis-programador/workdir/.opencode/agents")):
        args += ["--ro-bind", str(src), str(dest)]
    env = {"HOME": str(HOME), "USER": HOME.name, "LOGNAME": HOME.name,
           "PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "TMPDIR": "/tmp", "TZ": "UTC",
           "PYTHONDONTWRITEBYTECODE": "1", "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_TERMINAL_PROMPT": "0",
           "OPENCODE_DISABLE_AUTOUPDATE": "1", "OPENCODE_DISABLE_MODELS_FETCH": "1",
           "GH_CONFIG_DIR": str(CONFIG / "gh")}
    for key in ("REPOSITORY", "IDENTITY", "INSTANCE_ID", "AGENT", "MODEL", "OPENCODE", "REPO_DIR", "STATE_DIR",
                "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME", "XDG_STATE_HOME", "MODEL_TIMEOUT"):
        env[key] = values[key]
    for key, value in env.items():
        args += ["--setenv", key, value]
    if mode == "tls-smoke":
        # Only trusted initialization has these capabilities, in the private namespaces.
        # setpriv removes all capabilities before any verification/runner process.
        args += ["--cap-add", "CAP_NET_BIND_SERVICE", "--cap-add", "CAP_SETPCAP",
                 "--ro-bind", str(relay_directory), "/run/whereis-egress"]
    cwd = HOME / ".local/state/whereis-programador/workdir"
    if mode == "tls-smoke":
        command = ["/usr/bin/python3", str(CONTROL / "egress.py")]
    elif mode == "probe":
        command = ["/usr/bin/python3", str(CONTROL / "probe.py")]
    elif mode == "selftest":
        command = ["/usr/bin/python3", str(CONTROL / "review.py"), "--self-test"]
    else:
        command = [str(binary), "--version"] if mode == "version" else [str(binary), "debug", mode]
    return args + ["--chdir", str(cwd), "--remount-ro", "/", "--", *command]


def confined(mode):
    verify_scope()
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_NOFILE, (128, 128))
    resource.setrlimit(resource.RLIMIT_FSIZE, (16 * 1024**2, 16 * 1024**2))
    with tempfile.TemporaryDirectory(prefix="whereis-offline-", dir=HOME / ".local/state/whereis-programador/tmp") as name:
        os.chmod(name, 0o700)
        relays = []
        try:
            directory = Path(name) / 'egress'
            if mode == 'tls-smoke':
                from egress import APPROVED, Relay
                directory.mkdir(mode=0o700)
                for host in APPROVED:
                    relay = Relay(host, directory)
                    relays.append(relay)
                    relay.start()
            process = sp.Popen(bubblewrap(mode, Path(name), directory), close_fds=True, start_new_session=True)
            try:
                return process.wait(timeout=75)
            except sp.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
                raise RuntimeError("Offline validation timeout; sandbox tree terminated")
        finally:
            for relay in reversed(relays):
                relay.close()


def main():
    os.umask(0o077)
    args = sys.argv[1:]
    if not args or args == ["--run"]:
        raise RuntimeError("Real runner BLOCKED: dedicated credentials, reviewed egress, QA and project gates pending")
    if len(args) == 2 and args[0] == "--offline" and args[1] in MODES:
        unit = "whereis-isolation-" + uuid.uuid4().hex[:12]
        command = ["/usr/bin/systemd-run", "--user", "--scope", "--quiet", "--collect", "--unit=" + unit,
                   "-p", "MemoryMax=320M", "-p", "MemorySwapMax=0", "-p", "TasksMax=48", "-p", "CPUQuota=25%",
                   "/usr/bin/python3", str(CONTROL / "sandbox.py"), "--scoped", args[1]]
        return sp.run(command, close_fds=True).returncode
    if len(args) == 2 and args[0] == "--scoped" and args[1] in MODES:
        return confined(args[1])
    raise RuntimeError("Unsupported entry; no unsandboxed fallback")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print("WHEREIS_FAIL_CLOSED: " + str(exc), file=sys.stderr)
        sys.exit(78)
