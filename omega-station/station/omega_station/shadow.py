from __future__ import annotations

import hashlib
import json
from pathlib import Path

IGNORED_DIRS = {
    ".git", ".omega", "__pycache__", ".pytest_cache", ".mypy_cache",
    "node_modules", ".venv", "venv", "dist", "build", ".egg-info",
}


def seal_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def seal_tree(root: Path) -> dict[str, str]:
    """Filesystem truth: hash every file outside ignored dirs."""
    root = Path(root)
    out: dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue
        try:
            out[rel.as_posix()] = seal_bytes(p.read_bytes())
        except OSError:
            out[rel.as_posix()] = "UNREADABLE"
    return out


def manifest_diff(before: dict[str, str], after: dict[str, str]) -> dict:
    return {
        "added": sorted(set(after) - set(before)),
        "removed": sorted(set(before) - set(after)),
        "modified": sorted(
            k for k in set(before) & set(after) if before[k] != after[k]
        ),
    }


class Shadow:
    """Shadow integrity substrate.

    Baseline seals are held by the engine and only resealed after a
    mission is ACCEPTED by both overseers. The actor never sees a
    reseal primitive: integrity is not theirs to grant.

    Seals persist to <workspace>/seals.json so integrity survives
    process restarts: a new station instance reloads the baseline and
    keeps verifying against it (cross-session tamper detection).
    """

    def __init__(self, root: Path, ledger, workspace: Path | None = None):
        self.root = Path(root)
        self.ledger = ledger
        self.workspace = Path(workspace) if workspace else self.root / ".omega"
        self.baseline: dict[str, str] | None = None
        self._load()

    def _persist(self) -> None:
        if self.baseline is None:
            return
        self.workspace.mkdir(parents=True, exist_ok=True)
        (self.workspace / "seals.json").write_text(
            json.dumps(self.baseline, sort_keys=True), encoding="utf-8")

    def _load(self) -> None:
        p = self.workspace / "seals.json"
        if p.exists():
            try:
                self.baseline = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                self.baseline = None

    def seal(self) -> dict[str, str]:
        self.baseline = seal_tree(self.root)
        self._persist()
        self.ledger.append("shadow_sealed", {"files": len(self.baseline)})
        return self.baseline

    def _verify(self) -> dict:
        if self.baseline is None:
            return {"clean": True, "diff": {}, "note": "no baseline sealed"}
        diff = manifest_diff(self.baseline, seal_tree(self.root))
        clean = not (diff["added"] or diff["removed"] or diff["modified"])
        if not clean:
            self.ledger.append("shadow_anomaly", diff)
        return {"clean": clean, "diff": diff}

    def reseal(self, reason: str) -> dict[str, str]:
        old = self.baseline or {}
        new = seal_tree(self.root)
        self.ledger.append(
            "shadow_resealed", {"reason": reason, "diff": manifest_diff(old, new)}
        )
        self.baseline = new
        self._persist()
        return new

    def verify(self) -> dict:
        if self.baseline is None:
            self._load()
        return self._verify()
