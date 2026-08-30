"""Omega recon map — structure, not conclusions."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

IGNORED = {
    ".git",
    ".omega",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
}


class OmegaMapper:
    def __init__(self, root: Path):
        self.root = root.resolve()

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

    def build(self) -> dict[str, Any]:
        files = []
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            try:
                relative = path.relative_to(self.root)
            except ValueError:
                continue
            if any(part in IGNORED for part in relative.parts):
                continue
            try:
                size = path.stat().st_size
            except OSError:
                size = -1
            files.append(
                {"path": relative.as_posix(), "size": size, "suffix": path.suffix}
            )
        files.sort(key=lambda x: x["path"])
        deps = [
            name
            for name in (
                "requirements.txt",
                "pyproject.toml",
                "package.json",
                "catalog.json",
                "PORTFOLIO.md",
            )
            if (self.root / name).exists()
        ]
        tests = [
            item["path"]
            for item in files
            if "test" in item["path"].lower() or item["path"].startswith("tests/")
        ]
        return {
            "repository": self.root.name,
            "root": str(self.root),
            "git_commit": self._git("rev-parse", "HEAD"),
            "git_branch": self._git("branch", "--show-current"),
            "files": files,
            "dependencies": deps,
            "tests": tests,
            "fingerprint": hashlib.sha256(
                json.dumps(files, sort_keys=True).encode()
            ).hexdigest(),
        }

    def save(self, destination: Path) -> dict[str, Any]:
        mapping = self.build()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(mapping, indent=2), encoding="utf-8")
        return mapping
