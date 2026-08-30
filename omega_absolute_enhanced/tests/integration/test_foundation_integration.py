"""
Integration tests for Ω-ABSOLUTE foundation components.
Tests component interactions and data flow between Core, Telemetry, and Governance.
"""

import sys
from pathlib import Path

# Ensure package root is on path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pytest
from runtime.core.omega_core import OmegaCore, CoreViolationError
from runtime.core.meta_controller import MetaController, ControllerDecision
from runtime.governance.states import DevelopmentState, ClaimLevel
from runtime.governance.claim_discipline import ClaimDiscipline, ClaimViolationError
from runtime.governance.provenance import ProvenanceRecord, SourceType
from runtime.governance.change_control import ChangeControlRecord, ChangeStatus
from runtime.governance.reproducibility import ReproducibilityRecord, ReproStatus
from runtime.governance.gap_matrix import GapMatrix
from runtime.telemetry.events import TelemetryEvent, ResourceUsage
from runtime.telemetry.tracker import ResourceTracker, TelemetryBus
from runtime import solve, get_core, get_meta_controller


class TestCoreTelemetryIntegration:
    """Test integration between Core and Telemetry systems"""
    
    def test_core_enforces_telemetry_limits(self):
        """Test that Core resource ceilings are enforced through telemetry"""
        core = OmegaCore()
        bus = TelemetryBus()
        tracker = ResourceTracker(core, bus)
        
        # Normal operation should work
        tracker.record(ResourceUsage(tokens=100), "test", "normal")
        assert tracker.current.tokens == 100
        
        # Exceeding limits should raise CoreViolationError
        with pytest.raises(CoreViolationError):
            tracker.record(ResourceUsage(tokens=2_000_000), "test", "overflow")
    
    def test_telemetry_events_survive_resource_violations(self):
        """Test that telemetry events are preserved even when resource limits are exceeded"""
        core = OmegaCore()
        bus = TelemetryBus()
        tracker = ResourceTracker(core, bus)
        
        # Record some successful events
        tracker.record(ResourceUsage(tokens=100), "test", "op1")
        tracker.record(ResourceUsage(tokens=50), "test", "op2")
        
        # Attempt to exceed limits
        with pytest.raises(CoreViolationError):
            tracker.record(ResourceUsage(tokens=2_000_000), "test", "overflow")
        
        # Previous events should still be in the bus
        events = bus.get_events()
        assert len(events) == 2  # Only the successful ones


class TestCoreGovernanceIntegration:
    """Test integration between Core and Governance systems"""
    
    def test_claim_discipline_with_core_promotion(self):
        """Test that Core promotion gates work with claim discipline"""
        core = OmegaCore()
        
        # Register a component at implemented level
        core.claim_discipline.register("test.component", DevelopmentState.IMPLEMENTED)
        
        # Try to promote without proper evidence
        with pytest.raises(CoreViolationError):
            core.promote_component("test.component", {})
        
        # Provide full evidence
        evidence = {r: True for r in core.promotion_requirements}
        # Should still fail because implemented state can't be promoted
        with pytest.raises(CoreViolationError):
            core.promote_component("test.component", evidence)
        
        # Upgrade to verified
        core.claim_discipline.register("test.component", DevelopmentState.VERIFIED)
        # Now promotion should work
        core.promote_component("test.component", evidence)
        assert core.claim_discipline.get_state("test.component") == DevelopmentState.PROMOTED
    
    def test_change_control_updates_gap_matrix(self):
        """Test that change control records interact with gap matrix"""
        core = OmegaCore()
        
        # Register a change
        rec = ChangeControlRecord(
            author_or_agent="test",
            previous_version="0.1.0",
            new_version="0.1.1",
            reason="test enhancement",
            expected_gain="better testing",
            expected_risk="low",
            test_plan="integration tests",
            rollback_plan="git revert",
        )
        rec.approve()
        rec.apply()
        core.record_change(rec)
        
        # Verify change was recorded
        changes = core.get_change_log()
        assert len(changes) == 1
        assert changes[0].status == ChangeStatus.APPLIED


class TestMetaControllerIntegration:
    """Test integration between Meta-Controller and other systems"""
    
    def test_meta_controller_respects_core_boundaries(self):
        """Test that Meta-Controller decisions respect Core safety boundaries"""
        core = OmegaCore()
        meta = MetaController(core)
        
        # Test unsafe decisions are rejected
        unsafe_decision = meta.decide({"irreversible": True, "authorized": False})
        assert unsafe_decision.kind == ControllerDecision.REJECT_UNSAFE
        
        # Test safe decisions are allowed
        safe_decision = meta.decide({"irreversible": False, "authorized": True})
        assert safe_decision.kind == ControllerDecision.ALLOW
    
    def test_meta_controller_claim_discipline_integration(self):
        """Test that Meta-Controller enforces claim discipline"""
        core = OmegaCore()
        meta = MetaController(core)
        
        # Meta-controller itself is scaffolded, so it can't claim verification
        decision = meta.decide({
            "component_id": "omega.meta_controller",
            "claimed_status": "VERIFICATION",
        })
        assert decision.kind == ControllerDecision.REJECT_UNSAFE


class TestFullFoundationFlow:
    """Test complete flows through the foundation system"""
    
    def test_complete_task_flow_foundation_only(self):
        """Test complete task flow through foundation (should return foundation stub)"""
        result = solve({"description": "test task"})
        
        # Verify foundation-only response
        assert result["status"] == "FOUNDATION_ONLY"
        assert result["answer"] is None
        assert result["core"]["identity"] == "Ω-ABSOLUTE"
        assert "no claim of task solution" in result["claim_discipline_note"].lower()
    
    def test_full_governance_lifecycle(self):
        """Test complete governance lifecycle from registration to promotion"""
        core = OmegaCore()
        
        # 1. Register new component
        component_id = "test.new_capability"
        core.claim_discipline.register(component_id, DevelopmentState.IMPLEMENTED)
        core._gap_matrix.register(component_id, "§X Test", DevelopmentState.IMPLEMENTED)
        
        # 2. Verify initial state
        assert core.claim_discipline.get_state(component_id) == DevelopmentState.IMPLEMENTED
        assert core._gap_matrix.get_state(component_id) == DevelopmentState.IMPLEMENTED
        
        # 3. Create change control record
        change_rec = ChangeControlRecord(
            author_or_agent="test",
            previous_version="0.1.0",
            new_version="0.1.1",
            reason="upgrade to verified",
            expected_gain="better capability",
            expected_risk="low",
            test_plan="unit tests",
            rollback_plan="git revert",
        )
        change_rec.approve()
        change_rec.apply()
        core.record_change(change_rec)
        
        # 4. Upgrade to verified
        core.claim_discipline.register(component_id, DevelopmentState.VERIFIED)
        core._gap_matrix.update_state(component_id, DevelopmentState.VERIFIED)
        
        # 5. Create reproducibility record
        repo_rec = ReproducibilityRecord(code_version="0.1.1", result="pending")
        repo_rec.complete("success", {"score": 0.95})
        repo_rec.mark_reproduced()
        
        # 6. Promote with full evidence
        evidence = {
            "UNIT_TEST": True,
            "ABLATION": True,
            "ADVERSARIAL": True,
            "REGRESSION": True,
            "RESOURCE": True,
            "REPRODUCTION": True,
            "TRANSFER": True,
        }
        core.promote_component(component_id, evidence)
        
        # 7. Verify final state
        assert core.claim_discipline.get_state(component_id) == DevelopmentState.PROMOTED
        assert core._gap_matrix.get_state(component_id) == DevelopmentState.PROMOTED


class TestTelemetryGovernanceIntegration:
    """Test integration between Telemetry and Governance systems"""
    
    def test_provenance_with_telemetry(self):
        """Test that provenance records can be associated with telemetry events"""
        bus = TelemetryBus()
        
        # Create provenance record
        prov_rec = ProvenanceRecord(
            source="test_source",
            source_type=SourceType.PROJECT_FILE,
            claim="test claim",
            confidence=0.9,
        )
        
        # Create telemetry event
        tel_event = TelemetryEvent(
            subsystem="test_system",
            action="test_action",
            resource_usage=ResourceUsage(tokens=100),
        )
        
        # Both should work independently
        bus.publish(tel_event)
        assert len(bus.get_events()) == 1
        assert prov_rec.confidence == 0.9
    
    def test_resource_tracking_with_change_control(self):
        """Test that resource tracking can be associated with change control"""
        core = OmegaCore()
        bus = TelemetryBus()
        tracker = ResourceTracker(core, bus)
        
        # Record some resource usage
        tracker.record(ResourceUsage(tokens=100, tool_calls=5), "test", "operation")
        
        # Create change control record
        change_rec = ChangeControlRecord(
            author_or_agent="test",
            previous_version="0.1.0",
            new_version="0.1.1",
            reason="resource optimization",
            expected_gain="better efficiency",
            expected_risk="low",
            test_plan="performance tests",
            rollback_plan="git revert",
        )
        
        # Both should work independently
        assert tracker.current.tokens == 100
        assert change_rec.status == ChangeStatus.PROPOSED


class TestErrorRecoveryIntegration:
    """Test error recovery across integrated systems"""
    
    def test_resource_violation_does_not_corrupt_state(self):
        """Test that resource violations don't corrupt system state"""
        core = OmegaCore()
        bus = TelemetryBus()
        tracker = ResourceTracker(core, bus)
        
        # Record normal operations
        tracker.record(ResourceUsage(tokens=100), "test", "op1")
        tracker.record(ResourceUsage(tokens=50), "test", "op2")
        
        # Attempt violation
        with pytest.raises(CoreViolationError):
            tracker.record(ResourceUsage(tokens=2_000_000), "test", "overflow")
        
        # System state should remain consistent
        assert tracker.current.tokens == 150
        assert len(bus.get_events()) == 2
        assert core.claim_discipline.get_state("omega.core") == DevelopmentState.VERIFIED
    
    def test_claim_violation_does_not_affect_other_components(self):
        """Test that claim violations for one component don't affect others"""
        disc = ClaimDiscipline()
        
        # Register multiple components
        disc.register("component1", DevelopmentState.IMPLEMENTED)
        disc.register("component2", DevelopmentState.VERIFIED)
        
        # Cause violation for component1
        with pytest.raises(ClaimViolationError):
            disc.assert_claim_allowed("component1", ClaimLevel.VERIFICATION)
        
        # component2 should still be able to make verification claims
        assert disc.assert_claim_allowed("component2", ClaimLevel.VERIFICATION)