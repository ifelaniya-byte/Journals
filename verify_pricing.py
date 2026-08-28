#!/usr/bin/env python3
"""Fail closed when Wave 1 generated prices diverge from DECISIONS.md.

The machine-readable source of truth is the markdown table headed
"## Wave 1 canonical paperback pricing" in DECISIONS.md. A `TBD` value is
intentional: it blocks validation rather than allowing a generator default,
manual metadata edit, or marketplace price to become a decision by accident.

Checks all governed locations:
- build_catalog.py product tuples (the generation mechanism),
- CATALOG.csv (technical manifest),
- release/<SKU>/metadata.txt (current artifact), and
- source/baseline-kdp/<SKU>/metadata.txt (preserved baseline artifact).

This script does not authorize a price change. Update DECISIONS.md first, then
change the generator and rebuild all derived artifacts in one controlled commit.
"""
from __future__ import annotations

import ast
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WAVE1 = ("A01", "A04", "A05", "B10", "B12", "B18")
PRICE_LINE = re.compile(r"^PRICE:\s*\$(\d+\.\d{2})\s*$", re.M)


def products() -> dict[str, tuple]:
    """Read literal product configuration without importing/running the builder."""
    tree = ast.parse((ROOT / "build_catalog.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "PRODUCTS"
            for target in node.targets
        ):
            return {row[0]: row for row in ast.literal_eval(node.value)}
    raise ValueError("build_catalog.py is missing literal PRODUCTS configuration")


def canonical_prices() -> dict[str, float | None]:
    text = (ROOT / "DECISIONS.md").read_text(encoding="utf-8")
    marker = "## Wave 1 canonical paperback pricing"
    if marker not in text:
        raise ValueError("DECISIONS.md is missing the canonical Wave 1 pricing heading")
    section = text.split(marker, 1)[1].split("\n## ", 1)[0]
    result: dict[str, float | None] = {}
    for line in section.splitlines():
        match = re.match(r"\|\s*(A\d\d|B\d\d)\s*\|\s*([^|]+)\|", line)
        if not match:
            continue
        sku, raw = match.groups()
        raw = raw.strip().replace("**", "")
        if raw == "TBD":
            result[sku] = None
        else:
            price = re.fullmatch(r"\$(\d+\.\d{2})", raw)
            if not price:
                raise ValueError(f"{sku} has invalid canonical price {raw!r}")
            result[sku] = float(price.group(1))
    missing = set(WAVE1) - set(result)
    if missing:
        raise ValueError("canonical pricing table missing " + ", ".join(sorted(missing)))
    return result


def csv_prices() -> dict[str, float | None]:
    values: dict[str, float | None] = {}
    with (ROOT / "CATALOG.csv").open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["id"] not in WAVE1:
                continue
            raw = row["price"].strip()
            values[row["id"]] = float(raw.removeprefix("$")) if re.fullmatch(r"\$\d+\.\d{2}", raw) else None
    return values


def metadata_price(path: Path) -> float | None:
    if not path.is_file():
        return None
    match = PRICE_LINE.search(path.read_text(encoding="utf-8"))
    return float(match.group(1)) if match else None


def main() -> int:
    try:
        canonical = canonical_prices()
        product_rows = products()
        manifest = csv_prices()
    except (OSError, ValueError, SyntaxError) as exc:
        print(f"FAIL  {exc}")
        return 1

    failures = 0
    for sku in WAVE1:
        wanted = canonical[sku]
        if wanted is None:
            print(f"FAIL  {sku}: canonical price is TBD — founder decision required; price gate remains closed")
            failures += 1
            continue
        if sku not in product_rows:
            print(f"FAIL  {sku}: product missing from generator")
            failures += 1
            continue
        slug = product_rows[sku][1]
        checked = {
            "generator": float(product_rows[sku][9]),
            "CATALOG.csv": manifest.get(sku),
            "release metadata": metadata_price(ROOT / "release" / f"{sku}-{slug}" / "metadata.txt"),
            "baseline metadata": metadata_price(ROOT / "source" / "baseline-kdp" / f"{sku}-{slug}" / "metadata.txt"),
        }
        mismatches = [
            f"{where}={value if value is not None else 'missing'}"
            for where, value in checked.items()
            if value != wanted
        ]
        if mismatches:
            print(f"FAIL  {sku}: expected ${wanted:.2f}; " + "; ".join(mismatches))
            failures += 1
        else:
            print(f"PASS  {sku}: all governed values are ${wanted:.2f}")

    if failures:
        print(f"\nPricing verification blocked: {failures} Wave 1 issue(s). No upload, price test, or price-sensitive Gate 1 interpretation is authorized.")
        return 1
    print("\nWave 1 pricing verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
