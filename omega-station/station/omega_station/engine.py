from __future__ import annotations

import time
from pathlib import Path

from .actor import Actor
from .config import Config
from .execution import CommandRunner
from .gitflow import GitManager
from .ledger import Ledger
from .omega import missions_from_consensus, plan
from .overseer import RiskOverseer, ValueOverseer
from .scanner import reconcile, scan_filesystem, scan_git
from .shadow import Shadow, manifest_diff, seal_tree
from .stationary import Stationary
from .state import State
from .verifier import HostileVerifier, SpecVerifier

BLOCKING_STATIONARY = {
    "PASS_WITHOUT_CHANGE",
    "CLAIM_WITHOUT_CHANGE",
    "SCOPE_VIOLATION",
    "REQUIRED_FILE_MISSING",
}


class BudgetExceeded(Exception):
    pass


class OmegaStation:
    """The station. Wiring:

    recon: dual independent scans -> consensus -> missions
    run:   per mission, until budgets or completion:
             seals -> omega plan -> actor (jailed tool loop) ->
             seals -> stationary judge -> spec verifier ->
             hostile verifier -> value overseer + risk overseer ->
             accept -> reseal | rework -> directives fed back |
             escalate (incl. human-gate missions)
    """

    def __init__(self, root: Path, config: Config | None = None):
        self.root = Path(root).resolve()
        self.config = config or Config.load(self.root)
        self.workspace = self.root / self.config.workspace
        self.state = State(self.workspace / "state.sqlite3")
        self.ledger = Ledger(self.workspace / "evidence.jsonl")
        self.shadow = Shadow(self.root, self.ledger,
                             workspace=self.workspace)
        self.gitflow = GitManager(self.root, self.ledger)
        self.runner = CommandRunner(
            self.root,
            timeout=self.config.command_timeout,
            blocked=self.config.dangerous_commands,
            allow_network=self.config.allow_network,
            cpu_limit_s=self.config.cpu_limit_s,
            mem_limit_mb=self.config.mem_limit_mb,
            file_limit_mb=self.config.file_limit_mb,
            nproc_limit=self.config.nproc_limit,
            passthrough=self.config.env_passthrough,
        )
        self.actor = Actor(self.root, self.runner, self.ledger, self.config)
        self.stationary = Stationary()
        self.spec_verifier = SpecVerifier(self.runner)
        self.hostile_verifier = HostileVerifier(self.root, self.runner, self.ledger)
        self.value_overseer = ValueOverseer(self.config)
        self.risk_overseer = RiskOverseer(self.config, self.state, self.ledger)
        self._model_calls = 0
        self._started = time.monotonic()
        self.consensus: dict | None = None

    # ---------------- recon ----------------

    def recon(self) -> dict:
        a = scan_filesystem(self.root)
        self.ledger.append("scan_a_complete", {
            "method": a["method"], "files": len(a["inventory"]),
            "findings": len(a["findings"]),
        })
        b = scan_git(self.root)
        self.ledger.append("scan_b_complete", {
            "method": b["method"], "files": len(b["inventory"]),
            "findings": len(b["findings"]),
        })
        self.consensus = reconcile(a, b)
        self.ledger.append("consensus", {
            "confirmed": len(self.consensus["confirmed"]),
            "single_source": len(self.consensus["single_source"]),
            "disputed": len(self.consensus["disputed"]),
        })
        if (self.root / "tests").is_dir():
            res = self.runner.run(
                ["python", "-m", "unittest", "discover", "-s", "tests", "-q"])
            self.state.set_meta("tests_baseline_exit", res["exit_code"])
        return self.consensus

    def generate_missions(self) -> list[dict]:
        if self.consensus is None:
            self.recon()
        missions = missions_from_consensus(self.consensus, self.root)
        for m in missions:
            existing = self.state.get_mission(m["mission_id"])
            if not existing:
                self.state.save_mission(m)
                self.ledger.append("mission_created", {
                    "mission_id": m["mission_id"], "type": m["type"],
                    "risk": m["risk"], "priority": m["priority"],
                }, task_id=m["mission_id"])
        return missions

    # ---------------- reflective loop ----------------

    def run(self) -> list[dict]:
        missions = self.generate_missions()
        self.gitflow.begin(missions)
        results = []
        for mission in missions:
            m = self.state.get_mission(mission["mission_id"]) or mission
            if m.get("status") in {"complete", "escalated"}:
                continue
            try:
                results.append(self.run_mission(m))
            except BudgetExceeded as exc:
                m["status"] = "deferred"
                m["deferred_reason"] = str(exc)
                self.state.save_mission(m)
                self.ledger.append("station_budget_exhausted", {"reason": str(exc)})
                results.append({"mission_id": m["mission_id"],
                                "status": "deferred", "reason": str(exc)})
        self.ledger.append("station_run_complete", {
            "model_calls": self._model_calls,
            "elapsed": round(time.monotonic() - self._started, 1),
            "results": [{k: r.get(k) for k in ("mission_id", "status")}
                        for r in results],
        })
        self.gitflow.finalize(results, self.verify_ledger())
        return results

    def _budget_check(self):
        self._model_calls += 1
        if self._model_calls > self.config.max_model_calls:
            raise BudgetExceeded(
                f"model call budget: {self._model_calls} > "
                f"{self.config.max_model_calls}")
        elapsed = time.monotonic() - self._started
        if elapsed > self.config.max_runtime_seconds:
            raise BudgetExceeded(
                f"runtime budget: {elapsed:.0f}s > "
                f"{self.config.max_runtime_seconds}s")

    def run_mission(self, mission: dict) -> dict:
        mid = mission["mission_id"]
        mission["attempts"] = int(mission.get("attempts", 0)) + 1
        mission["status"] = "running"
        self.state.save_mission(mission)
        self.ledger.append("mission_started", {
            "attempt": mission["attempts"],
            "role": "helper" if mission["attempts"] >= 2 else "engineer",
        }, task_id=mid)

        if self.consensus is None:
            self.recon()

        before = seal_tree(self.root)
        context = {
            "role": "helper" if mission["attempts"] >= 2 else "engineer",
            "mission": {k: v for k, v in mission.items()
                        if k not in ("evidence",)},
            "omega_plan": plan(mission, self.consensus or {}),
            "directives": mission.get("directives", [])[-10:],
            "note": "attempt >= 2 runs as a fresh-context helper; prior "
                    "directives are your only inheritance",
        }
        report = self.actor.run(
            mission, context,
            on_model_call=self._budget_check,
            on_usage=lambda u: self.state.usage(
                mid, self.config.provider, self.config.model, u))
        after = seal_tree(self.root)
        diff = manifest_diff(before, after)

        stationary = self.stationary.observe(mission, before, after, report)
        self.ledger.append("stationary_directives", stationary, task_id=mid)

        if report["verdict"] == "ESCALATE":
            mission["status"] = "escalated"
            mission["final_verdict"] = "ESCALATE"
            mission["evidence"].append({"escalation": report["summary"]})
            self.state.save_mission(mission)
            self.ledger.append("mission_escalated",
                               {"summary": report["summary"]}, task_id=mid)
            return {"mission_id": mid, "status": "escalated",
                    "reason": report["summary"]}

        spec = self.spec_verifier.verify(mission)
        hostile = self.hostile_verifier.verify(mission, diff, self.state)
        value = self.value_overseer.decide(mission, diff)
        risk = self.risk_overseer.decide(
            mission, self._model_calls, time.monotonic() - self._started)
        self.ledger.append("verification_matrix", {
            "spec": {"passed": spec.passed, "reasons": spec.reasons},
            "hostile": {"passed": hostile.passed, "reasons": hostile.reasons},
            "value": {"accept": value.accept, "reasons": value.reasons},
            "risk": {"accept": risk.accept, "reasons": risk.reasons},
        }, task_id=mid)

        blocking = [d for d in stationary if d["code"] in BLOCKING_STATIONARY]
        accepted = (spec.passed and hostile.passed and value.accept
                    and risk.accept and not blocking)

        if accepted:
            mission["status"] = "complete"
            mission["final_verdict"] = "PASS"
            changed_sorted = sorted(set(diff["added"]) | set(diff["removed"])
                                    | set(diff["modified"]))
            mission["evidence"].append({
                "accepted": True,
                "changed": changed_sorted,
                "spec_commands": [c["command"] for c in spec.commands],
            })
            self.state.save_mission(mission)
            self.shadow.reseal(f"mission accepted: {mid}")
            self.gitflow.commit_mission(mission, changed_sorted)
            if (self.root / "tests").is_dir() and \
                    self.state.get_meta("tests_baseline_exit") is None:
                res = self.runner.run(
                    ["python", "-m", "unittest", "discover", "-s", "tests", "-q"])
                self.state.set_meta("tests_baseline_exit", res["exit_code"])
            self.ledger.append("mission_accepted", {
                "attempt": mission["attempts"],
            }, task_id=mid)
            return {"mission_id": mid, "status": "complete"}

        directives = (
            [{"code": f"STATIONARY:{d['code']}", "detail": d["detail"]}
             for d in blocking]
            + [{"code": "SPEC", "detail": r} for r in spec.reasons]
            + [{"code": "HOSTILE", "detail": r} for r in hostile.reasons]
            + [{"code": "VALUE", "detail": r} for r in value.reasons]
            + [{"code": "RISK", "detail": r} for r in risk.reasons]
        )
        mission["directives"] = (mission.get("directives", []) +
                                 directives)[-10:]

        if mission["attempts"] >= self.config.max_attempts:
            mission["status"] = "escalated"
            mission["final_verdict"] = "ESCALATE"
            self.state.save_mission(mission)
            self.ledger.append("mission_escalated",
                               {"reasons": directives}, task_id=mid)
            return {"mission_id": mid, "status": "escalated",
                    "reasons": directives}

        mission["status"] = "rework"
        self.state.save_mission(mission)
        self.ledger.append("mission_rework", {"directives": directives},
                           task_id=mid)
        return {"mission_id": mid, "status": "rework",
                "reasons": directives}

    # ---------------- reporting ----------------

    def verify_ledger(self) -> dict:
        return self.ledger.verify_chain()

    def verify_integrity(self) -> dict:
        return self.shadow.verify()

    def status(self) -> dict:
        missions = self.state.all_missions()
        counts: dict[str, int] = {}
        for m in missions:
            counts[m.get("status", "unknown")] = \
                counts.get(m.get("status", "unknown"), 0) + 1
        return {
            "root": str(self.root),
            "provider": self.config.provider,
            "model_calls": self._model_calls,
            "elapsed_s": round(time.monotonic() - self._started, 1),
            "missions": counts,
            "ledger": self.verify_ledger(),
            "details": [{"id": m["mission_id"], "status": m.get("status"),
                         "attempts": m.get("attempts"),
                         "type": m.get("type")} for m in missions],
        }
