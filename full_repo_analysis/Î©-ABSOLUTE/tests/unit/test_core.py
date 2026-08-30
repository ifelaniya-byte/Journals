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
    with pytest.raises(CoreViolationError):
        core.check_resource("max_tokens_per_task", 2_000_000)


def test_claim_discipline_blocks_overclaim():
    disc = ClaimDiscipline()
    disc.register("test.comp", DevelopmentState.IMPLEMENTED)
    # Implementation claim is allowed
    assert disc.assert_claim_allowed("test.comp", ClaimLevel.IMPLEMENTATION)
    # Verification claim is forbidden
    with pytest.raises(ClaimViolationError):
        disc.assert_claim_allowed("test.comp", ClaimLevel.VERIFICATION)


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
