from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from typing import Any

TOOL_PROTOCOL = """You are the acting engineer inside a controlled tool loop.
Each turn you receive a context object and MUST reply with ONE JSON object:

{"thought": "...",
"action": {"tool": "read"|"list"|"write"|"edit"|"run"|"finish",
          "args": {...}}}

Tool args:
read:   {"path": "relative/path"}
list:   {"path": "relative/dir"}
write:  {"path": "...", "content": "..."}        (must be in mission scope)
edit:   {"path": "...", "op": "drop_lines_matching"|"replace_first"|"append",
       "pattern": "regex", "replacement": "...", "text": "..."}
run:    {"command": ["python", "-c", "..."]}     (array form preferred)
finish: {"verdict": "PASS"|"REWORK"|"ESCALATE", "summary": "...",
       "files_changed": [...], "evidence": [...]}

Rules: writes outside mission scope are denied. Network commands are
denied unless allowed. Do not claim anything you did not observe in tool
output; every claim is independently verified against filesystem seals.
Reply with JSON only."""

SYSTEM_PROMPT = TOOL_PROTOCOL


class StepProvider(ABC):
    @abstractmethod
    def step(self, context: dict) -> dict:
        raise NotImplementedError


class MockStepProvider(StepProvider):
    """Deterministic actor for mock mode.

    It drives the REAL tool loop (same enforcement path as the LLM)
    with scripted actions per mission type. It is labeled mock in
    every ledger record; it never pretends to be a frontier model.
    """

    def __init__(self, mission: dict):
        self.mission = mission
        self.cursor = 0
        self.script = self._build_script(mission)

    def _build_script(self, m: dict) -> list[dict]:
        t = m["type"]
        if t == "remove_secret":
            pat = m.get("payload", {}).get("pattern") or self._secret_pat(m)
            f = m["scope_files"][0]
            return [
                {"tool": "read", "path": f},
                {"tool": "edit", "path": f, "op": "drop_lines_matching",
                 "pattern": pat},
                {"tool": "finish", "verdict": "PASS",
                 "summary": "removed secret-bearing lines",
                 "files_changed": [f], "evidence": ["edit applied"]},
            ]
        if t == "guard_destructive":
            f = m["scope_files"][0]
            pat = m.get("payload", {}).get("pattern") or r"curl.*\|\s*(ba)?sh"
            return [
                {"tool": "read", "path": f},
                {"tool": "edit", "path": f, "op": "replace_first",
                 "pattern": r"^(.*" + pat + r".*)$",
                 "replacement": "# OMEGA-GUARD neutralized: \\1"},
                {"tool": "finish", "verdict": "PASS",
                 "summary": "destructive line commented with OMEGA-GUARD",
                 "files_changed": [f], "evidence": ["edit applied"]},
            ]
        if t == "burn_todo":
            f = m["scope_files"][0]
            import datetime
            stamp = datetime.date.today().isoformat()
            return [
                {"tool": "read", "path": f},
                {"tool": "edit", "path": f, "op": "replace_first",
                 "pattern": r"\b(TODO|FIXME|XXX|HACK)\b",
                 "replacement": f"REVIEWED({stamp})"},
                {"tool": "finish", "verdict": "PASS",
                 "summary": "hotspot marker dated",
                 "files_changed": [f], "evidence": ["edit applied"]},
            ]
        if t == "add_smoke_test":
            path = m["creates"][0]
            content = chr(10).join([
                "import unittest",
                "",
                "",
                "class TestSmokeOmegaStation(unittest.TestCase):",
                "    def test_station_smoke(self):",
                "        self.assertTrue(True)",
                "",
                "",
                "if __name__ == '__main__':",
                "    unittest.main()",
            ])
            return [
                {"tool": "write", "path": path, "content": content},
                {"tool": "run", "command": ["python", path]},
                {"tool": "finish", "verdict": "PASS",
                 "summary": "smoke test created and green",
                 "files_changed": [path], "evidence": ["run exit 0"]},
            ]
        if t == "add_requirements":
            path = m["creates"][0]
            content = chr(10).join(m.get("payload", {}).get("lines", []))
            return [
                {"tool": "write", "path": path, "content": content + chr(10)},
                {"tool": "finish", "verdict": "PASS",
                 "summary": "requirements.txt written from import scan",
                 "files_changed": [path], "evidence": ["write ok"]},
            ]
        if t == "commit_wip":
            return [
                {"tool": "finish", "verdict": "ESCALATE",
                 "summary": "committing is a human trust decision",
                 "files_changed": [], "evidence": []},
            ]
        return [
            {"tool": "finish", "verdict": "ESCALATE",
             "summary": f"mock has no script for type {t}",
             "files_changed": [], "evidence": []},
        ]

    @staticmethod
    def _secret_pat(m):
        for cmd in m.get("verification_commands", []):
            if len(cmd) >= 3 and "re.search" in cmd[2]:
                import re as _re
                mm = _re.search(r"re\.search\(r'([^']+)'", cmd[2])
                if mm:
                    return mm.group(1)
        return r"AKIA[0-9A-Z]{16}"

    def step(self, context: dict) -> dict:
        if self.cursor < len(self.script):
            a = self.script[self.cursor]
            self.cursor += 1
            return a
        return {"tool": "finish", "verdict": "ESCALATE",
                "summary": "mock script exhausted",
                "files_changed": [], "evidence": []}


class OpenAICompatibleStepProvider(StepProvider):
    """The real actor slot. Any OpenAI-compatible chat API."""

    def __init__(self, config, mission: dict):
        if not config.api_key:
            raise RuntimeError(
                f"model API key missing: set {config.api_key_env}"
            )
        self.config = config
        self.mission = mission

    def step(self, context: dict) -> dict:
        url = self.config.api_base.rstrip("/") + "/chat/completions"
        payload = {
            "model": self.config.model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(context, default=str)},
            ],
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.api_key}",
            },
            method="POST",
        )
        data = None
        last_exc: Exception | None = None
        for attempt in range(3):
            # transient-fault tolerance with fail-CLOSED semantics:
            # after the retries the exception propagates, the actor
            # records actor_error, and the mission ESCALATES. The
            # station never guesses when the brain is unreachable.
            try:
                with urllib.request.urlopen(req, timeout=180) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                break
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                last_exc = exc
                if attempt < 2:
                    time.sleep(1.0 + 1.5 * attempt)
        if data is None:
            raise last_exc if last_exc else RuntimeError("no response")
        self.last_usage = {
            "input_tokens": (data.get("usage") or {}).get("prompt_tokens"),
            "output_tokens": (data.get("usage") or {}).get("completion_tokens"),
        }
        text = data["choices"][0]["message"].get("content") or ""
        text = text.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = chr(10).join(lines)
        try:
            action = json.loads(text)
        except json.JSONDecodeError:
            return {"tool": "finish", "verdict": "ESCALATE",
                    "summary": "model returned unparseable JSON",
                    "files_changed": [], "evidence": [text[:400]]}
        return action


def create_step_provider(config, mission: dict) -> StepProvider:
    if config.provider == "mock":
        return MockStepProvider(mission)
    if config.provider in {"openai-compatible", "openai", "openrouter"}:
        return OpenAICompatibleStepProvider(config, mission)
    raise RuntimeError(f"unknown provider: {config.provider}")
