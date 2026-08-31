"""Fail closed if an expansion release-gate record falsely presents a release approval."""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "EXPANSION_36_CONCEPT_REGISTER.csv"
REGISTER = ROOT / "EXPANSION_36_RELEASE_GATE_REGISTER.csv"
TITLE_LOG = ROOT / "EXPANSION_36_TITLE_SCREENING_LOG.csv"
OUT = ROOT / "expansion-release"
STATUS = "LOCAL PROTOTYPE PACKAGE - HOLD - NOT FOR SALE, UPLOAD, OR MANUFACTURE"
ALLOWED_TITLE_STATES = {"COUNSEL REVIEW REQUIRED", "RETITLE BEFORE RELEASE"}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower().replace("&", "and")).strip("-")


def fail(message: str) -> None:
    print("FAIL", message)
    raise SystemExit(1)


def main() -> None:
    source = list(csv.DictReader(SOURCE.open(encoding="utf-8", newline="")))
    register = list(csv.DictReader(REGISTER.open(encoding="utf-8", newline="")))
    title_log = list(csv.DictReader(TITLE_LOG.open(encoding="utf-8", newline="")))
    expected = [f"E{i:02d}" for i in range(1, 37)]
    if [row["candidate_id"] for row in source] != expected:
        fail("source register must be E01-E36")
    if [row["candidate_id"] for row in register] != expected or [row["candidate_id"] for row in title_log] != expected:
        fail("gate and title-screen registers must have exactly one ordered record per product")
    cleared_words = ("CLEARED", "APPROVED FOR SALE", "APPROVED FOR UPLOAD", "RELEASED")
    for src, gate, title in zip(source, register, title_log):
        ident = src["candidate_id"]
        if gate["working_title"] != src["working_title"] or title["working_title"] != src["working_title"]:
            fail(f"{ident}: title differs across source and gate records")
        if gate["overall_release_status"] != STATUS:
            fail(f"{ident}: overall status no longer preserves complete hold boundary")
        if gate["title_web_screen_status"] not in ALLOWED_TITLE_STATES:
            fail(f"{ident}: unsafe/unknown title-screen state")
        if title["disposition"] != gate["title_web_screen_status"]:
            fail(f"{ident}: title-screen status differs between registers")
        for value in gate.values():
            if any(word in value.upper() for word in cleared_words):
                fail(f"{ident}: release gate contains an unsafe clearance/release assertion")
        checklist = OUT / f"{ident}-{slugify(src['working_title'])}" / "RELEASE_GATE_CHECKLIST.md"
        if not checklist.is_file():
            fail(f"{ident}: per-package release-gate checklist missing")
        text = checklist.read_text(encoding="utf-8")
        if STATUS not in text or src["working_title"] not in text or "Approval record - intentionally blank" not in text:
            fail(f"{ident}: incomplete or unsafe per-package checklist")
    packet = (ROOT / "EXPANSION_36_RELEASE_GATE_PACKET.md").read_text(encoding="utf-8")
    template = (ROOT / "EXPANSION_36_OWNER_SIGNOFF_TEMPLATE.md").read_text(encoding="utf-8")
    if STATUS not in packet or template.count("| E") != 36 or "does not create an approval" not in template:
        fail("root release-gate packet or blank named-human template is incomplete")
    retitle = [row["candidate_id"] for row in register if row["title_web_screen_status"] == "RETITLE BEFORE RELEASE"]
    print(f"PASS  36/36 expansion release-gate packets are truthful and held; {len(retitle)} titles are explicitly blocked for retitle before any release; all remaining titles await qualified review.")


if __name__ == "__main__":
    main()
