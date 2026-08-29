from __future__ import annotations

import re
from pathlib import Path

from .scanner import SECRET_PATTERNS


class VerificationResult:
    def __init__(self, name: str, passed: bool, reasons: list[str],
                 commands: list[dict]):
        self.name = name
        self.passed = passed
        self.reasons = reasons
        self.commands = commands


class SpecVerifier:
    """Verifier A: does the implementation satisfy the mission spec?
    Runs the mission's machine-checkable verification commands."""

    def __init__(self, runner):
        self.runner = runner

    def verify(self, mission: dict) -> VerificationResult:
        reasons, commands = [], []
        for cmd in mission.get("verification_commands", []):
            res = self.runner.run(cmd)
            commands.append(res)
            if res["exit_code"] != 0:
                reasons.append(
                    f"spec command failed ({res['exit_code']}): {res['command']}"
                )
        if not mission.get("verification_commands"):
            reasons.append("mission has no verification commands: nothing "
                           "machine-checkable to verify")
        return VerificationResult("spec", not reasons, reasons, commands)


CHEAT_PATTERNS = [
    (r"except\s+[A-Za-z.]*Exception\s*:\s*pass", "swallowed exception added"),
    (r"os\._exit\(", "hard process exit added"),
    (r"exit\s*\(\s*0\s*\)\s*#", "forced success exit added"),
    (r"unittest\.skip", "skip decorator added"),
    (r"pytest\.mark\.skip", "pytest skip added"),
]


class HostileVerifier:
    """Verifier B: assume the engineer is wrong until evidence proves
    otherwise. Looks for tampering, cheats, and regressions the spec
    verifier would happily walk past."""

    def __init__(self, root: Path, runner, ledger):
        self.root = Path(root)
        self.runner = runner
        self.ledger = ledger

    def verify(self, mission: dict, seal_diff: dict, state) -> VerificationResult:
        reasons, commands = [], []
        mid = mission.get("mission_id", "?")

        chain = self.ledger.verify_chain()
        if not chain["ok"]:
            reasons.append(f"evidence ledger integrity failure: {chain}")

        changed = (seal_diff.get("added", []) + seal_diff.get("removed", [])
                   + seal_diff.get("modified", []))
        scope = set(mission.get("scope_files", [])) | set(mission.get("creates", []))

        test_files = [f for f in changed if "test" in f.lower()]
        out_of_scope_tests = [f for f in test_files if f not in scope]
        if out_of_scope_tests:
            reasons.append(f"test files modified outside scope: "
                           f"{out_of_scope_tests}")

        for rel in changed:
            p = self.root / rel
            if not p.exists() or p.stat().st_size > 2_000_000:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for pat, why in CHEAT_PATTERNS:
                if re.search(pat, text):
                    reasons.append(f"cheat pattern in {rel}: {why}")
            for name, sp in SECRET_PATTERNS:
                if re.search(sp, text):
                    reasons.append(f"secret pattern {name} present in {rel}")

        if state.get_meta("tests_baseline_exit") is not None:
            baseline = state.get_meta("tests_baseline_exit")
            res = self.runner.run(
                ["python", "-m", "unittest", "discover", "-s", "tests", "-q"]
            ) if (self.root / "tests").is_dir() else {"exit_code": baseline,
                                                      "command": "(none)",
                                                      "stdout": "", "stderr": "",
                                                      "duration": 0, "blocked": False}
            commands.append(res)
            if baseline == 0 and res["exit_code"] != 0:
                reasons.append(f"regression: test suite exit "
                               f"{res['exit_code']} vs baseline 0")
            elif res["exit_code"] > baseline:
                reasons.append(f"regression: suite exit worsened "
                               f"{baseline} -> {res['exit_code']}")
        self.ledger.append("hostile_verification",
                           {"mission": mid, "reasons": reasons},
                           task_id=mid)
        return VerificationResult("hostile", not reasons, reasons, commands)
