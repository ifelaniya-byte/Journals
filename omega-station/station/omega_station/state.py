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
