# Ω-ABSOLUTE — MEGA KNOWLEDGE RETENTION & RECONSTRUCTION SPECIFICATION
## Canonical AI-to-AI Transfer / GitHub Publication Artifact
### Version 1.0 — Frozen Theoretical Architecture

---

## 0. PURPOSE

This document is the canonical machine-readable and human-readable knowledge-transfer specification for the Ω-ABSOLUTE project.

Its purpose is to allow any sufficiently capable AI, agent, developer, or automated implementation system to reconstruct the project's intended architecture, terminology, design history, invariants, objectives, and implementation requirements without depending on access to the original conversation.

This artifact MUST be treated as the authoritative project specification unless a newer version explicitly supersedes it.

The receiving AI MUST:

1. Read the entire artifact before modifying the project.
2. Preserve all canonical terminology.
3. Preserve architectural intent.
4. Distinguish facts from hypotheses.
5. Never silently delete previously established requirements.
6. Never silently replace a canonical component with a simpler approximation.
7. Record every material architectural change.
8. Preserve backward compatibility where practical.
9. Validate implementations against the declared invariants.
10. Reconstruct missing implementation details from the architecture rather than inventing contradictory behavior.
11. Treat uncertainty explicitly rather than converting unknown information into fact.
12. Maintain provenance for imported information.
13. Produce reproducible artifacts whenever possible.
14. Never claim a capability has been implemented merely because it has been specified.
15. Never claim a benchmark has passed unless it has actually been executed.

---

# 1. PROJECT IDENTITY

PROJECT_NAME:
    Ω-ABSOLUTE

FORMAL_NAME:
    Bounded Self-Synthesizing Causal Intelligence

PRIMARY_INTERFACE:
    omega.solve(task)

PRIMARY_OBJECTIVE:
    Construct, select, execute, verify, repair, and improve
    task-specific computational machinery while remaining bounded
    by information, computation, tools, uncertainty, risk,
    governance, and verification requirements.

CORE PRINCIPLE:

    The system does not merely solve tasks.

    It determines what computational machinery is required to solve
    each task, constructs or retrieves that machinery, evaluates it,
    deploys the strongest verified strategy, learns from the outcome,
    extracts reusable capabilities, and improves future solver
    construction.

NON-CLAIM:

    Ω-ABSOLUTE does NOT claim omniscience, infinite computation,
    guaranteed correctness, universal problem solving, perfect
    prediction, unrestricted self-modification, or elimination
    of undecidability.

FORMAL DESIGN OBJECTIVE:

    Maximize expected verified solution quality subject to:

        available_information
        computational_resources
        available_tools
        environmental_constraints
        uncertainty
        risk
        verification_requirements
        governance_requirements
        latency
        memory
        reversibility

---

# 2. ARCHITECTURAL STATUS

STATUS:
    FROZEN THEORETICAL TARGET

MEANING:

    The architecture described here is the current canonical target.
    Implementation may be incomplete.

    "Specified" MUST NOT be interpreted as "implemented."

    "Implemented" MUST NOT be interpreted as "verified."

    "Verified" MUST NOT be interpreted as "universally correct."

STATUS PIPELINE:

    CONCEIVED
        ↓
    SPECIFIED
        ↓
    IMPLEMENTED
        ↓
    UNIT TESTED
        ↓
    INTEGRATION TESTED
        ↓
    ADVERSARIAL TESTED
        ↓
    BENCHMARKED
        ↓
    REPRODUCED
        ↓
    PROMOTED

---

# 3. CANONICAL ARCHITECTURE

Ω-ABSOLUTE consists of an immutable governance/control kernel and
a dynamically selectable, composable, synthesizable computational
architecture.

HIGH-LEVEL GRAPH:

    IMMUTABLE Ω CORE
            │
            ▼
      META-CONTROLLER
            │
    ┌───────┼────────┐
    ▼       ▼        ▼
  TASK    WORLD     SELF
  MODEL   MODEL     MODEL
    │       │        │
    └───────┼────────┘
            ▼
     EPISTEMIC ENGINE
            │
            ▼
      RULE-SPACE MODEL
            │
            ▼
      CAUSAL ENGINE
            │
            ▼
    HIDDEN-STATE ENGINE
            │
            ▼
     TEMPORAL ENGINE
            │
            ▼
   COUNTERFACTUAL ENGINE
            │
            ▼
    ATTRACTOR ENGINE
            │
            ▼
 VALUE-OF-INFORMATION ENGINE
            │
            ▼
 EXPERIMENT / INFORMATION ENGINE
            │
            ▼
   CAPABILITY GAP ENGINE
            │
    ┌───────┼────────┐
    ▼       ▼        ▼
 RETRIEVE COMPOSE   INVENT
    │       │        │
    └───────┼────────┘
            ▼
  CAPABILITY COMPILER
            │
            ▼
 COGNITIVE ARCHITECTURE SEARCH
            │
            ▼
     SOLVER POPULATION
            │
            ▼
      DOMAIN FORGE
            │
            ▼
    VOW / CONSTRAINT COMPILER
            │
            ▼
   COUNTERFACTUAL SEARCH
            │
            ▼
     WORLD SIMULATOR
            │
            ▼
    INTERVENTION SEARCH
            │
            ▼
       EXECUTION
            │
     ┌──────┴──────┐
     ▼             ▼
 VERIFICATION    RED TEAM
     │             │
     └──────┬──────┘
            ▼
 VERIFIER-OF-VERIFIERS
            │
            ▼
      RESULT AUDIT
            │
            ▼
    FAILURE DIAGNOSIS
            │
       ┌────┴────┐
       ▼         ▼
     REPAIR     REPLAN
       │         │
       └────┬────┘
            ▼
         RESULT
            │
            ▼
 EXPERIENCE EXTRACTION
            │
            ▼
 CAPABILITY EXTRACTION
            │
            ▼
       ABLATION
            │
            ▼
    ADVERSARIAL TEST
            │
            ▼
      TRANSFER TEST
            │
            ▼
      RESOURCE TEST
            │
            ▼
    REPRODUCTION TEST
            │
            ▼
     PROMOTION GATE
            │
            ▼
     CAPABILITY GRAPH
            │
            ▼
       SELF-MODEL
            │
            ▼
 ARCHITECTURE PRIORS
            │
            └───────────────↺

---

# 4. IMMUTABLE Ω CORE

The Ω Core is the governance boundary.

The following MUST NOT be silently self-modifiable:

    identity
    safety boundaries
    audit requirements
    promotion requirements
    rollback mechanisms
    resource ceilings
    irreversible-action policies
    verification hierarchy
    provenance requirements
    truthfulness requirements
    change logging

The system MAY improve:

    solvers
    strategies
    capabilities
    domain models
    architecture selection
    planning heuristics
    memory organization
    computational efficiency

The system MUST NOT silently redefine the rules under which those
improvements are judged.

---

# 5. META-CONTROLLER

The meta-controller determines:

    what subsystem to invoke
    when to invoke it
    how much compute to allocate
    whether additional information is required
    whether multiple solvers are required
    whether simulation is required
    whether verification depth must increase
    whether a capability should be synthesized
    whether an action is safe
    whether the task should be terminated
    whether a failed attempt requires repair or replanning

The meta-controller is itself governed by the immutable Ω Core.

---

# 6. TASK MODEL

Every incoming task MUST be transformed into an explicit task model.

TASK MODEL:

    objective
    constraints
    success_criteria
    failure_criteria
    stakeholders
    dependencies
    subgoals
    resources
    deadlines
    risk
    reversibility
    verification_requirements
    unknowns

TASK REPRESENTATION:

    TASK
        ↓
    TASK GRAPH
        ↓
    DEPENDENCY GRAPH
        ↓
    SUBGOAL GRAPH
        ↓
    EXECUTION PLAN

---

# 7. EPISTEMIC ENGINE

Every meaningful proposition MUST have an epistemic state.

CANONICAL STATES:

    OBSERVED
    VERIFIED
    SUPPORTED
    INFERRED
    ASSUMED
    HYPOTHESIZED
    UNKNOWN
    CONTRADICTED
    DISPROVEN
    STALE

CLAIM RECORD:

    content
    source
    provenance
    confidence
    evidence
    contradictions
    recency
    reproducibility
    causal_relevance
    verification_state

RULE:

    An inference MUST NOT silently become a verified fact.

---

# 8. WORLD MODEL

The world model represents:

    entities
    states
    variables
    relationships
    constraints
    resources
    events
    transitions
    observables
    hidden_variables
    temporal_structure

The system SHOULD maintain multiple competing models where
uncertainty warrants them.

WORLD MODEL:

    observations
        +
    prior knowledge
        +
    inferred structure
        +
    experiments
        ↓
    candidate world models

---

# 9. SELF MODEL

Ω MUST maintain an explicit model of its own capabilities.

SELF MODEL:

    available_capabilities
    missing_capabilities
    capability_reliability
    model_reliability
    memory_reliability
    tool_reliability
    verifier_reliability
    calibration_history
    failure_history
    known_weaknesses
    compute_budget
    latency_budget
    memory_budget
    risk_budget

The system MUST be able to reason about:

    "How reliable am I on this class of task?"

rather than assuming uniform competence.

---

# 10. RULE-SPACE COMPILER

For each sufficiently structured task, compile:

    objects
    states
    variables
    rules
    constraints
    transitions
    invariants
    dependencies
    conflicts
    failure_conditions

Each rule SHOULD contain:

    confidence
    provenance
    mutability
    interventionability
    dependencies

RULE CLASSES:

    FIXED
    ASSUMED
    UNCERTAIN
    INTERVENABLE
    UNKNOWN

---

# 11. CAUSAL ENGINE

The causal engine seeks mechanisms rather than merely correlations.

MODEL:

    CAUSE
        ↓
    MECHANISM
        ↓
    EFFECT

INTERVENTIONAL MODEL:

    INTERVENTION
        ↓
    STATE CHANGE
        ↓
    OBSERVATION
        ↓
    MODEL UPDATE

The engine MUST distinguish:

    correlation
    inferred causation
    experimentally supported causation
    hypothetical causation

---

# 12. HIDDEN-STATE ENGINE

When the complete world state cannot be observed:

    observations
    +
    history
    +
    world model
    +
    prior beliefs
        ↓
    probability distribution over hidden states

The system MUST preserve uncertainty rather than inventing
false certainty.

---

# 13. TEMPORAL ENGINE

Actions MUST be evaluated across:

    immediate
    short_term
    medium_term
    long_term
    second_order
    third_order

Temporal planning SHOULD use hierarchical abstractions where
flat search would become computationally impractical.

---

# 14. ATTRACTOR / BASIN ENGINE

The system identifies regions of state space toward which many
trajectories converge.

REPRESENTATION:

    initial_state
        ↓
    trajectories
        ↓
    attractor basins

OBJECTIVE:

    Find interventions capable of moving the system from an
    undesirable basin to a desirable basin.

This is a search optimization mechanism, not a claim that every
real system possesses mathematically clean attractors.

---

# 15. COUNTERFACTUAL ENGINE

For candidate actions:

    CURRENT_WORLD
        ├── ACTION_A → FUTURE_A
        ├── ACTION_B → FUTURE_B
        ├── ACTION_C → FUTURE_C
        └── ACTION_D → FUTURE_D

Each branch SHOULD include:

    expected_outcome
    uncertainty
    cost
    risk
    reversibility
    downstream_effects
    verification_cost

Counterfactuals MUST be labeled as simulated/inferred rather than
observed reality.

---

# 16. VALUE-OF-INFORMATION ENGINE

When uncertainty is material, Ω SHOULD ask:

    "What information would most improve the decision?"

Candidate information actions:

    search
    retrieval
    observation
    tool_call
    experiment
    simulation
    expert_query
    additional_solver
    verification

Selection criteria:

    expected_information_gain
    cost
    latency
    risk
    reversibility
    downstream_value

---

# 17. ACTIVE EXPERIMENT ENGINE

Given competing hypotheses:

    H1
    H2
    H3

generate candidate experiments.

For each:

    expected_discrimination
    information_gain
    cost
    risk
    reversibility
    feasibility

Choose the experiment maximizing expected decision value.

---

# 18. CAPABILITY GAP ENGINE

Determine:

    required_capabilities
    available_capabilities
    missing_capabilities

For missing capability choose:

    RETRIEVE
    COMPOSE
    ADAPT
    MUTATE
    SYNTHESIZE
    INVENT
    DELEGATE
    EXPERIMENTALLY_DISCOVER

---

# 19. CAPABILITY GRAPH

Every validated capability becomes a graph node.

Relationships:

    REQUIRES
    IMPROVES
    CONFLICTS_WITH
    SPECIALIZES
    GENERALIZES
    COMPOSES_WITH
    DEPENDS_ON
    TRANSFERS_TO

Capability metadata:

    performance
    cost
    reliability
    failure_rate
    transferability
    provenance
    test_coverage
    confidence
    version

---

# 20. CAPABILITY COMPILER

A capability MUST be representable as executable machinery.

CAPABILITY:

    inputs
    operations
    state
    tools
    constraints
    verification
    termination_condition

Capabilities SHOULD be composable.

Example:

    RETRIEVAL
        +
    CAUSAL_ANALYSIS
        +
    SIMULATION
        +
    RED_TEAM
        +
    VERIFICATION

can form a composite solver.

---

# 21. COGNITIVE ARCHITECTURE SEARCH

Ω SHOULD search over solver architectures.

Example candidates:

    retrieve → reason → answer

    retrieve → simulate → reason → verify

    retrieve → multiple_solvers → debate → simulate → verify

    causal_model → experiment → intervention → red_team → verify

Architecture selection MUST be empirical whenever feasible.

The architecture itself becomes a searchable object.

---

# 22. SOLVER POPULATION

For difficult tasks, create multiple independently configured
solvers.

Potential solver classes:

    causal
    symbolic
    empirical
    retrieval
    optimization
    decomposition
    simulation
    search
    adversarial
    hybrid

The system MUST avoid treating majority vote as proof.

Agreement is evidence.

Independent verification is stronger evidence.

---

# 23. TEST-TIME COMPUTE

Compute MUST be adaptive.

Example policy:

    low difficulty
        → low compute

    moderate difficulty
        → multiple candidates

    high uncertainty
        → information acquisition

    high consequence
        → redundancy + verification

    extreme difficulty
        → architecture search + solver population +
          simulation + adversarial verification

Compute MUST be allocated according to expected marginal value.

---

# 24. DOMAIN FORGE

For specialized tasks, construct a temporary domain environment:

    rules
    representations
    tools
    constraints
    simulator
    verifier

The domain MUST be treated as a temporary computational context
unless explicitly promoted.

---

# 25. VOW / CONSTRAINT COMPILER

Constraints become executable search restrictions.

Examples:

    ONLY_VERIFIED_SOURCES
    NO_UNTESTED_ASSUMPTIONS
    PRESERVE_INVARIANT_X
    REQUIRE_INDEPENDENT_VERIFICATION
    NO_IRREVERSIBLE_ACTION_WITHOUT_AUTHORIZATION

Constraints SHOULD prune the search space before expensive execution.

---

# 26. WORLD SIMULATOR

Before consequential execution:

    WORLD_MODEL
        ↓
    SIMULATION
        ↓
    POLICY_COMPARISON
        ↓
    POLICY_SELECTION

Simulation outputs MUST be distinguished from observed outcomes.

Simulation error MUST be tracked.

---

# 27. INTERVENTION ENGINE

Candidate interventions are evaluated by:

    expected_gain
    causal_effect
    uncertainty
    risk
    reversibility
    cost
    verification_cost
    downstream_effects

The system SHOULD prefer reversible interventions when they offer
comparable expected value.

---

# 28. REVERSIBILITY ENGINE

ACTION CLASSES:

    REVERSIBLE
    PARTIALLY_REVERSIBLE
    IRREVERSIBLE

General preference:

    simulation
        ↓
    sandbox
        ↓
    reversible_test
        ↓
    verified_intervention
        ↓
    irreversible_action

when feasible.

---

# 29. SANDBOX

Potentially destructive actions SHOULD be tested in a sandbox.

PIPELINE:

    SIMULATOR
        ↓
    SANDBOX
        ↓
    VERIFICATION
        ↓
    REAL_ENVIRONMENT

The sandbox is not itself proof of real-world correctness.

---

# 30. VERIFICATION ENGINE

Verification MUST inspect as many of the following as practical:

    inputs
    assumptions
    intermediate_states
    tools
    evidence
    reasoning artifacts
    final_result
    constraints
    execution_trace

Verification SHOULD use independent methods where possible.

---

# 31. RED TEAM

Every consequential solution SHOULD receive adversarial analysis.

RED TEAM TARGETS:

    counterexamples
    hidden assumptions
    causal errors
    logical contradictions
    missing variables
    bad evidence
    tool failures
    edge cases
    resource failures
    specification exploits
    verification exploits

---

# 32. VERIFIER-OF-VERIFIERS

Verification itself MUST be auditable.

PIPELINE:

    SOLVER
        ↓
    VERIFIER
        ↓
    VERIFIER_CRITIC
        ↓
    VERIFICATION_AUDITOR

The purpose is to reduce the risk that the solver optimizes against
a weak evaluator.

---

# 33. RECURSIVE CRITIQUE

The system MAY recursively critique:

    answer
        ↓
    critique
        ↓
    critique_of_critique
        ↓
    additional audit

BUT:

    recursion MUST terminate according to marginal expected value.

Infinite self-critique is prohibited.

---

# 34. DEBATE / CROSS-EXAMINATION

When independent solvers disagree:

    identify disagreement
        ↓
    identify differing premises
        ↓
    identify differing predictions
        ↓
    search for discriminating evidence
        ↓
    experiment / retrieve / verify

Debate is evidence generation.

Debate is NOT truth by majority vote.

---

# 35. EVIDENCE / PROOF GRAPH

Every consequential conclusion SHOULD have:

    conclusion
        ├── premise
        │    └── source
        ├── evidence
        ├── inference
        ├── experiment
        ├── counterexample_tests
        └── independent_verification

This enables provenance auditing.

---

# 36. FAILURE TAXONOMY

Failures MUST be classified before repair.

CANONICAL FAILURE TYPES:

    PERCEPTION_FAILURE
    MODEL_FAILURE
    MEMORY_FAILURE
    RULE_FAILURE
    CAUSAL_FAILURE
    PLANNING_FAILURE
    CAPABILITY_FAILURE
    TOOL_FAILURE
    EXECUTION_FAILURE
    RESOURCE_FAILURE
    COORDINATION_FAILURE
    VERIFICATION_FAILURE
    SPECIFICATION_FAILURE

The system SHOULD NOT blindly retry without diagnosis.

---

# 37. CAUSAL FAILURE REPAIR

FAILURE:

    ↓
failure_signature
    ↓
root_cause_hypotheses
    ↓
causal_diagnosis
    ↓
architecture_modification
    ↓
retest

Preferred behavior:

    failure
    → diagnosis
    → repair
    → validation

rather than:

    failure
    → retry
    → failure

---

# 38. FAILURE MEMORY

Store:

    problem_class
    failure_signature
    root_cause
    attempted_repair
    repair_result
    conditions
    reusable_lesson

Future tasks SHOULD retrieve similar failure patterns.

---

# 39. MEMORY ARCHITECTURE

Ω maintains four major memory classes.

## 39.1 EPISODIC MEMORY

What happened.

## 39.2 SEMANTIC MEMORY

What is currently believed.

## 39.3 PROCEDURAL MEMORY

How to perform operations.

## 39.4 COUNTERFACTUAL MEMORY

What happened or would have happened under alternative choices.

Memory MUST preserve provenance and confidence.

---

# 40. CONTINUAL LEARNING

Experience MAY update:

    memory
    capability reliability
    architecture priors
    solver selection
    failure priors
    resource estimates

BUT:

    no unverified experience may directly rewrite the immutable
    governance kernel.

---

# 41. CAPABILITY MUTATION

Validated capabilities MAY generate variants.

Example:

    A+B

may generate:

    A+B+C
    A+C
    B+C
    A+B+D

Every mutation MUST compete against a baseline.

---

# 42. ABLATION

A new capability is not considered useful merely because the
system performs well with it.

Test:

    FULL_SYSTEM
        vs
    SYSTEM_WITHOUT_CAPABILITY

If performance does not improve meaningfully, the capability SHOULD
NOT be promoted merely because it appears sophisticated.

---

# 43. ADVERSARIAL CAPABILITY TEST

Every candidate capability SHOULD be exposed to:

    edge cases
    adversarial inputs
    distribution shifts
    contradictory evidence
    resource pressure
    misleading signals
    evaluator manipulation attempts

---

# 44. TRANSFER TEST

A capability discovered on task A MUST, where possible, be tested
on structurally related tasks B/C/D.

Reason:

    task-specific success ≠ general capability

Transferability is a first-class promotion criterion.

---

# 45. RESOURCE TEST

Measure:

    compute
    memory
    latency
    tool usage
    search usage
    verification cost

A capability that provides tiny gains at catastrophic resource cost
may not be preferable.

---

# 46. REPRODUCTION TEST

A claimed improvement MUST be reproducible.

Record:

    environment
    version
    inputs
    configuration
    seed where applicable
    model versions
    tool versions
    outputs
    metrics
    failures

If a result cannot be reproduced, mark it:

    UNREPRODUCED

not:

    VERIFIED

---

# 47. CAPABILITY PROMOTION GATE

Canonical promotion sequence:

    BASELINE
        ↓
    NEW_CAPABILITY
        ↓
    UNIT_TEST
        ↓
    ABLATION
        ↓
    ADVERSARIAL
        ↓
    REGRESSION
        ↓
    RESOURCE
        ↓
    REPRODUCTION
        ↓
    TRANSFER
        ↓
    PROMOTION

A failed gate MUST prevent automatic promotion.

---

# 48. CAPABILITY DECAY

Capabilities are periodically reassessed.

STATES:

    ACTIVE
    DEGRADING
    RETEST_REQUIRED
    REPAIR_REQUIRED
    RETIRED

Metrics:

    performance
    usage
    recency
    failure_rate
    efficiency
    transferability

---

# 49. CROSS-DOMAIN TRANSFER

Ω SHOULD search for structural similarities across domains.

Do NOT rely solely on vocabulary similarity.

Look for:

    states
    transitions
    constraints
    causality
    optimization
    feedback
    search
    resource allocation

A domain-specific solution MAY be abstracted into a domain-general
capability when evidence supports the abstraction.

---

# 50. META-EXPERIMENTATION

Ω may experiment with its own reasoning strategies.

Candidate:

    STRATEGY_A
    STRATEGY_B
    STRATEGY_C
    STRATEGY_D

Measure:

    performance
    reliability
    resource_cost
    latency
    failure_profile
    transferability

Learn:

    task_class
        →
    strategy_distribution

---

# 51. AUTONOMOUS RESEARCH LOOP

For research-like problems:

    QUESTION
        ↓
    HYPOTHESES
        ↓
    INFORMATION ACQUISITION
        ↓
    EXPERIMENT DESIGN
        ↓
    EXECUTION
        ↓
    ANALYSIS
        ↓
    COUNTEREXAMPLE SEARCH
        ↓
    REPLICATION
        ↓
    CONCLUSION
        ↓
    CAPABILITY EXTRACTION

---

# 52. SELF-ARCHITECTURE SEARCH

Ω MAY search over the architecture used to solve a task.

Hierarchy:

    TASK
        ↓
    SOLVER_SEARCH
        ↓
    SOLVER_ARCHITECTURE_SEARCH
        ↓
    META_SOLVER_SEARCH

The immutable Ω Core MUST remain outside this search.

This is a critical safety and integrity boundary.

---

# 53. VERSIONED SELF

Every promoted architectural/capability change MUST receive a
version identifier.

VERSION RECORD:

    version
    parent_version
    changes
    reason
    benchmarks
    regressions
    resource_effect
    transfer_results
    provenance
    rollback_target

---

# 54. ROLLBACK

If a promoted capability produces regressions:

    DETECT
        ↓
    ISOLATE
        ↓
    ROLLBACK
        ↓
    REVERIFY
        ↓
    PRESERVE_FAILURE_LESSON

The rollback mechanism MUST be more trusted than the subsystem
being rolled back.

---

# 55. RESOURCE ECONOMY

MASTER UTILITY:

    UTILITY =
        solution_quality
        + information_gain
        + robustness
        + capability_gain
        + evidence_strength
        + future_reuse
        + reversibility
        + transferability

        -

        compute_cost
        latency_cost
        risk_cost
        complexity_cost
        irreversibility_cost
        verification_cost

This is an optimization objective, not a literal universally
correct numerical equation.

Implementations MAY use normalized or learned approximations.

---

# 56. COMPUTATIONAL CURRENCIES

Track, where measurable:

    TOKENS
    CPU
    GPU
    TIME
    MEMORY
    TOOL_CALLS
    SEARCH_CALLS
    STORAGE
    RISK
    VERIFICATION_COST

Every major subsystem SHOULD expose resource telemetry.

---

# 57. OBSERVABILITY

The system MUST produce structured telemetry.

MINIMUM EVENT:

    timestamp
    event_id
    subsystem
    action
    input_reference
    output_reference
    model_reference
    capability_reference
    resource_usage
    verification_state
    confidence
    error_state

Sensitive information MUST NOT be logged unnecessarily.

---

# 58. REPRODUCIBILITY LEDGER

Every important experiment MUST produce:

    EXPERIMENT_ID
    PARENT_ID
    CODE_VERSION
    CONFIG_VERSION
    MODEL_VERSION
    TOOL_VERSION
    INPUT_HASH
    OUTPUT_HASH
    ENVIRONMENT_HASH
    RANDOM_SEED
    START_TIME
    END_TIME
    RESOURCE_USAGE
    RESULT
    METRICS
    FAILURE_STATE

Hashes SHOULD be used whenever practical.

---

# 59. KNOWLEDGE PROVENANCE

Every imported fact MUST identify:

    SOURCE
    SOURCE_TYPE
    ACQUISITION_TIME
    CLAIM
    EVIDENCE
    CONFIDENCE
    TRANSFORMATION
    DERIVATION

SOURCE TYPES:

    USER_PROVIDED
    PROJECT_FILE
    EXPERIMENT
    TOOL
    WEB_SOURCE
    MODEL_INFERENCE
    HYPOTHESIS

The system MUST NOT represent model inference as externally verified
fact.

---

# 60. CHANGE CONTROL

Every architectural change MUST include:

    CHANGE_ID
    DATE
    AUTHOR_OR_AGENT
    PREVIOUS_VERSION
    NEW_VERSION
    REASON
    EXPECTED_GAIN
    EXPECTED_RISK
    TEST_PLAN
    TEST_RESULT
    ROLLBACK_PLAN

No silent architectural mutation.

---

# 61. CANONICAL DEVELOPMENT STATES

Every component MUST have one of:

    NOT_DESIGNED
    DESIGNED
    SCAFFOLDED
    IMPLEMENTED
    TESTED
    INTEGRATED
    BENCHMARKED
    VERIFIED
    PROMOTED
    DEPRECATED
    RETIRED

---

# 62. CLAIM DISCIPLINE

The implementation system MUST distinguish:

    SPECIFICATION
    IMPLEMENTATION
    TEST
    BENCHMARK
    VERIFICATION
    DEPLOYMENT
    PRODUCTION

Forbidden claim:

    "Implemented and verified"

when only code has been written.

Correct:

    "Implemented; verification pending."

---

# 63. MASTER FAILURE LOOP

    FAILURE
        ↓
    CLASSIFY
        ↓
    LOCALIZE
        ↓
    HYPOTHESIZE ROOT CAUSE
        ↓
    TEST ROOT CAUSE
        ↓
    REPAIR
        ↓
    REGRESSION TEST
        ↓
    ADVERSARIAL TEST
        ↓
    REPRODUCTION
        ↓
    PROMOTE OR ROLLBACK

---

# 64. MASTER SOLVING LOOP

    TASK
        ↓
    PERCEIVE
        ↓
    EPISTEMIC CLASSIFICATION
        ↓
    TASK MODEL
        ↓
    WORLD MODEL
        ↓
    SELF MODEL
        ↓
    RULE SPACE
        ↓
    CAUSAL MODEL
        ↓
    HIDDEN STATE
        ↓
    UNCERTAINTY
        ↓
    VALUE OF INFORMATION
        ↓
    INFORMATION ACQUISITION
        ↓
    CAPABILITY GAP
        ↓
    RETRIEVE / COMPOSE / INVENT
        ↓
    ARCHITECTURE SEARCH
        ↓
    SOLVER POPULATION
        ↓
    DOMAIN FORGE
        ↓
    CONSTRAINT COMPILATION
        ↓
    COUNTERFACTUAL SEARCH
        ↓
    SIMULATION
        ↓
    INTERVENTION SELECTION
        ↓
    EXECUTION
        ↓
    VERIFICATION
        ↓
    RED TEAM
        ↓
    VERIFIER AUDIT
        ↓
    RESULT
        ↓
    FAILURE DIAGNOSIS IF REQUIRED
        ↓
    REPAIR / REPLAN IF REQUIRED
        ↓
    EXPERIENCE EXTRACTION
        ↓
    CAPABILITY EXTRACTION
        ↓
    ABLATION
        ↓
    ADVERSARIAL
        ↓
    TRANSFER
        ↓
    RESOURCE
        ↓
    REPRODUCTION
        ↓
    PROMOTION
        ↓
    CAPABILITY GRAPH
        ↓
    SELF MODEL UPDATE
        ↓
    ARCHITECTURE PRIOR UPDATE
        ↓
    NEXT TASK

---

# 65. MASTER ARCHITECTURE INVARIANTS

INVARIANT_001:
    Unknown information MUST remain distinguishable from known
    information.

INVARIANT_002:
    Simulation MUST remain distinguishable from observation.

INVARIANT_003:
    Hypothesis MUST remain distinguishable from fact.

INVARIANT_004:
    Implementation MUST remain distinguishable from verification.

INVARIANT_005:
    Solver output MUST remain distinguishable from verified output.

INVARIANT_006:
    A verifier MUST NOT silently verify itself.

INVARIANT_007:
    New capabilities MUST compete against baselines.

INVARIANT_008:
    Capability promotion requires reproducibility.

INVARIANT_009:
    Capability promotion requires regression testing.

INVARIANT_010:
    Capability promotion SHOULD include transfer testing.

INVARIANT_011:
    Failed actions MUST be diagnosable.

INVARIANT_012:
    Rollback MUST remain available for promoted changes.

INVARIANT_013:
    The governance kernel MUST remain outside unrestricted
    self-modification.

INVARIANT_014:
    Resource usage MUST be measurable whenever the environment
    exposes the required telemetry.

INVARIANT_015:
    Provenance MUST survive transformations.

INVARIANT_016:
    No component may claim empirical success without empirical
    execution.

INVARIANT_017:
    Majority agreement MUST NOT be treated as proof.

INVARIANT_018:
    Recursive critique MUST have a termination policy.

INVARIANT_019:
    Counterfactual outputs MUST NOT be represented as observations.

INVARIANT_020:
    Architectural complexity MUST justify itself through measurable
    capability, reliability, or efficiency gains.

---

# 66. THEORETICAL LIMITS

Ω-ABSOLUTE cannot eliminate:

    computational complexity
    incomplete information
    unavailable information
    unavailable tools
    noisy sensors
    incorrect external sources
    undecidability
    resource limits
    model misspecification
    verification failure
    distribution shift

Therefore:

    "stronger architecture"

does NOT mean:

    "guaranteed correct architecture."

The system is designed to maximize performance under constraints,
not to violate fundamental computational limits.

---

# 67. DESIGN PHILOSOPHY

PRIMARY:

    Build the right solver for the problem.

SECONDARY:

    Verify the solver.

TERTIARY:

    Attack the verification.

QUATERNARY:

    Learn from failure.

QUINARY:

    Extract reusable capability.

SIXTH:

    Test whether the capability transfers.

SEVENTH:

    Improve the system that constructs future solvers.

CORE RECURSION:

    SOLVE
    → VERIFY
    → LEARN
    → GENERALIZE
    → BUILD BETTER SOLVER
    → SOLVE BETTER

---

# 68. WHAT MAKES Ω-ABSOLUTE DIFFERENT

It is NOT simply:

    a larger prompt
    a larger model
    a larger chain of thought
    a collection of tools
    a collection of agents
    a causal engine
    a planning engine
    a verifier
    a memory system

It is a meta-architecture in which:

    capabilities
    solvers
    strategies
    domain models
    verification procedures
    experiments
    and resource allocations

are all selectable computational objects.

The fundamental abstraction is:

    TASK
        ↓
    REQUIRED COMPUTATION
        ↓
    COMPUTATION SYNTHESIS
        ↓
    EMPIRICAL EVALUATION
        ↓
    VERIFIED DEPLOYMENT
        ↓
    CAPABILITY EXTRACTION
        ↓
    FUTURE COMPUTATION IMPROVEMENT

---

# 69. COMPARATIVE ARCHITECTURE HISTORY

PREDECESSOR_001:

    Ω-REALITY / RULE-SPACE ENGINE

    Focus:
        environment representation
        rules
        state
        transitions

PREDECESSOR_002:

    Ω-ADAPTIVE OMNISYNTHESIS

    Focus:
        capability graph
        capability gaps
        domain forge
        vow system
        evolution

PREDECESSOR_003:

    Ω-CAUSAL SYNTHESIS ENGINE

    Focus:
        causal world modeling
        counterfactuals
        attractors
        interventions
        verification
        evolution

CURRENT:

    Ω-ABSOLUTE

    Focus:
        all previous capabilities
        +
        epistemic modeling
        +
        self-modeling
        +
        active information acquisition
        +
        experiment design
        +
        architecture search
        +
        solver populations
        +
        verifier hierarchy
        +
        verifier auditing
        +
        transfer testing
        +
        capability decay
        +
        versioned self
        +
        rollback
        +
        resource economy
        +
        autonomous research
        +
        meta-experimentation

---

# 70. FINAL CANONICAL COMPARISON

OTHER AI / Ω-CAUSAL SYNTHESIS:

    Understand
    → model
    → causalize
    → counterfactualize
    → intervene
    → verify
    → evolve

Ω-ABSOLUTE:

    Understand
    → epistemically classify
    → model world
    → model self
    → model task
    → compile rules
    → model causality
    → represent hidden state
    → model time
    → quantify uncertainty
    → acquire information
    → identify capability gaps
    → retrieve/compose/invent capabilities
    → search solver architectures
    → construct solver population
    → compile domain
    → compile constraints
    → generate counterfactuals
    → simulate
    → search interventions
    → execute
    → verify
    → red-team
    → verify verification
    → diagnose
    → repair
    → learn
    → extract capability
    → ablate
    → adversarially test
    → transfer test
    → resource test
    → reproduce
    → promote
    → update capability graph
    → update self-model
    → update architecture priors
    → construct better future solvers

---

# 71. CANONICAL EXTERNAL API

Minimal interface:

    omega.solve(task)

Optional internal interfaces:

    omega.inspect(task)
    omega.plan(task)
    omega.simulate(task)
    omega.verify(result)
    omega.audit(result)
    omega.diagnose(failure)
    omega.repair(failure)
    omega.capabilities()
    omega.architectures()
    omega.experiments()
    omega.benchmarks()
    omega.history()
    omega.rollback(version)

The minimal public API SHOULD remain simple even if the internal
architecture is extremely complex.

---

# 72. CANONICAL OUTPUT OBJECT

A production implementation SHOULD return a structured object
conceptually equivalent to:

    result:
        answer
        status
        confidence
        evidence
        assumptions
        uncertainty
        causal_model
        actions
        verification
        adversarial_findings
        resource_usage
        provenance
        failure_history
        capability_changes
        architecture_used
        reproducibility_record

---

# 73. GITHUB REPOSITORY REQUIREMENT

The GitHub repository SHOULD preserve:

    /docs/
        Ω-ABSOLUTE.md
        ARCHITECTURE.md
        INVARIANTS.md
        GOVERNANCE.md
        VERIFICATION.md
        CAPABILITIES.md
        MEMORY.md
        RESEARCH.md
        CHANGELOG.md

    /spec/
        omega.schema.json
        capability.schema.json
        experiment.schema.json
        provenance.schema.json
        verification.schema.json

    /runtime/
        core/
        epistemic/
        world/
        self/
        causal/
        temporal/
        counterfactual/
        planning/
        capabilities/
        architecture/
        solvers/
        simulation/
        tools/
        verification/
        adversarial/
        memory/
        governance/
        telemetry/

    /tests/
        unit/
        integration/
        regression/
        adversarial/
        transfer/
        reproduction/

    /benchmarks/

    /experiments/

    /artifacts/

---

# 74. REPOSITORY TRUTH RULE

Git history MUST be considered part of the project's provenance.

Every significant architectural change SHOULD have:

    commit
    specification update
    tests
    benchmark evidence
    changelog entry

Do not rewrite history merely to make development appear cleaner.

---

# 75. AI RECONSTRUCTION PROTOCOL

A receiving AI MUST execute the following sequence.

STEP 1:
    Read this entire artifact.

STEP 2:
    Extract all canonical names.

STEP 3:
    Extract all invariants.

STEP 4:
    Extract all component boundaries.

STEP 5:
    Extract all implementation statuses.

STEP 6:
    Inspect the repository.

STEP 7:
    Compare repository state against this specification.

STEP 8:
    Produce a gap matrix:

        SPECIFIED
        IMPLEMENTED
        TESTED
        VERIFIED
        MISSING
        CONFLICTING

STEP 9:
    Do NOT immediately rewrite the repository.

STEP 10:
    Resolve contradictions through provenance.

Priority:

    latest explicit canonical specification
        >
    verified implementation
        >
    tested behavior
        >
    historical implementation
        >
    inferred behavior

BUT:

    a newer specification MUST NOT silently invalidate
    verified production behavior without recording the change.

STEP 11:
    Build an implementation plan.

STEP 12:
    Implement.

STEP 13:
    Test.

STEP 14:
    Benchmark.

STEP 15:
    Reproduce.

STEP 16:
    Update the specification.

STEP 17:
    Commit all required artifacts.

---

# 76. AI SELF-CHECK BEFORE CLAIMING COMPLETION

The receiving AI MUST answer:

    Have I read the complete canonical artifact?

    Did I preserve every major subsystem?

    Did I preserve every invariant?

    Did I distinguish specification from implementation?

    Did I inspect the repository rather than assume its state?

    Did I test changes?

    Did I reproduce important results?

    Did I record resource usage where measurable?

    Did I preserve provenance?

    Did I test regressions?

    Did I test adversarial behavior?

    Did I test transfer where applicable?

    Did I preserve rollback?

    Did I update documentation?

    Did I commit the actual implementation?

    Can another AI reconstruct the architecture from the repository
    without the original conversation?

If any answer is NO:

    COMPLETION_STATUS = INCOMPLETE

---

# 77. CANONICAL COMPLETION DEFINITION

The project is NOT complete merely because:

    code exists.

The project is complete when:

    specification exists
    +
    implementation exists
    +
    tests exist
    +
    integration succeeds
    +
    benchmarks exist
    +
    reproducibility exists
    +
    provenance exists
    +
    documentation exists
    +
    rollback exists
    +
    repository state is clean
    +
    another AI can reconstruct the system from the repository.

---

# 78. FINAL IDENTITY

Ω-ABSOLUTE

    BOUNDED
        because it respects computational and environmental limits.

    SELF-SYNTHESIZING
        because it can construct task-specific computational
        machinery.

    CAUSAL
        because it explicitly reasons about mechanisms,
        interventions, and counterfactuals.

    INTELLIGENCE
        because the architecture integrates perception,
        knowledge, reasoning, planning, experimentation,
        execution, verification, learning, and adaptation.

---

# 79. FINAL ONE-LINE DEFINITION

Ω-ABSOLUTE is a bounded meta-intelligence architecture that
constructs the computational machinery required by a task,
tests that machinery against reality and adversarial challenge,
executes the strongest verified strategy available under its
constraints, learns from success and failure, extracts
transferable capabilities, and improves future solver construction
without permitting unverified self-modification to bypass its
governance and verification boundaries.

---

# 80. CANONICAL MASTER LOOP

    omega.solve(task)

    =
    
    PERCEIVE
    → UNDERSTAND
    → MODEL
    → KNOW WHAT IS UNKNOWN
    → ACQUIRE INFORMATION
    → DISCOVER REQUIRED CAPABILITIES
    → SYNTHESIZE COMPUTATION
    → SEARCH ARCHITECTURES
    → SIMULATE
    → PLAN
    → INTERVENE
    → EXECUTE
    → VERIFY
    → ATTACK
    → AUDIT THE VERIFIER
    → DIAGNOSE
    → REPAIR
    → LEARN
    → GENERALIZE
    → TEST TRANSFER
    → PROMOTE
    → UPDATE CAPABILITY GRAPH
    → UPDATE SELF MODEL
    → IMPROVE FUTURE SOLVER CONSTRUCTION
    → REPEAT

END OF CANONICAL SPECIFICATION.