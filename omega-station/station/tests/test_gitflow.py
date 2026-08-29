import os
import subprocess
import tempfile
import unittest
from pathlib import Path

try:
    from .test_engine import _make_repo   # package-style discovery
except ImportError:
    from test_engine import _make_repo    # flat discovery (-s tests)
from omega_station.engine import OmegaStation


def _sha(root, ref):
    return subprocess.run(
        ["git", "rev-parse", ref], cwd=root, text=True,
        capture_output=True).stdout.strip()


class TestGitFlow(unittest.TestCase):
    def test_branch_isolation_pr_and_commits(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _make_repo(root)
            base_sha = _sha(root, "main")
            self.assertRegex(base_sha, r"^[0-9a-f]{40}$")
            station = OmegaStation(root)
            station.run()
            # station worked on an isolated branch; base untouched
            self.assertTrue(station.gitflow.isolated)
            self.assertTrue(station.gitflow.branch.startswith("omega/"))
            self.assertEqual(_sha(root, "main"), base_sha)
            cur = subprocess.run(
                ["git", "branch", "--show-current"], cwd=root, text=True,
                capture_output=True).stdout.strip()
            self.assertEqual(cur, station.gitflow.branch)
            # one commit per accepted mission on the branch
            n = subprocess.run(
                ["git", "rev-list", "--count", f"main..{cur}"],
                cwd=root, text=True, capture_output=True).stdout.strip()
            self.assertEqual(int(n), 5)
            # PR artifact exists and demands a human decision
            pr = (root / ".omega" / "PR.md").read_text()
            self.assertIn("human decision", pr)
            self.assertIn("OM-SEC-001", pr)
            self.assertIn("OK", pr)

    def test_push_to_local_origin(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            # origin must live OUTSIDE the worktree, else the repo is
            # legitimately dirty and the station correctly refuses
            # branch isolation
            origin = Path(tempfile.mkdtemp()) / "origin.git"
            _make_repo(root)
            subprocess.run(["git", "init", "-q", "--bare", str(origin)],
                           check=True)
            subprocess.run(["git", "remote", "add", "origin", str(origin)],
                           cwd=root, check=True)
            subprocess.run(["git", "push", "-q", "origin", "main"],
                           cwd=root, check=True)
            subprocess.run(
                ["git", "branch", "--set-upstream-to=origin/main", "main"],
                cwd=root, capture_output=True)
            station = OmegaStation(root)
            old = os.environ.get("OMEGA_PUSH")
            os.environ["OMEGA_PUSH"] = "1"
            try:
                station.run()
            finally:
                if old is None:
                    del os.environ["OMEGA_PUSH"]
                else:
                    os.environ["OMEGA_PUSH"] = old
            branches = subprocess.run(
                ["git", "branch", "--list", "omega/*"],
                cwd=origin, text=True, capture_output=True).stdout
            self.assertIn("omega/station-", branches)

    def test_dirty_repo_refuses_isolation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _make_repo(root)
            (root / "user_wip.txt").write_text("uncommitted user work")
            station = OmegaStation(root)
            station.run()
            self.assertFalse(station.gitflow.isolated)
            self.assertIsNone(station.gitflow.branch)
            events = [l for l in
                      (root / ".omega" / "evidence.jsonl").read_text()
                      .splitlines() if "gitflow_unisolated" in l]
            self.assertTrue(events)
            # user file untouched, work still done + committed on base
            self.assertTrue((root / "user_wip.txt").exists())
            self.assertNotIn("AKIA", (root / "app.py").read_text())
