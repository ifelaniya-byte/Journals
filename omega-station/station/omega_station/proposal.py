from __future__ import annotations

import json
import shutil
import time
from pathlib import Path

from .ledger import Ledger
from .policy import PolicyVerifier
from .shadow import manifest_diff, seal_tree

# Collaboration protocol (interoperates with the sibling
# omega-seller-station-sandbox COLLABORATION_PROTOCOL.md): an
# untrusted local proposal JSON is verified here, candidate-only.
# There is no success state beyond PASS_CANDIDATE - named human
# review is always required before anything ships.
INTAKE_DENY = ("publish", "price", "upload", "deploy", "post",
               "email", "curl", "wget", "git push", "http")


def _safe_rel(p) -> bool:
    if not isinstance(p, str) or not p:
        return False
    if p.startswith("/"):
        return False
    if chr(92) in p:            # backslash: windows-ish/escape games
        return False
    if ".." in Path(p).parts:
        return False
    return True


def run_proposal(root: Path, proposal_path: Path,
                 banned_file: Path | None = None,
                 prices_file: Path | None = None) -> dict:
    root = Path(root).resolve()
    workspace = root / ".omega"
    ledger = Ledger(workspace / "proposal-evidence.jsonl")
    prop = json.loads(Path(proposal_path).read_text(encoding="utf-8"))
    pid = str(prop.get("mission_id", "PROP-?"))
    ledger.append("proposal_received", {"mission_id": pid}, task_id=pid)

    def reject(reason):
        ledger.append("proposal_rejected", {"reason": reason},
                      task_id=pid)
        return {"result": "REJECT", "mission_id": pid, "reason": reason}

    # ---- intake gates: fail before anything is copied or written ----
    blob = json.dumps(prop).lower()
    for bad in INTAKE_DENY:
        if '"' + bad + '"' in blob:
            return reject(f"intake denied: '{bad}' action present")
    allowed = prop.get("allowed_paths")
    files = prop.get("files", {})
    if not isinstance(allowed, list) or not allowed:
        return reject("allowed_paths missing/empty")
    if not isinstance(files, dict) or not files:
        return reject("files missing/empty")
    for p in list(allowed) + list(files):
        if not _safe_rel(p):
            return reject(f"unsafe path: {p!r}")
    for p in files:
        if p not in set(allowed):
            return reject(f"write outside allowed_paths: {p}")

    # ---- fresh, disposable candidate copy of the source tree ----
    cand = workspace / f"candidate-{int(time.time())}-{pid}"
    if cand.exists():
        shutil.rmtree(cand)
    shutil.copytree(root, cand, ignore=shutil.ignore_patterns(
        ".git", ".omega", "__pycache__"))
    ledger.append("candidate_created", {"dir": cand.name}, task_id=pid)

    before = seal_tree(cand)
    for p, content in files.items():
        target = cand / p
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(str(content), encoding="utf-8")
    diff = manifest_diff(before, seal_tree(cand))
    changed = set(diff["added"]) | set(diff["modified"]) | set(diff["removed"])
    if changed != set(files):
        shutil.rmtree(cand, ignore_errors=True)
        return reject(f"undeclared changes: {sorted(changed - set(files))}")

    # ---- verifier B: allowlisted local test commands only ----
    from .execution import CommandRunner
    test_results = []
    for cmd in prop.get("run_tests", []):
        if not isinstance(cmd, list) or not cmd:
            return reject("bad test command")
        if cmd[0] not in ("python", "python3") or any(
                x in ("curl", "wget", "ssh", "git") for x in cmd):
            return reject(f"non-allowlisted test command: {cmd}")
        res = CommandRunner(cand, timeout=120).run(cmd)
        test_results.append(res)
        ledger.append("proposal_test", {"cmd": res["command"],
                                        "exit": res["exit_code"]},
                      task_id=pid)
        if res["exit_code"] != 0:
            shutil.rmtree(cand, ignore_errors=True)
            return reject(f"test failed: {res['command']}")

    # ---- policy audit on every written file ----
    if banned_file or prices_file:
        pv = PolicyVerifier.from_files(banned_file, prices_file)
        for p, content in files.items():
            rep = pv.check(str(content))
            if not rep["pass"]:
                shutil.rmtree(cand, ignore_errors=True)
                return reject(
                    f"policy violation in {p}: "
                    f"{[v['rule'] for v in rep['violations']]}")

    ledger.append("proposal_pass_candidate", {
        "files": sorted(files),
        "tests": [t["command"] for t in test_results],
        "candidate_dir": cand.name,
        "note": "PASS_CANDIDATE requires named human review",
    }, task_id=pid)
    return {
        "result": "PASS_CANDIDATE",
        "mission_id": pid,
        "candidate_dir": str(cand),
        "files": sorted(files),
        "requires": "named human review",
    }
