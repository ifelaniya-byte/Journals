from __future__ import annotations

import subprocess
from pathlib import Path


class GitManager:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def _run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args],
            cwd=self.root,
            text=True,
            capture_output=True,
            timeout=30,
        )

    def available(self) -> bool:
        try:
            return self._run("rev-parse", "--is-inside-work-tree").returncode == 0
        except Exception:
            return False

    def status(self) -> str:
        try:
            return self._run("status", "--short").stdout
        except Exception:
            return ""

    def no_force_push(self) -> None:
        raise RuntimeError("GitManager refuses force-push and merge-to-main.")
