"""
Ω-ABSOLUTE Governance Package
Canonical reference: §§4, 57–62, 65 (INVARIANT_013 especially).
The governance kernel MUST remain outside unrestricted self-modification.
"""

from .states import DevelopmentState, ClaimLevel, CapabilityState, EpistemicState, SourceType
from .provenance import ProvenanceRecord
from .change_control import ChangeControlRecord
from .reproducibility import ReproducibilityRecord
from .claim_discipline import ClaimDiscipline, ClaimViolationError
from .gap_matrix import GapMatrix, GapStatus

__all__ = [
    "DevelopmentState",
    "ClaimLevel",
    "CapabilityState",
    "EpistemicState",
    "SourceType",
    "ProvenanceRecord",
    "ChangeControlRecord",
    "ReproducibilityRecord",
    "ClaimDiscipline",
    "ClaimViolationError",
    "GapMatrix",
    "GapStatus",
]
