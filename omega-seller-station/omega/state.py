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
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    mission_id TEXT,
                    event TEXT NOT NULL,
                    data TEXT
                );
                CREATE TABLE IF NOT EXISTS usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    mission_id TEXT,
                    provider TEXT,
                    model TEXT,
                    input_tokens INTEGER,
                    output_tokens INTEGER,
                    total_tokens INTEGER,
                    cost REAL
                );
                """
            )
            self.conn.commit()

    def save_mission(self, mission: dict[str, Any]) -> None:
        with self.lock:
            self.conn.execute(
                """
                INSERT INTO missions(mission_id, data)
                VALUES (?, ?)
                ON CONFLICT(mission_id) DO UPDATE SET data=excluded.data
                """,
                (mission["mission_id"], json.dumps(mission, default=str)),
            )
            self.conn.commit()

    def get_mission(self, mission_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT data FROM missions WHERE mission_id=?", (mission_id,)
        ).fetchone()
        return None if row is None else json.loads(row["data"])

    def all_missions(self) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT data FROM missions ORDER BY rowid").fetchall()
        return [json.loads(row["data"]) for row in rows]

    def event(self, mission_id: str | None, event: str, data: Any = None) -> None:
        with self.lock:
            self.conn.execute(
                "INSERT INTO events(mission_id,event,data) VALUES (?,?,?)",
                (mission_id, event, json.dumps(data, default=str) if data is not None else None),
            )
            self.conn.commit()

    def usage(self, mission_id: str | None, provider: str, model: str, data: dict) -> None:
        with self.lock:
            self.conn.execute(
                """
                INSERT INTO usage(mission_id,provider,model,input_tokens,output_tokens,total_tokens,cost)
                VALUES (?,?,?,?,?,?,?)
                """,
                (
                    mission_id,
                    provider,
                    model,
                    data.get("input_tokens"),
                    data.get("output_tokens"),
                    data.get("total_tokens"),
                    data.get("cost"),
                ),
            )
            self.conn.commit()

    def close(self) -> None:
        self.conn.close()
