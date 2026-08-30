"""Experimental merged/combined/evolved actor — the only component that may write."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def parse_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    return json.loads(text)


class EvolvedActor:
    def __init__(self, root: Path, provider, generated_dir: str = "generated"):
        self.root = root.resolve()
        self.provider = provider
        self.generated_dir = generated_dir

    def think(self, prompt: str) -> dict[str, Any]:
        response = self.provider.generate(prompt)
        parsed = parse_json(response["text"])
        parsed["_usage"] = response.get("usage") or {}
        return parsed

    def apply(self, result: dict[str, Any]) -> list[str]:
        """Write only declared files, and only under generated/ unless allowed."""
        changed = []
        writes = (result.get("implementation") or {}).get("writes") or []
        for item in writes:
            rel = item.get("path")
            content = item.get("content", "")
            if not rel:
                continue
            path = (self.root / rel).resolve()
            try:
                path.relative_to(self.root)
            except ValueError:
                continue
            parts = Path(rel).parts
            allowed = parts and parts[0] in {self.generated_dir, "generated"}
            if not allowed:
                # Actor may only create marketing/engineering drafts in generated/.
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(content), encoding="utf-8")
            changed.append(rel)
        return changed
