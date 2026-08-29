import os
import tempfile
import unittest
from pathlib import Path

from omega_station.execution import CommandRunner


class TestCredentialHygiene(unittest.TestCase):
    def test_api_key_never_leaks_to_actor_commands(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            old = os.environ.get("OMEGA_API_KEY")
            os.environ["OMEGA_API_KEY"] = "supersecret-leaky-value"
            try:
                runner = CommandRunner(root)
                res = runner.run([
                    "python", "-c",
                    "import os; print(os.environ.get("
                    "'OMEGA_API_KEY', 'CLEAN'))"])
                self.assertEqual(res["stdout"].strip(), "CLEAN")
                res2 = runner.run([
                    "python", "-c",
                    "import os; print(os.environ.get('TMPDIR', ''))"])
                self.assertIn(".omega", res2["stdout"])
            finally:
                if old is None:
                    del os.environ["OMEGA_API_KEY"]
                else:
                    os.environ["OMEGA_API_KEY"] = old

    def test_token_env_also_scrubbed(self):
        with tempfile.TemporaryDirectory() as td:
            old = os.environ.get("GH_TOKEN")
            os.environ["GH_TOKEN"] = "ghp_shouldnotpassthrough"
            try:
                runner = CommandRunner(Path(td))
                res = runner.run([
                    "python", "-c",
                    "import os; print(os.environ.get("
                    "'GH_TOKEN', 'CLEAN'))"])
                self.assertEqual(res["stdout"].strip(), "CLEAN")
            finally:
                if old is None:
                    del os.environ["GH_TOKEN"]
                else:
                    os.environ["GH_TOKEN"] = old


class TestResourceLimits(unittest.TestCase):
    def test_cpu_rlimit_kills_runaway_command(self):
        with tempfile.TemporaryDirectory() as td:
            runner = CommandRunner(Path(td), cpu_limit_s=1)
            res = runner.run([
                "python", "-c", "while True: pass"])
            self.assertNotEqual(res["exit_code"], 0)
            self.assertLess(res["duration"], 20)
