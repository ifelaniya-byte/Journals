#!/usr/bin/env python3
"""Fail closed if local author attribution drifts across controlled catalog files.

This verifies that the owner-directed *provisional local* author string appears
consistently in the 17 book-format release packages and A03's non-KDP brief.
It does not establish name availability, ownership, trademark clearance,
publisher/imprint approval, or any permission to release a product.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent
BRAND = json.loads((ROOT / "brand_config.json").read_text(encoding="utf-8"))
AUTHOR = str(BRAND.get("author", "")).strip()


def text_from_pdf(path: Path, pages: int | None = None) -> str:
    document = fitz.open(path)
    try:
        selected = document if pages is None else [document[number] for number in range(min(pages, document.page_count))]
        return "\n".join(page.get_text("text") for page in selected)
    finally:
        document.close()


def metadata_value(path: Path, key: str) -> str | None:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(key + ": "):
            return line.split(": ", 1)[1]
    return None


def main() -> int:
    errors: list[str] = []
    if not AUTHOR or AUTHOR in {"[Author / Imprint]", "Author / Imprint"}:
        errors.append("brand_config.json has no valid provisional author string")
    if "provisional" not in str(BRAND.get("author_status", "")).casefold():
        errors.append("brand_config.json must state that author attribution remains provisional")

    with (ROOT / "CATALOG.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 18:
        errors.append(f"CATALOG.csv must retain 18 governed concepts, found {len(rows)}")

    for row in rows:
        sku = row["id"]
        if sku == "A03":
            brief = ROOT / row["folder"] / "PRODUCT_BRIEF.md"
            if not brief.is_file() or f"**Author:** {AUTHOR}" not in brief.read_text(encoding="utf-8"):
                errors.append("A03: non-KDP brief lacks the configured provisional author attribution")
            continue
        folder = ROOT / row["folder"]
        metadata, interior, wrap = folder / "metadata.txt", folder / "interior.pdf", folder / "cover_wrap.pdf"
        if not all(path.is_file() for path in (metadata, interior, wrap)):
            errors.append(f"{sku}: release artifact needed for author check is missing")
            continue
        if metadata_value(metadata, "AUTHOR") != AUTHOR:
            errors.append(f"{sku}: metadata author differs from configured author")
        if AUTHOR not in text_from_pdf(interior, pages=1):
            errors.append(f"{sku}: author is absent from title page")
        if AUTHOR.casefold() not in text_from_pdf(wrap).casefold():
            errors.append(f"{sku}: author is absent from cover wrap")

    # Preserve author attribution in the seven source baseline packages used to assemble existing release copies.
    for folder in sorted((ROOT / "source" / "baseline-kdp").glob("*")):
        if not folder.is_dir():
            continue
        metadata, interior, wrap = folder / "metadata.txt", folder / "interior.pdf", folder / "cover_wrap.pdf"
        if not all(path.is_file() for path in (metadata, interior, wrap)):
            errors.append(f"{folder.name}: baseline author artifact is missing")
            continue
        if metadata_value(metadata, "AUTHOR") != AUTHOR:
            errors.append(f"{folder.name}: baseline metadata author differs")
        if AUTHOR not in text_from_pdf(interior, pages=1):
            errors.append(f"{folder.name}: baseline title page lacks author")
        if AUTHOR.casefold() not in text_from_pdf(wrap).casefold():
            errors.append(f"{folder.name}: baseline wrap lacks author")

    if errors:
        for error in errors:
            print("FAIL ", error)
        print(f"\nAuthor-attribution verification blocked: {len(errors)} issue(s).")
        return 1
    print("PASS  the owner-directed provisional author attribution is consistent across 17 controlled book packages, seven preserved baseline packages, and the A03 brief; no release clearance is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
