#!/usr/bin/env python3
"""Fail closed if the generated multichannel model drifts from canonical prices.

This guard does not validate a platform's live calculator or authorize a
listing. It protects two limited things: only canonically priced Wave 1 books
may receive planning-price rows, and their current KDP US paperback anchors
must exactly match PORTFOLIO.md.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from build_multichannel_pricing import CHANNELS, LANGUAGES, PRICE_TIERS
from verify_canonical import canonical_rows

ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "MULTICHANNEL_PRICING_MODEL.csv"
LANGUAGE = ROOT / "BILINGUAL_LANGUAGE_REGISTER.csv"


def main() -> int:
    try:
        canonical = canonical_rows()
        rows = list(csv.DictReader(MODEL.open(encoding="utf-8", newline="")))
        languages = list(csv.DictReader(LANGUAGE.open(encoding="utf-8", newline="")))
    except (OSError, ValueError, csv.Error) as error:
        print(f"FAIL  multichannel model cannot be read: {error}")
        return 1

    errors: list[str] = []
    priced_wave1 = {
        sku: item for sku, item in canonical.items()
        if item["release_wave"] == "Wave 1" and item["price"] in PRICE_TIERS
    }
    if len(priced_wave1) != 6:
        errors.append(f"canonical baseline must contain six priced Wave 1 SKUs, found {len(priced_wave1)}")

    expected_rows = len(priced_wave1) * len(CHANNELS)
    if len(rows) != expected_rows:
        errors.append(f"pricing model has {len(rows)} rows; expected {expected_rows}")

    by_sku: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_sku[row.get("sku", "")].append(row)
        sku = row.get("sku", "")
        if sku not in priced_wave1:
            errors.append(f"{sku or '<blank>'}: model row exists for a non-priced/non-Wave-1 SKU")
            continue
        baseline = priced_wave1[sku]
        if row.get("canonical_title") != baseline["amazon_title"]:
            errors.append(f"{sku}: title drift in pricing model")
        if row.get("release_wave") != "Wave 1" or row.get("publication_status") != baseline["publication_status"]:
            errors.append(f"{sku}: release state drift in pricing model")
        if row.get("channel") == "Amazon KDP paperback" and row.get("edition") == "English paperback":
            if row.get("planned_list_price_usd") != baseline["price"]:
                errors.append(f"{sku}: KDP US anchor {row.get('planned_list_price_usd')!r} != canonical {baseline['price']!r}")
            if row.get("operational_state") != "CURRENT PRICE ANCHOR / HOLD":
                errors.append(f"{sku}: KDP anchor row is not explicitly HOLD")

    for sku in priced_wave1:
        if len(by_sku[sku]) != len(CHANNELS):
            errors.append(f"{sku}: expected {len(CHANNELS)} channel rows, found {len(by_sku[sku])}")
        anchors = [r for r in by_sku[sku] if r.get("channel") == "Amazon KDP paperback" and r.get("edition") == "English paperback"]
        if len(anchors) != 1:
            errors.append(f"{sku}: expected exactly one English KDP paperback anchor row")

    expected_languages = {"Spanish", "French", "Hindi", "Simplified Chinese", "Hausa", "Yorùbá"}
    seen_languages = {row.get("target_language") for row in languages}
    if seen_languages != expected_languages or len(languages) != len(LANGUAGES):
        errors.append("bilingual language register must contain exactly Spanish, French, Hindi, Simplified Chinese, Hausa, and Yorùbá")
    if any(row.get("current_state") != "No live text yet" for row in languages):
        errors.append("language register must not imply translated text is live")

    if errors:
        for error in errors:
            print("FAIL ", error)
        print(f"\nMultichannel pricing verification blocked: {len(errors)} mismatch(es).")
        return 1
    print(f"PASS  {len(rows)} controlled pricing-planning rows retain all six canonical Wave 1 KDP anchors; six bilingual target languages remain non-live.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
