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
