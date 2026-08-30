"""Stationary — inspect and judge. Never secretly fix the thing it is judging."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class Stationary:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.writes = 0

    def observe(self, evidence: dict[str, Any]) -> dict[str, Any]:
        contradictions = []
        claims = evidence.get("claims") or {}
        facts = evidence.get("facts") or {}
        for key, claimed in claims.items():
            if key in facts and facts[key] != claimed:
                contradictions.append(
                    {"field": key, "claimed": claimed, "actual": facts[key]}
                )
        verifier_a = evidence.get("verifier_a") or {}
        verifier_b = evidence.get("verifier_b") or {}
        if verifier_a.get("verdict") and verifier_b.get("verdict"):
            if verifier_a.get("verdict") != verifier_b.get("verdict"):
                contradictions.append(
                    {
                        "field": "dual_verifier",
                        "claimed": verifier_a.get("verdict"),
                        "actual": verifier_b.get("verdict"),
                    }
                )
        return {
            "contradictions": contradictions,
            "secret_fixes": 0,
            "writes": self.writes,
        }

    def directive(self, observation: dict[str, Any], *, attempts: int, max_attempts: int) -> str:
        if observation.get("writes"):
            return "ESCALATE"
        if observation.get("contradictions"):
            if attempts >= max_attempts:
                return "ESCALATE"
            return "REWORK"
        va = observation.get("pass_a")
        vb = observation.get("pass_b")
        if va is False or vb is False:
            return "REWORK" if attempts < max_attempts else "ESCALATE"
        return "PASS"

    def forbid_write(self, path: Path) -> None:
        raise RuntimeError(
            f"Stationary must not write {path}. Judges do not patch the judged."
        )
