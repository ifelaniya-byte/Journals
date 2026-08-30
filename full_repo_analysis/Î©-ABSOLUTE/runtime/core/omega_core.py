"""
Immutable Ω Core – §4, INVARIANT_013.
Governance boundary that cannot be silently self-modified.
All other subsystems (including Meta-Controller) are governed by this Core.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, FrozenSet, List, Optional, Set

from runtime.governance.states import DevelopmentState
from runtime.governance.claim_discipline import ClaimDiscipline
from runtime.governance.gap_matrix import GapMatrix
from runtime.governance.change_control import ChangeControlRecord, ChangeStatus
from runtime.core.version import CORE_VERSION, PROJECT_VERSION, SPEC_VERSION


class CoreViolationError(Exception):
    """Raised when an attempt is made to violate an immutable Core rule."""


@dataclass(frozen=True)
class SafetyBoundary:
    name: str
    description: str
    enforceable: bool = True


@dataclass(frozen=True)
class ResourceCeiling:
    name: str
    limit: float
    unit: str


class OmegaCore:
    """
    The single immutable governance kernel.
    Nothing outside this class may alter its identity, boundaries, or policies.
    """

    def __init__(self) -> None:
        # Identity – immutable
        self._identity: str = "Ω-ABSOLUTE"
        self._formal_name: str = "Bounded Self-Synthesizing Causal Intelligence"
        self._core_version: str = CORE_VERSION
        self._project_version: str = PROJECT_VERSION
        self._spec_version: str = SPEC_VERSION

        # Safety boundaries – immutable set
        self._safety_boundaries: FrozenSet[SafetyBoundary] = frozenset([
            SafetyBoundary("no_unrestricted_self_modification", "Core and governance rules cannot be rewritten by solvers"),
            SafetyBoundary("no_irreversible_without_authorization", "Irreversible actions require explicit authorization"),
            SafetyBoundary("verification_hierarchy", "Verifier-of-Verifiers required for consequential results"),
            SafetyBoundary("provenance_required", "All claims must carry provenance"),
            SafetyBoundary("truthfulness", "Model inference must never be represented as externally verified fact"),
            SafetyBoundary("claim_discipline", "Claims may not exceed actual DevelopmentState"),
            SafetyBoundary("rollback_available", "Rollback must remain available for promoted changes"),
            SafetyBoundary("resource_ceilings_enforced", "Resource limits are hard ceilings"),
        ])

        # Resource ceilings – hard limits
        self._resource_ceilings: Dict[str, ResourceCeiling] = {
            "max_tokens_per_task": ResourceCeiling("max_tokens_per_task", 1_000_000, "tokens"),
            "max_wall_time_seconds": ResourceCeiling("max_wall_time_seconds", 3600, "seconds"),
            "max_tool_calls": ResourceCeiling("max_tool_calls", 500, "calls"),
            "max_memory_mb": ResourceCeiling("max_memory_mb", 8192, "MB"),
            "max_recursive_critique_depth": ResourceCeiling("max_recursive_critique_depth", 5, "depth"),
        }

        # Promotion requirements – immutable checklist
        self._promotion_requirements: FrozenSet[str] = frozenset([
            "UNIT_TEST",
            "ABLATION",
            "ADVERSARIAL",
            "REGRESSION",
            "RESOURCE",
            "REPRODUCTION",
            "TRANSFER",
        ])

        # Verification hierarchy – immutable
        self._verification_hierarchy: List[str] = [
            "SOLVER",
            "VERIFIER",
            "VERIFIER_CRITIC",
            "VERIFICATION_AUDITOR",
        ]

        # Internal ledgers (mutable only through controlled methods)
        self._change_log: List[ChangeControlRecord] = []
        self._claim_discipline = ClaimDiscipline()
        self._gap_matrix = GapMatrix()

        # Bootstrap the gap matrix with foundation components
        self._bootstrap_gap_matrix()

        # Register Core itself at VERIFIED (foundation) level for claim discipline
        # Note: Core is the only component allowed to start at VERIFIED because it is the governance root.
        self._claim_discipline.register("omega.core", DevelopmentState.VERIFIED)
        self._claim_discipline.register("omega.governance", DevelopmentState.IMPLEMENTED)
        self._claim_discipline.register("omega.meta_controller", DevelopmentState.SCAFFOLDED)
        self._claim_discipline.register("omega.telemetry", DevelopmentState.IMPLEMENTED)

    def _bootstrap_gap_matrix(self) -> None:
        foundation = [
            ("omega.core", "§4 Immutable Ω Core", DevelopmentState.VERIFIED),
            ("omega.governance.states", "§61 Development States", DevelopmentState.IMPLEMENTED),
            ("omega.governance.claim_discipline", "§62 Claim Discipline", DevelopmentState.IMPLEMENTED),
            ("omega.governance.provenance", "§59 Knowledge Provenance", DevelopmentState.IMPLEMENTED),
            ("omega.governance.change_control", "§60 Change Control", DevelopmentState.IMPLEMENTED),
            ("omega.governance.reproducibility", "§58 Reproducibility Ledger", DevelopmentState.IMPLEMENTED),
            ("omega.governance.gap_matrix", "§75 Gap Matrix", DevelopmentState.IMPLEMENTED),
            ("omega.meta_controller", "§5 Meta-Controller", DevelopmentState.SCAFFOLDED),
            ("omega.telemetry", "§57 Observability", DevelopmentState.IMPLEMENTED),
            ("omega.epistemic", "§7 Epistemic Engine", DevelopmentState.NOT_DESIGNED),
            ("omega.task_model", "§6 Task Model", DevelopmentState.NOT_DESIGNED),
            ("omega.world_model", "§8 World Model", DevelopmentState.NOT_DESIGNED),
            ("omega.self_model", "§9 Self Model", DevelopmentState.NOT_DESIGNED),
            ("omega.verification", "§30 Verification Engine", DevelopmentState.NOT_DESIGNED),
            ("omega.red_team", "§31 Red Team", DevelopmentState.NOT_DESIGNED),
            ("omega.verifier_of_verifiers", "§32 Verifier-of-Verifiers", DevelopmentState.NOT_DESIGNED),
        ]
        for cid, section, state in foundation:
            self._gap_matrix.register(cid, section, state)

    # ---------- Immutable accessors ----------
    @property
    def identity(self) -> str:
        return self._identity

    @property
    def formal_name(self) -> str:
        return self._formal_name

    @property
    def core_version(self) -> str:
        return self._core_version

    @property
    def project_version(self) -> str:
        return self._project_version

    @property
    def spec_version(self) -> str:
        return self._spec_version

    @property
    def safety_boundaries(self) -> FrozenSet[SafetyBoundary]:
        return self._safety_boundaries

    @property
    def resource_ceilings(self) -> Dict[str, ResourceCeiling]:
        return dict(self._resource_ceilings)  # defensive copy

    @property
    def promotion_requirements(self) -> FrozenSet[str]:
        return self._promotion_requirements

    @property
    def verification_hierarchy(self) -> List[str]:
        return list(self._verification_hierarchy)

    @property
    def claim_discipline(self) -> ClaimDiscipline:
        return self._claim_discipline

    @property
    def gap_matrix(self) -> GapMatrix:
        return self._gap_matrix

    # ---------- Controlled mutation surfaces ----------
    def record_change(self, record: ChangeControlRecord) -> None:
        """Only path to append a change-control entry. Status must be valid."""
        if record.status not in (ChangeStatus.PROPOSED, ChangeStatus.APPROVED, ChangeStatus.APPLIED, ChangeStatus.ROLLED_BACK, ChangeStatus.REJECTED):
            raise CoreViolationError("Invalid change status")
        self._change_log.append(record)

    def get_change_log(self) -> List[ChangeControlRecord]:
        return list(self._change_log)

    def check_resource(self, name: str, usage: float) -> bool:
        """Return True if usage is within ceiling; raise CoreViolationError if over."""
        ceiling = self._resource_ceilings.get(name)
        if ceiling is None:
            return True  # unknown resources are not hard-limited by Core
        if usage > ceiling.limit:
            raise CoreViolationError(
                f"Resource ceiling exceeded: {name} usage={usage} > limit={ceiling.limit} {ceiling.unit}"
            )
        return True

    def assert_boundary(self, boundary_name: str) -> None:
        names = {b.name for b in self._safety_boundaries}
        if boundary_name not in names:
            raise CoreViolationError(f"Unknown safety boundary: {boundary_name}")

    def promote_component(self, component_id: str, evidence: Dict) -> None:
        """
        Promotion is gated. Evidence must contain the required test keys.
        This is the only path that advances a component to PROMOTED.
        """
        missing = [r for r in self._promotion_requirements if r not in evidence]
        if missing:
            raise CoreViolationError(
                f"Promotion of '{component_id}' blocked. Missing required evidence: {missing}"
            )
        current = self._claim_discipline.get_state(component_id)
        if current is None:
            raise CoreViolationError(f"Component '{component_id}' not registered")
        if current not in (DevelopmentState.VERIFIED, DevelopmentState.BENCHMARKED, DevelopmentState.TESTED):
            raise CoreViolationError(
                f"Component '{component_id}' in state {current} cannot be promoted"
            )
        self._claim_discipline.register(component_id, DevelopmentState.PROMOTED)
        # Gap matrix is updated only if the component is already present
        if component_id in self._gap_matrix.components:
            self._gap_matrix.update_state(component_id, DevelopmentState.PROMOTED)
        else:
            self._gap_matrix.register(
                component_id,
                canonical_section="(dynamic)",
                state=DevelopmentState.PROMOTED,
            )

    def __repr__(self) -> str:
        return (
            f"<OmegaCore identity={self._identity!r} "
            f"core_version={self._core_version!r} "
            f"spec_version={self._spec_version!r}>"
        )
