"""Actor slot: a client, never weights.

Swap mock → hosted → self-hosted without touching the control loop.
Network calls are fail-closed unless Config.allow_network is true.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from typing import Any
from urllib.parse import urlparse


LIVE_PROVIDERS = {
    "openai",
    "openai-compatible",
    "openrouter",
    "groq",
    "together",
    "ollama",
    "mistral",
}


class ModelProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> dict[str, Any]:
        raise NotImplementedError


class MockProvider(ModelProvider):
    """Deterministic actor slot. Does not pretend to be a frontier model."""

    def generate(self, prompt: str) -> dict[str, Any]:
        mission = {}
        try:
            marker = "MISSION_JSON:"
            if marker in prompt:
                raw = prompt.split(marker, 1)[1].strip()
                mission = json.loads(raw.split("\n", 1)[0])
        except Exception:
            mission = {}
        output = mission.get("output_path") or "generated/asset.json"
        title = mission.get("title") or "Draft asset"
        body = mission.get("mock_body") or (
            f"{title}. Tracking and management only. Paperback $9.99 on KDP. "
            "Quiet Mind Press. Not medical advice."
        )
        payload = {
            "understanding": {
                "problem": title,
                "requirements": mission.get("requirements", []),
            },
            "plan": ["Retrieve catalog facts", "Draft asset", "Self-check policy"],
            "implementation": {
                "files_changed": [output],
                "writes": [{"path": output, "content": body}],
            },
            "action": mission.get("action") or "draft_copy",
            "tests": {"commands": [], "passed": [], "failed": []},
            "self_review": {"remaining_risks": []},
            "evidence": ["mock actor produced a draft"],
            "requested_verdict": "PASS",
        }
        return {
            "text": json.dumps(payload),
            "usage": {
                "input_tokens": None,
                "output_tokens": None,
                "total_tokens": None,
                "cost": None,
            },
        }


class OpenAICompatibleProvider(ModelProvider):
    """HTTPS (or loopback HTTP for Ollama) chat-completions client. No weights."""

    def __init__(self, api_key: str | None, base_url: str, model: str, timeout: int = 180):
        self.api_key = api_key or ""
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self._assert_url()

    def _assert_url(self) -> None:
        parsed = urlparse(self.base_url)
        if parsed.scheme not in {"https", "http"}:
            raise RuntimeError(f"fail-closed: unsupported API scheme {parsed.scheme!r}")
        host = (parsed.hostname or "").lower()
        loopback = host in {"127.0.0.1", "localhost", "::1"}
        if parsed.scheme == "http" and not loopback:
            raise RuntimeError("fail-closed: non-loopback HTTP is not allowed")

    def generate(self, prompt: str) -> dict[str, Any]:
        url = self.base_url + "/chat/completions"
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are the experimental merged/combined/evolved actor "
                        "in an Omega seller station. Return ONLY JSON. "
                        "Do not claim tests passed unless run. "
                        "Never include manufacturer drug brands. "
                        "Never put B&N $14.99 on KDP. Tracking/management only. "
                        "Never publish, price, spend, or list items for sale."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:2000]
            raise RuntimeError(f"fail-closed: model HTTP {exc.code}: {body}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"fail-closed: model unreachable: {exc.reason}") from exc
        except TimeoutError as exc:
            raise RuntimeError("fail-closed: model timed out") from exc

        try:
            data = json.loads(raw)
            text = data["choices"][0]["message"].get("content") or ""
        except Exception as exc:
            raise RuntimeError("fail-closed: model returned non-schema JSON") from exc

        usage = data.get("usage") or {}
        return {
            "text": text,
            "usage": {
                "input_tokens": usage.get("prompt_tokens"),
                "output_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
                "cost": data.get("cost"),
            },
        }


def create_provider(config):
    name = (config.model_provider or "mock").lower()
    if name == "mock":
        return MockProvider()
    if name in LIVE_PROVIDERS:
        if not getattr(config, "allow_network", False):
            raise RuntimeError(
                "fail-closed: live model requested but allow_network is false. "
                "Stay on mock, or set allow_network true in .seller-station.json."
            )
        if name != "ollama" and not config.api_key:
            raise RuntimeError(f"fail-closed: set {config.api_key_env} for {name}.")
        return OpenAICompatibleProvider(
            config.api_key,
            config.api_base,
            config.model_name,
        )
    raise RuntimeError(f"fail-closed: unknown model provider {config.model_provider!r}")
