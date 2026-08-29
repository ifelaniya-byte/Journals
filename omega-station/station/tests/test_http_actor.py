import json
import os
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

try:
    from .test_engine import _make_repo
except ImportError:
    from test_engine import _make_repo
from omega_station.config import Config
from omega_station.engine import OmegaStation


def _reactive_action(ctx: dict) -> dict:
    """A non-scripted HTTP brain: decides the next tool action from the
    mission + observed history, exactly like a real LLM must."""
    mission = ctx["mission"]
    hist = ctx.get("history", [])
    t = mission["type"]
    last = hist[-1]["tool"] if hist else None

    def read(f):
        return {"tool": "read", "path": f}

    def finish(v="PASS", files=None, summ="done"):
        return {"tool": "finish", "verdict": v, "summary": summ,
                "files_changed": files or [],
                "evidence": ["http mock actor"]}

    if t == "commit_wip":
        return finish("ESCALATE", summ="human trust decision")
    f = (mission.get("scope_files") or [None])[0]
    if t == "remove_secret":
        if last is None:
            return read(f)
        if last == "read":
            cmd = mission["verification_commands"][0][2]
            import re
            m = re.search(r"re\.search\(r'([^']+)'", cmd)
            return {"tool": "edit", "path": f,
                    "op": "drop_lines_matching", "pattern": m.group(1)}
        return finish(files=[f])
    if t == "guard_destructive":
        if last is None:
            return read(f)
        if last == "read":
            pat = r"curl.*\|\s*(ba)?sh"
            return {"tool": "edit", "path": f, "op": "replace_first",
                    "pattern": r"^(.*" + pat + r".*)$",
                    "replacement": "# OMEGA-GUARD neutralized: \\1"}
        return finish(files=[f])
    if t == "burn_todo":
        if last is None:
            return read(f)
        if last == "read":
            import datetime
            stamp = datetime.date.today().isoformat()
            return {"tool": "edit", "path": f, "op": "replace_first",
                    "pattern": r"\b(TODO|FIXME|XXX|HACK)\b",
                    "replacement": "REVIEWED(" + stamp + ")"}
        return finish(files=[f])
    if t == "add_smoke_test":
        path = mission["creates"][0]
        if last is None:
            content = (
                "import unittest" + chr(10) + chr(10) + chr(10) +
                "class TestSmokeOmegaStation(unittest.TestCase):" +
                chr(10) + "    def test_station_smoke(self):" + chr(10) +
                "        self.assertTrue(True)" + chr(10) + chr(10) +
                chr(10) + "if __name__ == '__main__':" + chr(10) +
                "    unittest.main()" + chr(10))
            return {"tool": "write", "path": path, "content": content}
        if last == "write":
            return {"tool": "run", "command": ["python", path]}
        return finish(files=[path])
    if t == "add_requirements":
        path = mission["creates"][0]
        if last is None:
            lines = mission.get("payload", {}).get("lines", [])
            return {"tool": "write", "path": path,
                    "content": chr(10).join(lines) + chr(10)}
        return finish(files=[path])
    return finish("ESCALATE", summ="no policy for " + str(t))


class _Handler(BaseHTTPRequestHandler):
    mode = "reactive"

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n))
        user = body["messages"][-1]["content"]
        if _Handler.mode == "garbage":
            content = "this is {{{ definitely not json"
        else:
            content = json.dumps(_reactive_action(json.loads(user)))
        payload = json.dumps({
            "choices": [{"message": {"content": content}}],
            "usage": {"prompt_tokens": 111, "completion_tokens": 7},
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


class TestHTTPActor(unittest.TestCase):
    def _serve(self):
        srv = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        th = threading.Thread(target=srv.serve_forever, daemon=True)
        th.start()
        self.addCleanup(srv.shutdown)
        self.addCleanup(srv.server_close)
        return srv

    def _station(self, root, port):
        cfg = Config()
        cfg.provider = "openai-compatible"
        cfg.model = "mock-http-engineer"
        cfg.api_base = f"http://127.0.0.1:{port}"
        cfg.api_key_env = "OMEGA_API_KEY"
        return OmegaStation(root, config=cfg)

    def test_full_run_over_http(self):
        _Handler.mode = "reactive"
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _make_repo(root)
            srv = self._serve()
            old = os.environ.get("OMEGA_API_KEY")
            os.environ["OMEGA_API_KEY"] = "sk-test-key-must-not-leak"
            try:
                station = self._station(root, srv.server_port)
                results = station.run()
            finally:
                if old is None:
                    del os.environ["OMEGA_API_KEY"]
                else:
                    os.environ["OMEGA_API_KEY"] = old
            by = {r["mission_id"]: r["status"] for r in results}
            self.assertTrue(by)
            self.assertTrue(all(v == "complete" for v in by.values()), by)
            self.assertNotIn("AKIA", (root / "app.py").read_text())
            self.assertTrue(station.verify_ledger()["ok"])
            ledger = (root / ".omega" / "evidence.jsonl").read_text()
            self.assertIn("model_usage", ledger)
            self.assertNotIn("sk-test-key-must-not-leak", ledger)
            models = [r[0] for r in station.state.conn.execute(
                "SELECT DISTINCT model FROM usage").fetchall()]
            self.assertIn("mock-http-engineer", models)

    def test_unparseable_model_output_escalates(self):
        _Handler.mode = "garbage"
        old = os.environ.get("OMEGA_API_KEY")
        os.environ["OMEGA_API_KEY"] = "sk-dummy"
        try:
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                _make_repo(root)
                srv = self._serve()
                station = self._station(root, srv.server_port)
                results = station.run()
                by = {r["mission_id"]: r["status"] for r in results}
                self.assertTrue(by)
                self.assertTrue(all(v == "escalated" for v in by.values()),
                                by)
                self.assertTrue(station.verify_ledger()["ok"])
        finally:
            if old is None:
                del os.environ["OMEGA_API_KEY"]
            else:
                os.environ["OMEGA_API_KEY"] = old

    def test_missing_key_escalates_without_crashing(self):
        _Handler.mode = "reactive"
        old = os.environ.pop("OMEGA_API_KEY", None)
        try:
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                _make_repo(root)
                station = OmegaStation(root)   # provider: mock default
                cfg = Config()
                cfg.provider = "openai-compatible"
                cfg.api_key_env = "OMEGA_API_KEY"
                station2 = OmegaStation(root, config=cfg)
                results = station2.run()
                by = {r["mission_id"]: r["status"] for r in results}
                self.assertTrue(by)
                self.assertTrue(all(v == "escalated" for v in by.values()),
                                by)
                self.assertTrue(station2.verify_ledger()["ok"])
        finally:
            if old is not None:
                os.environ["OMEGA_API_KEY"] = old
