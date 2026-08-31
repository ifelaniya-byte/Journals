#!/usr/bin/env python3
"""Create the locked English-source manifest for future bilingual handoffs.

This program does not translate, alter, or release a product. It records the
exact source artifact and SHA-256 digest that a qualified translation team must
receive *after* the individual product clears its applicable English/name/claims
gates. The manifest is deliberately limited to the controlled 18-concept
portfolio; it never draws text/assets from the separate public repository.
"""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from verify_canonical import canonical_rows

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "TRANSLATION_SOURCE_MANIFEST.csv"
LANGUAGES = "Spanish|French|Hindi|Simplified Chinese|Hausa|Yorùbá"
NOT_STARTED = "NOT STARTED — no translation text or release authorization"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    canonical = canonical_rows()
    manifest = {row["id"]: row for row in csv.DictReader((ROOT / "CATALOG.csv").open(encoding="utf-8", newline=""))}
    if set(manifest) != set(canonical):
        raise ValueError("CATALOG.csv must first agree with the canonical portfolio table")

    rows: list[dict[str, str]] = []
    for sku, controlled in sorted(canonical.items()):
        catalog = manifest[sku]
        if sku == "A03":
            source = ROOT / catalog["folder"] / "PRODUCT_BRIEF.md"
            source_role = "calendar product brief — not a KDP manuscript"
        elif sku in {"A09", "B17"}:
            source = ROOT / catalog["folder"] / "interior.pdf"
            source_role = "English book-format reference interior PDF — not the actual product object"
        else:
            source = ROOT / catalog["folder"] / "interior.pdf"
            source_role = "English book-format interior PDF"
        if not source.is_file():
            raise FileNotFoundError(f"{sku}: source is missing: {source}")
        rows.append({
            "sku": sku,
            "canonical_title": controlled["amazon_title"],
            "release_wave": controlled["release_wave"],
            "publication_status": controlled["publication_status"],
            "source_role": source_role,
            "source_path": source.relative_to(ROOT).as_posix(),
            "source_sha256": sha256_file(source),
            "target_languages": LANGUAGES,
            "translation_state": NOT_STARTED,
        })

    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "sku", "canonical_title", "release_wave", "publication_status", "source_role",
            "source_path", "source_sha256", "target_languages", "translation_state",
        ], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {OUT.name}: {len(rows)} sealed English source entries; no translations created.")


if __name__ == "__main__":
    main()
