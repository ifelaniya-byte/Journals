#!/usr/bin/env python3
"""One minimum-price version of every title, for every print floor we can enter.

PDFs are identical across prices. Only listing.txt / METADATA change.
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
from lib.floors import CHANNELS, prices_for  # noqa: E402
from lib.titles import wrap_size  # noqa: E402

MARKETS = Path("/home/user/Range-Band-Markets")


def _clone(src: dict, price: float, note: str) -> dict:
    t = deepcopy(src)
    t["price"] = float(price)
    t["channel_note"] = note
    return t


def _write_csv(path: Path, titles: list[dict], channel: str):
    fields = [
        "n",
        "kdp_title",
        "pages",
        "trim",
        "price",
        "channel",
        "interior_file",
        "cover_file",
        "series",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for t in titles:
            w.writerow(
                dict(
                    n=t["n"],
                    kdp_title=t["kdp_title"],
                    pages=t["pages"],
                    trim=f"{t['trim'][0]:g}x{t['trim'][1]:g}",
                    price=f"{t['price']:.2f}",
                    channel=channel,
                    interior_file=t["file_interior"],
                    cover_file=f"{t['stem']}_COVER_WRAP.pdf",
                    series=t["series"],
                )
            )


def _copy_print_files(t: dict, dest: Path):
    src_folder = KIT / f"{t['n']}_{t['stem'][3:]}"
    dest.mkdir(parents=True, exist_ok=True)
    for name in (
        f"{t['stem']}_interior.pdf",
        f"{t['stem']}_COVER_WRAP.pdf",
        f"{t['stem']}_COVER_FRONT.pdf",
    ):
        shutil.copy2(src_folder / name, dest / name)


def _listing(t: dict, dest: Path):
    ww, hh, sp = wrap_size(t["trim"], t["pages"])
    (dest / "listing.txt").write_text(listing_txt(t, ww, hh, sp), encoding="utf-8")


def build_print_pack(slug: str, channel_id: str, start: str, copy_pdfs: bool) -> Path:
    out = MARKETS / slug
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "00_START_HERE.md").write_text(start, encoding="utf-8")
    titles = []
    ch = next(c for c in CHANNELS if c["id"] == channel_id)
    for src in ALL_TITLES:
        price = ch["price_fn"](src)
        note = (
            f"{ch['name']}  ·  TITLE {src['n']}  ·  ${price:.2f} (this store's print minimum)\n"
            f"Do not upload this price to a store with a different floor. KDP stays $9.99."
        )
        t = _clone(src, price, note)
        titles.append(t)
        folder = out / f"{t['n']}_{t['stem'][3:]}"
        folder.mkdir()
        if copy_pdfs:
            _copy_print_files(t, folder)
        else:
            (folder / "USE_PDFS_FROM.txt").write_text(
                "Same print files as KDP-Complete-Kit/"
                f"{t['n']}_{t['stem'][3:]}/\n"
                "Interior + wrap + front. This folder is the listing at this store's minimum.\n",
                encoding="utf-8",
            )
        _listing(t, folder)
    _write_csv(out / "METADATA.csv", titles, ch["name"])
    prices = sorted({t["price"] for t in titles})
    print(f"  {slug:20} {len(titles)} titles  prices {prices}")
    return out


def build_digital():
    import pymupdf

    out = MARKETS / "DIGITAL-9.99"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    start = f"""# DIGITAL $9.99 print-at-home PDF

Google Play Books, Gumroad, Payhip Free. No print floor. No monthly fee.

Author: **{IMPRINT}**. File = `*_printathome.pdf`. Thumbnail = `*_cover.jpg`.
Say it is a print-at-home PDF of the paperback, not a reflowable EPUB.
Do not upload to Apple or Kobo (they want EPUB).
"""
    (out / "00_START_HERE.md").write_text(start, encoding="utf-8")
    titles = []
    for src in ALL_TITLES:
        t = _clone(
            src,
            9.99,
            f"DIGITAL $9.99 PDF — {src['n']}\nGoogle Play / Gumroad / Payhip. Not Apple. Not Kobo.",
        )
        titles.append(t)
        folder = out / f"{t['n']}_{t['stem'][3:]}"
        folder.mkdir()
        src_folder = KIT / f"{t['n']}_{t['stem'][3:]}"
        shutil.copy2(
            src_folder / f"{t['stem']}_interior.pdf",
            folder / f"{t['stem']}_printathome.pdf",
        )
        doc = pymupdf.open(src_folder / f"{t['stem']}_COVER_FRONT.pdf")
        pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False)
        pix.save(str(folder / f"{t['stem']}_cover.jpg"))
        doc.close()
        _listing(t, folder)
    _write_csv(out / "METADATA.csv", titles, "digital PDF")
    print("  DIGITAL-9.99         36 titles  prices [9.99]")


def build_by_title():
    root = MARKETS / "by-title"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir()
    product_rows = []
    for src in ALL_TITLES:
        px = prices_for(src)
        folder = root / f"{src['n']}_{src['stem'][3:]}"
        folder.mkdir()
        lines = [
            f"# {src['n']}  {src['kdp_title']}",
            "",
            f"{src['pages']} pages · {src['trim'][0]:g}×{src['trim'][1]:g} in · {IMPRINT}",
            "",
            "One version per store, at **that store's print minimum**. Same interior PDF.",
            "",
            "| Channel | Price | Upload from | Go? |",
            "|---|---|---|---|",
        ]
        for ch in CHANNELS:
            p = px[ch["id"]]
            go = "YES" if ch["go"] else "PARKED"
            lines.append(f"| {ch['name']} | **${p:.2f}** | `{ch['pack']}/{src['n']}_{src['stem'][3:]}/` | {go} |")
            # listing-only subfolder
            sub = folder / ch["id"]
            sub.mkdir()
            t = _clone(
                src,
                p,
                f"{ch['name']}  ·  {src['n']}  ·  ${p:.2f}\n"
                + ("PARKED — " + ch["why"] if not ch["go"] else ch["why"]),
            )
            _listing(t, sub)
        (folder / "00_VERSIONS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        product_rows.append(
            {
                "n": src["n"],
                "title": src["kdp_title"],
                "pages": src["pages"],
                "trim": f"{src['trim'][0]:g}x{src['trim'][1]:g}",
                **{ch["id"]: f"{px[ch['id']]:.2f}" for ch in CHANNELS},
            }
        )
    fields = ["n", "title", "pages", "trim"] + [c["id"] for c in CHANNELS]
    with (MARKETS / "PRODUCTS.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(product_rows)
    print("  by-title             36 products ×", len(CHANNELS), "channels")


def write_floors_csv():
    with (MARKETS / "FLOORS.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["id", "name", "go", "upfront", "cut", "pack", "why"],
        )
        w.writeheader()
        for ch in CHANNELS:
            w.writerow(
                {
                    "id": ch["id"],
                    "name": ch["name"],
                    "go": "YES" if ch["go"] else "PARKED",
                    "upfront": ch["upfront"],
                    "cut": ch["cut"],
                    "pack": ch["pack"],
                    "why": ch["why"],
                }
            )


def main():
    if not KIT.exists():
        raise SystemExit(f"need {KIT}")
    if MARKETS.exists():
        shutil.rmtree(MARKETS)
    MARKETS.mkdir(parents=True)

    bn_start = f"""# BN Press — every title **$14.99**

Barnes & Noble Press will not create a paperback under $14.99 (22 Apr 2026).
This is the **minimum version** of each of the 36 titles for that store.

Same interiors/wraps as KDP. Author: **{IMPRINT}**. Free B&N ISBN.
Do **not** upload $14.99 to Amazon KDP.
"""
    lulu_start = f"""# Lulu Global — each title at **2× print cost** (x.99, never under $9.99)

Lulu print Global Distribution: list must be at least twice print cost.
That number is **different per book** (page count / trim). Confirm print cost
in Lulu's calculator; these listings use a 2026 B&W estimate.

Author: **{IMPRINT}**. PDFs = same as KDP. Skip Lulu *ebook* Global Dist ($4.99).
Lulu's own bookstore can stay $9.99 (see KDP kit listings).
"""
    ingram_start = f"""# IngramSpark — PARKED (ISBN costs money)

No catalog-wide $14.99 floor. Each title's listing is the estimated
compensation-positive minimum at 55% wholesale, rounded to x.99.

**Do not upload until you buy Bowker ISBNs.** Setup fee is $0 (2026);
the ISBN is the upfront cost. When you do: rebuild the wrap in Ingram's
template. Never reuse the KDP wrap blindly.

Author: **{IMPRINT}**.
"""

    print("building market packs…")
    build_print_pack("BN-Press", "BN", bn_start, copy_pdfs=True)
    build_print_pack("Lulu-Global", "LULU-GLOBAL", lulu_start, copy_pdfs=True)
    build_print_pack("Ingram-PARKED", "INGRAM", ingram_start, copy_pdfs=False)
    build_digital()
    build_by_title()
    write_floors_csv()
    play = ROOT / "MARKETS_PLAYBOOK.md"
    if play.exists():
        shutil.copy2(play, MARKETS / "PLAYBOOK.md")
    census = ROOT / "MARKETS_CENSUS.md"
    if census.exists():
        shutil.copy2(census, MARKETS / "CENSUS.md")
    (MARKETS / "README.md").write_text(
        "# Markets — one minimum per title, per store\n\n"
        "Read **PLAYBOOK.md**. Spreadsheet: **PRODUCTS.csv**. Per book: **by-title/**.\n\n"
        "| Folder | Price |\n|---|---|\n"
        "| `BN-Press/` | $14.99 every title (B&N catalog floor) |\n"
        "| `Lulu-Global/` | per title, 2× Lulu print, x.99, never under $9.99 |\n"
        "| `DIGITAL-9.99/` | $9.99 PDF |\n"
        "| `Ingram-PARKED/` | formula min, listings only — no upload |\n"
        "| `by-title/` | all channel listings for that one product |\n\n"
        "`FLOOR-14.99/` was renamed to `BN-Press/`.\n",
        encoding="utf-8",
    )
    old = MARKETS / "FLOOR-14.99"
    old.mkdir()
    (old / "MOVED.md").write_text(
        "This pack moved to `../BN-Press/`.\n"
        "B&N Press is still $14.99 on every title — that is their catalog floor, "
        "not a shared price we invented for other stores.\n",
        encoding="utf-8",
    )
    print("MARKETS", MARKETS)


if __name__ == "__main__":
    main()
