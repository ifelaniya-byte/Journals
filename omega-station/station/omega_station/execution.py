from __future__ import annotations

import os
import re
import shlex
import subprocess
import time
from pathlib import Path
from typing import Iterable

try:
    import resource
except ImportError:          # non-posix platforms
    resource = None

# Heuristic, not a container. Deny obvious network egress commands when
# allow_network is False. Real isolation = containers (see README).
NET_PATTERNS = (
    "curl ", "wget ", "pip install", "pip download", "npm install",
    "yarn ", "apt ", "apt-get ", "ssh ", "scp ", "rsync ",
    "git push", "git fetch", "git pull", "git clone",
)

# Credential hygiene: nothing matching these name patterns (or in the
# hard drop set) reaches an actor-spawned process. The station must
# never leak its own OMEGA_API_KEY / GH token into a command the
# actor tricked into printing its environment.
ENV_DROP_RE = re.compile(
    r"(KEY|TOKEN|SECRET|PASSWORD|PASSWD|PASS|CREDENTIAL|COOKIE|AUTH)", re.I)
ENV_DROP_HARD = {
    "SSH_AUTH_SOCK", "GIT_SSH_COMMAND", "GIT_CONFIG", "LD_PRELOAD",
    "LD_LIBRARY_PATH", "BASH_ENV", "ENV", "PROMPT_COMMAND", "SHELLOPTS",
    "PYTHONPATH", "PYTHONHOME", "DOCKER_HOST", "KUBECONFIG",
}
ENV_KEEP = {
    "PATH", "HOME", "LANG", "LC_ALL", "LC_CTYPE", "TZ", "TERM",
    "USER", "LOGNAME", "SHELL", "TMPDIR", "TMP", "TEMP", "HOSTNAME",
    "SYSTEMROOT", "COMSPEC", "PROGRAMFILES", "NUMBER_OF_PROCESSORS",
}


class CommandRunner:
    def __init__(
        self,
        root: Path,
        timeout: int = 180,
        blocked: Iterable[str] = (),
        allow_network: bool = False,
        cpu_limit_s: int = 30,
        mem_limit_mb: int = 2048,
        file_limit_mb: int = 256,
        nproc_limit: int = 128,
        passthrough: Iterable[str] = (),
    ):
        self.root = Path(root).resolve()
        self.timeout = timeout
        self.blocked = tuple(blocked)
        self.allow_network = allow_network
        self.cpu_limit_s = cpu_limit_s
        self.mem_limit_mb = mem_limit_mb
        self.file_limit_mb = file_limit_mb
        self.nproc_limit = nproc_limit
        self.passthrough = set(passthrough)
        self.tmpdir = self.root / ".omega" / "tmp"
        self.tmpdir.mkdir(parents=True, exist_ok=True)

    def _env(self) -> dict[str, str]:
        env: dict[str, str] = {}
        for k, v in os.environ.items():
            if k in self.passthrough or k in ENV_KEEP:
                if k not in ENV_DROP_HARD and not ENV_DROP_RE.search(k):
                    env[k] = v
        env["TMPDIR"] = str(self.tmpdir)
        return env

    def _preexec(self):
        if resource is None:
            return
        cpu = max(1, int(self.cpu_limit_s))
        mem = max(64, int(self.mem_limit_mb)) * 1024 * 1024
        fs = max(16, int(self.file_limit_mb)) * 1024 * 1024
        np_ = max(8, int(self.nproc_limit))
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))
        resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
        resource.setrlimit(resource.RLIMIT_FSIZE, (fs, fs))
        resource.setrlimit(resource.RLIMIT_NPROC, (np_, np_))

    def run(self, command, cwd: Path | None = None) -> dict:
        text = (
            command
            if isinstance(command, str)
            else " ".join(shlex.quote(x) for x in command)
        )
        lowered = text.lower()
        start = time.monotonic()

        def result(exit_code: int, stdout: str, stderr: str,
                   blocked: bool, reason: str = ""):
            return {
                "command": text,
                "exit_code": exit_code,
                "stdout": stdout[-20000:],
                "stderr": (stderr or reason)[-20000:],
                "duration": round(time.monotonic() - start, 3),
                "blocked": blocked,
            }

        for bad in self.blocked:
            if bad.lower() in lowered:
                return result(-999, "", "Blocked: dangerous command.", True)

        if not self.allow_network:
            for pat in NET_PATTERNS:
                if pat in lowered:
                    return result(
                        -997, "",
                        f"Blocked: network command '{pat.strip()}' denied "
                        "(set allow_network=true or OMEGA_ALLOW_NETWORK=1 "
                        "to permit).", True)

        actual_cwd = (cwd or self.root).resolve()
        if not str(actual_cwd).startswith(str(self.root)):
            return result(-998, "", "Blocked: cwd escapes workspace jail.",
                          True)

        try:
            proc = subprocess.run(
                command,
                cwd=actual_cwd,
                env=self._env(),
                text=True,
                capture_output=True,
                timeout=self.timeout,
                shell=isinstance(command, str),
                preexec_fn=self._preexec,
            )
            return result(proc.returncode, proc.stdout, proc.stderr, False)
        except subprocess.TimeoutExpired:
            return result(-124, "", "Command timed out.", False)
        except Exception as exc:
            return result(-1, "", str(exc), False)
