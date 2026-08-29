import json
import tempfile
import unittest
from pathlib import Path

from omega_station.ledger import Ledger


class TestLedger(unittest.TestCase):
    def test_chain_verifies(self):
        with tempfile.TemporaryDirectory() as td:
            led = Ledger(Path(td) / "ev.jsonl")
            led.append("a", {"x": 1})
            led.append("b", {"x": 2})
            self.assertTrue(led.verify_chain()["ok"])

    def test_tamper_detected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "ev.jsonl"
            led = Ledger(p)
            led.append("a", {"x": 1})
            led.append("b", {"x": 2})
            lines = p.read_text().splitlines()
            rec = json.loads(lines[0])
            rec["data"] = {"x": 999}
            lines[0] = json.dumps(rec, sort_keys=True)
            p.write_text(chr(10).join(lines) + chr(10))
            v = Ledger(p).verify_chain()
            self.assertFalse(v["ok"])
