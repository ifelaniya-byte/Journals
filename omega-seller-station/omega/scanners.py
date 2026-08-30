"""Dual independent Shadow scans.

Scan A and Scan B must not see each other's conclusions.
Traversal order is salted by identity so they do not walk the tree the same way.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path
from typing import Any

from .mapper import IGNORED

SECRET_RE = re.compile(
    r"(BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY"
    r"|sk-(?:live|proj)-[A-Za-z0-9]{16,}"
    r"|(?:api[_-]?key|password)\s*[:=]\s*['\"][^'\"]{8,})",
    re.I,
)
TODO_RE = re.compile(r"\b(TODO|FIXME|XXX|HACK)\b")
DESTRUCTIVE_RE = re.compile(
    r"\b(rm\s+-rf|force.push|drop\s+table|mkfs|eval\()\b", re.I
)


class ShadowScanner:
    def __init__(self, root: Path, identity: str):
        if identity not in {"A", "B"}:
            raise ValueError("identity must be A or B")
        self.root = root.resolve()
        self.identity = identity

    def _order_key(self, path: str) -> str:
        return hashlib.sha256(f"{self.identity}:{path}".encode()).hexdigest()

    def _git(self, *args: str) -> str:
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=self.root,
                text=True,
                capture_output=True,
                timeout=20,
            )
            return result.stdout.strip()
        except Exception:
            return ""

    def scan(self) -> dict[str, Any]:
        """Read-only. Never writes. Never reads the sibling scan."""
        files: list[dict[str, Any]] = []
        secrets: list[str] = []
        todos: list[str] = []
        destructive: list[str] = []
        ci: list[str] = []
        containers: list[str] = []
        generated: list[str] = []

        paths = []
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            try:
                relative = path.relative_to(self.root).as_posix()
            except ValueError:
                continue
            if any(part in IGNORED for part in Path(relative).parts):
                continue
            paths.append(path)

        paths.sort(key=lambda p: self._order_key(p.relative_to(self.root).as_posix()))

        for path in paths:
            rel = path.relative_to(self.root).as_posix()
            try:
                st = path.stat()
                mode = oct(st.st_mode & 0o777)
                size = st.st_size
            except OSError:
                mode, size = "?", -1
            rec = {"path": rel, "size": size, "mode": mode, "suffix": path.suffix}
            files.append(rec)
            name = path.name.lower()
            if name in {"dockerfile", "compose.yaml", "compose.yml", "docker-compose.yml"}:
                containers.append(rel)
            if rel.startswith(".github/workflows/") or name in {
                ".gitlab-ci.yml",
                "Jenkinsfile",
            }:
                ci.append(rel)
            if "generated" in Path(rel).parts or rel.endswith(".pyc"):
                generated.append(rel)
            if size > 400_000 or size < 0:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if SECRET_RE.search(text) and "example" not in name:
                secrets.append(rel)
            if TODO_RE.search(text):
                todos.append(rel)
            if DESTRUCTIVE_RE.search(text):
                destructive.append(rel)

        deps = [
            n
            for n in (
                "requirements.txt",
                "pyproject.toml",
                "package.json",
                "Cargo.toml",
                "go.mod",
            )
            if (self.root / n).exists()
        ]
        return {
            "scanner": self.identity,
            "root": str(self.root),
            "files": files,
            "file_count": len(files),
            "secrets_suspects": secrets,
            "todos": todos,
            "destructive_suspects": destructive,
            "ci": ci,
            "containers": containers,
            "generated": generated,
            "dependencies": deps,
            "git_head": self._git("rev-parse", "HEAD"),
            "git_status": self._git("status", "--short"),
        }


def independent_dual_scan(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """A and B constructed separately. Neither receives the other map."""
    scan_a = ShadowScanner(root, "A").scan()
    scan_b = ShadowScanner(root, "B").scan()
    return scan_a, scan_b
