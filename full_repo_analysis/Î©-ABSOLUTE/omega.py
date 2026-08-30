#!/usr/bin/env python3
"""
Ω-ABSOLUTE entry point.
Canonical external API: omega.solve(task) – §71.
"""

from runtime import solve, get_core, get_meta_controller


def main() -> None:
    core = get_core()
    meta = get_meta_controller()

    print("=" * 60)
    print(f"  {core.identity}")
    print(f"  {core.formal_name}")
    print(f"  Core version : {core.core_version}")
    print(f"  Spec version : {core.spec_version}")
    print("=" * 60)
    print()
    print("Meta-Controller status:")
    for k, v in meta.status().items():
        print(f"  {k}: {v}")
    print()
    print("Gap Matrix Summary:")
    for k, v in core.gap_matrix.summary().items():
        print(f"  {k}: {v}")
    print()
    print("Safety Boundaries:")
    for b in sorted(core.safety_boundaries, key=lambda x: x.name):
        print(f"  - {b.name}: {b.description}")
    print()
    print("Resource Ceilings:")
    for name, ceiling in core.resource_ceilings.items():
        print(f"  - {name}: {ceiling.limit} {ceiling.unit}")
    print()
    print("Promotion Requirements:")
    for r in sorted(core.promotion_requirements):
        print(f"  - {r}")
    print()
    print("Verification Hierarchy:")
    for i, stage in enumerate(core.verification_hierarchy, 1):
        print(f"  {i}. {stage}")
    print()
    print("--- Demo solve() call (foundation stub) ---")
    result = solve({"description": "placeholder task"})
    print(f"Status          : {result['status']}")
    print(f"Architecture    : {result['architecture_used']}")
    print(f"Claim note      : {result['claim_discipline_note']}")
    print(f"Meta decision   : {result['meta_decision']}")
    print()
    print("Foundation layer is live and Core-governed.")
    print("Next phases: Epistemic Engine → Task/World/Self models → … → Verification stack.")


if __name__ == "__main__":
    main()
