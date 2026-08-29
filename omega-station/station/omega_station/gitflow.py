from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path


class GitManager:
    """Final gate: git isolation + PR artifact. NEVER merges.

    - begin(): if the worktree is clean, move station work onto an
      omega/station-* branch so the base branch is never touched.
      If dirty, proceeds WITHOUT isolation and records that fact in
      the ledger (the station never stashes or discards user state).
    - commit_mission(): one commit per ACCEPTED mission, adding only
      the verified changed paths. Escalated/rework changes are never
      committed.
    - finalize(): writes .omega/PR.md (mission table + evidence
      summary). Pushes the branch only when OMEGA_PUSH=1 and an
      origin remote exists; opens a PR only when OMEGA_GH_TOKEN is
      set. Otherwise prints manual instructions. Merging stays a
      human decision, always.
    """

    def __init__(self, root: Path, ledger):
        self.root = Path(root)
        self.ledger = ledger
        self.branch: str | None = None
        self.base_ref: str | None = None
        self.isolated = False

    def _git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args], cwd=self.root, text=True, capture_output=True,
            timeout=60)

    def _ok(self, *args: str) -> str:
        r = self._git(*args)
        return r.stdout if r.returncode == 0 else ""

    def begin(self, missions: list[dict]) -> None:
        if not self._ok("rev-parse", "--is-inside-work-tree"):
            self.ledger.append("gitflow_skip", {"reason": "not a git repo"})
            return
        self.base_ref = (self._ok("branch", "--show-current").strip()
                         or self._ok("rev-parse", "HEAD").strip())
        dirty = bool(self._ok("status", "--short").strip())
        if dirty:
            self.ledger.append("gitflow_unisolated", {
                "reason": "worktree dirty at start; refusing to switch "
                          "branches; base branch carries station commits",
                "base": self.base_ref,
            })
            return
        import time
        self.branch = f"omega/station-{time.strftime('%Y%m%d-%H%M%S')}"
        r = self._git("checkout", "-q", "-b", self.branch)
        self.isolated = r.returncode == 0
        self.ledger.append("gitflow_begin", {
            "branch": self.branch, "base": self.base_ref,
            "isolated": self.isolated,
            "missions": len(missions),
        })

    def commit_mission(self, mission: dict, changed: list[str]) -> None:
        if not self._ok("rev-parse", "--is-inside-work-tree"):
            return
        if changed:
            self._git("add", "-A", "--", *changed)
        ident = ["-c", "user.email=station@omega.local",
                 "-c", "user.name=Omega Station"]
        r = self._git(*ident, "commit", "-qm",
                      f"omega: {mission['mission_id']} - {mission['title']}"
                      + chr(10) + chr(10)
                      + "Accepted by spec+hostile verifiers and both "
                        "overseers; evidence in .omega/evidence.jsonl")
        if r.returncode == 0:
            self.ledger.append("gitflow_commit", {
                "mission": mission["mission_id"], "files": changed,
                "branch": self.branch or self.base_ref,
            })

    def finalize(self, results: list[dict], ledger_check: dict) -> dict:
        if not self._ok("rev-parse", "--is-inside-work-tree"):
            return {"pr": None}
        rows = []
        for r in results:
            rows.append({
                "mission": r.get("mission_id"),
                "status": r.get("status"),
            })
        accepted = [r for r in results if r.get("status") == "complete"]
        escalated = [r for r in results if r.get("status") == "escalated"]
        body = [
            "# Omega Station pull request",
            "",
            f"Base: `{self.base_ref}`",
            f"Branch: `{self.branch or '(base - unisolated)'}`",
            f"Ledger chain: {'OK' if ledger_check.get('ok') else 'BROKEN'} "
            f"({ledger_check.get('records', 0)} records)",
            "",
            f"Accepted missions: {len(accepted)} | "
            f"escalated to human: {len(escalated)}",
            "",
            "| Mission | Status |",
            "|---|---|",
        ]
        for r in results:
            body.append(f"| {r.get('mission_id')} | {r.get('status')} |")
        body += [
            "",
            "Every accepted change was verified by the spec verifier, "
            "the hostile verifier, and both overseers. Full evidence "
            "chain: `.omega/evidence.jsonl`.",
            "",
            "**Merge is a human decision.** Review the diff, then merge "
            "or close.",
        ]
        pr_path = self.root / ".omega" / "PR.md"
        pr_path.parent.mkdir(parents=True, exist_ok=True)
        pr_path.write_text(chr(10).join(body), encoding="utf-8")

        pushed, pr_url = False, None
        if os.getenv("OMEGA_PUSH") == "1" and self.branch:
            if self._ok("remote", "get-url", "origin").strip():
                pr_push = self._git("push", "-q", "-u", "origin", self.branch)
                pushed = pr_push.returncode == 0
        token = os.getenv("OMEGA_GH_TOKEN")
        if token and pushed and self.branch:
            pr_url = self._create_pr(token)
        self.ledger.append("gitflow_finalize", {
            "pr_file": str(pr_path), "pushed": pushed, "pr_url": pr_url,
        })
        return {"pr": str(pr_path), "pushed": pushed, "pr_url": pr_url}

    def _create_pr(self, token: str) -> str | None:
        url = self._ok("remote", "get-url", "origin").strip()
        m = re.search(r"[:/]([^/:]+)/([^/.]+)(?:\.git)?$", url)
        if not m:
            return None
        owner, repo = m.group(1), m.group(2)
        import urllib.request
        payload = json.dumps({
            "title": "Omega Station: verified missions",
            "head": self.branch,
            "base": self.base_ref or "main",
            "body": "See .omega/PR.md (generated with the evidence "
                    "ledger chain).",
        }).encode()
        req = urllib.request.Request(
            f"https://api.github.com/repos/{owner}/{repo}/pulls",
            data=payload, method="POST",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
            })
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode()).get("html_url")
        except Exception as exc:
            self.ledger.append("gitflow_pr_error", {"error": str(exc)})
            return None
