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
