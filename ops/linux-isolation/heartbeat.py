"""Issue-scoped heartbeat. Transport is injected; this module never infers authority."""
import datetime as dt
import re
import uuid
from zoneinfo import ZoneInfo

UTC = dt.timezone.utc
ENTRY = re.compile(r"^(\S+) \[Atlantic/Canary .+?\] PROGRAMADOR-LINUX #(\d+) intervencion=(\S+) (INICIO|FIN)(?: (.*))?$")


class HeartbeatBlocked(RuntimeError):
    pass


class Conflict(RuntimeError):
    pass


def pending(text, issue, now):
    starts, finishes = {}, {}
    for line in text.splitlines():
        match = ENTRY.fullmatch(line)
        if not match or int(match[2]) != issue:
            continue  # Preserve historical text; never repair it.
        try:
            stamp = dt.datetime.strptime(match[1], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
        except ValueError as exc:
            raise HeartbeatBlocked("Uncertain UTC history for this issue") from exc
        target = starts if match[4] == "INICIO" else finishes
        if match[3] in target:
            raise HeartbeatBlocked("Duplicate intervention ID in history")
        target[match[3]] = stamp
    return [key for key, start in starts.items()
            if (key not in finishes or finishes[key] < start)
            and (now - start).total_seconds() < 1800]


def line_at(now, issue, intervention, event, result=""):
    if now.tzinfo is None or event not in ("INICIO", "FIN") or issue < 1:
        raise ValueError("Invalid heartbeat input")
    if not re.fullmatch(r"[a-zA-Z0-9-]+", intervention):
        raise ValueError("Invalid intervention ID")
    if event == "FIN" and not re.fullmatch(r"[A-Z0-9_]{1,100}", result):
        raise ValueError("Invalid result")
    stamp = now.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    local = now.astimezone(ZoneInfo("Atlantic/Canary")).isoformat(timespec="seconds")
    return f"{stamp} [Atlantic/Canary {local}] PROGRAMADOR-LINUX #{issue} intervencion={intervention} {event}" + (f" {result}" if result else "")


class Heartbeat:
    """read() -> (text, sha); write(text, sha) must reject stale SHA."""
    def __init__(self, read, write, clock=None):
        self.read, self.write = read, write
        self.clock = clock or (lambda: dt.datetime.now(UTC))
        self.current = None

    def start(self, issue):
        if self.current:
            raise HeartbeatBlocked("Intervention already open")
        intervention = "linux-" + uuid.uuid4().hex
        for _ in range(3):
            text, sha = self.read()  # Transport errors propagate: no model work.
            now = self.clock()
            if pending(text, issue, now):
                raise HeartbeatBlocked("Issue intervention younger than 30 minutes")
            entry = line_at(now, issue, intervention, "INICIO")
            new = "\n".join(([entry] + text.splitlines())[:100]) + "\n"
            try:
                self.write(new, sha)
            except Conflict:
                continue
            # Verify persistence without manufacturing a successful start.
            latest, _ = self.read()
            if entry not in latest.splitlines():
                raise HeartbeatBlocked("Start persistence uncertain")
            self.current = issue, intervention
            return intervention
        raise HeartbeatBlocked("Unresolved heartbeat write conflict")

    def finish(self, result):
        if not self.current:
            raise HeartbeatBlocked("No owned start to finish")
        issue, intervention = self.current
        for _ in range(3):
            text, sha = self.read()
            # A late finish cannot finish another intervention, or fabricate an evicted start.
            owned = [m for row in text.splitlines() if (m := ENTRY.fullmatch(row))
                     and int(m[2]) == issue and m[3] == intervention]
            if len(owned) != 1 or owned[0][4] != "INICIO":
                raise HeartbeatBlocked("Owned start absent, duplicated or already finished")
            now = self.clock()
            start = dt.datetime.strptime(owned[0][1], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
            if now < start:
                raise HeartbeatBlocked("Clock precedes start")
            entry = line_at(now, issue, intervention, "FIN", result)
            new = "\n".join(([entry] + text.splitlines())[:100]) + "\n"
            try:
                self.write(new, sha)
            except Conflict:
                continue
            latest, _ = self.read()
            if entry not in latest.splitlines():
                raise HeartbeatBlocked("Finish persistence uncertain")
            self.current = None
            return
        raise HeartbeatBlocked("Unresolved finish conflict")
