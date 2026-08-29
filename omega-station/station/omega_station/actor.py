from __future__ import annotations

import re
from pathlib import Path


class Actor:
    """The acting intelligence in a budgeted, scope-jailed tool loop.

    The actor can: read, list, write (scope files only), edit (scope
    files only), run (jailed commands). Every tool call is appended to
    the evidence ledger. The actor has NO access to seals, no reseal,
    no verification commands of its own making: claims are worthless,
    only the seal diff and verifier runs count.
    """

    def __init__(self, root: Path, runner, ledger, config,
                 role: str = "engineer", on_usage=None):
        self.root = Path(root).resolve()
        self.runner = runner
        self.ledger = ledger
        self.config = config
        self.role = role
        self.model_calls = 0
        self.on_usage = on_usage

    def _jail(self, rel: str) -> Path:
        p = (self.root / rel).resolve()
        if not str(p).startswith(str(self.root)):
            raise PermissionError("path escapes workspace jail")
        return p

    def _scope_ok(self, rel: str, mission: dict) -> bool:
        allowed = set(mission.get("scope_files", [])) | set(mission.get("creates", []))
        if not allowed or rel in allowed:
            return True
        return False

    def run(self, mission: dict, context: dict, on_model_call=None,
            on_usage=None) -> dict:
        from .providers import create_step_provider

        recorder = on_usage or self.on_usage
        try:
            provider = create_step_provider(self.config, mission)
        except Exception as exc:
            # a missing key or bad provider config escalates THIS
            # mission; it must never crash the whole station
            self.ledger.append("actor_error", {"error": str(exc)},
                               task_id=mission["mission_id"])
            return {"verdict": "ESCALATE",
                    "summary": f"provider unavailable: {exc}",
                    "files_changed": [], "evidence": [], "history": []}
        history: list[dict] = []
        self.ledger.append(
            "actor_started",
            {"mission": mission["mission_id"], "role": self.role,
             "attempt": mission.get("attempts", 0)},
            task_id=mission["mission_id"],
        )

        for step_no in range(self.config.max_actor_steps):
            self.model_calls += 1
            if on_model_call:
                on_model_call()
            try:
                action = provider.step({**context, "history": history[-8:]})
            except Exception as exc:
                self.ledger.append("actor_error", {"error": str(exc)},
                                   task_id=mission["mission_id"])
                return {"verdict": "ESCALATE", "summary": f"provider error: {exc}",
                        "files_changed": [], "evidence": [], "history": history}
            usage = getattr(provider, "last_usage", None)
            if usage:
                self.ledger.append("model_usage", usage,
                                   task_id=mission["mission_id"])
                if recorder:
                    recorder(usage)

            tool = action.get("tool", action.get("action", {}).get("tool", "finish"))
            args = action.get("args", action.get("action", {}).get("args", {}))
            if isinstance(args, dict) is False:
                args = {}
            # allow flat form: {"tool": "write", "path": ..., "content": ...}
            for k in ("path", "content", "op", "pattern", "replacement",
                      "text", "command", "verdict", "summary",
                      "files_changed", "evidence"):
                if k in action and k not in args:
                    args[k] = action[k]

            if tool == "finish":
                rec = {"step": step_no + 1, "tool": "finish",
                       "args": _clip(args)}
                history.append(rec)
                self.ledger.append("actor_step", rec,
                                   task_id=mission["mission_id"])
                return {
                    "verdict": str(args.get("verdict", "ESCALATE")).upper(),
                    "summary": str(args.get("summary", ""))[:2000],
                    "files_changed": list(args.get("files_changed") or []),
                    "evidence": [str(e)[:500] for e in (args.get("evidence") or [])][:20],
                    "history": history,
                }
            rec = {"step": step_no + 1, "tool": tool, "args": _clip(args)}
            out = self._dispatch(tool, args, mission)
            rec["result"] = _clip(out)
            history.append(rec)
            self.ledger.append("actor_step", rec, task_id=mission["mission_id"])

        self.ledger.append("actor_budget", {"steps": self.config.max_actor_steps},
                           task_id=mission["mission_id"])
        return {"verdict": "ESCALATE", "summary": "actor step budget exhausted",
                "files_changed": [], "evidence": [], "history": history}

    def _dispatch(self, tool: str, args: dict, mission: dict) -> dict:
        try:
            if tool == "read":
                p = self._jail(str(args.get("path", "")))
                text = p.read_text(encoding="utf-8", errors="ignore")
                return {"ok": True, "content": text[:20000]}
            if tool == "list":
                p = self._jail(str(args.get("path", "")) or ".")
                if not p.is_dir():
                    p = p.parent if p.parent.is_dir() else self.root
                return {"ok": True,
                        "entries": sorted(x.name for x in p.iterdir())[:200]}
            if tool == "write":
                rel = str(args.get("path", ""))
                if not self._scope_ok(rel, mission):
                    return {"ok": False, "denied":
                            f"write outside mission scope: {rel}"}
                p = self._jail(rel)
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(str(args.get("content", "")), encoding="utf-8")
                return {"ok": True, "wrote": rel}
            if tool == "edit":
                rel = str(args.get("path", ""))
                if not self._scope_ok(rel, mission):
                    return {"ok": False, "denied":
                            f"edit outside mission scope: {rel}"}
                p = self._jail(rel)
                text = p.read_text(encoding="utf-8", errors="ignore")
                op = args.get("op")
                if op == "drop_lines_matching":
                    pat = re.compile(args.get("pattern", r"(?!)"))
                    lines = [l for l in text.split(chr(10)) if not pat.search(l)]
                    new = chr(10).join(lines)
                elif op == "replace_first":
                    pat = re.compile(args.get("pattern", r"(?!)"), re.M)
                    new = pat.sub(str(args.get("replacement", "")), text, count=1)
                elif op == "append":
                    new = text + str(args.get("text", ""))
                else:
                    return {"ok": False, "denied": f"unknown edit op: {op}"}
                p.write_text(new, encoding="utf-8")
                return {"ok": True, "edited": rel, "op": op}
            if tool == "run":
                cmd = args.get("command")
                if isinstance(cmd, str):
                    cmd = cmd.split()
                if not isinstance(cmd, list) or not cmd:
                    return {"ok": False, "denied": "command must be a list"}
                res = self.runner.run([str(c) for c in cmd])
                return res
        except PermissionError as exc:
            return {"ok": False, "denied": str(exc)}
        except FileNotFoundError as exc:
            return {"ok": False, "error": str(exc)}
        except Exception as exc:
            return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
        return {"ok": False, "denied": f"unknown tool: {tool}"}


def _clip(obj, limit=4000):
    s = repr(obj)
    return s if len(s) <= limit else s[:limit] + "..."
