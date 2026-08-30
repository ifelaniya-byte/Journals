# Ω-ABSOLUTE

**Bounded Self-Synthesizing Causal Intelligence**

Canonical specification: `docs/Ω-ABSOLUTE.md` (Version 1.0 — Frozen Theoretical Architecture)

## Current Status

**Foundation Layer only** (v0.1.0-foundation)

| Layer | State |
|-------|-------|
| Immutable Ω Core | VERIFIED (governance root) |
| Governance primitives | IMPLEMENTED |
| Meta-Controller | SCAFFOLDED |
| Telemetry / Resource tracking | IMPLEMENTED |
| Epistemic Engine | NOT_DESIGNED |
| Task / World / Self models | NOT_DESIGNED |
| Verification stack | NOT_DESIGNED |
| Full solver | NOT_DESIGNED |

No claim of task-solving capability is made. See §62 Claim Discipline.

## Quick Start

```bash
cd Ω-ABSOLUTE
python omega.py          # prints Core status, gap matrix, safety boundaries
python -m pytest tests/unit -v
```

## Public API

```python
from runtime import solve
result = solve({"description": "..."})
# Returns foundation stub only. answer is always None at this stage.
```

## Reconstruction Protocol

Any receiving AI must follow §75 of the canonical specification before modifying the repository.

## Immutable Foundation Freeze

See `docs/FOUNDATION_RELEASE.md` for the permanent, auditable snapshot of this starting point.
The committed gap-matrix snapshot lives at `artifacts/GAP_MATRIX_FOUNDATION.md`.

This repository begins its permanent Git history at `v0.1.0-foundation`. Later commits must preserve the governance kernel and record every material change via ChangeControl (§60) and the Gap Matrix.
