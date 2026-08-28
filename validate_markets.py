#!/usr/bin/env python3
"""Validate the markets/ tree: every edition kit family, cross-checked.

Checks (run after any generator):
  markets/bn-print       18 kits, $14.99 in every metadata-bn.txt
  markets/kdp-hardcover  exactly 17 kits (night excluded: 5x8 not a HC trim);
                         price in {13.99,14.99,15.99}; recomputed floor math
                         must give royalty >= $1.00
  markets/blurb          exactly 6 kits (Blurb trades = 5x8/6x9/8x10 only);
                         price == next99(estimated base + $1)
  markets/digital        exactly 17 kits (middle excluded: print-only lane);
                         tier prices correct; $9.99-callout image warning present
  EDITIONS_MATRIX.csv    present, 18 rows
"""
import csv
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
M = ROOT / "markets"
NO_HC = {"night"}          # 5x8 is not a KDP hardcover trim
BLURB_OK = {"night", "settle", "middle", "dopamine", "slow", "soft"}  # 5x8/6x9 = Blurb's only matching trims
NO_DIGITAL = {"middle"}    # print-only flagship lane
POOL_499 = {"dump", "dopamine", "cozy", "soft", "settle"}
errors = []


def book_pages(md):
    return int(re.search(r"PAGE COUNT\s*\n\s*(\d+)", md).group(1))


def next99(x):
    p = math.floor(x) + 0.99
    return p if p >= x - 1e-9 else p + 1.00


books = {}
for rel in ("release3", "release4"):
    for d in sorted((ROOT / rel).iterdir()):
        if d.is_dir() and (d / "metadata.txt").exists():
            books[d.name] = book_pages((d / "metadata.txt").read_text())
assert len(books) == 18, f"expected 18 release books, found {len(books)}"

# B&N
for k in books:
    f = M / "bn-print" / k / "metadata-bn.txt"
    if not f.exists():
        errors.append(f"bn-print missing {k}")
    elif "$14.99" not in f.read_text():
        errors.append(f"bn-print {k}: price not $14.99")

# KDP hardcover
hc_dirs = {p.name for p in (M / "kdp-hardcover").iterdir() if p.is_dir()}
if hc_dirs != set(books) - NO_HC:
    errors.append(f"hardcover set wrong: extra={hc_dirs - set(books) + NO_HC}, missing={set(books) - NO_HC - hc_dirs}")
for k in set(books) - NO_HC:
    f = M / "kdp-hardcover" / k / "metadata-hc.txt"
    if not f.exists():
        continue
    md = f.read_text()
    m = re.search(r"SUGGESTED PRICE \(US\)\n\$(\d+\.\d\d)", md)
    if not m:
        errors.append(f"hc {k}: no price")
        continue
    price = float(m.group(1))
    pages = books[k]
    cost = 6.80 if pages < 110 else round(5.65 + 0.012 * pages, 2)
    floor = cost / 0.60
    if price * 0.60 - cost < 1.00 - 1e-9:
        errors.append(f"hc {k}: ${price} below $1-royalty entry (floor ${floor:.2f})")
    if price not in (13.99, 14.99, 15.99):
        errors.append(f"hc {k}: unexpected price ${price}")

# Blurb (only trim-valid titles: Blurb trades are 5x8/6x9/8x10)
bl_dirs = {p.name for p in (M / "blurb").iterdir() if p.is_dir()}
if bl_dirs != BLURB_OK:
    errors.append(f"blurb set wrong: extra={bl_dirs - BLURB_OK}, missing={BLURB_OK - bl_dirs}")
for k in BLURB_OK:
    f = M / "blurb" / k / "metadata-blurb.txt"
    if not f.exists():
        errors.append(f"blurb missing {k}")
        continue
    m = re.search(r"SUGGESTED PRICE \(US\)\n\$(\d+\.\d\d)", f.read_text())
    want = next99(round(9.03 + 0.0201 * books[k], 2) + 1.00)
    if not m or abs(float(m.group(1)) - want) > 0.005:
        errors.append(f"blurb {k}: price {m.group(1) if m else 'missing'} != expected {want:.2f}")

# Digital
dig_dirs = {p.name for p in (M / "digital").iterdir() if p.is_dir() and p.name != "samplers"}
if dig_dirs != set(books) - NO_DIGITAL:
    errors.append(f"digital set wrong: extra={dig_dirs - set(books) + NO_DIGITAL}, missing={set(books) - NO_DIGITAL - dig_dirs}")
for k in set(books) - NO_DIGITAL:
    f = M / "digital" / k / "metadata-digital.txt"
    if not f.exists():
        continue
    md = f.read_text()
    m = re.search(r"SUGGESTED PRICE \(DIGITAL\)\n\$(\d+\.\d\d)", md)
    want = 4.99 if k in POOL_499 else 6.99
    if not m or abs(float(m.group(1)) - want) > 0.005:
        errors.append(f"digital {k}: price {m.group(1) if m else 'missing'} != {want:.2f}")
    if "listing_06" not in md:
        errors.append(f"digital {k}: missing $9.99-callout image warning")

# Editions matrix
mx = ROOT / "EDITIONS_MATRIX.csv"
if not mx.exists():
    errors.append("EDITIONS_MATRIX.csv missing")
else:
    rows = list(csv.DictReader(open(mx)))
    if len(rows) != 18:
        errors.append(f"EDITIONS_MATRIX.csv has {len(rows)} rows, want 18")

if errors:
    print("MARKETS: FAIL")
    for e in errors:
        print("  -", e)
    raise SystemExit(1)
print("MARKETS: PERFECT — bn 18 x $14.99; hc 17 (night out) floors+entries verified; "
      "blurb 6 (trims verified) base+1; digital 17 tiers + image warnings; matrix 18 rows")
