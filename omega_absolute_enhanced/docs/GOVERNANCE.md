# Ω-ABSOLUTE Governance

## Immutable Ω Core (§4)

The following are **not** silently self-modifiable:

- identity
- safety boundaries
- audit requirements
- promotion requirements
- rollback mechanisms
- resource ceilings
- irreversible-action policies
- verification hierarchy
- provenance requirements
- truthfulness requirements
- change logging

The system **may** improve solvers, strategies, capabilities, domain models, architecture selection, planning heuristics, memory organization, and computational efficiency — but **must not** redefine the rules under which those improvements are judged.

## Claim Discipline (§62)

Correct phrasing examples:

- “Implemented; verification pending.”
- “Tested; verification and benchmarking pending.”
- “Verified.”
- “Promoted to active capability.”

Forbidden:

- “Implemented and verified” when only code exists.

## Promotion Gate (§47)

Canonical sequence (enforced by `OmegaCore.promote_component`):

```
BASELINE → NEW_CAPABILITY → UNIT_TEST → ABLATION → ADVERSARIAL
→ REGRESSION → RESOURCE → REPRODUCTION → TRANSFER → PROMOTION
```

A failed gate prevents automatic promotion.

## Change Control (§60)

Every architectural change requires a `ChangeControlRecord` with reason, expected gain/risk, test plan, and rollback plan. No silent mutation.
