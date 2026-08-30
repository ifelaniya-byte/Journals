"""Seller Station orchestrator — disposable, isolated, evidence-gated."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .actor import EvolvedActor
from .config import Config
from .consensus import reconcile
from .engineers import EngineerPool
from .gitops import GitManager
from .ledger import EvidenceLedger
from .loop import run_loop
from .mapper import OmegaMapper
from .overseers import dual_oversee
from .providers import create_provider
from .sandbox import CommandRunner
from .scanners import independent_dual_scan
from .shadow import ShadowStore
from .state import State
from .stationary import Stationary
from .verifiers import dual_verify


class SellerStation:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.config = Config.load(self.root)
        self.workspace = self.root / self.config.workspace
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.state = State(self.workspace / "state.sqlite3")
        self.ledger = EvidenceLedger(self.workspace / "evidence.jsonl")
        self.shadow = ShadowStore(self.workspace / "shadow.json")
        self.mapper = OmegaMapper(self.root)
        self.stationary = Stationary(self.root)
        self.runner = CommandRunner(
            self.root,
            timeout=self.config.command_timeout_seconds,
            blocked=self.config.dangerous_commands,
        )
        self.provider = create_provider(self.config)
        self.actor = EvolvedActor(self.root, self.provider, self.config.generated_dir)
        self.pool = EngineerPool()
        self.git = GitManager(self.root)

    def _log(self, mission_id: str | None, event: str, data: Any = None) -> None:
        self.ledger.append(mission_id, event, data)
        self.state.event(mission_id, event, data)

    def map_repository(self) -> dict[str, Any]:
        mapping = self.mapper.save(self.workspace / "repository-map.json")
        self.shadow.put("omega-map", mapping, reason="recon")
        return mapping

    def scan(self) -> dict[str, Any]:
        scan_a, scan_b = independent_dual_scan(self.root)
        self.shadow.put("scan-A", scan_a, reason="independent")
        self.shadow.put("scan-B", scan_b, reason="independent")
        # Prove independence: A payload must not contain B's conclusions.
        if "scanner" in (scan_a.get("peer") or {}):
            raise RuntimeError("Scan A saw a peer — independence broken.")
        consensus = reconcile(scan_a, scan_b)
        self.shadow.put("consensus", consensus, reason="reconcile")
        self.map_repository()
        return {
            "scan_a_files": scan_a["file_count"],
            "scan_b_files": scan_b["file_count"],
            "consensus": consensus,
            "seals": {
                "A": self.shadow.verify("scan-A"),
                "B": self.shadow.verify("scan-B"),
                "consensus": self.shadow.verify("consensus"),
            },
        }

    def add_mission(self, mission: dict[str, Any]) -> None:
        mission.setdefault("status", "pending")
        mission.setdefault("attempts", 0)
        mission.setdefault("final_verdict", None)
        if "mission_id" not in mission and "task_id" in mission:
            mission["mission_id"] = mission["task_id"]
        self.state.save_mission(mission)

    def import_missions(self, path: Path) -> int:
        data = json.loads(path.read_text(encoding="utf-8"))
        items = data["missions"] if isinstance(data, dict) and "missions" in data else data
        if isinstance(data, dict) and "tasks" in data:
            items = data["tasks"]
        for item in items:
            self.add_mission(item)
        return len(items)

    def _ready(self) -> list[dict[str, Any]]:
        done = {
            m["mission_id"]
            for m in self.state.all_missions()
            if m.get("status") == "complete"
        }
        ready = []
        for mission in self.state.all_missions():
            if mission.get("status") not in {"pending", "ready", "rework"}:
                continue
            deps = mission.get("dependencies") or []
            if all(dep in done for dep in deps):
                ready.append(mission)
        ready.sort(
            key=lambda m: (
                -int(m.get("priority") or 0),
                {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(
                    str(m.get("risk", "medium")), 2
                ),
            )
        )
        return ready

    def run_mission(self, mission: dict[str, Any]) -> dict[str, Any]:
        mid = mission["mission_id"]
        mission["status"] = "running"
        mission["attempts"] = int(mission.get("attempts") or 0) + 1
        self.state.save_mission(mission)
        self._log(mid, "mission_started", {"attempt": mission["attempts"]})

        scan = self.scan()
        atlas = json.loads((self.workspace / "repository-map.json").read_text())
        failures = list(mission.get("last_failure") or [])

        def ledger_stage(stage: str, data: Any) -> None:
            sealed = self.shadow.put(f"loop-{mid}-{stage}", data, reason=stage)
            self._log(mid, stage, {"seal": sealed})

        looped = run_loop(
            mission,
            atlas,
            failures,
            actor_fn=self.actor.think,
            apply_fn=self.actor.apply,
            ledger_fn=ledger_stage,
        )
        actor_result = looped["actor_result"]
        usage = actor_result.pop("_usage", {})
        self.state.usage(
            mid, self.config.model_provider, self.config.model_name, usage
        )

        v_a, v_b = dual_verify(self.root, self.runner, mission, actor_result)
        self.shadow.put(f"verifier-A-{mid}", v_a, reason="hostile")
        self.shadow.put(f"verifier-B-{mid}", v_b, reason="hostile")
        self._log(mid, "dual_verify", {"A": v_a["verdict"], "B": v_b["verdict"]})

        o_a, o_b = dual_oversee(
            mission,
            v_a,
            v_b,
            consensus=scan["consensus"],
            auto_merge=self.config.auto_merge,
        )
        self._log(mid, "dual_oversee", {"A": o_a, "B": o_b})

        observation = self.stationary.observe(
            {
                "claims": {
                    "files": (actor_result.get("implementation") or {}).get(
                        "files_changed"
                    )
                },
                "facts": {"files": looped["changed"]},
                "verifier_a": v_a,
                "verifier_b": v_b,
            }
        )
        observation["pass_a"] = v_a["verdict"] == "PASS"
        observation["pass_b"] = v_b["verdict"] == "PASS"
        directive = self.stationary.directive(
            observation,
            attempts=mission["attempts"],
            max_attempts=self.config.max_attempts,
        )
        if not (o_a["accept"] and o_b["accept"]):
            directive = "REWORK" if mission["attempts"] < self.config.max_attempts else "ESCALATE"
            if v_a["verdict"] == "PASS" and v_b["verdict"] == "PASS":
                # Verifiers passed, overseers hold for human gate.
                directive = "HOLD"

        if directive == "PASS" and o_a["accept"] and o_b["accept"]:
            mission["status"] = "complete"
            mission["final_verdict"] = "PASS"
            self.shadow.reseal(f"mission-{mid}", mission, reason="accepted")
            self.state.save_mission(mission)
            self.map_repository()
            return {"mission_id": mid, "status": "complete", "directive": directive}

        if directive == "HOLD":
            mission["status"] = "hold"
            mission["final_verdict"] = "HOLD"
            mission["overseer_reasons"] = o_a["reasons"] + o_b["reasons"]
            self.state.save_mission(mission)
            return {
                "mission_id": mid,
                "status": "hold",
                "directive": "HOLD",
                "note": "Human gate. Not sold, not published.",
                "reasons": mission["overseer_reasons"],
            }

        reasons = list(v_a.get("reasons") or []) + list(v_b.get("reasons") or [])
        if directive == "ESCALATE" or mission["attempts"] >= self.config.max_attempts:
            mission["status"] = "escalated"
            mission["final_verdict"] = "ESCALATE"
            mission["last_failure"] = reasons
            self.state.save_mission(mission)
            return {"mission_id": mid, "status": "escalated", "reasons": reasons}

        mission["status"] = "rework"
        mission["last_failure"] = reasons
        self.state.save_mission(mission)
        return {"mission_id": mid, "status": "rework", "reasons": reasons}

    def run(self) -> list[dict[str, Any]]:
        self.scan()
        results = []
        safety = 0
        while True:
            ready = self._ready()
            if not ready:
                break
            safety += 1
            if safety > 64:
                break
            mission = ready[0]
            results.append(self.run_mission(mission))
        return results

    def status(self) -> dict[str, Any]:
        missions = self.state.all_missions()
        counts: dict[str, int] = {}
        for mission in missions:
            key = mission.get("status") or "unknown"
            counts[key] = counts.get(key, 0) + 1
        return {
            "station": str(self.root),
            "missions": len(missions),
            "counts": counts,
            "details": missions,
            "shadow_ok": self.shadow.verify("consensus").get("ok")
            if "consensus" in getattr(self.shadow, "_data", {})
            else None,
        }
