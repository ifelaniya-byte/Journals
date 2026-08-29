#!/usr/bin/env python3
"""Quiet Mind Press — per-store minimum listings. PDFs stay in release3/release4."""

from __future__ import annotations

import csv
import math
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from i18n_listings import LANGS, copy_for  # noqa: E402

MARKETS = ROOT / "MARKETS"
CATALOG = ROOT / "CATALOG.csv"
BN_FLOOR = 14.99
HOUSE = 9.99
# Owner digital tiers (2026-08-28): $4.99 large-pool attractors, $6.99 rest,
# The Middle Season has NO digital edition (print-only flagship lane).
POOL_499 = {"dump", "dopamine", "cozy", "soft", "settle"}
NO_DIGITAL = {"middle"}
# PLATFORM_DECISIONS.md: B&N lists only ≥120pp. Thin kits still exist as HOLD.
BN_HOLD = {"firststroke", "garden", "cozy", "botanical", "celestial", "tidal", "soft"}


def round_99(x: float) -> float:
    if x <= 0.99:
        return 0.99
    n = math.floor(x)
    cand = n + 0.99
    if cand + 1e-9 < x:
        cand += 1.0
    return round(cand, 2)


def parse_price(s: str) -> float:
    return float(str(s).replace("$", "").strip())


def parse_trim(s: str) -> tuple[float, float]:
    a, b = s.lower().replace("×", "x").split("x")
    return float(a), float(b)


def lulu_print(pages: int, tw: float, th: float) -> float:
    base = 1.64 + 0.021 * pages
    if tw >= 8.0 or th >= 10.5:
        base *= 1.22
    return round(base, 2)


def ingram_print(pages: int, tw: float) -> float:
    base = 1.33 + 0.0146 * pages
    if tw >= 8.0:
        base *= 1.15
    return round(base, 2)


def load_titles() -> list[dict]:
    rows = []
    with CATALOG.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            tw, th = parse_trim(r["trim"])
            pages = int(r["pages"])
            kdp = parse_price(r["price"])
            rel = "release3" if r["batch"] == "B3" else "release4"
            slug = r["interior_file"].split("/")[0]
            src = ROOT / rel / slug
            lp = lulu_print(pages, tw, th)
            ip = ingram_print(pages, tw)
            rows.append(
                dict(
                    n=r["n"].zfill(2) if r["n"].isdigit() else r["n"],
                    n_raw=r["n"],
                    batch=r["batch"],
                    title=r["amazon_title"],
                    cover_title=r["cover_title"],
                    subtitle=r["subtitle"],
                    pages=pages,
                    trim=r["trim"],
                    tw=tw,
                    th=th,
                    paper=r["paper"],
                    series=r["series"],
                    slug=slug,
                    rel=rel,
                    src=src,
                    kdp=kdp,
                    bn=round(max(kdp, BN_FLOOR), 2),
                    bn_go=slug not in BN_HOLD,
                    lulu=round_99(max(2.0 * lp, kdp, HOUSE)),
                    digital=(None if r["interior_file"].split("/")[0] in NO_DIGITAL
                             else 4.99 if r["interior_file"].split("/")[0] in POOL_499 else 6.99),
                    ingram=round_99(max(ip / 0.43125, kdp, HOUSE)),
                    lulu_unit=lp,
                    interior=r["interior_file"],
                    cover=r["cover_file"],
                    keywords=r["keywords"],
                    categories=r["categories"],
                    difficulty=r.get("difficulty") or "",
                )
            )
    return rows


def retarget(meta: str, banner: str, price: float) -> str:
    meta = re.sub(r"^.*\n================================", banner + "\n================================", meta, count=1)
    meta = re.sub(r"(SUGGESTED PRICE \(US\)\n)\$[0-9.]+", rf"\1${price:.2f}", meta)
    meta = re.sub(r"(Price: )\$[0-9.]+", rf"\1${price:.2f}", meta)
    return meta


def write_listing(t: dict, dest: Path, channel: str, price: float, extra: str):
    dest.mkdir(parents=True, exist_ok=True)
    src_meta = t["src"] / "metadata.txt"
    banner = f"{channel}  ·  TITLE {t['n']}  ·  ${price:.2f}\n{extra}"
    text = retarget(src_meta.read_text(encoding="utf-8"), banner, price)
    (dest / "listing.txt").write_text(text, encoding="utf-8")
    (dest / "USE_PDFS_FROM.txt").write_text(
        f"Interior: {t['rel']}/{t['slug']}/{t['slug']}_interior.pdf\n"
        f"Wrap:     {t['rel']}/{t['slug']}/{t['slug']}_cover_wrap.pdf\n"
        f"Front JPG:{t['rel']}/{t['slug']}/{t['slug']}_cover.jpg\n"
        f"Listing images 02–07 in the same folder.\n",
        encoding="utf-8",
    )


def write_csv(path: Path, titles: list[dict], price_key: str, channel: str):
    fields = ["n", "title", "pages", "trim", "price", "channel", "pdf_from", "series"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for t in titles:
            w.writerow(
                dict(
                    n=t["n"],
                    title=t["title"],
                    pages=t["pages"],
                    trim=t["trim"],
                    price=f"{t[price_key]:.2f}",
                    channel=channel,
                    pdf_from=f"{t['rel']}/{t['slug']}/",
                    series=t["series"],
                )
            )


def build_pack(slug: str, price_key: str, start: str, channel: str, extra: str):
    out = MARKETS / slug
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "00_START_HERE.md").write_text(start, encoding="utf-8")
    titles = load_titles()
    for t in titles:
        extra_t = extra
        if slug == "BN-Press" and not t.get("bn_go", True):
            extra_t = (
                "HOLD — do not upload. PLATFORM_DECISIONS.md: B&N only for titles ≥120pp. "
                "This file is the $14.99 floor kit kept on disk. KDP stays $9.99."
            )
        write_listing(t, out / f"{t['n']}_{t['slug']}", channel, t[price_key], extra_t)
    write_csv(out / "METADATA.csv", titles, price_key, channel)
    prices = sorted({t[price_key] for t in titles})
    print(f"  {slug:18} {len(titles)}  prices {prices}")


def build_digital():
    out = MARKETS / "DIGITAL"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "00_START_HERE.md").write_text(
        "# DIGITAL — print-at-home PDF, $4.99 attractors / $6.99 (owner tiers)\n\n"        "\nMiddle Season: NO digital edition (print-only flagship lane).\n"
        "Google Play, Gumroad, Payhip, Ko-fi, itch.io, Lemon Squeezy, Whop.\n"
        "File = interior PDF. Thumbnail = cover.jpg.\n"
        "Say it is a print-at-home PDF of the paperback. Book language: English.\n"
        "Translated sales copy: ../i18n/ (do not change the PDF language on Google Play).\n",
        encoding="utf-8",
    )
    titles = load_titles()
    digital_titles = [t for t in titles if t["digital"] is not None]
    for t in digital_titles:
        dest = out / f"{t['n']}_{t['slug']}"
        write_listing(
            t,
            dest,
            "DIGITAL PDF",
            t["digital"],
            "Google Play / Gumroad / Payhip / Ko-fi / itch.io. Not Apple. Not Kobo.",
        )
        jpg = t["src"] / f"{t['slug']}_cover.jpg"
        if jpg.exists():
            shutil.copy2(jpg, dest / f"{t['slug']}_cover.jpg")
    write_csv(out / "METADATA.csv", digital_titles, "digital", "digital PDF")
    print(f"  DIGITAL            {len(digital_titles)} (middle print-only)")


def build_by_title():
    root = MARKETS / "by-title"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir()
    titles = load_titles()
    channels = [
        ("KDP", "kdp", "Amazon KDP paperback", f"{'{rel}'}/{'{slug}'}/", True),
        ("BN", "bn", "Barnes & Noble Press", "MARKETS/BN-Press/{n}_{slug}/", True),
        ("LULU-GLOBAL", "lulu", "Lulu print Global Dist.", "MARKETS/Lulu-Global/{n}_{slug}/", True),
        ("DIGITAL", "digital", "Google Play / Gumroad / Payhip PDF", "MARKETS/DIGITAL/{n}_{slug}/", True),
        ("INGRAM", "ingram", "IngramSpark paperback", "MARKETS/Ingram-PARKED/{n}_{slug}/", False),
    ]
    product_rows = []
    for t in titles:
        folder = root / f"{t['n']}_{t['slug']}"
        folder.mkdir()
        lines = [
            f"# {t['n']}  {t['title']}",
            "",
            f"{t['pages']} pages · {t['trim']} in · Quiet Mind Press · {t['series']}",
            "",
            "One version per store at **that store's minimum**. Same interior PDF (English).",
            "",
            "| Channel | Price | Upload from | Go? |",
            "|---|---|---|---|",
        ]
        for cid, key, name, pack, go in channels:
            p = t[key]
            path = pack.format(**t)
            sub = folder / cid
            if cid == "BN":
                go = t.get("bn_go", go)
            if p is None:
                lines.append(f"| {name} | **print only** | — | NO |")
                sub.mkdir(exist_ok=True)
                (sub / "PRINT_ONLY.txt").write_text(
                    "No digital edition: the flagship stays print-only (owner lane).\n",
                    encoding="utf-8")
                continue
            if cid == "BN" and not go:
                lines.append(f"| {name} | **${p:.2f}** | `{path}` | HOLD |")
                extra = "HOLD — <120pp at B&N $14.99 looks overpriced vs our $9.99 Amazon edition (PLATFORM_DECISIONS.md). Files exist; do not upload."
                write_listing(t, sub, name, p, extra)
                continue
            lines.append(f"| {name} | **${p:.2f}** | `{path}` | {'YES' if go else 'PARKED'} |")
            extra = ("PARKED — Bowker ISBN is upfront money." if not go else "Cut on sale only.")
            write_listing(t, sub, name, p, extra)
        (folder / "00_VERSIONS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        product_rows.append(
            {
                "n": t["n"],
                "title": t["title"],
                "pages": t["pages"],
                "trim": t["trim"],
                "KDP": f"{t['kdp']:.2f}",
                "BN": f"{t['bn']:.2f}",
                "LULU-GLOBAL": f"{t['lulu']:.2f}",
                "DIGITAL": "print only" if t["digital"] is None else f"{t['digital']:.2f}",
                "INGRAM": f"{t['ingram']:.2f}",
            }
        )
    fields = ["n", "title", "pages", "trim", "KDP", "BN", "LULU-GLOBAL", "DIGITAL", "INGRAM"]
    with (MARKETS / "PRODUCTS.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(product_rows)
    print("  by-title           18 × 5")


def build_i18n():
    titles = load_titles()
    root = MARKETS / "i18n"
    if root.exists():
        shutil.rmtree(root)
    for code, lang in LANGS.items():
        d = root / code
        d.mkdir(parents=True)
        (d / "00_README.md").write_text(
            f"# {lang['name']} listings — Quiet Mind Press\n\n"
            f"Paste on Gumroad / Payhip / Ko-fi / itch.io.\n"
            f"Do **not** set Google Play book-language to {lang['name']} — the PDF is English.\n"
            f"Imprint stays **Quiet Mind Press** in the author field.\n"
            f"Prices: $4.99 attractors / $6.99 (The Middle Season is print-only).\n",
            encoding="utf-8",
        )
        i18n_titles = [t for t in titles if t["digital"] is not None]
        for t in i18n_titles:
            body = copy_for(t, code)
            (d / f"{t['n']}_{t['slug']}.txt").write_text(body, encoding="utf-8")
        print(f"  i18n/{code:4}         {len(i18n_titles)}")


def main():
    if MARKETS.exists():
        shutil.rmtree(MARKETS)
    MARKETS.mkdir()
    titles = load_titles()
    assert len(titles) == 18, len(titles)
    for t in titles:
        if not (t["src"] / "metadata.txt").exists():
            raise SystemExit(f"missing metadata {t['src']}")

    build_pack(
        "BN-Press",
        "bn",
        "# B&N Press — max(KDP list, $14.99)\n\n"
        "B&N will not create a paperback under $14.99 (22 Apr 2026).\n"
        "LIST the 11 titles ≥120 pages. HOLD the 7 thin titles (96–104pp) — kits exist, do not upload.\n"
        "PDFs = release3/release4. Never upload this price to KDP.\n",
        "BN Press",
        "Hard floor $14.99. Do not put this price on Amazon.",
    )
    build_pack(
        "Lulu-Global",
        "lulu",
        "# Lulu Global — max(KDP list, 2× print, $9.99)\n\n"
        "Confirm print cost in Lulu's calculator. Skip ebook Global Dist ($4.99).\n",
        "Lulu Global",
        "List ≥ 2× Lulu print. Confirm calculator.",
    )
    build_pack(
        "Ingram-PARKED",
        "ingram",
        "# IngramSpark — PARKED (ISBN costs money)\n\nDo not upload until Bowker ISBNs exist. New wrap in Ingram's template.\n",
        "IngramSpark PARKED",
        "PARKED — Bowker ISBN is upfront.",
    )
    build_digital()
    build_by_title()
    build_i18n()
    for name in ("MARKETS_PLAYBOOK.md", "MARKETS_CENSUS.md"):
        src = ROOT / name
        if src.exists():
            shutil.copy2(src, MARKETS / ("PLAYBOOK.md" if "PLAYBOOK" in name else "CENSUS.md"))
    (MARKETS / "README.md").write_text(
        "# Quiet Mind Press markets\n\n"
        "Read **PLAYBOOK.md** and **CENSUS.md**. Spreadsheet: **PRODUCTS.csv**.\n"
        "Translated copy: **i18n/** (zh hi es fr ha yo).\n"
        "PDFs stay in `release3/` and `release4/`.\n",
        encoding="utf-8",
    )
    # proof
    under_bn = [t for t in titles if t["kdp"] < BN_FLOOR]
    print("BN raised", len(under_bn), "titles to $14.99")
    print("MARKETS", MARKETS)


if __name__ == "__main__":
    main()
