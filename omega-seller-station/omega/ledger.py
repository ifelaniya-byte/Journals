from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class EvidenceLedger:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, mission_id: str | None, event: str, data: Any = None) -> None:
        record = {"mission_id": mission_id, "event": event, "data": data}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, default=str, sort_keys=True) + "\n")
