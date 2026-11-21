"""Offline integration fixtures for check-documentation.py. Uses only disposable Git repos."""
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCANNER = pathlib.Path(__file__).with_name("check-documentation.py")


def run(*args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)


class DocumentationPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="whereis-ci-fixture-")
        self.addCleanup(self.temp.cleanup)
        self.repo = pathlib.Path(self.temp.name)
        self.assertEqual(run("git", "init", "-q", cwd=self.repo).returncode, 0)
        self.assertEqual(run("git", "config", "user.name", "Synthetic QA", cwd=self.repo).returncode, 0)
        self.assertEqual(run("git", "config", "user.email", "qa@example.invalid", cwd=self.repo).returncode, 0)
        self.write("baseline.md", b"baseline\n")
        self.commit()
        self.base = run("git", "rev-parse", "HEAD", cwd=self.repo).stdout.strip()

    def write(self, path, data):
        dest = self.repo / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)

    def commit(self):
        self.assertEqual(run("git", "add", "-A", cwd=self.repo).returncode, 0)
        result = run("git", "-c", "user.name=Synthetic QA",
                     "-c", "user.email=qa@example.invalid",
                     "commit", "--quiet", "-m", "synthetic case", cwd=self.repo)
        self.assertEqual(result.returncode, 0, result.stderr)

    def check(self, base=None):
        return run(sys.executable, str(SCANNER), base or self.base, cwd=self.repo)

    def test_clean_document_passes(self):
        self.write("docs/clean.md", b"Valid text\n")
        self.commit()
        self.assertEqual(self.check().returncode, 0)

    def test_secret_pattern_in_dot_env_rejected_without_leaking(self):
        marker = "ghp_" + "A" * 24
        self.write(".env.local", ("CREDENTIAL=" + marker + "\n").encode())
        self.commit()
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(marker, result.stdout + result.stderr)
        self.assertNotIn(".env.local", result.stdout + result.stderr)

    def test_secret_pattern_in_extensionless_file_rejected(self):
        self.write("credentials", ("ghp_" + "A" * 24).encode())
        self.commit()
        self.assertEqual(self.check().returncode, 1)

    def test_trailing_whitespace_rejected(self):
        self.write("docs/notes.md", b"bad whitespace  \n")
        self.commit()
        self.assertEqual(self.check().returncode, 1)

    def test_merge_markers_rejected(self):
        self.write("docs/notes.md", b"<<<<<<< HEAD\nconflict\n=======\nother\n>>>>>>> branch\n")
        self.commit()
        self.assertEqual(self.check().returncode, 1)

    def test_invalid_utf8_markdown_rejected(self):
        self.write("docs/notes.md", b"invalid\xff\n")
        self.commit()
        self.assertEqual(self.check().returncode, 1)

    def test_binary_nul_markdown_rejected(self):
        self.write("docs/notes.md", b"binary\x00")
        self.commit()
        self.assertEqual(self.check().returncode, 1)

    def test_empty_changed_text_rejected(self):
        self.write("docs/notes.md", b"")
        self.commit()
        self.assertEqual(self.check().returncode, 1)

    def test_worktree_modification_cannot_hide_committed_secret(self):
        marker = "ghp_" + "A" * 24
        self.write("docs/notes.md", marker.encode())
        self.commit()
        self.write("docs/notes.md", b"working tree cleaned\n")
        self.assertEqual(self.check().returncode, 1)

    def test_uncommitted_secret_not_part_of_head(self):
        self.write("docs/notes.md", b"safe committed contents\n")
        self.commit()
        self.write("docs/notes.md", ("ghp_" + "A" * 24).encode())
        self.assertEqual(self.check().returncode, 0)

    def test_missing_base_fails_closed(self):
        self.write("docs/notes.md", b"safe\n")
        self.commit()
        self.assertEqual(self.check("0" * 40).returncode, 1)

    def test_missing_argument_returns_usage_code(self):
        self.assertEqual(run(sys.executable, str(SCANNER), cwd=self.repo).returncode, 2)


if __name__ == "__main__":
    unittest.main()
