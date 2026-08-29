import json
import tempfile
import unittest
from pathlib import Path

from omega_station.proposal import run_proposal


def _src(root):
    (root / "README.md").write_text("source snapshot", encoding="utf-8")
    (root / "app.py").write_text("x = 1" + chr(10), encoding="utf-8")


def _prop(root, **over):
    p = {
        "mission_id": "PROP-1",
        "title": "add a notes file",
        "allowed_paths": ["notes.txt"],
        "files": {"notes.txt": "hello candidate" + chr(10)},
    }
    p.update(over)
    f = root / "proposal.json"
    f.write_text(json.dumps(p), encoding="utf-8")
    return f


class TestProposal(unittest.TestCase):
    def test_valid_proposal_pass_candidate_source_untouched(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _src(root)
            before = (root / "app.py").read_bytes()
            res = run_proposal(root, _prop(root))
            self.assertEqual(res["result"], "PASS_CANDIDATE")
            self.assertEqual(res["requires"], "named human review")
            # source snapshot unchanged; write landed in candidate copy
            self.assertEqual((root / "app.py").read_bytes(), before)
            self.assertFalse((root / "notes.txt").exists())
            cand = Path(res["candidate_dir"])
            self.assertEqual((cand / "notes.txt").read_text().strip(),
                             "hello candidate")
            # ledger chain verifies
            from omega_station.ledger import Ledger
            led = Ledger(root / ".omega" / "proposal-evidence.jsonl")
            self.assertTrue(led.verify_chain()["ok"])

    def test_reject_path_escape(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _src(root)
            res = run_proposal(root, _prop(
                root, files={"../evil.txt": "x"}))
            self.assertEqual(res["result"], "REJECT")
            self.assertIn("unsafe path", res["reason"])

    def test_reject_write_outside_allowed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _src(root)
            res = run_proposal(root, _prop(
                root, files={"other.txt": "x"}))
            self.assertEqual(res["result"], "REJECT")
            self.assertIn("outside allowed_paths", res["reason"])

    def test_reject_intake_action(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _src(root)
            res = run_proposal(root, _prop(root, action="publish"))
            self.assertEqual(res["result"], "REJECT")
            self.assertIn("intake denied", res["reason"])

    def test_reject_policy_violation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _src(root)
            banned = root / "banned.txt"
            banned.write_text("cure" + chr(10) + "guaranteed" + chr(10))
            res = run_proposal(root, _prop(root, files={
                "notes.txt": "a guaranteed cure for boredom" + chr(10)}),
                banned_file=banned)
            self.assertEqual(res["result"], "REJECT")
            self.assertIn("policy violation", res["reason"])
