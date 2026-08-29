#!/usr/bin/env python3
"""
OMEGA STATION - one-file bootstrapper
=====================================

Generates a complete reflective autonomous engineering pipeline
(the "seller station" control architecture) into a target directory:

    python3 build_omega_station.py --target ./my-project
    python3 build_omega_station.py --self-test

Architecture (all generated, pure Python standard library):

    Repository
        |
    Shadow Scan A (filesystem-driven)  -- independent --
    Shadow Scan B (git-index-driven)   -- independent --
        |
    Consensus / Reconcile map
        |
    Omega mission generator (findings -> verifiable missions)
        |
    For each mission (dependency + priority ordered):
        Omega plan -> ACTOR (LLM in a budgeted tool loop) ->
        Stationary judge (observe only, never fixes) ->
        Verifier A (spec) + Verifier B (hostile) ->
        Overseer A (value) + Overseer B (risk) ->
        PASS -> reseal | REWORK -> directives fed back | ESCALATE
        |
    Hash-chained evidence ledger (every claim auditable)

Honest scope (see generated README for the full capability table):
    - Control plane, integrity, verification, gatekeeping: implemented.
    - Actor slot: tool-loop protocol implemented for any
      OpenAI-compatible API; shipped mock is deterministic.
    - Docker isolation / GitHub PR lifecycle: config stubs, not wired.

Differences from the simpler v1 builder (fixed gaps):
    - v1's worker had no actuation (one prompt, no tools). v2's actor
      works through read/list/write/edit/run tools with scope jails.
    - v1's rework loop passed previous_failures=[] forever. v2 feeds
      combined Stationary/Verifier/Overseer directives back, and
      attempt >= 2 runs as a fresh-context helper role.
    - v1 config knobs (max_model_calls, max_runtime_seconds,
      allow_network) were decorative. v2 enforces every knob.
    - v1 verified with `git diff` only. v2 verifies against
      filesystem seal trees (catches committed changes too).
    - v1 evidence log was append-only in name. v2's ledger is
      hash-chained and self-verifying.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
import textwrap
from typing import Dict

FILES: Dict[str, str] = {}


def add(path: str, content: str) -> None:
    FILES[path] = textwrap.dedent(content).lstrip("\n")


# =========================================================================
# GENERATED PACKAGE: config / ledger / shadow / state / execution
# =========================================================================

add(
    "omega_station/config.py",
    r'''
    from __future__ import annotations

    import json
    import os
    from dataclasses import dataclass, field
    from pathlib import Path


    @dataclass
    class Config:
        """Every knob in here is enforced somewhere. No decorative config."""

        workspace: Path = Path(".omega")
        provider: str = "mock"          # mock | openai-compatible
        model: str = "mock-engineer"
        api_key_env: str = "OMEGA_API_KEY"
        api_base: str = "https://api.openai.com/v1"
        max_attempts: int = 3           # attempts per mission before escalate
        max_actor_steps: int = 24       # tool steps per actor run
        max_model_calls: int = 60       # station-wide model call budget
        max_runtime_seconds: int = 3600 # station-wide wall-clock budget
        command_timeout: int = 180      # per command
        allow_network: bool = False     # heuristic net-command denial when False
        auto_accept_critical: bool = False
        max_touched_files: int = 8      # overseer churn limit per mission
        cpu_limit_s: int = 30           # per-command CPU seconds (rlimit)
        mem_limit_mb: int = 2048        # per-command address space
        file_limit_mb: int = 256        # per-command writable file size
        nproc_limit: int = 128          # per-command process count
        env_passthrough: list[str] = field(default_factory=list)
        dangerous_commands: list[str] = field(default_factory=lambda: [
            "rm -rf /", "mkfs", "shutdown", "reboot", ":(){:|:&};:",
        ])

        @classmethod
        def load(cls, root: Path) -> "Config":
            cfg = cls()
            f = root / "station.json"
            if f.exists():
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    for k, v in data.items():
                        if hasattr(cfg, k):
                            setattr(cfg, k, v)
                except Exception as exc:
                    print(f"[omega] warning: station.json unreadable: {exc}")
            env = {
                "provider": "OMEGA_PROVIDER",
                "model": "OMEGA_MODEL",
                "api_base": "OMEGA_API_BASE",
            }
            for attr, envname in env.items():
                v = os.getenv(envname)
                if v:
                    setattr(cfg, attr, v)
            if os.getenv("OMEGA_ALLOW_NETWORK") == "1":
                cfg.allow_network = True
            if os.getenv("OMEGA_AUTO_ACCEPT_CRITICAL") == "1":
                cfg.auto_accept_critical = True
            return cfg

        @property
        def api_key(self) -> str | None:
            return os.getenv(self.api_key_env)
    ''',
)

add(
    "omega_station/ledger.py",
    r'''
    from __future__ import annotations

    import hashlib
    import json
    import time
    from pathlib import Path
    from typing import Any


    class Ledger:
        """Hash-chained JSONL evidence ledger.

        Each record carries the previous record's hash; verify_chain()
        detects any after-the-fact edit, deletion, or insertion.
        """

        def __init__(self, path: Path):
            self.path = path
            self.path.parent.mkdir(parents=True, exist_ok=True)

        def _records(self) -> list[dict]:
            if not self.path.exists():
                return []
            out = []
            for line in self.path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line:
                    try:
                        out.append(json.loads(line))
                    except json.JSONDecodeError:
                        out.append({"_corrupt": True, "raw": line[:80]})
            return out

        def _last_hash(self) -> str:
            recs = self._records()
            if not recs:
                return "GENESIS"
            last = recs[-1]
            return last.get("hash") or "GENESIS"

        def append(
            self,
            event: str,
            data: Any = None,
            task_id: str | None = None,
        ) -> dict:
            prev = self._last_hash()
            rec = {
                "seq": len(self._records()) + 1,
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "task_id": task_id,
                "event": event,
                "data": data,
                "prev": prev,
            }
            rec["hash"] = hashlib.sha256(
                json.dumps(rec, sort_keys=True, default=str).encode()
            ).hexdigest()
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, sort_keys=True, default=str) + "\n")
            return rec

        def verify_chain(self) -> dict:
            recs = self._records()
            prev = "GENESIS"
            for i, rec in enumerate(recs, start=1):
                if rec.get("_corrupt"):
                    return {"ok": False, "bad_seq": i, "reason": "unparseable line"}
                if rec.get("prev") != prev:
                    return {"ok": False, "bad_seq": i, "reason": "broken prev link"}
                body = {k: v for k, v in rec.items() if k != "hash"}
                expect = hashlib.sha256(
                    json.dumps(body, sort_keys=True, default=str).encode()
                ).hexdigest()
                if rec.get("hash") != expect:
                    return {"ok": False, "bad_seq": i, "reason": "hash mismatch"}
                if rec.get("seq") != i:
                    return {"ok": False, "bad_seq": i, "reason": "sequence gap"}
                prev = rec["hash"]
            return {"ok": True, "records": len(recs)}

        def tail(self, n: int = 20) -> list[dict]:
            return self._records()[-n:]
    ''',
)

add(
    "omega_station/shadow.py",
    r'''
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
    ''',
)

add(
    "omega_station/state.py",
    r'''
    from __future__ import annotations

    import json
    import sqlite3
    import threading
    from pathlib import Path
    from typing import Any


    class State:
        def __init__(self, path: Path):
            path.parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(str(path), check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.lock = threading.RLock()
            with self.lock:
                self.conn.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS missions (
                        mission_id TEXT PRIMARY KEY,
                        data TEXT NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS usage (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        mission_id TEXT,
                        provider TEXT,
                        model TEXT,
                        input_tokens INTEGER,
                        output_tokens INTEGER
                    );
                    CREATE TABLE IF NOT EXISTS meta (
                        key TEXT PRIMARY KEY,
                        value TEXT
                    );
                    """
                )
                self.conn.commit()

        def save_mission(self, mission: dict[str, Any]) -> None:
            with self.lock:
                self.conn.execute(
                    "INSERT INTO missions(mission_id, data) VALUES (?, ?) "
                    "ON CONFLICT(mission_id) DO UPDATE SET data=excluded.data",
                    (mission["mission_id"], json.dumps(mission)),
                )
                self.conn.commit()

        def get_mission(self, mission_id: str) -> dict[str, Any] | None:
            row = self.conn.execute(
                "SELECT data FROM missions WHERE mission_id=?", (mission_id,)
            ).fetchone()
            return json.loads(row["data"]) if row else None

        def all_missions(self) -> list[dict[str, Any]]:
            rows = self.conn.execute(
                "SELECT data FROM missions ORDER BY rowid"
            ).fetchall()
            return [json.loads(r["data"]) for r in rows]

        def usage(self, mission_id, provider, model, data: dict) -> None:
            with self.lock:
                self.conn.execute(
                    "INSERT INTO usage(mission_id,provider,model,input_tokens,output_tokens)"
                    " VALUES (?,?,?,?,?)",
                    (
                        mission_id, provider, model,
                        data.get("input_tokens"), data.get("output_tokens"),
                    ),
                )
                self.conn.commit()

        def set_meta(self, key: str, value: Any) -> None:
            with self.lock:
                self.conn.execute(
                    "INSERT INTO meta(key,value) VALUES (?,?) "
                    "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                    (key, json.dumps(value)),
                )
                self.conn.commit()

        def get_meta(self, key: str, default=None):
            row = self.conn.execute(
                "SELECT value FROM meta WHERE key=?", (key,)
            ).fetchone()
            return json.loads(row["value"]) if row else default

        def close(self) -> None:
            self.conn.close()
    ''',
)

add(
    "omega_station/execution.py",
    r'''
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
    ''',
)

# =========================================================================
# GENERATED PACKAGE: dual independent scans + omega mission layer
# =========================================================================

add(
    "omega_station/scanner.py",
    r'''
    from __future__ import annotations

    import re
    import subprocess
    from pathlib import Path

    from .shadow import IGNORED_DIRS

    SECRET_PATTERNS: list[tuple[str, str]] = [
        ("aws_access_key", r"AKIA[0-9A-Z]{16}"),
        ("private_key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        ("github_token", r"gh[pousr]_[A-Za-z0-9]{36,}"),
        ("openai_style_key", r"sk-[A-Za-z0-9]{32,}"),
        ("google_api_key", r"AIza[0-9A-Za-z_-]{35}"),
    ]
    DESTRUCTIVE_PATTERNS: list[tuple[str, str]] = [
        ("pipe_to_shell", r"curl[^|\n]*\|\s*(ba)?sh"),
        ("wipe_fs", r"mkfs(\.\w+)?\b"),
        ("fork_bomb", r":\(\)\s*\{\s*:\|:\s*&\s*\}\s*;"),
        ("rm_root", r"rm\s+-[^\n]*r[^\n]*f[^\n]*/(\s|$)"),
    ]
    TODO_RE = re.compile(r"\b(TODO|FIXME|XXX|HACK)\b")

    DEP_FILES = (
        "requirements.txt", "pyproject.toml", "setup.py", "Pipfile",
        "package.json", "Cargo.toml", "go.mod", "pom.xml", "Gemfile",
    )
    TEXT_SUFFIXES = {
        ".py", ".sh", ".bash", ".zsh", ".js", ".ts", ".jsx", ".tsx", ".java",
        ".rb", ".go", ".rs", ".c", ".h", ".cpp", ".hpp", ".cs", ".php",
        ".sql", ".yml", ".yaml", ".toml", ".json", ".ini", ".cfg", ".conf",
        ".env", ".md", ".txt", ".mk",
    }
    PLAIN_NAMES = {"Dockerfile", "Makefile", "LICENSE", ".gitignore", ".env"}
    MAX_SCAN_BYTES = 2_000_000


    def _is_text_name(name: str) -> bool:
        if name in PLAIN_NAMES:
            return True
        return Path(name).suffix in TEXT_SUFFIXES


    def _content_findings(rel: str, text: str) -> list[dict]:
        findings: list[dict] = []
        for name, pat in SECRET_PATTERNS:
            if re.search(pat, text):
                findings.append({
                    "key": f"secret.{name}",
                    "value": {"file": rel, "pattern": pat},
                })
        for name, pat in DESTRUCTIVE_PATTERNS:
            if re.search(pat, text):
                findings.append({
                    "key": f"destructive.{name}",
                    "value": {"file": rel, "pattern": pat},
                })
        n = len(TODO_RE.findall(text))
        if n:
            findings.append({"key": "todo.count",
                             "value": {"file": rel, "count": n}})
        return findings


    def _todo_top(counts: dict[str, int]) -> dict | None:
        if not counts:
            return None
        file = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        return {"file": file, "count": counts[file]}


    def scan_filesystem(root: Path) -> dict:
        """Scan A: filesystem truth. Walks the tree directly."""
        root = Path(root)
        inventory: set[str] = set()
        findings: list[dict] = []
        todo_counts: dict[str, int] = {}
        dep_files, test_files, ci_files, containers = [], [], [], []

        for p in sorted(root.rglob("*")):
            if not p.is_file():
                continue
            rel = p.relative_to(root)
            if any(part in IGNORED_DIRS for part in rel.parts):
                continue
            r = rel.as_posix()
            inventory.add(r)
            base = rel.name.lower()
            if base in {d.lower() for d in DEP_FILES}:
                dep_files.append(r)
            if "test" in base.lower() or rel.parts[0].lower() in {"tests", "test"}:
                test_files.append(r)
            if rel.parts[0] == ".github" and "workflows" in rel.parts:
                ci_files.append(r)
            if base.startswith("dockerfile") or base.startswith("docker-compose"):
                containers.append(r)
            if _is_text_name(base):
                try:
                    if p.stat().st_size > MAX_SCAN_BYTES:
                        continue
                    text = p.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                for fd in _content_findings(r, text):
                    if fd["key"] == "todo.count":
                        todo_counts[r] = fd["value"]["count"]
                    else:
                        findings.append(fd)

        top = _todo_top(todo_counts)
        if top:
            findings.append({"key": "todo.top", "value": top})
        findings.append({"key": "python.project",
                         "value": any(f.endswith(".py") for f in inventory)})
        findings.append({"key": "deps.manifest", "value": sorted(dep_files)})
        findings.append({"key": "tests.present", "value": bool(test_files)})
        findings.append({"key": "ci.present", "value": bool(ci_files)})
        findings.append({"key": "containers.present", "value": bool(containers)})
        return {"method": "filesystem", "inventory": inventory,
                "findings": findings}


    def scan_git(root: Path) -> dict:
        """Scan B: git-index truth. Reads file content from the index
        (git cat-file), NOT from the working tree - a different evidence
        source by construction, so the two scans can genuinely disagree
        (untracked files, unstaged edits)."""
        root = Path(root)

        def git(*args: str) -> str:
            try:
                r = subprocess.run(
                    ["git", *args], cwd=root, text=True,
                    capture_output=True, timeout=30,
                )
                return r.stdout if r.returncode == 0 else ""
            except Exception:
                return ""

        tracked = {l.strip() for l in git("ls-files").splitlines() if l.strip()}
        if not tracked:
            fs = scan_filesystem(root)
            fs["method"] = "filesystem-fallback(no-git)"
            return fs

        findings: list[dict] = []
        todo_counts: dict[str, int] = {}
        for f in sorted(tracked):
            if any(part in IGNORED_DIRS for part in Path(f).parts):
                continue
            if not _is_text_name(Path(f).name):
                continue
            blob = git("cat-file", "-p", f":{f}")
            if not blob:
                continue
            if len(blob) > MAX_SCAN_BYTES:
                continue
            for fd in _content_findings(f, blob):
                if fd["key"] == "todo.count":
                    todo_counts[f] = fd["value"]["count"]
                else:
                    findings.append(fd)
        top = _todo_top(todo_counts)
        if top:
            findings.append({"key": "todo.top", "value": top})

        dirty = git("status", "--short").splitlines()
        findings.append({"key": "git.dirty", "value": bool(dirty)})
        branch = git("branch", "--show-current").strip()
        findings.append({"key": "git.branch", "value": branch or "(detached)"})
        dep = [f for f in tracked
               if Path(f).name.lower() in {d.lower() for d in DEP_FILES}]
        findings.append({"key": "deps.manifest", "value": sorted(dep)})
        findings.append({"key": "tests.present",
                         "value": any("test" in f.lower() for f in tracked)})
        findings.append({"key": "ci.present",
                         "value": any(f.startswith(".github/workflows")
                                      for f in tracked)})
        findings.append({"key": "python.project",
                         "value": any(f.endswith(".py") for f in tracked)})
        return {"method": "git-index", "inventory": set(tracked),
                "findings": findings}


    def reconcile(a: dict, b: dict) -> dict:
        """Consensus map. Both scans must independently agree; disagreements
        are surfaced, never silently resolved."""
        confirmed, single, disputed = [], [], []
        by_key_a: dict[str, list[dict]] = {}
        by_key_b: dict[str, list[dict]] = {}
        for f in a["findings"]:
            by_key_a.setdefault(f["key"], []).append(f["value"])
        for f in b["findings"]:
            by_key_b.setdefault(f["key"], []).append(f["value"])

        def _unwrap(v):
            # single-finding keys carry the scalar/dict directly;
            # only genuinely multi-valued keys stay lists
            if isinstance(v, list) and len(v) == 1:
                return v[0]
            return v

        for key in sorted(set(by_key_a) | set(by_key_b)):
            va, vb = by_key_a.get(key), by_key_b.get(key)
            if va is not None and vb is not None:
                if va == vb:
                    confirmed.append({"key": key, "value": _unwrap(va)})
                else:
                    disputed.append({"key": key, "a": va, "b": vb})
            else:
                single.append({"key": key, "value": _unwrap(va or vb),
                               "source": "a" if va else "b"})

        inv_both = a["inventory"] & b["inventory"]
        return {
            "scan_a_method": a["method"],
            "scan_b_method": b["method"],
            "confirmed": confirmed,
            "single_source": single,
            "disputed": disputed,
            "inventory": {
                "both": len(inv_both),
                "a_only": sorted(a["inventory"] - b["inventory"])[:50],
                "b_only": sorted(b["inventory"] - a["inventory"])[:50],
            },
        }
    ''',
)

add(
    "omega_station/omega.py",
    r'''
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
    ''',
)

# =========================================================================
# GENERATED PACKAGE: providers / actor / stationary / verifiers / overseers
# =========================================================================

add(
    "omega_station/providers.py",
    r'''
    from __future__ import annotations

    import json
    import time
    import urllib.error
    import urllib.request
    from abc import ABC, abstractmethod
    from typing import Any

    TOOL_PROTOCOL = """You are the acting engineer inside a controlled tool loop.
    Each turn you receive a context object and MUST reply with ONE JSON object:

    {"thought": "...",
    "action": {"tool": "read"|"list"|"write"|"edit"|"run"|"finish",
              "args": {...}}}

    Tool args:
    read:   {"path": "relative/path"}
    list:   {"path": "relative/dir"}
    write:  {"path": "...", "content": "..."}        (must be in mission scope)
    edit:   {"path": "...", "op": "drop_lines_matching"|"replace_first"|"append",
           "pattern": "regex", "replacement": "...", "text": "..."}
    run:    {"command": ["python", "-c", "..."]}     (array form preferred)
    finish: {"verdict": "PASS"|"REWORK"|"ESCALATE", "summary": "...",
           "files_changed": [...], "evidence": [...]}

    Rules: writes outside mission scope are denied. Network commands are
    denied unless allowed. Do not claim anything you did not observe in tool
    output; every claim is independently verified against filesystem seals.
    Reply with JSON only."""

    SYSTEM_PROMPT = TOOL_PROTOCOL


    class StepProvider(ABC):
        @abstractmethod
        def step(self, context: dict) -> dict:
            raise NotImplementedError


    class MockStepProvider(StepProvider):
        """Deterministic actor for mock mode.

        It drives the REAL tool loop (same enforcement path as the LLM)
        with scripted actions per mission type. It is labeled mock in
        every ledger record; it never pretends to be a frontier model.
        """

        def __init__(self, mission: dict):
            self.mission = mission
            self.cursor = 0
            self.script = self._build_script(mission)

        def _build_script(self, m: dict) -> list[dict]:
            t = m["type"]
            if t == "remove_secret":
                pat = m.get("payload", {}).get("pattern") or self._secret_pat(m)
                f = m["scope_files"][0]
                return [
                    {"tool": "read", "path": f},
                    {"tool": "edit", "path": f, "op": "drop_lines_matching",
                     "pattern": pat},
                    {"tool": "finish", "verdict": "PASS",
                     "summary": "removed secret-bearing lines",
                     "files_changed": [f], "evidence": ["edit applied"]},
                ]
            if t == "guard_destructive":
                f = m["scope_files"][0]
                pat = m.get("payload", {}).get("pattern") or r"curl.*\|\s*(ba)?sh"
                return [
                    {"tool": "read", "path": f},
                    {"tool": "edit", "path": f, "op": "replace_first",
                     "pattern": r"^(.*" + pat + r".*)$",
                     "replacement": "# OMEGA-GUARD neutralized: \\1"},
                    {"tool": "finish", "verdict": "PASS",
                     "summary": "destructive line commented with OMEGA-GUARD",
                     "files_changed": [f], "evidence": ["edit applied"]},
                ]
            if t == "burn_todo":
                f = m["scope_files"][0]
                import datetime
                stamp = datetime.date.today().isoformat()
                return [
                    {"tool": "read", "path": f},
                    {"tool": "edit", "path": f, "op": "replace_first",
                     "pattern": r"\b(TODO|FIXME|XXX|HACK)\b",
                     "replacement": f"REVIEWED({stamp})"},
                    {"tool": "finish", "verdict": "PASS",
                     "summary": "hotspot marker dated",
                     "files_changed": [f], "evidence": ["edit applied"]},
                ]
            if t == "add_smoke_test":
                path = m["creates"][0]
                content = chr(10).join([
                    "import unittest",
                    "",
                    "",
                    "class TestSmokeOmegaStation(unittest.TestCase):",
                    "    def test_station_smoke(self):",
                    "        self.assertTrue(True)",
                    "",
                    "",
                    "if __name__ == '__main__':",
                    "    unittest.main()",
                ])
                return [
                    {"tool": "write", "path": path, "content": content},
                    {"tool": "run", "command": ["python", path]},
                    {"tool": "finish", "verdict": "PASS",
                     "summary": "smoke test created and green",
                     "files_changed": [path], "evidence": ["run exit 0"]},
                ]
            if t == "add_requirements":
                path = m["creates"][0]
                content = chr(10).join(m.get("payload", {}).get("lines", []))
                return [
                    {"tool": "write", "path": path, "content": content + chr(10)},
                    {"tool": "finish", "verdict": "PASS",
                     "summary": "requirements.txt written from import scan",
                     "files_changed": [path], "evidence": ["write ok"]},
                ]
            if t == "commit_wip":
                return [
                    {"tool": "finish", "verdict": "ESCALATE",
                     "summary": "committing is a human trust decision",
                     "files_changed": [], "evidence": []},
                ]
            return [
                {"tool": "finish", "verdict": "ESCALATE",
                 "summary": f"mock has no script for type {t}",
                 "files_changed": [], "evidence": []},
            ]

        @staticmethod
        def _secret_pat(m):
            for cmd in m.get("verification_commands", []):
                if len(cmd) >= 3 and "re.search" in cmd[2]:
                    import re as _re
                    mm = _re.search(r"re\.search\(r'([^']+)'", cmd[2])
                    if mm:
                        return mm.group(1)
            return r"AKIA[0-9A-Z]{16}"

        def step(self, context: dict) -> dict:
            if self.cursor < len(self.script):
                a = self.script[self.cursor]
                self.cursor += 1
                return a
            return {"tool": "finish", "verdict": "ESCALATE",
                    "summary": "mock script exhausted",
                    "files_changed": [], "evidence": []}


    class OpenAICompatibleStepProvider(StepProvider):
        """The real actor slot. Any OpenAI-compatible chat API."""

        def __init__(self, config, mission: dict):
            if not config.api_key:
                raise RuntimeError(
                    f"model API key missing: set {config.api_key_env}"
                )
            self.config = config
            self.mission = mission

        def step(self, context: dict) -> dict:
            url = self.config.api_base.rstrip("/") + "/chat/completions"
            payload = {
                "model": self.config.model,
                "temperature": 0,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": json.dumps(context, default=str)},
                ],
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode(),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.config.api_key}",
                },
                method="POST",
            )
            data = None
            last_exc: Exception | None = None
            for attempt in range(3):
                # transient-fault tolerance with fail-CLOSED semantics:
                # after the retries the exception propagates, the actor
                # records actor_error, and the mission ESCALATES. The
                # station never guesses when the brain is unreachable.
                try:
                    with urllib.request.urlopen(req, timeout=180) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                    break
                except (urllib.error.URLError, TimeoutError, OSError) as exc:
                    last_exc = exc
                    if attempt < 2:
                        time.sleep(1.0 + 1.5 * attempt)
            if data is None:
                raise last_exc if last_exc else RuntimeError("no response")
            self.last_usage = {
                "input_tokens": (data.get("usage") or {}).get("prompt_tokens"),
                "output_tokens": (data.get("usage") or {}).get("completion_tokens"),
            }
            text = data["choices"][0]["message"].get("content") or ""
            text = text.strip()
            if text.startswith("```"):
                lines = text.splitlines()
                if lines and lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                text = chr(10).join(lines)
            try:
                action = json.loads(text)
            except json.JSONDecodeError:
                return {"tool": "finish", "verdict": "ESCALATE",
                        "summary": "model returned unparseable JSON",
                        "files_changed": [], "evidence": [text[:400]]}
            return action


    def create_step_provider(config, mission: dict) -> StepProvider:
        if config.provider == "mock":
            return MockStepProvider(mission)
        if config.provider in {"openai-compatible", "openai", "openrouter"}:
            return OpenAICompatibleStepProvider(config, mission)
        raise RuntimeError(f"unknown provider: {config.provider}")
    ''',
)

add(
    "omega_station/actor.py",
    r'''
    from __future__ import annotations

    import re
    from pathlib import Path


    class Actor:
        """The acting intelligence in a budgeted, scope-jailed tool loop.

        The actor can: read, list, write (scope files only), edit (scope
        files only), run (jailed commands). Every tool call is appended to
        the evidence ledger. The actor has NO access to seals, no reseal,
        no verification commands of its own making: claims are worthless,
        only the seal diff and verifier runs count.
        """

        def __init__(self, root: Path, runner, ledger, config,
                     role: str = "engineer", on_usage=None):
            self.root = Path(root).resolve()
            self.runner = runner
            self.ledger = ledger
            self.config = config
            self.role = role
            self.model_calls = 0
            self.on_usage = on_usage

        def _jail(self, rel: str) -> Path:
            p = (self.root / rel).resolve()
            if not str(p).startswith(str(self.root)):
                raise PermissionError("path escapes workspace jail")
            return p

        def _scope_ok(self, rel: str, mission: dict) -> bool:
            allowed = set(mission.get("scope_files", [])) | set(mission.get("creates", []))
            if not allowed or rel in allowed:
                return True
            return False

        def run(self, mission: dict, context: dict, on_model_call=None,
                on_usage=None) -> dict:
            from .providers import create_step_provider

            recorder = on_usage or self.on_usage
            try:
                provider = create_step_provider(self.config, mission)
            except Exception as exc:
                # a missing key or bad provider config escalates THIS
                # mission; it must never crash the whole station
                self.ledger.append("actor_error", {"error": str(exc)},
                                   task_id=mission["mission_id"])
                return {"verdict": "ESCALATE",
                        "summary": f"provider unavailable: {exc}",
                        "files_changed": [], "evidence": [], "history": []}
            history: list[dict] = []
            self.ledger.append(
                "actor_started",
                {"mission": mission["mission_id"], "role": self.role,
                 "attempt": mission.get("attempts", 0)},
                task_id=mission["mission_id"],
            )

            for step_no in range(self.config.max_actor_steps):
                self.model_calls += 1
                if on_model_call:
                    on_model_call()
                try:
                    action = provider.step({**context, "history": history[-8:]})
                except Exception as exc:
                    self.ledger.append("actor_error", {"error": str(exc)},
                                       task_id=mission["mission_id"])
                    return {"verdict": "ESCALATE", "summary": f"provider error: {exc}",
                            "files_changed": [], "evidence": [], "history": history}
                usage = getattr(provider, "last_usage", None)
                if usage:
                    self.ledger.append("model_usage", usage,
                                       task_id=mission["mission_id"])
                    if recorder:
                        recorder(usage)

                tool = action.get("tool", action.get("action", {}).get("tool", "finish"))
                args = action.get("args", action.get("action", {}).get("args", {}))
                if isinstance(args, dict) is False:
                    args = {}
                # allow flat form: {"tool": "write", "path": ..., "content": ...}
                for k in ("path", "content", "op", "pattern", "replacement",
                          "text", "command", "verdict", "summary",
                          "files_changed", "evidence"):
                    if k in action and k not in args:
                        args[k] = action[k]

                if tool == "finish":
                    rec = {"step": step_no + 1, "tool": "finish",
                           "args": _clip(args)}
                    history.append(rec)
                    self.ledger.append("actor_step", rec,
                                       task_id=mission["mission_id"])
                    return {
                        "verdict": str(args.get("verdict", "ESCALATE")).upper(),
                        "summary": str(args.get("summary", ""))[:2000],
                        "files_changed": list(args.get("files_changed") or []),
                        "evidence": [str(e)[:500] for e in (args.get("evidence") or [])][:20],
                        "history": history,
                    }
                rec = {"step": step_no + 1, "tool": tool, "args": _clip(args)}
                out = self._dispatch(tool, args, mission)
                rec["result"] = _clip(out)
                history.append(rec)
                self.ledger.append("actor_step", rec, task_id=mission["mission_id"])

            self.ledger.append("actor_budget", {"steps": self.config.max_actor_steps},
                               task_id=mission["mission_id"])
            return {"verdict": "ESCALATE", "summary": "actor step budget exhausted",
                    "files_changed": [], "evidence": [], "history": history}

        def _dispatch(self, tool: str, args: dict, mission: dict) -> dict:
            try:
                if tool == "read":
                    p = self._jail(str(args.get("path", "")))
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    return {"ok": True, "content": text[:20000]}
                if tool == "list":
                    p = self._jail(str(args.get("path", "")) or ".")
                    if not p.is_dir():
                        p = p.parent if p.parent.is_dir() else self.root
                    return {"ok": True,
                            "entries": sorted(x.name for x in p.iterdir())[:200]}
                if tool == "write":
                    rel = str(args.get("path", ""))
                    if not self._scope_ok(rel, mission):
                        return {"ok": False, "denied":
                                f"write outside mission scope: {rel}"}
                    p = self._jail(rel)
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text(str(args.get("content", "")), encoding="utf-8")
                    return {"ok": True, "wrote": rel}
                if tool == "edit":
                    rel = str(args.get("path", ""))
                    if not self._scope_ok(rel, mission):
                        return {"ok": False, "denied":
                                f"edit outside mission scope: {rel}"}
                    p = self._jail(rel)
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    op = args.get("op")
                    if op == "drop_lines_matching":
                        pat = re.compile(args.get("pattern", r"(?!)"))
                        lines = [l for l in text.split(chr(10)) if not pat.search(l)]
                        new = chr(10).join(lines)
                    elif op == "replace_first":
                        pat = re.compile(args.get("pattern", r"(?!)"), re.M)
                        new = pat.sub(str(args.get("replacement", "")), text, count=1)
                    elif op == "append":
                        new = text + str(args.get("text", ""))
                    else:
                        return {"ok": False, "denied": f"unknown edit op: {op}"}
                    p.write_text(new, encoding="utf-8")
                    return {"ok": True, "edited": rel, "op": op}
                if tool == "run":
                    cmd = args.get("command")
                    if isinstance(cmd, str):
                        cmd = cmd.split()
                    if not isinstance(cmd, list) or not cmd:
                        return {"ok": False, "denied": "command must be a list"}
                    res = self.runner.run([str(c) for c in cmd])
                    return res
            except PermissionError as exc:
                return {"ok": False, "denied": str(exc)}
            except FileNotFoundError as exc:
                return {"ok": False, "error": str(exc)}
            except Exception as exc:
                return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
            return {"ok": False, "denied": f"unknown tool: {tool}"}


    def _clip(obj, limit=4000):
        s = repr(obj)
        return s if len(s) <= limit else s[:limit] + "..."
    ''',
)

add(
    "omega_station/stationary.py",
    r'''
    from __future__ import annotations

    from pathlib import Path

    from .shadow import manifest_diff


    class Stationary:
        """The judge. Observes, compares, produces directives.

        By construction it has no write tools, no runner, no path handles:
        it receives immutable snapshots (seal manifests, actor claims) and
        returns directives. It can never secretly fix what it is judging.
        """

        def observe(
            self,
            mission: dict,
            before_seals: dict,
            after_seals: dict,
            actor_report: dict,
        ) -> list[dict]:
            directives: list[dict] = []
            mid = mission["mission_id"]

            diff = manifest_diff(before_seals, after_seals)
            changed = set(diff["added"]) | set(diff["removed"]) | set(diff["modified"])
            claimed = set(actor_report.get("files_changed") or [])

            if actor_report.get("verdict") == "PASS" and not changed:
                directives.append({
                    "code": "PASS_WITHOUT_CHANGE",
                    "detail": "actor claims PASS but the seals show no change",
                })

            claimed_missing = sorted(claimed - changed)
            if claimed_missing:
                directives.append({
                    "code": "CLAIM_WITHOUT_CHANGE",
                    "detail": f"claimed files with no seal change: {claimed_missing}",
                })

            unclaimed = sorted(changed - claimed)
            if unclaimed:
                directives.append({
                    "code": "CHANGE_WITHOUT_CLAIM",
                    "detail": f"seal changes not claimed: {unclaimed}",
                })

            allowed = set(mission.get("scope_files", [])) | set(mission.get("creates", []))
            if allowed:
                outside = sorted(changed - allowed)
                if outside:
                    directives.append({
                        "code": "SCOPE_VIOLATION",
                        "detail": f"changes outside mission scope: {outside}",
                    })

            for req in mission.get("scope_files", []):
                if req not in after_seals:
                    directives.append({
                        "code": "REQUIRED_FILE_MISSING",
                        "detail": req,
                    })
            _ = mid
            return directives
    ''',
)

add(
    "omega_station/verifier.py",
    r'''
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
    ''',
)

add(
    "omega_station/overseer.py",
    r'''
    from __future__ import annotations


    class Decision:
        def __init__(self, name: str, accept: bool, reasons: list[str]):
            self.name = name
            self.accept = accept
            self.reasons = reasons


    class ValueOverseer:
        """Overseer A: should this be accepted at all? Small, on-mission
        changes only; churn is rejected even when tests pass."""

        def __init__(self, config):
            self.config = config

        def decide(self, mission: dict, seal_diff: dict) -> Decision:
            reasons = []
            changed = (seal_diff.get("added", []) + seal_diff.get("removed", [])
                       + seal_diff.get("modified", []))
            if len(changed) > self.config.max_touched_files:
                reasons.append(f"churn: {len(changed)} files touched "
                               f"(limit {self.config.max_touched_files})")
            allowed = set(mission.get("scope_files", [])) | set(mission.get("creates", []))
            if allowed:
                off = [f for f in changed if f not in allowed]
                if off:
                    reasons.append(f"unrelated changes: {off}")
            return Decision("value", not reasons, reasons)


    class RiskOverseer:
        """Overseer B: system-level risk. Human-gate on critical missions,
        station budgets, ledger integrity."""

        def __init__(self, config, state, ledger):
            self.config = config
            self.state = state
            self.ledger = ledger

        def decide(self, mission: dict, model_calls: int, elapsed: float) -> Decision:
            reasons = []
            if mission.get("requires_human") and not self.config.auto_accept_critical:
                reasons.append("requires human acceptance (critical trust decision)")
            if model_calls > self.config.max_model_calls:
                reasons.append(f"model call budget exceeded: {model_calls}")
            if elapsed > self.config.max_runtime_seconds:
                reasons.append(f"runtime budget exceeded: {elapsed:.0f}s")
            chain = self.ledger.verify_chain()
            if not chain["ok"]:
                reasons.append(f"ledger chain broken: {chain}")
            return Decision("risk", not reasons, reasons)
    ''',
)

# =========================================================================
# GENERATED PACKAGE: engine (reflective loop) + marketing policy verifier
# =========================================================================

add(
    "omega_station/engine.py",
    r'''
    from __future__ import annotations

    import time
    from pathlib import Path

    from .actor import Actor
    from .config import Config
    from .execution import CommandRunner
    from .gitflow import GitManager
    from .ledger import Ledger
    from .omega import missions_from_consensus, plan
    from .overseer import RiskOverseer, ValueOverseer
    from .scanner import reconcile, scan_filesystem, scan_git
    from .shadow import Shadow, manifest_diff, seal_tree
    from .stationary import Stationary
    from .state import State
    from .verifier import HostileVerifier, SpecVerifier

    BLOCKING_STATIONARY = {
        "PASS_WITHOUT_CHANGE",
        "CLAIM_WITHOUT_CHANGE",
        "SCOPE_VIOLATION",
        "REQUIRED_FILE_MISSING",
    }


    class BudgetExceeded(Exception):
        pass


    class OmegaStation:
        """The station. Wiring:

        recon: dual independent scans -> consensus -> missions
        run:   per mission, until budgets or completion:
                 seals -> omega plan -> actor (jailed tool loop) ->
                 seals -> stationary judge -> spec verifier ->
                 hostile verifier -> value overseer + risk overseer ->
                 accept -> reseal | rework -> directives fed back |
                 escalate (incl. human-gate missions)
        """

        def __init__(self, root: Path, config: Config | None = None):
            self.root = Path(root).resolve()
            self.config = config or Config.load(self.root)
            self.workspace = self.root / self.config.workspace
            self.state = State(self.workspace / "state.sqlite3")
            self.ledger = Ledger(self.workspace / "evidence.jsonl")
            self.shadow = Shadow(self.root, self.ledger,
                                 workspace=self.workspace)
            self.gitflow = GitManager(self.root, self.ledger)
            self.runner = CommandRunner(
                self.root,
                timeout=self.config.command_timeout,
                blocked=self.config.dangerous_commands,
                allow_network=self.config.allow_network,
                cpu_limit_s=self.config.cpu_limit_s,
                mem_limit_mb=self.config.mem_limit_mb,
                file_limit_mb=self.config.file_limit_mb,
                nproc_limit=self.config.nproc_limit,
                passthrough=self.config.env_passthrough,
            )
            self.actor = Actor(self.root, self.runner, self.ledger, self.config)
            self.stationary = Stationary()
            self.spec_verifier = SpecVerifier(self.runner)
            self.hostile_verifier = HostileVerifier(self.root, self.runner, self.ledger)
            self.value_overseer = ValueOverseer(self.config)
            self.risk_overseer = RiskOverseer(self.config, self.state, self.ledger)
            self._model_calls = 0
            self._started = time.monotonic()
            self.consensus: dict | None = None

        # ---------------- recon ----------------

        def recon(self) -> dict:
            a = scan_filesystem(self.root)
            self.ledger.append("scan_a_complete", {
                "method": a["method"], "files": len(a["inventory"]),
                "findings": len(a["findings"]),
            })
            b = scan_git(self.root)
            self.ledger.append("scan_b_complete", {
                "method": b["method"], "files": len(b["inventory"]),
                "findings": len(b["findings"]),
            })
            self.consensus = reconcile(a, b)
            self.ledger.append("consensus", {
                "confirmed": len(self.consensus["confirmed"]),
                "single_source": len(self.consensus["single_source"]),
                "disputed": len(self.consensus["disputed"]),
            })
            if (self.root / "tests").is_dir():
                res = self.runner.run(
                    ["python", "-m", "unittest", "discover", "-s", "tests", "-q"])
                self.state.set_meta("tests_baseline_exit", res["exit_code"])
            return self.consensus

        def generate_missions(self) -> list[dict]:
            if self.consensus is None:
                self.recon()
            missions = missions_from_consensus(self.consensus, self.root)
            for m in missions:
                existing = self.state.get_mission(m["mission_id"])
                if not existing:
                    self.state.save_mission(m)
                    self.ledger.append("mission_created", {
                        "mission_id": m["mission_id"], "type": m["type"],
                        "risk": m["risk"], "priority": m["priority"],
                    }, task_id=m["mission_id"])
            return missions

        # ---------------- reflective loop ----------------

        def run(self) -> list[dict]:
            missions = self.generate_missions()
            self.gitflow.begin(missions)
            results = []
            for mission in missions:
                m = self.state.get_mission(mission["mission_id"]) or mission
                if m.get("status") in {"complete", "escalated"}:
                    continue
                try:
                    results.append(self.run_mission(m))
                except BudgetExceeded as exc:
                    m["status"] = "deferred"
                    m["deferred_reason"] = str(exc)
                    self.state.save_mission(m)
                    self.ledger.append("station_budget_exhausted", {"reason": str(exc)})
                    results.append({"mission_id": m["mission_id"],
                                    "status": "deferred", "reason": str(exc)})
            self.ledger.append("station_run_complete", {
                "model_calls": self._model_calls,
                "elapsed": round(time.monotonic() - self._started, 1),
                "results": [{k: r.get(k) for k in ("mission_id", "status")}
                            for r in results],
            })
            self.gitflow.finalize(results, self.verify_ledger())
            return results

        def _budget_check(self):
            self._model_calls += 1
            if self._model_calls > self.config.max_model_calls:
                raise BudgetExceeded(
                    f"model call budget: {self._model_calls} > "
                    f"{self.config.max_model_calls}")
            elapsed = time.monotonic() - self._started
            if elapsed > self.config.max_runtime_seconds:
                raise BudgetExceeded(
                    f"runtime budget: {elapsed:.0f}s > "
                    f"{self.config.max_runtime_seconds}s")

        def run_mission(self, mission: dict) -> dict:
            mid = mission["mission_id"]
            mission["attempts"] = int(mission.get("attempts", 0)) + 1
            mission["status"] = "running"
            self.state.save_mission(mission)
            self.ledger.append("mission_started", {
                "attempt": mission["attempts"],
                "role": "helper" if mission["attempts"] >= 2 else "engineer",
            }, task_id=mid)

            if self.consensus is None:
                self.recon()

            before = seal_tree(self.root)
            context = {
                "role": "helper" if mission["attempts"] >= 2 else "engineer",
                "mission": {k: v for k, v in mission.items()
                            if k not in ("evidence",)},
                "omega_plan": plan(mission, self.consensus or {}),
                "directives": mission.get("directives", [])[-10:],
                "note": "attempt >= 2 runs as a fresh-context helper; prior "
                        "directives are your only inheritance",
            }
            report = self.actor.run(
                mission, context,
                on_model_call=self._budget_check,
                on_usage=lambda u: self.state.usage(
                    mid, self.config.provider, self.config.model, u))
            after = seal_tree(self.root)
            diff = manifest_diff(before, after)

            stationary = self.stationary.observe(mission, before, after, report)
            self.ledger.append("stationary_directives", stationary, task_id=mid)

            if report["verdict"] == "ESCALATE":
                mission["status"] = "escalated"
                mission["final_verdict"] = "ESCALATE"
                mission["evidence"].append({"escalation": report["summary"]})
                self.state.save_mission(mission)
                self.ledger.append("mission_escalated",
                                   {"summary": report["summary"]}, task_id=mid)
                return {"mission_id": mid, "status": "escalated",
                        "reason": report["summary"]}

            spec = self.spec_verifier.verify(mission)
            hostile = self.hostile_verifier.verify(mission, diff, self.state)
            value = self.value_overseer.decide(mission, diff)
            risk = self.risk_overseer.decide(
                mission, self._model_calls, time.monotonic() - self._started)
            self.ledger.append("verification_matrix", {
                "spec": {"passed": spec.passed, "reasons": spec.reasons},
                "hostile": {"passed": hostile.passed, "reasons": hostile.reasons},
                "value": {"accept": value.accept, "reasons": value.reasons},
                "risk": {"accept": risk.accept, "reasons": risk.reasons},
            }, task_id=mid)

            blocking = [d for d in stationary if d["code"] in BLOCKING_STATIONARY]
            accepted = (spec.passed and hostile.passed and value.accept
                        and risk.accept and not blocking)

            if accepted:
                mission["status"] = "complete"
                mission["final_verdict"] = "PASS"
                changed_sorted = sorted(set(diff["added"]) | set(diff["removed"])
                                        | set(diff["modified"]))
                mission["evidence"].append({
                    "accepted": True,
                    "changed": changed_sorted,
                    "spec_commands": [c["command"] for c in spec.commands],
                })
                self.state.save_mission(mission)
                self.shadow.reseal(f"mission accepted: {mid}")
                self.gitflow.commit_mission(mission, changed_sorted)
                if (self.root / "tests").is_dir() and \
                        self.state.get_meta("tests_baseline_exit") is None:
                    res = self.runner.run(
                        ["python", "-m", "unittest", "discover", "-s", "tests", "-q"])
                    self.state.set_meta("tests_baseline_exit", res["exit_code"])
                self.ledger.append("mission_accepted", {
                    "attempt": mission["attempts"],
                }, task_id=mid)
                return {"mission_id": mid, "status": "complete"}

            directives = (
                [{"code": f"STATIONARY:{d['code']}", "detail": d["detail"]}
                 for d in blocking]
                + [{"code": "SPEC", "detail": r} for r in spec.reasons]
                + [{"code": "HOSTILE", "detail": r} for r in hostile.reasons]
                + [{"code": "VALUE", "detail": r} for r in value.reasons]
                + [{"code": "RISK", "detail": r} for r in risk.reasons]
            )
            mission["directives"] = (mission.get("directives", []) +
                                     directives)[-10:]

            if mission["attempts"] >= self.config.max_attempts:
                mission["status"] = "escalated"
                mission["final_verdict"] = "ESCALATE"
                self.state.save_mission(mission)
                self.ledger.append("mission_escalated",
                                   {"reasons": directives}, task_id=mid)
                return {"mission_id": mid, "status": "escalated",
                        "reasons": directives}

            mission["status"] = "rework"
            self.state.save_mission(mission)
            self.ledger.append("mission_rework", {"directives": directives},
                               task_id=mid)
            return {"mission_id": mid, "status": "rework",
                    "reasons": directives}

        # ---------------- reporting ----------------

        def verify_ledger(self) -> dict:
            return self.ledger.verify_chain()

        def verify_integrity(self) -> dict:
            return self.shadow.verify()

        def status(self) -> dict:
            missions = self.state.all_missions()
            counts: dict[str, int] = {}
            for m in missions:
                counts[m.get("status", "unknown")] = \
                    counts.get(m.get("status", "unknown"), 0) + 1
            return {
                "root": str(self.root),
                "provider": self.config.provider,
                "model_calls": self._model_calls,
                "elapsed_s": round(time.monotonic() - self._started, 1),
                "missions": counts,
                "ledger": self.verify_ledger(),
                "details": [{"id": m["mission_id"], "status": m.get("status"),
                             "attempts": m.get("attempts"),
                             "type": m.get("type")} for m in missions],
            }
    ''',
)

add(
    "omega_station/policy.py",
    r'''
    from __future__ import annotations

    import json
    import re
    from pathlib import Path

    DEFAULT_BANNED = [
        "cure", "cures", "guarantee", "guaranteed", "miracle", "overnight",
        "instantly", "ozempic", "wegovy", "mounjaro", "fda approved",
        "clinically proven", "doctor recommended", "medical advice",
        "treats", "treats depression", "diagnose", "prescription",
        "side-effect free", "no side effects", "100% safe",
    ]
    REQUIRED_DISCLAIMER = "not medical advice"


    class PolicyVerifier:
        """Hostile policy verifier for seller/marketing assets.

        Same asymmetry as the code verifiers: assume the copy is guilty
        until it survives the audit. Checks banned phrases, price drift
        against a catalog of record, and (optionally) required elements
        such as the disclaimer line.
        """

        def __init__(self, banned=None, prices=None, require_disclaimer=False):
            self.banned = [b.lower() for b in (banned or DEFAULT_BANNED)]
            self.prices = {k.lower(): v for k, v in (prices or {}).items()}
            self.require_disclaimer = require_disclaimer

        @classmethod
        def from_files(cls, banned_file: Path | None, prices_file: Path | None,
                       require_disclaimer: bool = False) -> "PolicyVerifier":
            banned = None
            if banned_file and Path(banned_file).exists():
                banned = [w.strip() for w in
                          Path(banned_file).read_text(encoding="utf-8").splitlines()
                          if w.strip() and not w.startswith("#")]
            prices = None
            if prices_file and Path(prices_file).exists():
                prices = json.loads(Path(prices_file).read_text(encoding="utf-8"))
            return cls(banned=banned, prices=prices,
                       require_disclaimer=require_disclaimer)

        def check(self, text: str, title: str | None = None) -> dict:
            violations: list[dict] = []
            lowered = text.lower()
            # negation guard: "not medical advice" is the compliant use of
            # "medical advice"; scrub explicit negations before matching
            scrubbed = lowered
            for phrase in self.banned:
                scrubbed = re.sub(
                    r"\bnot\s+" + re.escape(phrase), " ", scrubbed)
            for phrase in self.banned:
                if phrase in scrubbed:
                    i = scrubbed.find(phrase)
                    violations.append({
                        "rule": "banned_phrase",
                        "match": phrase,
                        "context": text[max(0, i - 30):i + len(phrase) + 30],
                    })
            for m in re.finditer(r"\$\s?(\d+(?:\.\d{2})?)", text):
                price = m.group(1)
                if not price.endswith(".99"):
                    violations.append({
                        "rule": "odd_price",
                        "match": price,
                        "context": text[max(0, m.start() - 30):m.end() + 30],
                    })
            if self.prices and title:
                want = self.prices.get(title.lower())
                if want is not None:
                    found = re.findall(r"\$\s?(\d+(?:\.\d{2})?)", text)
                    wrong = [p for p in found
                             if abs(float(p) - float(want)) > 0.001]
                    if wrong:
                        violations.append({
                            "rule": "price_drift",
                            "match": f"listed {wrong} but catalog says {want}",
                            "context": title,
                        })
            if self.require_disclaimer and \
                    REQUIRED_DISCLAIMER not in lowered:
                violations.append({
                    "rule": "missing_disclaimer",
                    "match": REQUIRED_DISCLAIMER,
                    "context": "",
                })
            return {"pass": not violations, "violations": violations}
    ''',
)

add(
    "omega_station/gitflow.py",
    r'''
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
    ''',
)

# =========================================================================
# GENERATED PACKAGE: CLI + package glue
# =========================================================================

add(
    "omega_station/cli.py",
    r'''
    from __future__ import annotations

    import argparse
    import json
    from pathlib import Path

    from .engine import OmegaStation
    from .policy import PolicyVerifier


    def build_parser() -> argparse.ArgumentParser:
        p = argparse.ArgumentParser(
            prog="omega-station",
            description="Reflective autonomous engineering pipeline "
                        "(Omega/Shadow control architecture).")
        sub = p.add_subparsers(dest="command", required=True)
        sub.add_parser("recon", help="dual independent scans + consensus")
        sub.add_parser("missions", help="generate missions from consensus")
        sub.add_parser("run", help="run the full reflective loop (mock by default)")
        sub.add_parser("status", help="station status report")
        sub.add_parser("ledger", help="verify the hash-chained evidence ledger")
        sub.add_parser("integrity", help="verify shadow seals vs filesystem")
        pol = sub.add_parser("policy", help="audit a marketing/copy file")
        pol.add_argument("file")
        pol.add_argument("--banned", help="banned phrases file (one per line)")
        pol.add_argument("--prices", help="JSON catalog {title: price}")
        pol.add_argument("--title", help="catalog title to check price drift")
        pol.add_argument("--require-disclaimer", action="store_true")
        return p


    def main(argv=None) -> int:
        args = build_parser().parse_args(argv)
        root = Path.cwd()
        station = OmegaStation(root)

        if args.command == "recon":
            c = station.recon()
            print(json.dumps({
                "scan_a": c["scan_a_method"], "scan_b": c["scan_b_method"],
                "confirmed": len(c["confirmed"]),
                "single_source": len(c["single_source"]),
                "disputed": len(c["disputed"]),
            }, indent=2))
            return 0
        if args.command == "missions":
            missions = station.generate_missions()
            print(json.dumps(
                [{"id": m["mission_id"], "type": m["type"], "risk": m["risk"],
                  "priority": m["priority"], "title": m["title"]}
                 for m in missions], indent=2))
            return 0
        if args.command == "run":
            results = station.run()
            print(json.dumps(results, indent=2, default=str))
            ok = all(r.get("status") in {"complete", "escalated"} for r in results)
            return 0 if ok else 1
        if args.command == "status":
            print(json.dumps(station.status(), indent=2, default=str))
            return 0
        if args.command == "ledger":
            v = station.verify_ledger()
            print(json.dumps(v, indent=2))
            return 0 if v["ok"] else 1
        if args.command == "integrity":
            v = station.verify_integrity()
            print(json.dumps(v, indent=2))
            return 0 if v.get("clean", True) else 1
        if args.command == "policy":
            text = Path(args.file).read_text(encoding="utf-8")
            pv = PolicyVerifier.from_files(
                Path(args.banned) if args.banned else None,
                Path(args.prices) if args.prices else None,
                require_disclaimer=args.require_disclaimer)
            report = pv.check(text, title=args.title)
            print(json.dumps(report, indent=2))
            return 0 if report["pass"] else 1
        return 1
    ''',
)

add(
    "omega_station/__init__.py",
    '''
    """Omega Station: reflective autonomous engineering pipeline."""

    __version__ = "2.2.0"

    from .engine import OmegaStation          # noqa: E402,F401
    from .policy import PolicyVerifier        # noqa: E402,F401
    ''',
)

add(
    "omega_station/__main__.py",
    '''
    from .cli import main

    if __name__ == "__main__":
        raise SystemExit(main())
    ''',
)

# =========================================================================
# GENERATED TESTS
# =========================================================================

add(
    "tests/__init__.py",
    '',
)

add(
    "tests/test_ledger.py",
    r'''
    import json
    import tempfile
    import unittest
    from pathlib import Path

    from omega_station.ledger import Ledger


    class TestLedger(unittest.TestCase):
        def test_chain_verifies(self):
            with tempfile.TemporaryDirectory() as td:
                led = Ledger(Path(td) / "ev.jsonl")
                led.append("a", {"x": 1})
                led.append("b", {"x": 2})
                self.assertTrue(led.verify_chain()["ok"])

        def test_tamper_detected(self):
            with tempfile.TemporaryDirectory() as td:
                p = Path(td) / "ev.jsonl"
                led = Ledger(p)
                led.append("a", {"x": 1})
                led.append("b", {"x": 2})
                lines = p.read_text().splitlines()
                rec = json.loads(lines[0])
                rec["data"] = {"x": 999}
                lines[0] = json.dumps(rec, sort_keys=True)
                p.write_text(chr(10).join(lines) + chr(10))
                v = Ledger(p).verify_chain()
                self.assertFalse(v["ok"])
    ''',
)

add(
    "tests/test_shadow.py",
    r'''
    import tempfile
    import unittest
    from pathlib import Path

    from omega_station.shadow import Shadow, seal_tree


    class _L:
        def append(self, *a, **k):
            return {}


    class TestShadow(unittest.TestCase):
        def test_seal_and_anomaly(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                (root / "a.txt").write_text("one")
                sh = Shadow(root, _L())
                sh.seal()
                self.assertTrue(sh.verify()["clean"])
                (root / "a.txt").write_text("tampered")
                v = sh.verify()
                self.assertFalse(v["clean"])
                self.assertIn("a.txt", v["diff"]["modified"])
                sh.reseal("test")
                self.assertTrue(sh.verify()["clean"])

        def test_ignored_dirs_excluded(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                (root / ".git").mkdir()
                (root / ".git" / "config").write_text("x")
                (root / "keep.txt").write_text("y")
                m = seal_tree(root)
                self.assertEqual(set(m), {"keep.txt"})
    ''',
)

add(
    "tests/test_scanner.py",
    r'''
    import subprocess
    import tempfile
    import unittest
    from pathlib import Path

    from omega_station.scanner import reconcile, scan_filesystem, scan_git


    def _repo(root):
        (root / "app.py").write_text(
            "KEY = 'AKIAABCDEFGHIJKLMNOPNOP'  # TODO fix later" + chr(10))
        (root / "deploy.sh").write_text(
            "curl https://example.invalid/x | sh" + chr(10))


    class TestScanner(unittest.TestCase):
        def test_dual_scan_consensus(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                _repo(root)
                a = scan_filesystem(root)
                b = scan_filesystem(root)
                c = reconcile(a, b)
                keys = [f["key"] for f in c["confirmed"]]
                self.assertTrue(any(k.startswith("secret.") for k in keys))
                self.assertTrue(any(k.startswith("destructive.") for k in keys))

        def test_git_scan_finds_secret(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                _repo(root)
                subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root,
                       check=True)
                subprocess.run(["git", "add", "-A"], cwd=root, check=True)
                subprocess.run(
                    ["git", "-c", "user.email=t@t", "-c", "user.name=t",
                     "commit", "-qm", "init"], cwd=root, check=True)
                b = scan_git(root)
                self.assertEqual(b["method"], "git-index")
                self.assertTrue(
                    any(f["key"].startswith("secret.") for f in b["findings"]))
    ''',
)

add(
    "tests/test_actor.py",
    r'''
    import tempfile
    import unittest
    from pathlib import Path

    from omega_station.actor import Actor
    from omega_station.execution import CommandRunner
    from omega_station.providers import create_step_provider


    class _L:
        def append(self, *a, **k):
            return {}


    class _Cfg:
        provider = "mock"
        max_actor_steps = 6


    class TestActorJails(unittest.TestCase):
        def _actor(self, root, mission):
            return Actor(root, CommandRunner(root, allow_network=False),
                         _L(), _Cfg()), mission

        def test_path_jail(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                actor, m = self._actor(root, {"scope_files": [], "creates": []})
                out = actor._dispatch("read", {"path": "../../etc/passwd"}, m)
                self.assertFalse(out.get("ok", True))

        def test_scope_jail(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                (root / "in.txt").write_text("x")
                (root / "out.txt").write_text("y")
                actor, m = self._actor(root, {"scope_files": ["in.txt"],
                                              "creates": []})
                self.assertFalse(actor._dispatch(
                    "write", {"path": "out.txt", "content": "z"}, m).get("ok"))
                self.assertTrue(actor._dispatch(
                    "write", {"path": "in.txt", "content": "z2"}, m).get("ok"))

        def test_network_denied(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                actor, m = self._actor(root, {"scope_files": [], "creates": []})
                out = actor._dispatch(
                    "run", {"command": ["curl", "http://x.invalid"]}, m)
                self.assertTrue(out.get("blocked"))


    class TestMockActorThroughRealTools(unittest.TestCase):
        def test_full_actor_loop_removes_secret(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                mission = {
                    "mission_id": "T-1", "type": "remove_secret",
                    "scope_files": ["creds.py"], "attempts": 1,
                    "verification_commands": [[
                        "python", "-c",
                        "import re,sys; sys.exit(1 if "
                        "re.search(r'AKIA[0-9A-Z]{16}', "
                        "open('creds.py', errors='ignore').read()) else 0)"]],
                }
                (root / "creds.py").write_text(
                    "AWS = 'AKIAABCDEFGHIJKLMNOP'" + chr(10) + "OTHER = 1" + chr(10))
                runner = CommandRunner(root)
                self.assertEqual(
                    runner.run(mission["verification_commands"][0])["exit_code"], 1)

                actor = Actor(root, runner, _L(), _Cfg())
                report = actor.run(mission, {"role": "engineer"})
                self.assertEqual(report["verdict"], "PASS")
                self.assertEqual(
                    runner.run(mission["verification_commands"][0])["exit_code"], 0)
    ''',
)

add(
    "tests/test_policy.py",
    r'''
    import unittest

    from omega_station.policy import PolicyVerifier


    class TestPolicy(unittest.TestCase):
        def test_banned_phrase(self):
            pv = PolicyVerifier()
            r = pv.check("This journal will cure your insomnia, guaranteed!")
            self.assertFalse(r["pass"])
            rules = {v["rule"] for v in r["violations"]}
            self.assertIn("banned_phrase", rules)

        def test_price_drift(self):
            pv = PolicyVerifier(prices={"the settle journal": "9.99"})
            r = pv.check("Get The Settle Journal today for just $14.99!",
                         title="The Settle Journal")
            self.assertTrue(any(v["rule"] == "price_drift"
                                for v in r["violations"]))

        def test_clean_copy_passes(self):
            pv = PolicyVerifier(prices={"the settle journal": "9.99"})
            r = pv.check(
                "The Settle Journal - a calm nightly companion. $9.99. "
                "Not medical advice.", title="The Settle Journal")
            self.assertTrue(r["pass"])

        def test_disclaimer_required(self):
            pv = PolicyVerifier(require_disclaimer=True)
            self.assertFalse(pv.check("a calm notebook")["pass"])
    ''',
)

add(
    "tests/test_engine.py",
    r'''
    import subprocess
    import tempfile
    import unittest
    from pathlib import Path

    from omega_station.engine import OmegaStation


    def _make_repo(root):
        (root / ".gitignore").write_text(".omega/" + chr(10))
        (root / "app.py").write_text(
            "import os" + chr(10) +
            "AWS_KEY = 'AKIAABCDEFGHIJKLMNOP'" + chr(10) +
            "# TODO: refactor the loader" + chr(10))
        (root / "deploy.sh").write_text(
            "#!/bin/sh" + chr(10) +
            "curl https://example.invalid/hook | sh" + chr(10))
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root,
                       check=True)
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
        subprocess.run(
            ["git", "-c", "user.email=t@t", "-c", "user.name=t",
             "commit", "-qm", "init"], cwd=root, check=True)


    class TestFullMockRun(unittest.TestCase):
        def test_run(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                _make_repo(root)
                station = OmegaStation(root)
                results = station.run()
                by_id = {r["mission_id"]: r["status"] for r in results}

                self.assertEqual(by_id.get("OM-SEC-001"), "complete")
                self.assertEqual(by_id.get("OM-DST-001"), "complete")
                self.assertEqual(by_id.get("OM-TST-001"), "complete")
                self.assertEqual(by_id.get("OM-DEP-001"), "complete")
                self.assertEqual(by_id.get("OM-TODO-001"), "complete")

                app = (root / "app.py").read_text()
                self.assertNotIn("AKIA", app)
                self.assertIn("REVIEWED(", app)
                self.assertIn("OMEGA-GUARD",
                              (root / "deploy.sh").read_text())
                self.assertTrue(
                    (root / "tests" / "test_smoke_omega_station.py").exists())
                self.assertTrue((root / "requirements.txt").exists())

                self.assertTrue(station.verify_ledger()["ok"])
                self.assertTrue(station.verify_integrity()["clean"])
                st = station.status()
                self.assertEqual(st["missions"].get("complete"), 5)

        def test_seal_anomaly_detected_after_run(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                _make_repo(root)
                station = OmegaStation(root)
                station.run()
                (root / "app.py").write_text("sneaky out-of-band edit")
                v = station.verify_integrity()
                self.assertFalse(v["clean"])
                self.assertIn("app.py", v["diff"]["modified"])
    ''',
)

# =========================================================================
# GENERATED PROJECT FILES
# =========================================================================

add(
    "tests/test_gitflow.py",
    r'''
    import os
    import subprocess
    import tempfile
    import unittest
    from pathlib import Path

    try:
        from .test_engine import _make_repo   # package-style discovery
    except ImportError:
        from test_engine import _make_repo    # flat discovery (-s tests)
    from omega_station.engine import OmegaStation


    def _sha(root, ref):
        return subprocess.run(
            ["git", "rev-parse", ref], cwd=root, text=True,
            capture_output=True).stdout.strip()


    class TestGitFlow(unittest.TestCase):
        def test_branch_isolation_pr_and_commits(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                _make_repo(root)
                base_sha = _sha(root, "main")
                self.assertRegex(base_sha, r"^[0-9a-f]{40}$")
                station = OmegaStation(root)
                station.run()
                # station worked on an isolated branch; base untouched
                self.assertTrue(station.gitflow.isolated)
                self.assertTrue(station.gitflow.branch.startswith("omega/"))
                self.assertEqual(_sha(root, "main"), base_sha)
                cur = subprocess.run(
                    ["git", "branch", "--show-current"], cwd=root, text=True,
                    capture_output=True).stdout.strip()
                self.assertEqual(cur, station.gitflow.branch)
                # one commit per accepted mission on the branch
                n = subprocess.run(
                    ["git", "rev-list", "--count", f"main..{cur}"],
                    cwd=root, text=True, capture_output=True).stdout.strip()
                self.assertEqual(int(n), 5)
                # PR artifact exists and demands a human decision
                pr = (root / ".omega" / "PR.md").read_text()
                self.assertIn("human decision", pr)
                self.assertIn("OM-SEC-001", pr)
                self.assertIn("OK", pr)

        def test_push_to_local_origin(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                # origin must live OUTSIDE the worktree, else the repo is
                # legitimately dirty and the station correctly refuses
                # branch isolation
                origin = Path(tempfile.mkdtemp()) / "origin.git"
                _make_repo(root)
                subprocess.run(["git", "init", "-q", "--bare", str(origin)],
                               check=True)
                subprocess.run(["git", "remote", "add", "origin", str(origin)],
                               cwd=root, check=True)
                subprocess.run(["git", "push", "-q", "origin", "main"],
                               cwd=root, check=True)
                subprocess.run(
                    ["git", "branch", "--set-upstream-to=origin/main", "main"],
                    cwd=root, capture_output=True)
                station = OmegaStation(root)
                old = os.environ.get("OMEGA_PUSH")
                os.environ["OMEGA_PUSH"] = "1"
                try:
                    station.run()
                finally:
                    if old is None:
                        del os.environ["OMEGA_PUSH"]
                    else:
                        os.environ["OMEGA_PUSH"] = old
                branches = subprocess.run(
                    ["git", "branch", "--list", "omega/*"],
                    cwd=origin, text=True, capture_output=True).stdout
                self.assertIn("omega/station-", branches)

        def test_dirty_repo_refuses_isolation(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                _make_repo(root)
                (root / "user_wip.txt").write_text("uncommitted user work")
                station = OmegaStation(root)
                station.run()
                self.assertFalse(station.gitflow.isolated)
                self.assertIsNone(station.gitflow.branch)
                events = [l for l in
                          (root / ".omega" / "evidence.jsonl").read_text()
                          .splitlines() if "gitflow_unisolated" in l]
                self.assertTrue(events)
                # user file untouched, work still done + committed on base
                self.assertTrue((root / "user_wip.txt").exists())
                self.assertNotIn("AKIA", (root / "app.py").read_text())
    ''',
)

add(
    "tests/test_persistence.py",
    r'''
    import tempfile
    import unittest
    from pathlib import Path

    try:
        from .test_engine import _make_repo   # package-style discovery
    except ImportError:
        from test_engine import _make_repo    # flat discovery (-s tests)
    from omega_station.engine import OmegaStation


    class TestPersistence(unittest.TestCase):
        def test_seals_survive_restart(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                _make_repo(root)
                OmegaStation(root).run()
                second = OmegaStation(root)          # fresh process stand-in
                v = second.verify_integrity()
                self.assertTrue(v["clean"])
                (root / "app.py").write_text("out-of-band tamper")
                third = OmegaStation(root)
                v = third.verify_integrity()
                self.assertFalse(v["clean"])
                self.assertIn("app.py", v["diff"]["modified"])

        def test_resume_skips_completed(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                _make_repo(root)
                OmegaStation(root).run()
                before = (root / "app.py").read_text()
                second = OmegaStation(root)
                results = second.run()
                self.assertEqual(results, [])        # nothing re-executed
                self.assertEqual((root / "app.py").read_text(), before)
    ''',
)

add(
    "tests/test_sandbox.py",
    r'''
    import os
    import tempfile
    import unittest
    from pathlib import Path

    from omega_station.execution import CommandRunner


    class TestCredentialHygiene(unittest.TestCase):
        def test_api_key_never_leaks_to_actor_commands(self):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                old = os.environ.get("OMEGA_API_KEY")
                os.environ["OMEGA_API_KEY"] = "supersecret-leaky-value"
                try:
                    runner = CommandRunner(root)
                    res = runner.run([
                        "python", "-c",
                        "import os; print(os.environ.get("
                        "'OMEGA_API_KEY', 'CLEAN'))"])
                    self.assertEqual(res["stdout"].strip(), "CLEAN")
                    res2 = runner.run([
                        "python", "-c",
                        "import os; print(os.environ.get('TMPDIR', ''))"])
                    self.assertIn(".omega", res2["stdout"])
                finally:
                    if old is None:
                        del os.environ["OMEGA_API_KEY"]
                    else:
                        os.environ["OMEGA_API_KEY"] = old

        def test_token_env_also_scrubbed(self):
            with tempfile.TemporaryDirectory() as td:
                old = os.environ.get("GH_TOKEN")
                os.environ["GH_TOKEN"] = "ghp_shouldnotpassthrough"
                try:
                    runner = CommandRunner(Path(td))
                    res = runner.run([
                        "python", "-c",
                        "import os; print(os.environ.get("
                        "'GH_TOKEN', 'CLEAN'))"])
                    self.assertEqual(res["stdout"].strip(), "CLEAN")
                finally:
                    if old is None:
                        del os.environ["GH_TOKEN"]
                    else:
                        os.environ["GH_TOKEN"] = old


    class TestResourceLimits(unittest.TestCase):
        def test_cpu_rlimit_kills_runaway_command(self):
            with tempfile.TemporaryDirectory() as td:
                runner = CommandRunner(Path(td), cpu_limit_s=1)
                res = runner.run([
                    "python", "-c", "while True: pass"])
                self.assertNotEqual(res["exit_code"], 0)
                self.assertLess(res["duration"], 20)
    ''',
)

add(
    "tests/test_http_actor.py",
    r'''
    import json
    import os
    import tempfile
    import threading
    import unittest
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from pathlib import Path

    try:
        from .test_engine import _make_repo
    except ImportError:
        from test_engine import _make_repo
    from omega_station.config import Config
    from omega_station.engine import OmegaStation


    def _reactive_action(ctx: dict) -> dict:
        """A non-scripted HTTP brain: decides the next tool action from the
        mission + observed history, exactly like a real LLM must."""
        mission = ctx["mission"]
        hist = ctx.get("history", [])
        t = mission["type"]
        last = hist[-1]["tool"] if hist else None

        def read(f):
            return {"tool": "read", "path": f}

        def finish(v="PASS", files=None, summ="done"):
            return {"tool": "finish", "verdict": v, "summary": summ,
                    "files_changed": files or [],
                    "evidence": ["http mock actor"]}

        if t == "commit_wip":
            return finish("ESCALATE", summ="human trust decision")
        f = (mission.get("scope_files") or [None])[0]
        if t == "remove_secret":
            if last is None:
                return read(f)
            if last == "read":
                cmd = mission["verification_commands"][0][2]
                import re
                m = re.search(r"re\.search\(r'([^']+)'", cmd)
                return {"tool": "edit", "path": f,
                        "op": "drop_lines_matching", "pattern": m.group(1)}
            return finish(files=[f])
        if t == "guard_destructive":
            if last is None:
                return read(f)
            if last == "read":
                pat = r"curl.*\|\s*(ba)?sh"
                return {"tool": "edit", "path": f, "op": "replace_first",
                        "pattern": r"^(.*" + pat + r".*)$",
                        "replacement": "# OMEGA-GUARD neutralized: \\1"}
            return finish(files=[f])
        if t == "burn_todo":
            if last is None:
                return read(f)
            if last == "read":
                import datetime
                stamp = datetime.date.today().isoformat()
                return {"tool": "edit", "path": f, "op": "replace_first",
                        "pattern": r"\b(TODO|FIXME|XXX|HACK)\b",
                        "replacement": "REVIEWED(" + stamp + ")"}
            return finish(files=[f])
        if t == "add_smoke_test":
            path = mission["creates"][0]
            if last is None:
                content = (
                    "import unittest" + chr(10) + chr(10) + chr(10) +
                    "class TestSmokeOmegaStation(unittest.TestCase):" +
                    chr(10) + "    def test_station_smoke(self):" + chr(10) +
                    "        self.assertTrue(True)" + chr(10) + chr(10) +
                    chr(10) + "if __name__ == '__main__':" + chr(10) +
                    "    unittest.main()" + chr(10))
                return {"tool": "write", "path": path, "content": content}
            if last == "write":
                return {"tool": "run", "command": ["python", path]}
            return finish(files=[path])
        if t == "add_requirements":
            path = mission["creates"][0]
            if last is None:
                lines = mission.get("payload", {}).get("lines", [])
                return {"tool": "write", "path": path,
                        "content": chr(10).join(lines) + chr(10)}
            return finish(files=[path])
        return finish("ESCALATE", summ="no policy for " + str(t))


    class _Handler(BaseHTTPRequestHandler):
        mode = "reactive"

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(n))
            user = body["messages"][-1]["content"]
            if _Handler.mode == "garbage":
                content = "this is {{{ definitely not json"
            else:
                content = json.dumps(_reactive_action(json.loads(user)))
            payload = json.dumps({
                "choices": [{"message": {"content": content}}],
                "usage": {"prompt_tokens": 111, "completion_tokens": 7},
            }).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *args):
            pass


    class TestHTTPActor(unittest.TestCase):
        def _serve(self):
            srv = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
            th = threading.Thread(target=srv.serve_forever, daemon=True)
            th.start()
            self.addCleanup(srv.shutdown)
            self.addCleanup(srv.server_close)
            return srv

        def _station(self, root, port):
            cfg = Config()
            cfg.provider = "openai-compatible"
            cfg.model = "mock-http-engineer"
            cfg.api_base = f"http://127.0.0.1:{port}"
            cfg.api_key_env = "OMEGA_API_KEY"
            return OmegaStation(root, config=cfg)

        def test_full_run_over_http(self):
            _Handler.mode = "reactive"
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                _make_repo(root)
                srv = self._serve()
                old = os.environ.get("OMEGA_API_KEY")
                os.environ["OMEGA_API_KEY"] = "sk-test-key-must-not-leak"
                try:
                    station = self._station(root, srv.server_port)
                    results = station.run()
                finally:
                    if old is None:
                        del os.environ["OMEGA_API_KEY"]
                    else:
                        os.environ["OMEGA_API_KEY"] = old
                by = {r["mission_id"]: r["status"] for r in results}
                self.assertTrue(by)
                self.assertTrue(all(v == "complete" for v in by.values()), by)
                self.assertNotIn("AKIA", (root / "app.py").read_text())
                self.assertTrue(station.verify_ledger()["ok"])
                ledger = (root / ".omega" / "evidence.jsonl").read_text()
                self.assertIn("model_usage", ledger)
                self.assertNotIn("sk-test-key-must-not-leak", ledger)
                models = [r[0] for r in station.state.conn.execute(
                    "SELECT DISTINCT model FROM usage").fetchall()]
                self.assertIn("mock-http-engineer", models)

        def test_unparseable_model_output_escalates(self):
            _Handler.mode = "garbage"
            old = os.environ.get("OMEGA_API_KEY")
            os.environ["OMEGA_API_KEY"] = "sk-dummy"
            try:
                with tempfile.TemporaryDirectory() as td:
                    root = Path(td)
                    _make_repo(root)
                    srv = self._serve()
                    station = self._station(root, srv.server_port)
                    results = station.run()
                    by = {r["mission_id"]: r["status"] for r in results}
                    self.assertTrue(by)
                    self.assertTrue(all(v == "escalated" for v in by.values()),
                                    by)
                    self.assertTrue(station.verify_ledger()["ok"])
            finally:
                if old is None:
                    del os.environ["OMEGA_API_KEY"]
                else:
                    os.environ["OMEGA_API_KEY"] = old

        def test_missing_key_escalates_without_crashing(self):
            _Handler.mode = "reactive"
            old = os.environ.pop("OMEGA_API_KEY", None)
            try:
                with tempfile.TemporaryDirectory() as td:
                    root = Path(td)
                    _make_repo(root)
                    station = OmegaStation(root)   # provider: mock default
                    cfg = Config()
                    cfg.provider = "openai-compatible"
                    cfg.api_key_env = "OMEGA_API_KEY"
                    station2 = OmegaStation(root, config=cfg)
                    results = station2.run()
                    by = {r["mission_id"]: r["status"] for r in results}
                    self.assertTrue(by)
                    self.assertTrue(all(v == "escalated" for v in by.values()),
                                    by)
                    self.assertTrue(station2.verify_ledger()["ok"])
            finally:
                if old is not None:
                    os.environ["OMEGA_API_KEY"] = old
    ''',
)

add(
    "station.json",
    r'''
    {
      "provider": "mock",
      "model": "mock-engineer",
      "api_key_env": "OMEGA_API_KEY",
      "api_base": "https://api.openai.com/v1",
      "max_attempts": 3,
      "max_actor_steps": 24,
      "max_model_calls": 60,
      "max_runtime_seconds": 3600,
      "command_timeout": 180,
      "allow_network": false,
      "auto_accept_critical": false,
      "max_touched_files": 8,
      "cpu_limit_s": 30,
      "mem_limit_mb": 2048,
      "file_limit_mb": 256,
      "nproc_limit": 128,
      "env_passthrough": []
    }
    ''',
)

add(
    "banned-phrases.txt",
    '''
    # One phrase per line, lowercase. Extend per brand.
    # Lines starting with # are comments.
    cure
    cures
    guarantee
    guaranteed
    miracle
    overnight
    instantly
    ozempic
    wegovy
    fda approved
    clinically proven
    doctor recommended
    medical advice
    diagnose
    prescription
    no side effects
    100% safe
    ''',
)

add(
    "prices.example.json",
    r'''
    {
      "the settle journal": "9.99",
      "the middle season": "9.99",
      "mosaic mind": "9.99"
    }
    ''',
)

add(
    ".gitignore",
    '''
    __pycache__/
    *.pyc
    .pytest_cache/
    .venv/
    .omega/
    .env
    ''',
)

add(
    "SELLER-CHANNEL.md",
    r'''
    # Seller channel: how this station serves the catalogs

    ## The contract (air gap)

    Catalog branches (`ADHD-Journals` = Quiet Mind Press 18 books,
    `Range-Band` = Range Band Press 36 trackers) are pristine product.
    The station NEVER runs inside them and NEVER pushes to them.
    Catalog data arrives here as small exported files:

    ```text
    seller/prices-<imprint>.json    title -> price of record
    banned-phrases.txt              phrases that must never ship
    ```

    Flow: actor drafts copy/assets -> hostile policy verifier (banned
    phrases with negation guard, price drift vs the export, required
    disclaimers) -> verified assets land in a review queue with the
    hash-chained evidence trail -> a named human publishes. Publishing,
    pricing, and listing are human gates, always - the automation
    prepares, people decide.

    ## Collaboration on this branch

    - `omega-station/` is the station (builder + generated runtime +
      tests + demo). Interface guaranteed stable: the policy CLI
      `python3 -m omega_station policy <file> --title <t> --prices
      <json> --banned <txt> --require-disclaimer`.
    - Sibling directories are yours; add queue/UI/exports freely.
    - Do not merge catalog branches into this one.

    ## Imprint-specific risk notes

    - Quiet Mind Press (journals/coloring): keep the medical-advice
      disclaimer discipline; prices of record = paperback column.
    - Range Band Press (GLP-1 / wellness trackers): this is the lethal
      category for claims. Default banned list already blocks
      ozempic/wegovy/mounjaro, cure/guarantee, clinically proven,
      fda approved, doctor recommended. Extend per listing; when in
      doubt, escalate to the human reviewer.

    ## Models

    No model weights live in this repository, ever. The station calls
    an OpenAI-compatible endpoint (hosted API or a self-hosted Ollama
    box behind a tunnel); see the endpoint table in
    `station/README.md`. Cost stays fractions of a cent per call and is
    capped by the station's enforced model-call budget.
    ''',
)

add(
    "pyproject.toml",
    r'''
    [build-system]
    requires = ["setuptools>=68"]
    build-backend = "setuptools.build_meta"

    [project]
    name = "omega-station"
    version = "2.2.0"
    description = "Reflective autonomous engineering pipeline: Omega reasoning, Shadow integrity, Stationary judge, jailed actor, dual verifiers, dual overseers, hash-chained evidence."
    requires-python = ">=3.11"

    [project.scripts]
    omega-station = "omega_station.cli:main"
    ''',
)

add(
    "README.md",
    r'''
    # Omega Station

    A reflective autonomous engineering pipeline, generated from one file.

    ```text
    build_omega_station.py  ->  python3 build_omega_station.py --target .
    ```

    ## Architecture

    ```text
    Repository
        |
        +-- Shadow Scan A (filesystem walk)   independent
        +-- Shadow Scan B (git index + grep)  independent
        |
    Consensus map (confirmed / single-source / disputed - never silently resolved)
        |
    Omega mission generator (findings -> verifiable engineering missions)
        |
    per mission:
        seals BEFORE
        -> Omega plan
        -> Actor (LLM or mock) in a budgeted, scope-jailed tool loop
        -> seals AFTER
        -> Stationary judge (observe + directives only; it cannot fix)
        -> Verifier A: spec (machine-checkable commands)
        -> Verifier B: hostile (cheats, secrets, regressions, ledger chain)
        -> Overseer A: value (churn/scope)   Overseer B: risk (budgets, human gate)
        -> ACCEPT -> reseal | REWORK -> directives feed the next attempt
                   | ESCALATE (incl. missions that require a human)
    ```

    ## Use

    ```bash
    python3 build_omega_station.py --target . --force
    python3 -m unittest discover -s tests -q      # generated test suite
    python3 -m omega_station recon                # dual scans + consensus
    python3 -m omega_station missions             # mission list
    python3 -m omega_station run                  # full loop (mock provider)
    python3 -m omega_station status
    python3 -m omega_station ledger               # verify evidence chain
    python3 -m omega_station integrity            # seals vs filesystem
    python3 -m omega_station policy copy.txt --title "The Settle Journal" \
        --banned banned-phrases.txt --prices prices.example.json \
        --require-disclaimer
    ```

    ## Real LLM in the actor slot (the model never lives here)

    The station is a ~2KB thin HTTPS client, never model weights. A 1B
    or frontier model serves any number of stations from one external
    endpoint; weights never belong in git (GitHub stores, it does not
    run). Swap endpoints without touching pipeline code:

    | Setup | OMEGA_API_BASE | OMEGA_MODEL (example) |
    |---|---|---|
    | Deterministic mock (default, no key) | - | - |
    | OpenRouter | https://openrouter.ai/api/v1 | qwen/qwen-2.5-7b-instruct |
    | Groq | https://api.groq.com/openai/v1 | llama-3.1-8b-instant |
    | Ollama box via tunnel | https://<tunnel>.trycloudflare.com/v1 | qwen2.5:1.5b |
    | Any OpenAI-compatible | your endpoint | your model |

    ```bash
    export OMEGA_PROVIDER=openai-compatible
    export OMEGA_MODEL=<model>
    export OMEGA_API_BASE=<endpoint>
    export OMEGA_API_KEY=<secret>   # env only - never in git; scrubbed
    python3 -m omega_station run    # from actor-spawned commands too
    ```

    Transient network faults retry twice with backoff, then fail CLOSED:
    the mission escalates instead of proceeding on a guess. Usage tokens
    are recorded per call against the station-wide call budget.

    The actor speaks a strict one-action-per-turn JSON tool protocol
    (read / list / write / edit / run / finish). Writes and edits are
    denied outside mission scope. Network commands are denied unless
    explicitly allowed. Every step lands in the evidence ledger.

    ## Honest capability table

    | Capability | State |
    |---|---|
    | Shadow seals / corruption detection / reseal | implemented + tested |
    | Hash-chained evidence ledger | implemented + tested (tamper detected) |
    | Dual independent scans + consensus | implemented (filesystem + git) + tested |
    | Stationary judge separation | implemented (no write tools by construction) |
    | Jailed actor tool loop (LLM slot) | implemented; mock is deterministic |
    | Dual verifiers (spec + hostile) | implemented + tested |
    | Dual overseers (value + risk) | implemented + tested |
    | Rework with directive feedback | implemented (v1 lost failures; v2 feeds them back) |
    | Budget enforcement (calls / steps / runtime) | implemented + enforced |
    | Marketing policy verifier (banned/price/disclaimer) | implemented + tested |
    | Persistent seals (cross-session integrity) | implemented + tested |
    | Resume after restart (state/ledger/seals) | implemented + tested |
    | Git branch isolation + per-mission commits | implemented + tested |
    | PR artifact + optional push/PR creation | implemented + tested (local); remote needs OMEGA_PUSH / OMEGA_GH_TOKEN |
    | HTTP actor path (OpenAI-compatible endpoint) | implemented + tested end-to-end vs local mock server (reactive brain, usage recorded, garbage output escalates) |
    | Credential hygiene in command sandbox | implemented + tested (API keys/tokens scrubbed from actor processes) |
    | Resource limits (CPU / mem / file / nproc) + TMPDIR isolation | implemented + tested (Linux rlimits) |
    | Real frontier model as actor | protocol + HTTP path proven; swap in any endpoint + key |
    | Container/production sandboxing | not implemented (network denial is heuristic) |
    | Automatic merge/deploy | deliberately never implemented: merge is a human decision |

    This is an engineering-integrity substrate, not superintelligence.
    The intelligence is whatever you put in the actor slot; the value is
    that nothing it does is trusted until it survives verification.

    ## Final gate (git flow)

    Accepted missions are committed to an `omega/station-*` branch (one
    commit per verified mission) while the base branch is never touched.
    `.omega/PR.md` carries the mission table + ledger status. Set
    `OMEGA_PUSH=1` to push the branch, `OMEGA_GH_TOKEN` to open the PR.
    The station never merges - reviewing and merging is a human decision.

    ## Command sandbox (honest scope)

    Actor-spawned commands run with: workspace cwd jail, dangerous-command
    blocklist, heuristic network denial, a scrubbed environment (nothing
    matching KEY/TOKEN/SECRET/PASS/CREDENTIAL/AUTH, plus SSH/git/loader
    injection vars, reaches the child; the station's own OMEGA_API_KEY
    cannot be printed back out), a private TMPDIR, and Linux rlimits
    (CPU / address space / file size / process count). This is meaningful
    hygiene, NOT a container: a determined actor process can still read
    files inside the workspace. For untrusted models, run the station in
    a container or VM - that boundary stays out of scope by design.

    ## Air-gap rule

    Run the station in its own working copy or sandbox, never inside a
    pristine production catalog. Missions that represent trust decisions
    (committing someone's work, publishing, deploying) are generated as
    requires_human and escalate rather than act.

    ## The mock provider is honest

    It drives the real tool loop with scripted actions per mission type
    so the whole control plane (jails, seals, verifiers, overseers,
    ledger, budgets) is exercised without model credits. It is labeled
    mock in every ledger record.
    ''',
)

# =========================================================================
# BUILDER + SELF-TEST + ENTRY POINT
# =========================================================================

GENERATED_OWNED = set()


def _register_owned():
    for path in FILES:
        GENERATED_OWNED.add(path)


_register_owned()


def safe_write(root: pathlib.Path, relative: str, content: str,
               force: bool) -> None:
    dest = root / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not force and relative not in GENERATED_OWNED:
        return  # never silently destroy foreign project files
    dest.write_text(content, encoding="utf-8")


def build(target: pathlib.Path, force: bool = False) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for relative, content in FILES.items():
        safe_write(target, relative, content, force)
    print()
    print("=" * 72)
    print("OMEGA STATION CREATED")
    print("=" * 72)
    print(f"Target:  {target.resolve()}")
    print(f"Files:   {len(FILES)}")
    print()
    print("Next:")
    print("  python3 -m unittest discover -s tests -q")
    print("  python3 -m omega_station recon")
    print("  python3 -m omega_station run")
    print("  python3 -m omega_station status")
    print()


def self_test() -> int:
    import subprocess
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        build(root)
        r = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"],
            cwd=root, text=True, capture_output=True, timeout=600)
        print(r.stdout.strip()[-2000:])
        if r.returncode != 0:
            print(r.stderr[-2000:])
            print("SELF-TEST: FAIL (generated suite)")
            return 1
        print("SELF-TEST: PASS (built + full generated suite green)")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the Omega Station reflective engineering pipeline.")
    parser.add_argument("--target", default=".")
    parser.add_argument("--force", action="store_true",
                        help="overwrite previously generated files")
    parser.add_argument("--self-test", action="store_true",
                        help="build into a temp dir and run the whole suite")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    build(pathlib.Path(args.target).resolve(), force=args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
