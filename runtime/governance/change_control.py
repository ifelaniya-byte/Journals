"""
Change Control Record – §60.
No silent architectural mutation.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class ChangeStatus(str, Enum):
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    APPLIED = "APPLIED"
    ROLLED_BACK = "ROLLED_BACK"
    REJECTED = "REJECTED"


@dataclass
class ChangeControlRecord:
    """Matches change_control.schema.json. Every architectural change MUST include these fields."""

    author_or_agent: str
    previous_version: str
    new_version: str
    reason: str
    expected_gain: str
    expected_risk: str
    test_plan: str
    rollback_plan: str
    change_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    test_result: Optional[str] = None
    status: ChangeStatus = ChangeStatus.PROPOSED

    def approve(self) -> None:
        if self.status != ChangeStatus.PROPOSED:
            raise ValueError(f"Cannot approve change in status {self.status}")
        self.status = ChangeStatus.APPROVED

    def apply(self) -> None:
        if self.status != ChangeStatus.APPROVED:
            raise ValueError(f"Cannot apply change in status {self.status}")
        self.status = ChangeStatus.APPLIED

    def rollback(self) -> None:
        if self.status != ChangeStatus.APPLIED:
            raise ValueError(f"Cannot rollback change in status {self.status}")
        self.status = ChangeStatus.ROLLED_BACK

    def to_dict(self) -> dict:
        return {
            "change_id": self.change_id,
            "date": self.date.isoformat(),
            "author_or_agent": self.author_or_agent,
            "previous_version": self.previous_version,
            "new_version": self.new_version,
            "reason": self.reason,
            "expected_gain": self.expected_gain,
            "expected_risk": self.expected_risk,
            "test_plan": self.test_plan,
            "test_result": self.test_result,
            "rollback_plan": self.rollback_plan,
            "status": self.status.value,
        }
