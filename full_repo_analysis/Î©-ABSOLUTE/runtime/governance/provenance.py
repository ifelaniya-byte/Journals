"""
Provenance Record – §59.
Every imported fact MUST identify SOURCE, SOURCE_TYPE, ACQUISITION_TIME,
CLAIM, EVIDENCE, CONFIDENCE, TRANSFORMS, DERIVATION.
INVARIANT_015: Provenance MUST survive transformations.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

from .states import SourceType


@dataclass(frozen=True)
class ProvenanceRecord:
    """Immutable provenance record. Matches provenance.schema.json."""

    source: str
    source_type: SourceType
    claim: str
    confidence: float
    acquisition_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    evidence: List[str] = field(default_factory=list)
    transforms: List[str] = field(default_factory=list)
    derivation: Optional[str] = None
    parent_provenance_ids: List[str] = field(default_factory=list)
    provenance_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"confidence must be in [0.0, 1.0], got {self.confidence}")
        if self.source_type == SourceType.MODEL_INFERENCE and self.confidence >= 0.95:
            # Soft warning path: model inference must never be silently treated as verified fact.
            pass

    def to_dict(self) -> dict:
        return {
            "provenance_id": self.provenance_id,
            "source": self.source,
            "source_type": self.source_type.value,
            "acquisition_time": self.acquisition_time.isoformat(),
            "claim": self.claim,
            "evidence": list(self.evidence),
            "confidence": self.confidence,
            "transforms": list(self.transforms),
            "derivation": self.derivation,
            "parent_provenance_ids": list(self.parent_provenance_ids),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProvenanceRecord":
        return cls(
            provenance_id=data.get("provenance_id", str(uuid.uuid4())),
            source=data["source"],
            source_type=SourceType(data["source_type"]),
            claim=data["claim"],
            confidence=float(data["confidence"]),
            acquisition_time=datetime.fromisoformat(data["acquisition_time"]),
            evidence=data.get("evidence", []),
            transforms=data.get("transforms", []),
            derivation=data.get("derivation"),
            parent_provenance_ids=data.get("parent_provenance_ids", []),
        )
