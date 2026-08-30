"""Shadow Alphabet — integrity substrate.

Seals are SHA-256 of canonical JSON. Stationary and overseers read seals.
Only reseal after a verified correction, with a provenance reason.
"""

from __future__ import annotations

import hashlib
import json
import threading
from pathlib import Path
from typing import Any


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode(
        "utf-8"
    )


def seal(obj: Any) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


class ShadowStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self._data: dict[str, dict[str, Any]] = {}
        if self.path.exists():
            try:
                self._data = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                self._data = {}

    def _flush(self) -> None:
        self.path.write_text(
            json.dumps(self._data, indent=2, sort_keys=True, default=str),
            encoding="utf-8",
        )

    def put(self, name: str, payload: Any, *, reason: str = "create") -> str:
        digest = seal(payload)
        with self.lock:
            history = list(self._data.get(name, {}).get("history", []))
            history.append({"seal": digest, "reason": reason})
            self._data[name] = {
                "seal": digest,
                "payload": payload,
                "history": history[-32:],
            }
            self._flush()
        return digest

    def get(self, name: str) -> Any | None:
        row = self._data.get(name)
        return None if row is None else row.get("payload")

    def verify(self, name: str, payload: Any | None = None) -> dict[str, Any]:
        row = self._data.get(name)
        if row is None:
            return {"ok": False, "reason": f"no seal for {name}"}
        subject = row["payload"] if payload is None else payload
        actual = seal(subject)
        if actual != row["seal"]:
            return {
                "ok": False,
                "reason": "CORRUPTION",
                "expected": row["seal"],
                "actual": actual,
            }
        return {"ok": True, "seal": actual}

    def reseal(self, name: str, payload: Any, reason: str) -> str:
        """Restore integrity after a verified correction. Never silent."""
        return self.put(name, payload, reason=f"reseal:{reason}")
