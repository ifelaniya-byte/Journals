#!/usr/bin/env python3
"""Fail closed if a future translation handoff no longer matches frozen source.

The guard protects source provenance only. A pass says nothing about language
quality, rights, product clearance, claims, typography, retail pricing, or
release authorization. It intentionally verifies that no completed translation
is falsely represented in the current English-only portfolio.
"""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from build_translation_manifest import LANGUAGES, NOT_STARTED
from verify_canonical import canonical_rows

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "TRANSLATION_SOURCE_MANIFEST.csv"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    try:
        canonical = canonical_rows()
        catalog_rows = {row["id"]: row for row in csv.DictReader((ROOT / "CATALOG.csv").open(encoding="utf-8", newline=""))}
        rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8", newline="")))
    except (OSError, ValueError, csv.Error) as error:
        print(f"FAIL  translation source manifest cannot be read: {error}")
        return 1

    errors: list[str] = []
    if len(rows) != 18:
        errors.append(f"translation source manifest must contain 18 rows, found {len(rows)}")
    by_sku: dict[str, dict[str, str]] = {}
    for row in rows:
        sku = row.get("sku", "")
        if not sku or sku in by_sku:
            errors.append(f"duplicate or blank manifest SKU: {sku!r}")
        by_sku[sku] = row

    if set(by_sku) != set(canonical):
        errors.append("manifest SKU set differs from the canonical 18-product portfolio")

    for sku, expected in canonical.items():
        row = by_sku.get(sku)
        if row is None:
            continue
        if row.get("canonical_title") != expected["amazon_title"]:
            errors.append(f"{sku}: canonical title differs in translation manifest")
        if (row.get("release_wave"), row.get("publication_status")) != (expected["release_wave"], expected["publication_status"]):
            errors.append(f"{sku}: wave/status differs in translation manifest")
        expected_relative = (
            f"{catalog_rows[sku]['folder']}/PRODUCT_BRIEF.md"
            if sku == "A03"
            else f"{catalog_rows[sku]['folder']}/interior.pdf"
        )
        if row.get("source_path") != expected_relative:
            errors.append(f"{sku}: manifest source path differs from controlled catalog source")
        source_path = ROOT / row.get("source_path", "")
        if not source_path.is_file():
            errors.append(f"{sku}: source file missing from translation manifest: {row.get('source_path')!r}")
        elif row.get("source_sha256") != sha256_file(source_path):
            errors.append(f"{sku}: frozen translation source digest no longer matches")
        if sku == "A03":
            if row.get("source_role") != "calendar product brief — not a KDP manuscript":
                errors.append("A03: manifest must retain non-KDP calendar source role")
        elif sku in {"A09", "B17"}:
            if row.get("source_role") != "English book-format reference interior PDF — not the actual product object":
                errors.append(f"{sku}: manifest must retain its non-production object reference role")
        elif row.get("source_role") != "English book-format interior PDF":
            errors.append(f"{sku}: manifest source role must be English book-format interior PDF")
        if row.get("target_languages") != LANGUAGES:
            errors.append(f"{sku}: multilingual scope differs from the six approved target languages")
        if row.get("translation_state") != NOT_STARTED:
            errors.append(f"{sku}: translation state must not claim completed multilingual text")

    if errors:
        for error in errors:
            print("FAIL ", error)
        print(f"\nTranslation-manifest verification blocked: {len(errors)} mismatch(es).")
        return 1
    print("PASS  all 18 controlled English sources are frozen to the translation manifest; six target languages remain not started and non-live.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
