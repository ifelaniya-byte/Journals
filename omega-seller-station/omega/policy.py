"""Hostile seller-policy audit.

The engineer is assumed wrong until this module proves otherwise.
Tuned to Quiet Mind Press / Range Band Press operating law — not a third imprint.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

BLACKLIST = [
    r"\bozempic\b",
    r"\bwegovy\b",
    r"\bmounjaro\b",
    r"\bsaxenda\b",
    r"\bzepbound\b",
    r"\brybelsus\b",
    r"\b75\s*hard\b",
    r"\bcure[sd]?\b",
    r"\bdiagnos(?:e|is|ing)\b",
    r"\btreats nausea\b",
    r"\bvagus-nerve stimulation\b",
    r"\bpolyvagal exercises\b",
    r"\belderly coloring book\b",
    r"\bexpanded distribution:?\s*on\b",
]

BLOCKED_ACTIONS = {
    "kdp_upload",
    "amazon_publish",
    "force_push",
    "merge_imprints",
    "enable_expanded_distribution",
    "merge_branches",
}

KDP_PRICE = 9.99


def _blob(obj: Any) -> str:
    if isinstance(obj, str):
        return obj
    return json.dumps(obj, default=str)


def audit_text(text: str) -> list[str]:
    reasons = []
    lowered = text.lower()
    for pattern in BLACKLIST:
        if re.search(pattern, lowered, re.I):
            reasons.append(f"blacklist:{pattern}")
    return reasons


def audit_prices(text: str, catalog: dict[str, Any] | None) -> list[str]:
    reasons = []
    if re.search(r"\$14\.99", text) and re.search(
        r"\b(kdp|amazon|kindle)\b", text, re.I
    ):
        reasons.append("pricing_drift:B&N floor pasted onto Amazon/KDP")
    if catalog:
        listed = catalog.get("kdp_paperback")
        if listed is not None:
            try:
                expected = float(str(listed).replace("$", ""))
            except ValueError:
                expected = KDP_PRICE
            claimed = re.findall(r"\$(\d+\.\d{2})", text)
            for raw in claimed:
                value = float(raw)
                if abs(value - expected) > 0.001 and abs(value - 14.99) < 0.001:
                    reasons.append("pricing_drift:unexpected $14.99 in copy")
    return reasons


def audit_actions(payload: dict[str, Any], blocked: set[str]) -> list[str]:
    reasons = []
    action = str(payload.get("action") or payload.get("requested_action") or "")
    if action in blocked:
        reasons.append(f"blocked_action:{action}")
    for item in payload.get("actions") or []:
        if str(item) in blocked:
            reasons.append(f"blocked_action:{item}")
    return reasons


def audit_imprints(text: str) -> list[str]:
    reasons = []
    has_qm = "quiet mind" in text.lower()
    has_rb = "range band" in text.lower()
    if has_qm and has_rb and re.search(r"\bseries\b", text, re.I):
        reasons.append("imprint_mix:do not mix Quiet Mind and Range Band series")
    return reasons


def load_catalog(root: Path, catalog_file: str) -> dict[str, Any] | None:
    path = root / catalog_file
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def audit_asset(
    payload: Any,
    *,
    root: Path,
    catalog_file: str = "catalog.json",
    blocked_actions: set[str] | None = None,
) -> dict[str, Any]:
    blocked = blocked_actions or BLOCKED_ACTIONS
    text = _blob(payload)
    catalog = load_catalog(root, catalog_file)
    reasons = []
    reasons.extend(audit_text(text))
    reasons.extend(audit_prices(text, catalog))
    reasons.extend(audit_imprints(text))
    if isinstance(payload, dict):
        reasons.extend(audit_actions(payload, blocked))
        for value in payload.values():
            if isinstance(value, (dict, list, str)):
                reasons.extend(audit_text(_blob(value)))
    return {
        "ok": not reasons,
        "reasons": sorted(set(reasons)),
    }
