#!/usr/bin/env python3
"""Build minimum-price market kits for platforms whose price floors exceed $10.

  markets/kdp-hardcover/ - Amazon KDP hardcover (free, free ISBN), 17 titles.
      Night Pages (5x8) is EXCLUDED: 5x8 is not among KDP's hardcover trims
      (5.5x8.5, 6x9, 6.14x9.21, 6.69x9.61, 7x10, 7.44x9.69, 7.5x9.25, 8.5x11);
      interiors are locked, so no resizing. B&W cost: $6.80 flat (75-108pp)
      or $5.65 + $0.012/page (110-550pp). Floor = cost/0.60.
      Entry = smallest x.99 price with royalty >= $1.
  markets/blurb/ - Blurb trade book B&W (free), 18 titles (confirm trim
      availability in their calculator; estimate $9.03 + $0.0201/page).

NOT built: Lulu / IngramSpark hardcover (floors are breakeven; $0 at minimum).

Cover art: reuse the 300 DPI panels in markets/bn-print/<book>/.
Main catalog ($9.99) and its validators are untouched.
"""
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_HC = ROOT / "markets" / "kdp-hardcover"
OUT_BL = ROOT / "markets" / "blurb"

HC_FLAT = 6.80
HC_FIXED = 5.65
HC_PER_PAGE = 0.012
BL_FIXED = 9.03
BL_PER_PAGE = 0.0201
NO_HARDCOVER = {"night"}   # 5x8 is not a KDP hardcover trim
# PLATFORM_DECISIONS.md: coloring hardcovers HELD (buyers want cheap flat-opening paperbacks).
HC_HOLD = {"firststroke", "garden", "mosaic", "woodland", "fractal", "architect",
           "cozy", "botanical", "celestial", "tidal"}
# Blurb trade books exist in exactly three trims: 5x8, 6x9, 8x10 (Blurb's
# own spec, verified 2026-08-28). Our 8.5x11 color line, 5.5x8.5 dump and
# 7x10 parallel do not match; interiors are locked, so no resizing.
BLURB_OK = {"night", "settle", "middle", "dopamine", "slow", "soft"}


def hc_cost(pages):
    return HC_FLAT if pages < 110 else round(HC_FIXED + HC_PER_PAGE * pages, 2)


def next99(x):
    p = math.floor(x) + 0.99
    return p if p >= x - 1e-9 else p + 1.00


def entry_hc(pages):
    cost = hc_cost(pages)
    floor = cost / 0.60
    price = next99(floor)
    while price * 0.60 - cost < 1.00:
        price += 1.00
    return cost, floor, price, round(price * 0.60 - cost, 2)


def entry_blurb(pages):
    base = round(BL_FIXED + BL_PER_PAGE * pages, 2)
    price = next99(base + 1.00)
    return base, price, round(price - base, 2)


def wipe(out):
    if out.exists():
        for p in out.iterdir():
            if p.is_dir():
                for f in p.iterdir():
                    f.unlink()
                p.rmdir()
            else:
                p.unlink()
    out.mkdir(parents=True, exist_ok=True)


def main():
    wipe(OUT_HC)
    wipe(OUT_BL)
    matrix = []
    for rel in ("release3", "release4"):
        for d in sorted((ROOT / rel).iterdir()):
            if not (d.is_dir() and (d / "metadata.txt").exists()):
                continue
            md = (d / "metadata.txt").read_text()
            pages = int(re.search(r"PAGE COUNT\s*\n\s*(\d+)", md).group(1))
            title = re.search(r"AMAZON TITLE[^\n]*\n(.+)", md).group(1).strip()

            if d.name in BLURB_OK:
                base, bprice, profit = entry_blurb(pages)
                bl = md.replace("KDP LISTING",
                                "BLURB TRADE BOOK EDITION (matched minimum pricing) - KDP LISTING", 1)
                bl = bl.replace(
                    "SUGGESTED PRICE (US)\n$9.99",
                    f"SUGGESTED PRICE (US)\n${bprice:.2f}   (Blurb base cost approx ${base:.2f}; entry = base + $1)")
                bl = bl.replace("Price: $9.99", f"Price: ${bprice:.2f}")
                bl += (
                    "\n" + "-" * 80 +
                    "\nBLURB NOTES (this edition only)\n"
                    f"- Base print cost ESTIMATE ${base:.2f} ({pages}pp B&W trade). Confirm in Blurb's\n"
                    "  calculator at project setup; if it differs, price at (their base + $1.00).\n"
                    "- Trim verified: Blurb trade books come in 5x8, 6x9, 8x10 only; this book's\n"
                    "  trim fits. (8.5x11 / 5.5x8.5 / 7x10 titles have no Blurb edition.)\n"
                    f"- Entry price ${bprice:.2f} -> approx ${profit:.2f} per sale on the Blurb Bookstore.\n"
                    "- $0 upfront. Interior PDF unchanged; cover rebuilt in Blurb's template from\n"
                    f"  markets/bn-print/{d.name}/ panels.\n")
                (OUT_BL / d.name).mkdir(exist_ok=True)
                (OUT_BL / d.name / "metadata-blurb.txt").write_text(bl)

            if d.name in NO_HARDCOVER:
                matrix.append((f"{title}  [NO hardcover: 5x8 not a KDP HC trim]",
                               pages, None, None, None, None, d.name))
                continue
            cost, floor, hprice, roy = entry_hc(pages)
            hc = md.replace("KDP LISTING",
                            "KDP HARDCOVER EDITION (case laminate, matched minimum pricing) - KDP LISTING", 1)
            hc = hc.replace(
                "SUGGESTED PRICE (US)\n$9.99",
                f"SUGGESTED PRICE (US)\n${hprice:.2f}   (hardcover floor for {pages}pp is ${floor:.2f}; "
                f"lowest x.99 price paying at least $1.00 royalty)")
            hc = hc.replace("Price: $9.99", f"Price: ${hprice:.2f}")
            hc = hc.replace(
                f"COVER FILE\n{d.name}_cover_wrap.pdf",
                "COVER FILE\nKDP hardcover needs its own case-laminate wrap (no bleed, 0.625 wrap,\n"
                "0.375 hinge). Download KDP's hardcover template for this trim + page count;\n"
                f"rebuild from markets/bn-print/{d.name}/ panels (300 DPI).\n"
                "Interior: same PDF, upload unchanged (B&W, bleed OFF).")
            hc += (
                "\n" + "-" * 80 +
                f"\nHARDCOVER NOTES (this edition only; paperback everywhere else stays $9.99)\n"
                f"- B&W hardcover print cost (2026 rates): ${cost:.2f}. Floor = cost/0.60 = ${floor:.2f}.\n"
                f"- Entry price ${hprice:.2f} -> royalty ${roy:.2f} per Amazon sale.\n"
                "- Verify in KDP's printing-cost calculator and size picker at setup; rates drift.\n"
                "- Free to publish, free ISBN, 75-550 pages B&W, matte case laminate.\n"
                "- Series, imprint, keywords, categories: identical to the paperback listing.\n")
            if d.name in HC_HOLD:
                hc = hc.replace("KDP HARDCOVER EDITION",
                                "KDP HARDCOVER EDITION HOLD — DO NOT UPLOAD (coloring HC held)", 1)
                hc += ("\nHOLD — PLATFORM_DECISIONS.md: do not list coloring hardcovers.\n"
                       "Kit kept on disk. Release only if this paperback clearly outsells its print peers.\n")
            (OUT_HC / d.name).mkdir(exist_ok=True)
            (OUT_HC / d.name / "metadata-hc.txt").write_text(hc)
            matrix.append((title, pages, cost, floor, hprice, roy, d.name))

    lines = ["# Minimum-price markets: platforms whose floor is over $10", "",
             "Matched-pricing editions from each platform's own minimum rules. All $0 upfront.",
             "Main catalog stays $9.99 everywhere. Interiors unchanged.",
             "Hardcover: journals LIST, coloring HOLD. B&N print: ≥120pp LIST, thin HOLD.", "",
             "| Book | Pages | KDP-HC cost | HC floor | HC entry | HC royalty |",
             "|---|---|---|---|---|---|"]
    for title, pages, cost, floor, hprice, roy, slug in matrix:
        tag = "**HOLD** " if slug in HC_HOLD else ""
        if cost is None:
            lines.append(f"| {title} | {pages} | - | - | - | - |")
        else:
            lines.append(f"| {tag}{title} | {pages} | ${cost:.2f} | ${floor:.2f} | ${hprice:.2f} | ${roy:.2f} |")
    lines += ["",
              "**LIST 7 journal hardcovers** (dump, settle, parallel, middle, dopamine, slow, soft).",
              "**HOLD 10 coloring hardcovers** — kits exist; do not upload (PLATFORM_DECISIONS.md).",
              "Night Pages has NO hardcover kit: 5x8 is not among KDP's hardcover trims",
              "(5.5x8.5, 6x9, 6.14x9.21, 6.69x9.61, 7x10, 7.44x9.69, 7.5x9.25, 8.5x11), and",
              "interiors are locked so we do not resize. Verify the 8.5x11 hardcover option in",
              "KDP's size picker at setup (source lists differ slightly on the largest sizes).",
              "",
              "Blurb kits live in markets/blurb/ (one per book; entry = estimated base + $1;",
              "confirm base cost AND trim availability in their calculator before publishing).",
              "B&N Press print ($14.99 platform minimum): markets/bn-print/.",
              "",
              "## Floors over $10 NOT entered at the minimum (zero royalty at floor)",
              "| Platform | Format | Our floor | Why",
              "|---|---|---|---|",
              "| Lulu | hardcover | ~$21+ (mfg ~$20.22 at 160pp) | minimum = breakeven; $0 at floor |",
              "| IngramSpark | hardcover | ~$23.56 (200pp, 55% discount) | minimum = breakeven; $0 at floor |",
              "",
              "IngramSpark paperback floors are under $10 for all 18 books; standard $9.99 works there.",
              "", "Regenerate: python3 make_min_market_kits.py (deterministic)"]
    (OUT_HC / "README.md").write_text("\n".join(lines) + "\n")
    (OUT_BL / "README.md").write_text("\n".join(lines) + "\n")
    hc_n = sum(1 for m in matrix if m[2] is not None)
    print(f"built {hc_n} KDP-hardcover kits (night excluded) + {len(BLURB_OK)} Blurb kits (trims verified)")


if __name__ == "__main__":
    main()
