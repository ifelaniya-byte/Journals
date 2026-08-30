"""Engineer pool + closed-loop assistance.

Helpers propose. They do not overwrite. Merge only after independent verification.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


ROLES = (
    "architecture",
    "core",
    "tests",
    "security",
    "performance",
    "integration",
)


@dataclass
class Engineer:
    role: str
    busy: bool = False
    completed: int = 0
    last_evidence: dict[str, Any] = field(default_factory=dict)


class EngineerPool:
    def __init__(self):
        self.engineers = {role: Engineer(role=role) for role in ROLES}

    def idle(self) -> list[Engineer]:
        return [e for e in self.engineers.values() if not e.busy]

    def select_helper(self, struggling_role: str) -> Engineer | None:
        candidates = [e for e in self.idle() if e.role != struggling_role]
        if not candidates:
            return None
        candidates.sort(key=lambda e: -e.completed)
        return candidates[0]

    def assist(
        self,
        struggling_role: str,
        proposal_fn: Callable[[], dict[str, Any]],
        verify_fn: Callable[[dict[str, Any]], dict[str, Any]],
        merge_fn: Callable[[dict[str, Any]], None],
    ) -> dict[str, Any]:
        helper = self.select_helper(struggling_role)
        if helper is None:
            return {"ok": False, "reason": "no idle helper"}
        proposal = proposal_fn()
        checked = verify_fn(proposal)
        if not checked.get("ok"):
            return {
                "ok": False,
                "reason": "helper proposal failed verification",
                "details": checked,
                "helper": helper.role,
            }
        merge_fn(proposal)
        helper.completed += 1
        helper.last_evidence = checked
        return {"ok": True, "helper": helper.role, "proposal": proposal}
