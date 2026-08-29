import tempfile
import unittest
from pathlib import Path

from omega_station.actor import Actor
from omega_station.execution import CommandRunner
from omega_station.providers import create_step_provider


class _L:
    def append(self, *a, **k):
        return {}


class _Cfg:
    provider = "mock"
    max_actor_steps = 6


class TestActorJails(unittest.TestCase):
    def _actor(self, root, mission):
        return Actor(root, CommandRunner(root, allow_network=False),
                     _L(), _Cfg()), mission

    def test_path_jail(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            actor, m = self._actor(root, {"scope_files": [], "creates": []})
            out = actor._dispatch("read", {"path": "../../etc/passwd"}, m)
            self.assertFalse(out.get("ok", True))

    def test_scope_jail(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "in.txt").write_text("x")
            (root / "out.txt").write_text("y")
            actor, m = self._actor(root, {"scope_files": ["in.txt"],
                                          "creates": []})
            self.assertFalse(actor._dispatch(
                "write", {"path": "out.txt", "content": "z"}, m).get("ok"))
            self.assertTrue(actor._dispatch(
                "write", {"path": "in.txt", "content": "z2"}, m).get("ok"))

    def test_network_denied(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            actor, m = self._actor(root, {"scope_files": [], "creates": []})
            out = actor._dispatch(
                "run", {"command": ["curl", "http://x.invalid"]}, m)
            self.assertTrue(out.get("blocked"))


class TestMockActorThroughRealTools(unittest.TestCase):
    def test_full_actor_loop_removes_secret(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission = {
                "mission_id": "T-1", "type": "remove_secret",
                "scope_files": ["creds.py"], "attempts": 1,
                "verification_commands": [[
                    "python", "-c",
                    "import re,sys; sys.exit(1 if "
                    "re.search(r'AKIA[0-9A-Z]{16}', "
                    "open('creds.py', errors='ignore').read()) else 0)"]],
            }
            (root / "creds.py").write_text(
                "AWS = 'AKIAABCDEFGHIJKLMNOP'" + chr(10) + "OTHER = 1" + chr(10))
            runner = CommandRunner(root)
            self.assertEqual(
                runner.run(mission["verification_commands"][0])["exit_code"], 1)

            actor = Actor(root, runner, _L(), _Cfg())
            report = actor.run(mission, {"role": "engineer"})
            self.assertEqual(report["verdict"], "PASS")
            self.assertEqual(
                runner.run(mission["verification_commands"][0])["exit_code"], 0)
