from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    workspace: str = ".omega"
    model_provider: str = "mock"
    model_name: str = "mock"
    api_key_env: str = "OPENAI_API_KEY"
    api_base: str = "https://api.openai.com/v1"
    max_attempts: int = 3
    max_workers: int = 2
    command_timeout_seconds: int = 120
    allow_network: bool = False
    auto_merge: bool = False
    docker_enabled: bool = False
    catalog_file: str = "catalog.json"
    generated_dir: str = "generated"
    dangerous_commands: list[str] = field(
        default_factory=lambda: [
            "rm -rf /",
            "shutdown",
            "reboot",
            "mkfs",
            "force-push",
            "git push --force",
            "kdp upload",
            "amazon publish",
        ]
    )
    blocked_actions: list[str] = field(
        default_factory=lambda: [
            "kdp_upload",
            "amazon_publish",
            "force_push",
            "merge_imprints",
            "enable_expanded_distribution",
        ]
    )

    @classmethod
    def load(cls, root: Path) -> "Config":
        cfg = cls()
        path = root / ".seller-station.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                for key, value in data.items():
                    if hasattr(cfg, key):
                        setattr(cfg, key, value)
            except Exception as exc:
                print(f"Warning: config load failed: {exc}")
        env = {
            "model_provider": "OMEGA_PROVIDER",
            "model_name": "OMEGA_MODEL",
            "api_base": "OMEGA_API_BASE",
        }
        for field_name, env_name in env.items():
            value = os.getenv(env_name)
            if value:
                setattr(cfg, field_name, value)
        return cfg

    @property
    def api_key(self) -> str | None:
        return os.getenv(self.api_key_env)
