#!/usr/bin/env python3
"""Offline, dependency-free preflight for a documentation pull request."""
import pathlib
import re
import subprocess
import sys

TEXT_SUFFIXES = {'.md', '.txt', '.yaml', '.yml', '.json', '.sh', '.py', '.xml', '.kt', '.gradle', '.properties'}
SUSPECT_SECRETS = re.compile(rb'(?:-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----|github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{35})')


def git(*args):
    return subprocess.run(['git', *args], capture_output=True, check=True).stdout


def main():
    if len(sys.argv) != 2:
        print('Usage: python3 scripts/check-documentation.py <base-commit>', file=sys.stderr)
        return 2
    base = sys.argv[1]
    try:
        git('rev-parse', '--verify', f'{base}^{{commit}}')
        git('rev-parse', '--verify', 'HEAD^{commit}')
        git('diff', '--check', f'{base}...HEAD')
        changed = git('diff', '--name-only', '--diff-filter=ACMR', '-z', f'{base}...HEAD').split(b'\0')
    except subprocess.CalledProcessError:
        print('FAIL: missing Git base/HEAD or whitespace errors in diff (details suppressed).', file=sys.stderr)
        return 1
    failures = 0
    inspected = 0
    for raw in filter(None, changed):
        path = pathlib.Path(raw.decode('utf-8', errors='surrogateescape'))
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        inspected += 1
        try:
            content = path.read_bytes()
            decoded = content.decode('utf-8')
        except (OSError, UnicodeError):
            print('FAIL: changed text file unreadable or not UTF-8 (path suppressed).', file=sys.stderr)
            failures += 1
            continue
        if not content:
            print('FAIL: changed text file empty (path suppressed).', file=sys.stderr)
            failures += 1
        if any(line.startswith('<<<<<<< ') or line == '=======' or line.startswith('>>>>>>> ') for line in decoded.splitlines()):
            print('FAIL: unresolved merge markers in changed text (path suppressed).', file=sys.stderr)
            failures += 1
        if SUSPECT_SECRETS.search(content):
            print('FAIL: possible secret in changed text (content/path suppressed).', file=sys.stderr)
            failures += 1
    if failures:
        return 1
    print(f'PASS: diff whitespace and {inspected} changed text file(s) checked; no configured patterns detected.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
