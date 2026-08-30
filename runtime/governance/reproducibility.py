"""
Reproducibility Ledger – §58.
If a result cannot be reproduced, mark it UNREPRODUCED, not VERIFIED.
INVARIANT_008: Capability promotion requires reproducibility.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class ReproStatus(str, Enum):
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    UNREPRODUCED = "UNREPRODUCED"
    REPRODUCED = "REPRODUCED"


@dataclass
class ReproducibilityRecord:
    """Matches reproducibility.schema.json."""

    code_version: str
    result: str
    experiment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: Optional[str] = None
    config_version: Optional[str] = None
    model_version: Optional[str] = None
    tool_version: Optional[str] = None
    input_hash: Optional[str] = None
    output_hash: Optional[str] = None
    environment_hash: Optional[str] = None
    random_seed: Optional[int] = None
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    resource_usage: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    failure_state: Optional[str] = None
    status: ReproStatus = ReproStatus.RUNNING

    def complete(self, result: str, metrics: Optional[Dict[str, Any]] = None) -> None:
        self.end_time = datetime.now(timezone.utc)
        self.result = result
        if metrics:
            self.metrics.update(metrics)
        self.status = ReproStatus.COMPLETED

    def mark_failed(self, failure_state: str) -> None:
        self.end_time = datetime.now(timezone.utc)
        self.failure_state = failure_state
        self.status = ReproStatus.FAILED

    def mark_unreproduced(self) -> None:
        self.status = ReproStatus.UNREPRODUCED

    def mark_reproduced(self) -> None:
        if self.status != ReproStatus.COMPLETED:
            raise ValueError("Only COMPLETED records can be marked REPRODUCED")
        self.status = ReproStatus.REPRODUCED

    @staticmethod
    def compute_hash(data: Any) -> str:
        payload = json.dumps(data, sort_keys=True, default=str).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def to_dict(self) -> dict:
        return {
            "experiment_id": self.experiment_id,
            "parent_id": self.parent_id,
            "code_version": self.code_version,
            "config_version": self.config_version,
            "model_version": self.model_version,
            "tool_version": self.tool_version,
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "environment_hash": self.environment_hash,
            "random_seed": self.random_seed,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "resource_usage": self.resource_usage,
            "result": self.result,
            "metrics": self.metrics,
            "failure_state": self.failure_state,
            "status": self.status.value,
        }
