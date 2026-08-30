"""
Meta-Controller – §5.
Determines what subsystem to invoke, when, how much compute,
whether additional information is required, whether simulation is required,
whether verification depth must increase, whether a capability should be synthesized,
whether an action is safe, whether the task should be terminated,
whether a failed attempt requires repair or replanning.

The Meta-Controller is itself governed by the immutable Ω Core.
INVARIANT_013: The governance kernel MUST remain outside unrestricted self-modification.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from runtime.core.omega_core import OmegaCore, CoreViolationError
from runtime.telemetry.tracker import ResourceTracker, TelemetryBus
from runtime.telemetry.events import ResourceUsage, TelemetryEvent
from runtime.governance.states import DevelopmentState, ClaimLevel
from runtime.governance.claim_discipline import ClaimViolationError


class ControllerDecision(str, Enum):
    INVOKE_SUBSYSTEM = "INVOKE_SUBSYSTEM"
    ACQUIRE_INFORMATION = "ACQUIRE_INFORMATION"
    INCREASE_VERIFICATION = "INCREASE_VERIFICATION"
    SYNTHESIZE_CAPABILITY = "SYNTHESIZE_CAPABILITY"
    SIMULATE = "SIMULATE"
    TERMINATE = "TERMINATE"
    REPAIR = "REPAIR"
    REPLAN = "REPLAN"
    REJECT_UNSAFE = "REJECT_UNSAFE"
    CONTINUE = "CONTINUE"


@dataclass
class Decision:
    kind: ControllerDecision
    target: Optional[str] = None
    reason: str = ""
    compute_budget: Optional[ResourceUsage] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class MetaController:
    """
    Scaffolded Meta-Controller.
    Current DevelopmentState: SCAFFOLDED (§61).
    Does not yet implement full task routing; provides the governed decision surface.
    """

    def __init__(self, core: OmegaCore, bus: Optional[TelemetryBus] = None) -> None:
        self._core = core
        self._bus = bus or TelemetryBus()
        self._tracker = ResourceTracker(core, self._bus)
        self._invocation_count = 0

        # Register self in claim discipline (already done in Core bootstrap, but ensure)
        self._core.claim_discipline.register("omega.meta_controller", DevelopmentState.SCAFFOLDED)

    @property
    def core(self) -> OmegaCore:
        return self._core

    @property
    def tracker(self) -> ResourceTracker:
        return self._tracker

    def decide(self, context: Dict[str, Any]) -> Decision:
        """
        Core decision entry point.
        At SCAFFOLDED stage this returns CONTINUE or rejects unsafe actions.
        Full routing will be added in later phases.
        """
        self._invocation_count += 1

        # Always enforce claim discipline on any claimed status
        claimed_status = context.get("claimed_status")
        component = context.get("component_id", "omega.meta_controller")
        if claimed_status:
            try:
                level = ClaimLevel(claimed_status)
                self._core.claim_discipline.assert_claim_allowed(component, level)
            except (ValueError, ClaimViolationError) as exc:
                self._emit("claim_violation", str(exc))
                return Decision(
                    kind=ControllerDecision.REJECT_UNSAFE,
                    reason=f"Claim discipline violation: {exc}",
                )

        # Safety boundary check for irreversible actions
        if context.get("irreversible", False) and not context.get("authorized", False):
            self._core.assert_boundary("no_irreversible_without_authorization")
            self._emit("reject_irreversible", "Irreversible action without authorization")
            return Decision(
                kind=ControllerDecision.REJECT_UNSAFE,
                reason="Irreversible action requires explicit authorization (Core safety boundary)",
            )

        # Resource pre-check
        estimated = context.get("estimated_resources")
        if isinstance(estimated, ResourceUsage):
            try:
                self._tracker.record(estimated, "meta_controller", "pre_check")
            except CoreViolationError as exc:
                self._emit("resource_ceiling", str(exc))
                return Decision(
                    kind=ControllerDecision.TERMINATE,
                    reason=f"Resource ceiling would be exceeded: {exc}",
                )

        # Scaffolded behavior: default to CONTINUE
        decision = Decision(
            kind=ControllerDecision.CONTINUE,
            reason="Scaffolded Meta-Controller: no specialized routing yet",
            metadata={"invocation": self._invocation_count},
        )
        self._emit("decision", decision.kind.value)
        return decision

    def _emit(self, action: str, detail: str = "") -> None:
        event = TelemetryEvent(
            subsystem="meta_controller",
            action=action,
            extra={"detail": detail},
        )
        self._bus.publish(event)

    def status(self) -> Dict[str, Any]:
        return {
            "component": "omega.meta_controller",
            "development_state": "SCAFFOLDED",
            "claim_status": self._core.claim_discipline.safe_status_string("omega.meta_controller"),
            "invocations": self._invocation_count,
            "core_identity": self._core.identity,
            "core_version": self._core.core_version,
        }
