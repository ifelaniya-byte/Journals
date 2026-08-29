from __future__ import annotations

from pathlib import Path

from .shadow import manifest_diff


class Stationary:
    """The judge. Observes, compares, produces directives.

    By construction it has no write tools, no runner, no path handles:
    it receives immutable snapshots (seal manifests, actor claims) and
    returns directives. It can never secretly fix what it is judging.
    """

    def observe(
        self,
        mission: dict,
        before_seals: dict,
        after_seals: dict,
        actor_report: dict,
    ) -> list[dict]:
        directives: list[dict] = []
        mid = mission["mission_id"]

        diff = manifest_diff(before_seals, after_seals)
        changed = set(diff["added"]) | set(diff["removed"]) | set(diff["modified"])
        claimed = set(actor_report.get("files_changed") or [])

        if actor_report.get("verdict") == "PASS" and not changed:
            directives.append({
                "code": "PASS_WITHOUT_CHANGE",
                "detail": "actor claims PASS but the seals show no change",
            })

        claimed_missing = sorted(claimed - changed)
        if claimed_missing:
            directives.append({
                "code": "CLAIM_WITHOUT_CHANGE",
                "detail": f"claimed files with no seal change: {claimed_missing}",
            })

        unclaimed = sorted(changed - claimed)
        if unclaimed:
            directives.append({
                "code": "CHANGE_WITHOUT_CLAIM",
                "detail": f"seal changes not claimed: {unclaimed}",
            })

        allowed = set(mission.get("scope_files", [])) | set(mission.get("creates", []))
        if allowed:
            outside = sorted(changed - allowed)
            if outside:
                directives.append({
                    "code": "SCOPE_VIOLATION",
                    "detail": f"changes outside mission scope: {outside}",
                })

        for req in mission.get("scope_files", []):
            if req not in after_seals:
                directives.append({
                    "code": "REQUIRED_FILE_MISSING",
                    "detail": req,
                })
        _ = mid
        return directives
