# Ω-ABSOLUTE Changelog

## [0.1.0-foundation] – 2026-08-30

### Added
- Repository skeleton matching canonical §73 layout.
- Immutable Ω Core (`runtime/core/omega_core.py`) with safety boundaries, resource ceilings, promotion requirements, verification hierarchy.
- Development-state machine and Claim Discipline (`runtime/governance/`).
- Provenance, Change-Control, and Reproducibility ledger types + JSON schemas.
- Gap Matrix with living status and markdown export.
- Telemetry / Resource tracking (`runtime/telemetry/`) enforcing Core ceilings.
- Meta-Controller skeleton (`runtime/core/meta_controller.py`) – SCAFFOLDED.
- Minimal `omega.solve(task)` public API that returns a foundation stub only (no false claims).
- Documentation: ARCHITECTURE.md, INVARIANTS.md, GOVERNANCE.md, FOUNDATION_RELEASE.md, this CHANGELOG.
- Canonical specification copied to `docs/Ω-ABSOLUTE.md`.
- Committed gap-matrix snapshot: `artifacts/GAP_MATRIX_FOUNDATION.md`.
- `.gitignore` for clean permanent history.

### Status Notes
- All foundation components registered in Gap Matrix.
- No task-solving capability is claimed.
- Verification stack, Epistemic Engine, Task/World/Self models remain NOT_DESIGNED.
- This release is the permanent, auditable starting point for GitHub (§74 Repository Truth Rule).
- 13/13 unit tests passed at freeze time.
