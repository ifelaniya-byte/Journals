from __future__ import annotations

import os
import shlex
import subprocess
import time
from pathlib import Path
from typing import Iterable


class CommandRunner:
    def __init__(self, root: Path, timeout: int = 120, blocked: Iterable[str] = ()):
        self.root = root.resolve()
        self.timeout = timeout
        self.blocked = tuple(blocked)

    def run(
        self,
        command: str | list[str],
        *,
        cwd: Path | None = None,
        env: dict[str, str] | None = None,
    ) -> dict:
        text = (
            command
            if isinstance(command, str)
            else " ".join(shlex.quote(x) for x in command)
        )
        lowered = text.lower()
        for dangerous in self.blocked:
            if dangerous.lower() in lowered:
                return {
                    "command": text,
                    "exit_code": -999,
                    "stdout": "",
                    "stderr": "Blocked dangerous command.",
                    "duration": 0,
                    "blocked": True,
                }
        actual_cwd = (cwd or self.root).resolve()
        try:
            actual_cwd.relative_to(self.root)
        except ValueError:
            return {
                "command": text,
                "exit_code": -998,
                "stdout": "",
                "stderr": "Working directory escapes workspace.",
                "duration": 0,
                "blocked": True,
            }
        start = time.monotonic()
        try:
            result = subprocess.run(
                command,
                cwd=actual_cwd,
                env={**os.environ, **(env or {})},
                text=True,
                capture_output=True,
                timeout=self.timeout,
                shell=isinstance(command, str),
            )
            return {
                "command": text,
                "exit_code": result.returncode,
                "stdout": (result.stdout or "")[-20000:],
                "stderr": (result.stderr or "")[-20000:],
                "duration": time.monotonic() - start,
                "blocked": False,
            }
        except subprocess.TimeoutExpired:
            return {
                "command": text,
                "exit_code": -124,
                "stdout": "",
                "stderr": "Command timed out.",
                "duration": time.monotonic() - start,
                "blocked": False,
            }
        except Exception as exc:
            return {
                "command": text,
                "exit_code": -1,
                "stdout": "",
                "stderr": str(exc),
                "duration": time.monotonic() - start,
                "blocked": False,
            }
