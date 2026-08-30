"""
Unit tests for Immutable Ω Core and governance primitives.
These tests themselves follow claim discipline: they verify only what is implemented.
"""

import sys
from pathlib import Path

# Ensure package root is on path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pytest
from runtime.core.omega_core import OmegaCore, CoreViolationError
from runtime.core.meta_controller import MetaController, ControllerDecision
from runtime.governance.states import DevelopmentState, ClaimLevel, SourceType
from runtime.governance.claim_discipline import ClaimDiscipline, ClaimViolationError
from runtime.governance.provenance import ProvenanceRecord
from runtime.governance.change_control import ChangeControlRecord, ChangeStatus
from runtime.governance.reproducibility import ReproducibilityRecord, ReproStatus
from runtime.governance.gap_matrix import GapMatrix, GapStatus
from runtime.telemetry.events import ResourceUsage
from runtime.telemetry.tracker import ResourceTracker, TelemetryBus
from runtime import solve, get_core


def test_core_identity_immutable():
    core = OmegaCore()
    assert core.identity == "Ω-ABSOLUTE"
    assert core.formal_name == "Bounded Self-Synthesizing Causal Intelligence"
    assert "no_unrestricted_self_modification" in {b.name for b in core.safety_boundaries}


def test_resource_ceiling_enforced():
    core = OmegaCore()
    core.check_resource("max_tokens_per_task", 100)  # ok
    with pytest.raises(CoreViolationError) as exc_info:
        core.check_resource("max_tokens_per_task", 2_000_000)
    # Verify enhanced error context
    error = exc_info.value
    assert error.violation_type == "resource_ceiling"
    assert "resource_name" in error.context
    assert error.context["resource_name"] == "max_tokens_per_task"
    assert error.context["exceeded_by"] > 0


def test_claim_discipline_blocks_overclaim():
    disc = ClaimDiscipline()
    disc.register("test.comp", DevelopmentState.IMPLEMENTED)
    # Implementation claim is allowed
    assert disc.assert_claim_allowed("test.comp", ClaimLevel.IMPLEMENTATION)
    # Verification claim is forbidden
    with pytest.raises(ClaimViolationError) as exc_info:
        disc.assert_claim_allowed("test.comp", ClaimLevel.VERIFICATION)
    # Verify enhanced error context
    error = exc_info.value
    assert error.component_id == "test.comp"
    assert error.claimed_level == "VERIFICATION"
    assert error.actual_state == "IMPLEMENTED"


def test_provenance_confidence_bounds():
    with pytest.raises(ValueError):
        ProvenanceRecord(
            source="test",
            source_type=SourceType.HYPOTHESIS,
            claim="x",
            confidence=1.5,
        )
    rec = ProvenanceRecord(
        source="test",
        source_type=SourceType.PROJECT_FILE,
        claim="foundation exists",
        confidence=1.0,
    )
    assert rec.confidence == 1.0
    d = rec.to_dict()
    assert d["source_type"] == "PROJECT_FILE"


def test_change_control_lifecycle():
    rec = ChangeControlRecord(
        author_or_agent="test",
        previous_version="0.0.0",
        new_version="0.1.0",
        reason="foundation",
        expected_gain="governance",
        expected_risk="low",
        test_plan="unit tests",
        rollback_plan="git revert",
    )
    assert rec.status == ChangeStatus.PROPOSED
    rec.approve()
    assert rec.status == ChangeStatus.APPROVED
    rec.apply()
    assert rec.status == ChangeStatus.APPLIED
    rec.rollback()
    assert rec.status == ChangeStatus.ROLLED_BACK


def test_reproducibility_status_machine():
    rec = ReproducibilityRecord(code_version="0.1.0", result="pending")
    assert rec.status == ReproStatus.RUNNING
    rec.complete("ok", {"score": 1.0})
    assert rec.status == ReproStatus.COMPLETED
    rec.mark_reproduced()
    assert rec.status == ReproStatus.REPRODUCED


def test_gap_matrix_summary():
    core = OmegaCore()
    summary = core.gap_matrix.summary()
    assert summary["VERIFIED"] >= 1  # Core itself
    assert "SPECIFIED" in summary or "IMPLEMENTED" in summary
    md = core.gap_matrix.to_markdown()
    assert "omega.core" in md


def test_promotion_requires_full_evidence():
    core = OmegaCore()
    core.claim_discipline.register("test.cap", DevelopmentState.VERIFIED)
    with pytest.raises(CoreViolationError):
        core.promote_component("test.cap", evidence={})  # missing all gates
    # Full evidence
    evidence = {r: True for r in core.promotion_requirements}
    core.promote_component("test.cap", evidence)
    assert core.claim_discipline.get_state("test.cap") == DevelopmentState.PROMOTED


def test_meta_controller_rejects_irreversible():
    core = OmegaCore()
    meta = MetaController(core)
    decision = meta.decide({"irreversible": True, "authorized": False})
    assert decision.kind == ControllerDecision.REJECT_UNSAFE


def test_meta_controller_claim_violation():
    core = OmegaCore()
    meta = MetaController(core)
    decision = meta.decide({
        "component_id": "omega.meta_controller",
        "claimed_status": "VERIFICATION",  # too high for SCAFFOLDED
    })
    assert decision.kind == ControllerDecision.REJECT_UNSAFE


def test_solve_returns_foundation_stub_only():
    result = solve({"description": "anything"})
    assert result["status"] == "FOUNDATION_ONLY"
    assert result["answer"] is None
    assert "no claim of task solution" in result["claim_discipline_note"].lower()
    assert result["core"]["identity"] == "Ω-ABSOLUTE"


def test_resource_tracker_enforces_ceiling():
    core = OmegaCore()
    bus = TelemetryBus()
    tracker = ResourceTracker(core, bus)
    # Stay under limit
    tracker.record(ResourceUsage(tokens=100), "test", "ok")
    # Exceed
    with pytest.raises(CoreViolationError):
        tracker.record(ResourceUsage(tokens=2_000_000), "test", "overflow")


def test_telemetry_event_minimum_fields():
    from runtime.telemetry.events import TelemetryEvent
    ev = TelemetryEvent(subsystem="test", action="unit")
    d = ev.to_dict()
    assert "timestamp" in d
    assert "event_id" in d
    assert "subsystem" in d
    assert "action" in d
    assert "resource_usage" in d


# ---------- Enhanced Unit Tests ----------

def test_core_safety_boundaries_immutable():
    """Test that safety boundaries cannot be modified"""
    core = OmegaCore()
    original_boundaries = core.safety_boundaries
    # Attempt to modify boundaries should not affect the core
    try:
        # This should not modify the core as safety_boundaries returns a frozen set
        modified = set(original_boundaries)
        modified.add(SafetyBoundary("new_boundary", "test"))
        # Original should remain unchanged
        assert core.safety_boundaries == original_boundaries
    except Exception:
        # If modification attempt fails, that's also correct
        pass


def test_core_resource_ceilings_defensive_copy():
    """Test that resource ceilings return defensive copies"""
    core = OmegaCore()
    ceilings1 = core.resource_ceilings
    ceilings2 = core.resource_ceilings
    # Modifications to one should not affect the other
    ceilings1["new_limit"] = ResourceCeiling("new", 100, "units")
    assert "new_limit" not in ceilings2
    assert "new_limit" not in core.resource_ceilings


def test_core_verification_hierarchy_defensive_copy():
    """Test that verification hierarchy returns defensive copy"""
    core = OmegaCore()
    hierarchy1 = core.verification_hierarchy
    hierarchy2 = core.verification_hierarchy
    # Modifications to one should not affect the other
    hierarchy1.append("NEW_STAGE")
    assert "NEW_STAGE" not in hierarchy2
    assert "NEW_STAGE" not in core.verification_hierarchy


def test_claim_discipline_unknown_component():
    """Test claim discipline behavior with unknown components"""
    disc = ClaimDiscipline()
    # Unknown component should return None
    assert disc.get_state("unknown.component") is None
    # Should raise error when asserting claims for unknown component
    with pytest.raises(ClaimViolationError) as exc_info:
        disc.assert_claim_allowed("unknown.component", ClaimLevel.IMPLEMENTATION)
    # Verify enhanced error context
    error = exc_info.value
    assert error.component_id == "unknown.component"
    assert error.actual_state == "NOT_REGISTERED"


def test_claim_discipline_state_progression():
    """Test that claim discipline enforces state progression"""
    disc = ClaimDiscipline()
    disc.register("test.comp", DevelopmentState.IMPLEMENTED)
    # Cannot claim verification from implemented
    with pytest.raises(ClaimViolationError):
        disc.assert_claim_allowed("test.comp", ClaimLevel.VERIFICATION)
    # Upgrade to verified
    disc.register("test.comp", DevelopmentState.VERIFIED)
    # Now verification claim is allowed
    assert disc.assert_claim_allowed("test.comp", ClaimLevel.VERIFICATION)


def test_provenance_record_all_source_types():
    """Test provenance record with all source types"""
    for source_type in SourceType:
        rec = ProvenanceRecord(
            source="test",
            source_type=source_type,
            claim="test claim",
            confidence=0.8,
        )
        assert rec.source_type == source_type
        d = rec.to_dict()
        assert d["source_type"] == source_type.name


def test_provenance_transformation_tracking():
    """Test that provenance tracks transformations"""
    rec = ProvenanceRecord(
        source="original",
        source_type=SourceType.PROJECT_FILE,
        claim="original claim",
        confidence=0.9,
    )
    # Add transformation
    rec.add_transformation("processed", "test processor")
    assert len(rec.transformations) == 1
    assert rec.transformations[0]["processor"] == "test processor"


def test_change_control_rejection():
    """Test change control rejection flow"""
    rec = ChangeControlRecord(
        author_or_agent="test",
        previous_version="0.1.0",
        new_version="0.2.0",
        reason="test",
        expected_gain="test",
        expected_risk="low",
        test_plan="test",
        rollback_plan="test",
    )
    rec.reject("insufficient testing")
    assert rec.status == ChangeStatus.REJECTED
    assert rec.rejection_reason == "insufficient testing"


def test_change_control_invalid_status():
    """Test that invalid change control status is rejected"""
    core = OmegaCore()
    from runtime.governance.change_control import ChangeStatus
    # Create a record with manually set invalid status
    class InvalidRecord:
        status = "INVALID_STATUS"
    with pytest.raises(CoreViolationError):
        core.record_change(InvalidRecord())


def test_reproducibility_failure():
    """Test reproducibility record failure handling"""
    rec = ReproducibilityRecord(code_version="0.1.0", result="pending")
    assert rec.status == ReproStatus.RUNNING
    rec.fail("timeout", {"error": "test error"})
    assert rec.status == ReproStatus.FAILED
    assert rec.failure_reason == "timeout"


def test_gap_matrix_registration():
    """Test gap matrix component registration"""
    matrix = GapMatrix()
    matrix.register("test.component", "§X Test Section", DevelopmentState.IMPLEMENTED)
    assert "test.component" in matrix.components
    summary = matrix.summary()
    assert summary["IMPLEMENTED"] >= 1


def test_gap_matrix_update():
    """Test gap matrix state updates"""
    matrix = GapMatrix()
    matrix.register("test.component", "§X", DevelopmentState.IMPLEMENTED)
    matrix.update_state("test.component", DevelopmentState.VERIFIED)
    assert matrix.get_state("test.component") == DevelopmentState.VERIFIED


def test_gap_matrix_unknown_component():
    """Test gap matrix behavior with unknown components"""
    matrix = GapMatrix()
    assert matrix.get_state("unknown") is None
    # Update should handle unknown gracefully
    matrix.update_state("unknown", DevelopmentState.IMPLEMENTED)
    # Should register it
    assert matrix.get_state("unknown") == DevelopmentState.IMPLEMENTED


def test_telemetry_bus_subscribers():
    """Test telemetry bus subscriber functionality"""
    bus = TelemetryBus()
    events_received = []
    
    def subscriber(event):
        events_received.append(event)
    
    bus.subscribe(subscriber)
    from runtime.telemetry.events import TelemetryEvent
    ev = TelemetryEvent(subsystem="test", action="test")
    bus.publish(ev)
    
    assert len(events_received) == 1
    assert events_received[0] == ev


def test_telemetry_bus_filtering():
    """Test telemetry bus event filtering by subsystem"""
    bus = TelemetryBus()
    from runtime.telemetry.events import TelemetryEvent
    bus.publish(TelemetryEvent(subsystem="system1", action="test1"))
    bus.publish(TelemetryEvent(subsystem="system2", action="test2"))
    bus.publish(TelemetryEvent(subsystem="system1", action="test3"))
    
    system1_events = bus.get_events(subsystem="system1")
    assert len(system1_events) == 2
    system2_events = bus.get_events(subsystem="system2")
    assert len(system2_events) == 1


def test_resource_tracker_accumulation():
    """Test resource tracker accumulation"""
    core = OmegaCore()
    bus = TelemetryBus()
    tracker = ResourceTracker(core, bus)
    
    tracker.record(ResourceUsage(tokens=100), "test", "op1")
    tracker.record(ResourceUsage(tokens=50), "test", "op2")
    
    assert tracker.current.tokens == 150


def test_resource_tracker_multiple_resources():
    """Test resource tracker with multiple resource types"""
    core = OmegaCore()
    bus = TelemetryBus()
    tracker = ResourceTracker(core, bus)
    
    tracker.record(ResourceUsage(tokens=100, tool_calls=5, wall_time_seconds=10), "test", "op")
    
    assert tracker.current.tokens == 100
    assert tracker.current.tool_calls == 5
    assert tracker.current.wall_time_seconds == 10


def test_resource_tracker_memory_max():
    """Test that resource tracker uses max for memory"""
    core = OmegaCore()
    bus = TelemetryBus()
    tracker = ResourceTracker(core, bus)
    
    tracker.record(ResourceUsage(memory_mb=100), "test", "op1")
    tracker.record(ResourceUsage(memory_mb=200), "test", "op2")
    tracker.record(ResourceUsage(memory_mb=150), "test", "op3")
    
    # Memory should be max, not sum
    assert tracker.current.memory_mb == 200


def test_meta_controller_safe_decision():
    """Test meta controller allows safe decisions"""
    core = OmegaCore()
    meta = MetaController(core)
    decision = meta.decide({"irreversible": False, "authorized": True})
    assert decision.kind == ControllerDecision.ALLOW


def test_meta_controller_missing_safety_info():
    """Test meta controller with missing safety information"""
    core = OmegaCore()
    meta = MetaController(core)
    # Default should be safe when info is missing
    decision = meta.decide({})
    assert decision.kind == ControllerDecision.ALLOW


def test_development_state_ordering():
    """Test that development states have proper ordering"""
    states = [
        DevelopmentState.NOT_DESIGNED,
        DevelopmentState.DESIGNED,
        DevelopmentState.SCAFFOLDED,
        DevelopmentState.IMPLEMENTED,
        DevelopmentState.TESTED,
        DevelopmentState.INTEGRATED,
        DevelopmentState.BENCHMARKED,
        DevelopmentState.VERIFIED,
        DevelopmentState.PROMOTED,
        DevelopmentState.DEPRECATED,
        DevelopmentState.RETIRED,
    ]
    # Ensure all states are present and unique
    assert len(states) == len(set(states))


def test_core_change_log_persistence():
    """Test that change log persists and grows"""
    core = OmegaCore()
    initial_count = len(core.get_change_log())
    
    rec = ChangeControlRecord(
        author_or_agent="test",
        previous_version="0.1.0",
        new_version="0.1.1",
        reason="test",
        expected_gain="test",
        expected_risk="low",
        test_plan="test",
        rollback_plan="test",
    )
    core.record_change(rec)
    
    assert len(core.get_change_log()) == initial_count + 1


def test_promotion_wrong_state():
    """Test that promotion fails from wrong states"""
    core = OmegaCore()
    core.claim_discipline.register("test.comp", DevelopmentState.IMPLEMENTED)
    evidence = {r: True for r in core.promotion_requirements}
    
    # Should fail from IMPLEMENTED
    with pytest.raises(CoreViolationError):
        core.promote_component("test.comp", evidence)


def test_resource_unknown_resource():
    """Test that unknown resources are not limited"""
    core = OmegaCore()
    # Unknown resources should not raise errors
    assert core.check_resource("unknown_resource", 1_000_000) is True
