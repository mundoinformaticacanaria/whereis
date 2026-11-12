"""Synthetic negative gates for #100; no real credentials, API calls or runner invocation.

These tests validate the provider credential parser only. They do NOT certify
sandbox mounts, GH permissions, process-level isolation or host egress.
"""
import json
import os
from pathlib import Path
import tempfile
import unittest

from engine import credential_environment

PROFILES = {
    "fixture": {
        "approved": True,
        "endpoint": "https://example.invalid",
        "package": "fixture-only",
        "credential_env": "FIXTURE_KEY",
    }
}
VALUES = {"MODEL": "fixture/offline"}


class CredentialFixtureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.secret = self.root / "own.json"

    def write(self, payload, mode=0o600):
        self.secret.write_text(payload)
        self.secret.chmod(mode)
        return self.secret

    def test_private_dedicated_fixture_is_accepted(self):
        path = self.write(json.dumps({"FIXTURE_KEY": "not-a-token-fixture"}))
        self.assertEqual(
            credential_environment(VALUES, PROFILES, path),
            {"FIXTURE_KEY": "not-a-token-fixture"},
        )

    def test_absent_file_fails_closed(self):
        with self.assertRaises(FileNotFoundError):
            credential_environment(VALUES, PROFILES, self.secret)

    def test_world_readable_file_rejected(self):
        with self.assertRaises(ValueError):
            credential_environment(VALUES, PROFILES, self.write('{"FIXTURE_KEY":"x"}', 0o644))

    def test_group_readable_file_rejected(self):
        with self.assertRaises(ValueError):
            credential_environment(VALUES, PROFILES, self.write('{"FIXTURE_KEY":"x"}', 0o640))

    def test_symlink_rejected(self):
        target = self.root / "target.json"
        target.write_text('{"FIXTURE_KEY":"x"}')
        target.chmod(0o600)
        self.secret.symlink_to(target)
        with self.assertRaises(ValueError):
            credential_environment(VALUES, PROFILES, self.secret)

    def test_symlinked_parent_rejected(self):
        actual = self.root / "private"
        actual.mkdir()
        secret = actual / "own.json"
        secret.write_text('{"FIXTURE_KEY":"x"}')
        secret.chmod(0o600)
        alias = self.root / "alias"
        alias.symlink_to(actual, target_is_directory=True)
        with self.assertRaises(ValueError):
            credential_environment(VALUES, PROFILES, alias / "own.json")

    def test_file_replaced_between_stat_and_open_rejected(self):
        from unittest.mock import patch
        path = self.write('{"FIXTURE_KEY":"x"}')
        original_open = os.open

        def replace_before_open(candidate, flags, *args, **kwargs):
            if Path(candidate) == path:
                path.unlink()
                path.write_text('{"FIXTURE_KEY":"replacement"}')
                path.chmod(0o600)
            return original_open(candidate, flags, *args, **kwargs)

        with patch("engine.os.open", side_effect=replace_before_open):
            with self.assertRaises(ValueError):
                credential_environment(VALUES, PROFILES, path)

    def test_hardlink_rejected(self):
        path = self.write('{"FIXTURE_KEY":"x"}')
        os.link(path, self.root / "other.json")
        with self.assertRaises(ValueError):
            credential_environment(VALUES, PROFILES, path)

    def test_malformed_json_rejected(self):
        with self.assertRaises(json.JSONDecodeError):
            credential_environment(VALUES, PROFILES, self.write("{broken"))

    def test_other_provider_key_rejected(self):
        with self.assertRaises(ValueError):
            credential_environment(VALUES, PROFILES, self.write('{"SHARED_KEY":"x"}'))

    def test_extra_key_rejected(self):
        with self.assertRaises(ValueError):
            credential_environment(VALUES, PROFILES, self.write('{"FIXTURE_KEY":"x","OTHER":"y"}'))

    def test_empty_key_rejected(self):
        with self.assertRaises(ValueError):
            credential_environment(VALUES, PROFILES, self.write('{"FIXTURE_KEY":"  "}'))

    def test_directory_rejected(self):
        with self.assertRaises(ValueError):
            credential_environment(VALUES, PROFILES, self.root)

    def test_owner_mismatch_rejected(self):
        # Mock only the metadata returned by lstat; never change host ownership.
        from unittest.mock import patch
        original = Path.lstat
        path = self.write('{"FIXTURE_KEY":"x"}')
        def fake_lstat(candidate):
            result = original(candidate)
            if candidate == path:
                fields = list(result)
                fields[4] = os.getuid() + 1
                return os.stat_result(fields)
            return result
        with patch.object(Path, "lstat", fake_lstat):
            with self.assertRaises(ValueError):
                credential_environment(VALUES, PROFILES, path)

    def test_sandbox_does_not_import_shared_gh_or_provider_auth(self):
        # Until a reviewed per-file delivery exists, reject accidental host credential exposure.
        source = Path(__file__).with_name("sandbox.py").read_text()
        self.assertNotIn('HOME / ".config/gh"', source)
        self.assertNotIn('HOME / ".ssh"', source)
        self.assertNotIn('"--ro-bind", str(CONFIG / "auth")', source)
        self.assertNotIn('"--bind", str(CONFIG / "auth")', source)

    def test_real_execution_stays_explicitly_blocked(self):
        # This is a source-level guard only; it does not replace host integration QA.
        source = Path(__file__).with_name("sandbox.py").read_text()
        self.assertIn('if not args or args == ["--run"]:', source)
        self.assertIn('Real runner BLOCKED:', source)

    def test_sandbox_private_path_rejects_hardlink(self):
        from sandbox import private_path
        path = self.write('{"FIXTURE_KEY":"x"}')
        os.link(path, self.root / "linked.json")
        with self.assertRaises(RuntimeError):
            private_path(path)

    def test_sandbox_private_path_rejects_symlink_parent(self):
        from sandbox import private_path
        actual = self.root / "isolated"
        actual.mkdir()
        secret = actual / "secret.json"
        secret.write_text("{}")
        alias = self.root / "alias"
        alias.symlink_to(actual, target_is_directory=True)
        with self.assertRaises(RuntimeError):
            private_path(alias / "secret.json")

    def test_sandbox_private_path_rejects_wrong_owner(self):
        from sandbox import private_path
        from unittest.mock import patch
        path = self.write("{}")
        original = Path.lstat

        def other_owner(candidate):
            result = original(candidate)
            if candidate == path:
                fields = list(result)
                fields[4] = os.getuid() + 1
                return os.stat_result(fields)
            return result

        with patch.object(Path, "lstat", other_owner):
            with self.assertRaises(RuntimeError):
                private_path(path)

    def test_sandbox_private_path_rejects_directory_as_file(self):
        from sandbox import private_path
        with self.assertRaises(RuntimeError):
            private_path(self.root)


if __name__ == "__main__":
    unittest.main()
