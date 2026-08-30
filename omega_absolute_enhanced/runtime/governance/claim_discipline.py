"""
Claim Discipline – §62.
Forbidden claim: "Implemented and verified" when only code has been written.
Correct: "Implemented; verification pending."
INVARIANT_004: Implementation MUST remain distinguishable from verification.
INVARIANT_016: No component may claim empirical success without empirical execution.
"""

from __future__ import annotations

from typing import Dict, Optional, Any

from .states import ClaimLevel, DevelopmentState


class ClaimViolationError(Exception):
    """Raised when a claim exceeds the actual development state."""
    
    def __init__(self, message: str, component_id: Optional[str] = None, 
                 claimed_level: Optional[str] = None, actual_state: Optional[str] = None):
        """
        Initialize ClaimViolationError with enhanced context.
        
        Args:
            message: Error message
            component_id: Component that caused the violation
            claimed_level: The claimed level that was too high
            actual_state: The actual development state
        """
        super().__init__(message)
        self.component_id = component_id
        self.claimed_level = claimed_level
        self.actual_state = actual_state
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging/telemetry"""
        return {
            "error_type": "ClaimViolationError",
            "component_id": self.component_id,
            "claimed_level": self.claimed_level,
            "actual_state": self.actual_state,
            "message": str(self)
        }


# Mapping of DevelopmentState → highest allowable ClaimLevel
_STATE_TO_MAX_CLAIM: Dict[DevelopmentState, ClaimLevel] = {
    DevelopmentState.NOT_DESIGNED: ClaimLevel.SPECIFICATION,
    DevelopmentState.DESIGNED: ClaimLevel.SPECIFICATION,
    DevelopmentState.SCAFFOLDED: ClaimLevel.SPECIFICATION,
    DevelopmentState.IMPLEMENTED: ClaimLevel.IMPLEMENTATION,
    DevelopmentState.TESTED: ClaimLevel.TEST,
    DevelopmentState.INTEGRATED: ClaimLevel.TEST,
    DevelopmentState.BENCHMARKED: ClaimLevel.BENCHMARK,
    DevelopmentState.VERIFIED: ClaimLevel.VERIFICATION,
    DevelopmentState.PROMOTED: ClaimLevel.PRODUCTION,
    DevelopmentState.DEPRECATED: ClaimLevel.DEPLOYMENT,
    DevelopmentState.RETIRED: ClaimLevel.DEPLOYMENT,
}


class ClaimDiscipline:
    """
    Enforces that no component may claim a higher status than its
    actual DevelopmentState. Used by Meta-Controller and promotion gates.
    """

    def __init__(self) -> None:
        self._component_states: Dict[str, DevelopmentState] = {}

    def register(self, component_id: str, state: DevelopmentState) -> None:
        self._component_states[component_id] = state

    def get_state(self, component_id: str) -> Optional[DevelopmentState]:
        return self._component_states.get(component_id)

    def assert_claim_allowed(
        self,
        component_id: str,
        claimed: ClaimLevel,
        *,
        raise_on_violation: bool = True,
    ) -> bool:
        current = self._component_states.get(component_id)
        if current is None:
            msg = f"Component '{component_id}' is not registered; cannot validate claim {claimed.value}"
            if raise_on_violation:
                raise ClaimViolationError(
                    msg,
                    component_id=component_id,
                    claimed_level=claimed.value,
                    actual_state="NOT_REGISTERED"
                )
            return False

        max_allowed = _STATE_TO_MAX_CLAIM[current]
        # ClaimLevel ordering by severity
        order = list(ClaimLevel)
        if order.index(claimed) > order.index(max_allowed):
            msg = (
                f"Claim violation for '{component_id}': "
                f"claimed {claimed.value} but current DevelopmentState is {current.value} "
                f"(max allowed claim: {max_allowed.value}). "
                f"See §62 Claim Discipline and INVARIANT_004 / INVARIANT_016."
            )
            if raise_on_violation:
                raise ClaimViolationError(
                    msg,
                    component_id=component_id,
                    claimed_level=claimed.value,
                    actual_state=current.value
                )
            return False
        return True

    def safe_status_string(self, component_id: str) -> str:
        """Return a claim-discipline-compliant status phrase (§62)."""
        state = self._component_states.get(component_id)
        if state is None:
            return "UNKNOWN (not registered)"
        mapping = {
            DevelopmentState.NOT_DESIGNED: "Not designed; specification only.",
            DevelopmentState.DESIGNED: "Designed; implementation pending.",
            DevelopmentState.SCAFFOLDED: "Scaffolded; implementation incomplete.",
            DevelopmentState.IMPLEMENTED: "Implemented; verification pending.",
            DevelopmentState.TESTED: "Tested; verification and benchmarking pending.",
            DevelopmentState.INTEGRATED: "Integrated; benchmarking and verification pending.",
            DevelopmentState.BENCHMARKED: "Benchmarked; verification pending.",
            DevelopmentState.VERIFIED: "Verified.",
            DevelopmentState.PROMOTED: "Promoted to active capability.",
            DevelopmentState.DEPRECATED: "Deprecated.",
            DevelopmentState.RETIRED: "Retired.",
        }
        return mapping.get(state, f"State: {state.value}")
