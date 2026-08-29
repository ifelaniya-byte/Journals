from __future__ import annotations

import re
from pathlib import Path

RISK_WEIGHT = {"critical": 4, "high": 3, "medium": 2, "low": 1}


def _pyver_check(file: str) -> list:
    return [["python", "-c",
            f"import sys; sys.exit(0) if __import__('os').path.exists('{file}') else sys.exit(1)"]]


def missions_from_consensus(consensus: dict, root: Path) -> list[dict]:
    """Findings -> verifiable engineering missions. Deterministic here:
    Omega's decomposition is a substrate; the LLM creativity lives in
    the actor. Every mission carries machine-checkable verification."""
    root = Path(root)
    missions: list[dict] = []
    confirmed = {c["key"]: c["value"] for c in consensus.get("confirmed", [])}

    def add_mission(m):
        m.setdefault("status", "pending")
        m.setdefault("attempts", 0)
        m.setdefault("evidence", [])
        m.setdefault("directives", [])
        m.setdefault("dependencies", [])
        m.setdefault("creates", [])
        missions.append(m)

    # 1. secrets (critical) - from confirmed findings (list-valued keys)
    secrets = []
    for c in consensus.get("confirmed", []):
        if c["key"].startswith("secret."):
            vals = c["value"] if isinstance(c["value"], list) else [c["value"]]
            secrets.extend(vals)
    seen = set()
    for s in secrets:
        f = s["file"]
        if f in seen:
            continue
        seen.add(f)
        pat = s["pattern"]
        add_mission({
            "mission_id": f"OM-SEC-{len(seen):03d}",
            "type": "remove_secret",
            "title": f"Remove exposed secret from {f}",
            "description": (
                "A secret matching a known credential pattern is committed "
                "in this file. Remove the line(s). Rotating the credential "
                "is a human task and is explicitly out of scope."
            ),
            "requirements": ["Pattern no longer present in the file."],
            "scope_files": [f],
            "risk": "critical",
            "priority": 100,
            "verification_commands": [[
                "python", "-c",
                "import re,sys; sys.exit(1 if re.search(r'%s', "
                "open('%s', errors='ignore').read()) else 0)" % (pat, f),
            ]],
        })

    # 2. destructive scripts (high)
    destr = []
    for c in consensus.get("confirmed", []):
        if c["key"].startswith("destructive."):
            vals = c["value"] if isinstance(c["value"], list) else [c["value"]]
            destr.extend(vals)
    seen = set()
    for d in destr:
        f = d["file"]
        if f in seen:
            continue
        seen.add(f)
        add_mission({
            "mission_id": f"OM-DST-{len(seen):03d}",
            "type": "guard_destructive",
            "title": f"Neutralize destructive pattern in {f}",
            "description": (
                "Script contains a destructive pattern (pipe-to-shell / "
                "filesystem wipe / fork bomb). Comment it out with an "
                "OMEGA-GUARD marker so it cannot execute silently."
            ),
            "requirements": ["File contains the OMEGA-GUARD marker."],
            "scope_files": [f],
            "risk": "high",
            "priority": 80,
            "verification_commands": [[
                "python", "-c",
                "import sys; sys.exit(0 if 'OMEGA-GUARD' in "
                "open('%s', errors='ignore').read() else 1)" % f,
            ]],
        })

    # 3. todo hotspot (low)
    top = confirmed.get("todo.top")
    if top and isinstance(top, dict) and top.get("file"):
        f = top["file"]
        add_mission({
            "mission_id": "OM-TODO-001",
            "type": "burn_todo",
            "title": f"Triage the worst TODO hotspot: {f}",
            "description": (
                "Replace the first TODO/FIXME marker in the file with a "
                "REVIEWED(<date>) marker so the debt is at least visible "
                "and dated. Full resolution may need a human."
            ),
            "requirements": ["File contains a REVIEWED marker."],
            "scope_files": [f],
            "risk": "low",
            "priority": 20,
            "verification_commands": [[
                "python", "-c",
                "import sys; sys.exit(0 if 'REVIEWED' in "
                "open('%s', errors='ignore').read() else 1)" % f,
            ]],
        })

    # 4. missing tests for a python project (medium)
    if confirmed.get("python.project") and not confirmed.get("tests.present"):
        add_mission({
            "mission_id": "OM-TST-001",
            "type": "add_smoke_test",
            "title": "Add a smoke test suite",
            "description": (
                "Python project has no tests. Create a stdlib-only smoke "
                "test that runs green so later missions have a regression "
                "baseline."
            ),
            "requirements": ["Smoke test exists and exits 0."],
            "scope_files": [],
            "creates": ["tests/test_smoke_omega_station.py"],
            "risk": "medium",
            "priority": 40,
            "verification_commands": [["python", "tests/test_smoke_omega_station.py"]],
        })

    # 5. missing dependency manifest (medium)
    deps = confirmed.get("deps.manifest")
    if confirmed.get("python.project") and deps == [] and any(
        (root.rglob("*.py"))
    ):
        third_party = set()
        stdlib = set(getattr(__import__("sys"), "stdlib_module_names", ()))
        for p in root.rglob("*.py"):
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for m in re.finditer(r"^\s*(?:import|from)\s+([A-Za-z_][\w]*)", text, re.M):
                mod = m.group(1)
                if mod not in stdlib and mod != "omega_station":
                    third_party.add(mod)
        content_lines = sorted(third_party) or ["# no third-party imports found"]
        add_mission({
            "mission_id": "OM-DEP-001",
            "type": "add_requirements",
            "title": "Record dependency manifest",
            "description": (
                "Python project has no dependency manifest. Write "
                "requirements.txt from the third-party imports found."
            ),
            "requirements": ["requirements.txt exists."],
            "scope_files": [],
            "creates": ["requirements.txt"],
            "risk": "medium",
            "priority": 30,
            "payload": {"lines": content_lines},
            "verification_commands": _pyver_check("requirements.txt"),
        })

    # 6. dirty worktree (high, requires human) - demonstrates risk gate
    if confirmed.get("git.dirty"):
        add_mission({
            "mission_id": "OM-WIP-001",
            "type": "commit_wip",
            "title": "Uncommitted changes present",
            "description": (
                "The worktree is dirty. Committing on behalf of the owner "
                "is a trust decision: this mission always escalates to a "
                "human unless OMEGA_AUTO_ACCEPT_CRITICAL=1."
            ),
            "requirements": ["Human decides whether to commit."],
            "scope_files": [],
            "risk": "critical",
            "priority": 5,
            "requires_human": True,
            "verification_commands": [],
        })

    return rank(missions)


def rank(missions: list[dict]) -> list[dict]:
    missions.sort(key=lambda m: (-m.get("priority", 0),
                                 -RISK_WEIGHT.get(m.get("risk", "medium"), 2)))
    return missions


def plan(mission: dict, consensus: dict) -> dict:
    """Deterministic Omega planning template per mission type."""
    steps_by_type = {
        "remove_secret": [
            "read the file", "remove lines matching the pattern",
            "verify pattern absent",
        ],
        "guard_destructive": [
            "read the script", "comment out the destructive line with marker",
            "verify marker present",
        ],
        "burn_todo": [
            "read the file", "replace first TODO/FIXME with REVIEWED(date)",
            "verify marker present",
        ],
        "add_smoke_test": ["write tests/test_smoke_omega_station.py", "run it"],
        "add_requirements": ["write requirements.txt from payload lines"],
        "commit_wip": ["escalate: human trust decision"],
    }
    return {
        "mission_id": mission["mission_id"],
        "stages": ["retrieve", "plan", "act", "critique", "revise"],
        "steps": steps_by_type.get(mission["type"], ["inspect", "act", "verify"]),
        "context_slice": [
            c for c in consensus.get("confirmed", [])
            if c["key"].startswith(("secret.", "destructive.", "todo."))
        ][:8],
    }
