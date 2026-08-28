#!/usr/bin/env python3
"""Build no-upfront-fee market packs.

KDP stays $9.99 (60% paperback floor). Stores with a higher print floor get
a separate $14.99 listing pack using the SAME interiors and wraps.
Digital PDF (print-at-home) stays $9.99 for Google Play / Gumroad / Payhip.

Never copies money-up-front platforms into the go-list.
"""

from __future__ import annotations

import csv
import shutil
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from assemble_kit import ALL_TITLES, KIT, listing_txt  # noqa: E402
from lib.brand import IMPRINT  # noqa: E402
from lib.kit import OUTPUT  # noqa: E402
from lib.titles import wrap_size  # noqa: E402

FLOOR = 14.99  # B&N Press print minimum as of 2026-04-22
DIGITAL = 9.99
MARKETS = ROOT.parent / "Range-Band-Markets"
# when run from kdp-journals, parent is /home/user
MARKETS = Path("/home/user/Range-Band-Markets")
FLOOR_DIR = MARKETS / "FLOOR-14.99"
DIGITAL_DIR = MARKETS / "DIGITAL-9.99"

FIXED = 0.85
PER_PAGE = 0.012


def print_cost(pages: int) -> float:
    return round(FIXED + PER_PAGE * pages, 4)


def write_csv(path: Path, titles: list[dict], extra: dict | None = None):
    fields = [
        "n",
        "kdp_title",
        "kdp_subtitle",
        "pages",
        "trim",
        "price",
        "channel",
        "interior_file",
        "cover_file",
        "keywords",
        "series",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for t in titles:
            row = dict(
                n=t["n"],
                kdp_title=t["kdp_title"],
                kdp_subtitle=t["kdp_subtitle"],
                pages=t["pages"],
                trim=f"{t['trim'][0]:g}x{t['trim'][1]:g}",
                price=f"{t['price']:.2f}",
                channel=(extra or {}).get("channel", ""),
                interior_file=t["file_interior"],
                cover_file=f"{t['stem']}_COVER_WRAP.pdf",
                keywords=" | ".join(t["keywords"]),
                series=t["series"],
            )
            w.writerow(row)


FLOOR_START = f"""# Range Band Press — FLOOR $14.99 print pack

**Use this pack only on stores whose print floor is $14.99.**
Right now that is **Barnes & Noble Press** (effective 22 April 2026).

Do **not** upload these prices to Amazon KDP. KDP stays **$9.99** (the 60% royalty floor) in `KDP-Complete-Kit/`.

Interiors and wrap PDFs are the **same print files** as the $9.99 kit. Only the listing price and the channel note change.

## Upload (B&N Press)

1. [press.barnesandnoble.com](https://press.barnesandnoble.com) — free account, no monthly fee, no setup fee.
2. Paperback · black & white · white paper · bleed OFF.
3. Interior = `*_interior.pdf`. Cover = `*_COVER_WRAP.pdf` (full wrap). If B&N rejects the wrap, download *their* template and drop in `*_COVER_FRONT.pdf` as the front panel. Never reuse a rejected wrap blindly.
4. Paste `listing.txt`. Author: **{IMPRINT}**. US price **$14.99**.
5. Free B&N ISBN is fine (B&N-exclusive). Do not buy Bowker ISBNs for this pack — that is upfront money.
6. Print royalty is about **55% of list − print cost**. Confirm live on their pricing page.

B&N also caps accounts around 100 live titles. We have 36. Fine.

Read `../PLAYBOOK.md` before you open another store.
"""

DIGITAL_START = f"""# Range Band Press — DIGITAL $9.99 print-at-home PDFs

Print-layout PDFs for stores that take a cut **only when a copy sells**. No monthly fee. No setup fee.

This is **not** a reflowable EPUB. Readers get the same pages as the paperback. Say that in the listing.

## Where these go

| Store | File | Price | Cut |
|---|---|---|---|
| Google Play Books | interior PDF + cover JPG | $9.99 | ~30% (you keep ~70%) |
| Gumroad | same | $9.99 | 10% + $0.50 (direct) |
| Payhip Free | same | $9.99 | 5% + Stripe |

## Do not

- Enroll a Kindle edition of the same file in **KDP Select** (that exclusivity fights Google Play).
- Upload these to Apple Books or Kobo (they want EPUB, not PDF).
- Pay Lulu **$4.99** for ebook global distribution — use Google Play direct instead.
- Put $14.99 on these. Digital has no $14.99 floor.

Author: **{IMPRINT}**. Paste `listing.txt`.
"""


def build_floor():
    if FLOOR_DIR.exists():
        shutil.rmtree(FLOOR_DIR)
    FLOOR_DIR.mkdir(parents=True)
    (FLOOR_DIR / "00_START_HERE.md").write_text(FLOOR_START, encoding="utf-8")
    titles = []
    for src in ALL_TITLES:
        t = deepcopy(src)
        t["price"] = FLOOR
        t["channel_note"] = (
            f"FLOOR $14.99 LISTING — {t['n']}  ·  B&N Press / any $14.99 print floor\n"
            "Do not upload this price to Amazon KDP ($9.99 kit)."
        )
        titles.append(t)
        folder = FLOOR_DIR / f"{t['n']}_{t['stem'][3:]}"
        folder.mkdir()
        src_folder = KIT / f"{t['n']}_{t['stem'][3:]}"
        for name in (
            f"{t['stem']}_interior.pdf",
            f"{t['stem']}_COVER_WRAP.pdf",
            f"{t['stem']}_COVER_FRONT.pdf",
        ):
            shutil.copy2(src_folder / name, folder / name)
        ww, hh, sp = wrap_size(t["trim"], t["pages"])
        (folder / "listing.txt").write_text(listing_txt(t, ww, hh, sp), encoding="utf-8")
    write_csv(FLOOR_DIR / "METADATA.csv", titles, {"channel": "BN Press print floor $14.99"})
    # royalty note
    lines = ["# Floor pack proof", "", "All 36 list at **$14.99**. Interiors/wraps identical to the $9.99 kit.", ""]
    lines.append("| # | pages | est. print $ | B&N ~55% − print $ |")
    lines.append("|---|---|---|---|")
    for t in titles:
        pc = print_cost(t["pages"])
        bn = round(FLOOR * 0.55 - pc, 2)
        assert abs(t["price"] - 14.99) < 1e-9
        assert bn > 0, t["n"]
        lines.append(f"| {t['n']} | {t['pages']} | {pc:.2f} | {bn:.2f} |")
    (FLOOR_DIR / "PROOF.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("FLOOR", FLOOR_DIR, "titles", len(titles))


def build_digital():
    import pymupdf

    if DIGITAL_DIR.exists():
        shutil.rmtree(DIGITAL_DIR)
    DIGITAL_DIR.mkdir(parents=True)
    (DIGITAL_DIR / "00_START_HERE.md").write_text(DIGITAL_START, encoding="utf-8")
    titles = []
    for src in ALL_TITLES:
        t = deepcopy(src)
        t["price"] = DIGITAL
        t["channel_note"] = (
            f"DIGITAL $9.99 PRINT-AT-HOME PDF — {t['n']}\n"
            "Google Play / Gumroad / Payhip. Not an EPUB. Not for Apple or Kobo."
        )
        titles.append(t)
        folder = DIGITAL_DIR / f"{t['n']}_{t['stem'][3:]}"
        folder.mkdir()
        src_folder = KIT / f"{t['n']}_{t['stem'][3:]}"
        shutil.copy2(src_folder / f"{t['stem']}_interior.pdf", folder / f"{t['stem']}_printathome.pdf")
        front = src_folder / f"{t['stem']}_COVER_FRONT.pdf"
        doc = pymupdf.open(front)
        pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False)
        pix.save(str(folder / f"{t['stem']}_cover.jpg"))
        doc.close()
        ww, hh, sp = wrap_size(t["trim"], t["pages"])
        text = listing_txt(t, ww, hh, sp)
        text += (
            "\nDIGITAL FILE NOTES\n"
            "-------------------\n"
            f"Upload `{t['stem']}_printathome.pdf` as the book file.\n"
            f"Upload `{t['stem']}_cover.jpg` as the store thumbnail.\n"
            "Say: print-at-home PDF of the paperback interior. Not a reflowable ebook.\n"
            "Trim / print: bleed OFF, white paper, same page count as the paperback.\n"
        )
        (folder / "listing.txt").write_text(text, encoding="utf-8")
    write_csv(DIGITAL_DIR / "METADATA.csv", titles, {"channel": "digital PDF $9.99"})
    print("DIGITAL", DIGITAL_DIR, "titles", len(titles))


def main():
    if not KIT.exists():
        raise SystemExit(f"need {KIT} first (run refresh_packaging.py)")
    MARKETS.mkdir(parents=True, exist_ok=True)
    build_floor()
    build_digital()
    play = ROOT / "MARKETS_PLAYBOOK.md"
    if play.exists():
        shutil.copy2(play, MARKETS / "PLAYBOOK.md")
    print("MARKETS", MARKETS)


if __name__ == "__main__":
    main()
