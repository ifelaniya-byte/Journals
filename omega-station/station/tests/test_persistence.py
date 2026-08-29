import tempfile
import unittest
from pathlib import Path

try:
    from .test_engine import _make_repo   # package-style discovery
except ImportError:
    from test_engine import _make_repo    # flat discovery (-s tests)
from omega_station.engine import OmegaStation


class TestPersistence(unittest.TestCase):
    def test_seals_survive_restart(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _make_repo(root)
            OmegaStation(root).run()
            second = OmegaStation(root)          # fresh process stand-in
            v = second.verify_integrity()
            self.assertTrue(v["clean"])
            (root / "app.py").write_text("out-of-band tamper")
            third = OmegaStation(root)
            v = third.verify_integrity()
            self.assertFalse(v["clean"])
            self.assertIn("app.py", v["diff"]["modified"])

    def test_resume_skips_completed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _make_repo(root)
            OmegaStation(root).run()
            before = (root / "app.py").read_text()
            second = OmegaStation(root)
            results = second.run()
            self.assertEqual(results, [])        # nothing re-executed
            self.assertEqual((root / "app.py").read_text(), before)
