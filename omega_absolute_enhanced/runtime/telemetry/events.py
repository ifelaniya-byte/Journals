"""
Telemetry event and resource usage structures – §57, §56.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class ResourceUsage:
    """Computational currencies tracked where measurable (§56)."""
    tokens: float = 0.0
    cpu_seconds: float = 0.0
    gpu_seconds: float = 0.0
    wall_time_seconds: float = 0.0
    memory_mb: float = 0.0
    tool_calls: int = 0
    search_calls: int = 0
    storage_bytes: int = 0
    risk_score: float = 0.0
    verification_cost: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tokens": self.tokens,
            "cpu_seconds": self.cpu_seconds,
            "gpu_seconds": self.gpu_seconds,
            "wall_time_seconds": self.wall_time_seconds,
            "memory_mb": self.memory_mb,
            "tool_calls": self.tool_calls,
            "search_calls": self.search_calls,
            "storage_bytes": self.storage_bytes,
            "risk_score": self.risk_score,
            "verification_cost": self.verification_cost,
        }

    def merge(self, other: "ResourceUsage") -> "ResourceUsage":
        return ResourceUsage(
            tokens=self.tokens + other.tokens,
            cpu_seconds=self.cpu_seconds + other.cpu_seconds,
            gpu_seconds=self.gpu_seconds + other.gpu_seconds,
            wall_time_seconds=self.wall_time_seconds + other.wall_time_seconds,
            memory_mb=max(self.memory_mb, other.memory_mb),
            tool_calls=self.tool_calls + other.tool_calls,
            search_calls=self.search_calls + other.search_calls,
            storage_bytes=self.storage_bytes + other.storage_bytes,
            risk_score=max(self.risk_score, other.risk_score),
            verification_cost=self.verification_cost + other.verification_cost,
        )


@dataclass
class TelemetryEvent:
    """MINIMUM EVENT structure (§57)."""
    subsystem: str
    action: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    input_reference: Optional[str] = None
    output_reference: Optional[str] = None
    model_reference: Optional[str] = None
    capability_reference: Optional[str] = None
    resource_usage: ResourceUsage = field(default_factory=ResourceUsage)
    verification_state: Optional[str] = None
    confidence: Optional[float] = None
    error_state: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "event_id": self.event_id,
            "subsystem": self.subsystem,
            "action": self.action,
            "input_reference": self.input_reference,
            "output_reference": self.output_reference,
            "model_reference": self.model_reference,
            "capability_reference": self.capability_reference,
            "resource_usage": self.resource_usage.to_dict(),
            "verification_state": self.verification_state,
            "confidence": self.confidence,
            "error_state": self.error_state,
            "extra": self.extra,
        }
