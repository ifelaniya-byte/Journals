"""Hostile dual verifiers. Assume the engineer is wrong until evidence says otherwise."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from .policy import audit_asset
from .sandbox import CommandRunner


class Verifier:
    def __init__(self, root: Path, runner: CommandRunner, identity: str):
        self.root = root.resolve()
        self.runner = runner
        self.identity = identity

    def changed_files(self) -> list[str]:
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.root,
                text=True,
                capture_output=True,
                timeout=20,
            )
            files = []
            for line in result.stdout.splitlines():
                path = line[3:].strip()
                if path:
                    files.append(path.split(" -> ")[-1])
            return files
        except Exception:
            return []

    def verify(self, mission: dict[str, Any], actor_result: dict[str, Any]) -> dict[str, Any]:
        reasons: list[str] = []
        commands: list[dict[str, Any]] = []
        changed = self.changed_files()
        declared = set(
            (actor_result.get("implementation") or {}).get("files_changed") or []
        )
        generated = [
            item.get("path")
            for item in (actor_result.get("implementation") or {}).get("writes") or []
            if item.get("path")
        ]
        on_disk = [p for p in generated if (self.root / p).exists()]
        if declared and not on_disk and not set(declared).intersection(set(changed)):
            reasons.append("claim_without_artifact: declared files not on disk or in git")

        allowed = set(mission.get("files") or [])
        if allowed:
            outside = [p for p in on_disk if p not in allowed]
            if outside:
                reasons.append("scope:" + ", ".join(outside))

        for required in mission.get("files") or []:
            if not (self.root / required).exists():
                reasons.append(f"missing:{required}")

        policy = audit_asset(
            actor_result,
            root=self.root,
            catalog_file=mission.get("catalog_file") or "catalog.json",
        )
        if not policy["ok"]:
            reasons.extend("policy:" + r for r in policy["reasons"])

        for write in (actor_result.get("implementation") or {}).get("writes") or []:
            policy_w = audit_asset(write.get("content", ""), root=self.root)
            if not policy_w["ok"]:
                reasons.extend("policy:" + r for r in policy_w["reasons"])

        for command in mission.get("verification_commands") or []:
            result = self.runner.run(command)
            commands.append(result)
            if result["exit_code"] != 0 or result.get("blocked"):
                reasons.append(f"command_failed:{command}")

        requested = actor_result.get("requested_verdict")
        if requested == "PASS" and reasons:
            reasons.append("model_verdict_ignored")

        verdict = "PASS" if not reasons else "REWORK"
        return {
            "verifier": self.identity,
            "verdict": verdict,
            "reasons": sorted(set(reasons)),
            "commands": commands,
            "changed_files": changed,
            "on_disk": on_disk,
            "assumed_wrong": True,
            "trusted_model": False,
        }


def dual_verify(
    root: Path,
    runner: CommandRunner,
    mission: dict[str, Any],
    actor_result: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    a = Verifier(root, runner, "A").verify(mission, actor_result)
    b = Verifier(root, runner, "B").verify(mission, actor_result)
    return a, b
