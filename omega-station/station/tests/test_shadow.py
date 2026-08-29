import tempfile
import unittest
from pathlib import Path

from omega_station.shadow import Shadow, seal_tree


class _L:
    def append(self, *a, **k):
        return {}


class TestShadow(unittest.TestCase):
    def test_seal_and_anomaly(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "a.txt").write_text("one")
            sh = Shadow(root, _L())
            sh.seal()
            self.assertTrue(sh.verify()["clean"])
            (root / "a.txt").write_text("tampered")
            v = sh.verify()
            self.assertFalse(v["clean"])
            self.assertIn("a.txt", v["diff"]["modified"])
            sh.reseal("test")
            self.assertTrue(sh.verify()["clean"])

    def test_ignored_dirs_excluded(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".git").mkdir()
            (root / ".git" / "config").write_text("x")
            (root / "keep.txt").write_text("y")
            m = seal_tree(root)
            self.assertEqual(set(m), {"keep.txt"})
