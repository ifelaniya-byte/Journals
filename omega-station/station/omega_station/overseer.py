from __future__ import annotations


class Decision:
    def __init__(self, name: str, accept: bool, reasons: list[str]):
        self.name = name
        self.accept = accept
        self.reasons = reasons


class ValueOverseer:
    """Overseer A: should this be accepted at all? Small, on-mission
    changes only; churn is rejected even when tests pass."""

    def __init__(self, config):
        self.config = config

    def decide(self, mission: dict, seal_diff: dict) -> Decision:
        reasons = []
        changed = (seal_diff.get("added", []) + seal_diff.get("removed", [])
                   + seal_diff.get("modified", []))
        if len(changed) > self.config.max_touched_files:
            reasons.append(f"churn: {len(changed)} files touched "
                           f"(limit {self.config.max_touched_files})")
        allowed = set(mission.get("scope_files", [])) | set(mission.get("creates", []))
        if allowed:
            off = [f for f in changed if f not in allowed]
            if off:
                reasons.append(f"unrelated changes: {off}")
        return Decision("value", not reasons, reasons)


class RiskOverseer:
    """Overseer B: system-level risk. Human-gate on critical missions,
    station budgets, ledger integrity."""

    def __init__(self, config, state, ledger):
        self.config = config
        self.state = state
        self.ledger = ledger

    def decide(self, mission: dict, model_calls: int, elapsed: float) -> Decision:
        reasons = []
        if mission.get("requires_human") and not self.config.auto_accept_critical:
            reasons.append("requires human acceptance (critical trust decision)")
        if model_calls > self.config.max_model_calls:
            reasons.append(f"model call budget exceeded: {model_calls}")
        if elapsed > self.config.max_runtime_seconds:
            reasons.append(f"runtime budget exceeded: {elapsed:.0f}s")
        chain = self.ledger.verify_chain()
        if not chain["ok"]:
            reasons.append(f"ledger chain broken: {chain}")
        return Decision("risk", not reasons, reasons)
