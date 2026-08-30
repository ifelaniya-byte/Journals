"""Overseers — should this implementation be accepted at all?"""

from __future__ import annotations

from typing import Any


class Overseer:
    def __init__(self, identity: str, auto_merge: bool = False):
        self.identity = identity
        self.auto_merge = auto_merge

    def judge(
        self,
        mission: dict[str, Any],
        verifier_a: dict[str, Any],
        verifier_b: dict[str, Any],
        consensus: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        reasons = []
        if verifier_a.get("verdict") != "PASS" or verifier_b.get("verdict") != "PASS":
            reasons.append("verifiers_not_unanimous_pass")
        if verifier_a.get("verdict") != verifier_b.get("verdict"):
            reasons.append("verifier_disagreement")
        if consensus:
            live_secrets = [
                p
                for p in consensus.get("secrets_suspects") or []
                if not str(p).startswith("tests/")
            ]
            if live_secrets:
                reasons.append("secrets_in_tree")
        if consensus and consensus.get("destructive_suspects") and mission.get("risk") == "critical":
            reasons.append("destructive_markers_on_critical_mission")
        action = mission.get("action") or ""
        if action in {"kdp_upload", "amazon_publish", "force_push"}:
            reasons.append("action_not_sellable_without_human")
        if self.auto_merge:
            reasons.append("auto_merge_forbidden_by_default")
            accept = False
        else:
            accept = not reasons
        return {
            "overseer": self.identity,
            "accept": accept,
            "verdict": "PASS" if accept else "HOLD",
            "reasons": reasons,
            "human_gate": True,
        }


def dual_oversee(
    mission: dict[str, Any],
    verifier_a: dict[str, Any],
    verifier_b: dict[str, Any],
    consensus: dict[str, Any] | None = None,
    auto_merge: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    a = Overseer("A", auto_merge=auto_merge).judge(
        mission, verifier_a, verifier_b, consensus
    )
    b = Overseer("B", auto_merge=auto_merge).judge(
        mission, verifier_a, verifier_b, consensus
    )
    return a, b
