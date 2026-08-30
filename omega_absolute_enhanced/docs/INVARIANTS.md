# Ω-ABSOLUTE Master Architecture Invariants

Source: Canonical Specification §65.

These invariants are enforced by the Immutable Ω Core and Claim Discipline.

| ID | Invariant | Foundation Status |
|----|-----------|-------------------|
| 001 | Unknown information MUST remain distinguishable from known information | Reserved (Epistemic Engine) |
| 002 | Simulation MUST remain distinguishable from observation | Reserved |
| 003 | Hypothesis MUST remain distinguishable from fact | Reserved (Epistemic) |
| 004 | Implementation MUST remain distinguishable from verification | **ENFORCED** (ClaimDiscipline) |
| 005 | Solver output MUST remain distinguishable from verified output | Reserved |
| 006 | A verifier MUST NOT silently verify itself | **ENFORCED** (hierarchy + Core) |
| 007 | New capabilities MUST compete against baselines | Reserved (Promotion Gate) |
| 008 | Capability promotion requires reproducibility | **ENFORCED** (Core.promote_component) |
| 009 | Capability promotion requires regression testing | **ENFORCED** (promotion requirements) |
| 010 | Capability promotion SHOULD include transfer testing | **ENFORCED** (promotion requirements) |
| 011 | Failed actions MUST be diagnosable | Reserved |
| 012 | Rollback MUST remain available for promoted changes | **ENFORCED** (ChangeControl + Core) |
| 013 | The governance kernel MUST remain outside unrestricted self-modification | **ENFORCED** (OmegaCore design) |
| 014 | Resource usage MUST be measurable whenever the environment exposes telemetry | **ENFORCED** (ResourceTracker) |
| 015 | Provenance MUST survive transformations | **ENFORCED** (ProvenanceRecord immutable) |
| 016 | No component may claim empirical success without empirical execution | **ENFORCED** (ClaimDiscipline) |
| 017 | Majority agreement MUST NOT be treated as proof | Reserved |
| 018 | Recursive critique MUST have a termination policy | **ENFORCED** (resource ceiling max_recursive_critique_depth) |
| 019 | Counterfactual outputs MUST NOT be represented as observations | Reserved |
| 020 | Architectural complexity MUST justify itself through measurable gains | Reserved |

Any future component that violates an enforced invariant will raise `CoreViolationError` or `ClaimViolationError`.
