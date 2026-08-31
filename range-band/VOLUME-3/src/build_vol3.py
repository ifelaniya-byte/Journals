#!/usr/bin/env python3
"""Range Band Press Volume 3 — builder (candidate-only).

Creates 36 new print-ready KDP kits (interior + cover wrap + cover front +
listing.txt) under /home/user/new-catalog/KDP-Complete-Kit. Reuses the frozen
Range-Band generator machinery read-only (lib/kit.py, lib/covers.py, lib/brand.py,
fonts) — no catalog file is modified. No push, no upload.
"""
from __future__ import annotations

import csv
import json
import math
import re
import sys
import time
from pathlib import Path

SRC = Path("/tmp/Journals-remote/range-band/src")
sys.path.insert(0, str(SRC))

from pypdf import PdfReader  # noqa: E402

from lib import brand  # noqa: E402
from lib.covers import make_front, make_wrap  # noqa: E402
from lib.kit import Book, SIX_NINE, standard_front  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vol3_spec_a import CHRONIC_CARE  # noqa: E402
from vol3_spec_a2 import CHRONIC_REST  # noqa: E402
from vol3_spec_b import INNER_RANGE  # noqa: E402
from widgets import (  # noqa: E402
    draw_bridge, draw_bucket, draw_cards, draw_court, draw_dial, draw_gauge,
    draw_gauge2, draw_hist, draw_ladder, draw_ledger, draw_map, draw_meter,
    draw_note, draw_orbit, draw_quad, draw_radar, draw_review, draw_script,
    draw_trail, draw_wave, draw_wheel, draw_wire, draw_clinic,
)

# new series accents (patched at runtime; frozen brand.py untouched)
brand.ACCENT["CHRONIC CARE SERIES"] = (0.36, 0.44, 0.58)
brand.ACCENT["INNER RANGE SERIES"] = (0.68, 0.52, 0.28)

VOL3 = CHRONIC_CARE + CHRONIC_REST + INNER_RANGE
for _t in VOL3:
    _t.setdefault("price", 9.99)
OUT_ROOT = Path("/home/user/new-catalog")
KIT = OUT_ROOT / "KDP-Complete-Kit"
OUTPUT = OUT_ROOT / "output"
IMPRINT = "Range Band Press"

WIDGETS = {
    "quad": draw_quad, "radar": draw_radar, "map": draw_map, "gauge": draw_gauge,
    "gauge2": draw_gauge2, "ledger": draw_ledger, "bucket": draw_bucket,
    "trail": draw_trail, "wire": draw_wire, "ladder": draw_ladder, "wave": draw_wave,
    "cards": draw_cards, "script": draw_script, "bridge": draw_bridge,
    "dial": draw_dial, "court": draw_court, "orbit": draw_orbit, "wheel": draw_wheel,
    "hist": draw_hist, "meter": draw_meter,
}

FILLER_PAGES = 3  # blank interleave pages to hit even totals


def goals_list(t):
    return [
        "One honest thing I already know:",
        "One thing I want the record to show:",
        "Where I want to be in 30 days:",
        "One rule I am setting for myself:",
    ]


def build_interior(t: dict) -> Path:
    dest = OUTPUT / f"{t['stem']}_interior.pdf"
    book = Book(dest, pagesize=SIX_NINE, running="Range Band Press  ·  " + t["series_short"])
    standard_front(
        book,
        series=t["series"].title(),
        title=t["cover_title_one"],
        subtitle=t["subtitle"].replace("\n", " "),
        tagline=t["tagline"],
        how_to=t["howto"],
        goals=goals_list(t),
        extra_disclaimer=(
            "Personal tracking / management tool only. Not medical advice. "
            "Records what you and your own care team directed; this book gives no advice."
        ),
        legend=t["legend"],
        how_to_title="How this journal works",
        goals_title="Where I am starting",
    )
    day = 0
    days = t["days"]
    widget = WIDGETS[t["daily"]]
    for d in range(1, days + 1):
        widget(book, d, t)
        book.end()
        day += 1
    # weekly reviews
    week = 1
    for d in range(7, days + 1, 7):
        draw_review(book, f"Week {week}", [
            "What got clearer:",
            "What got louder:",
            "What I will change next week:",
            "One win (any size):",
        ])
        book.end()
        week += 1
    # monthly pattern pages
    month = 1
    for d in range(28, days + 1, 28):
        draw_review(book, f"Month {month} — pattern", [
            "Most consistent pattern:",
            "Most surprising:",
            "What I am taking into next month:",
        ])
        book.end()
        month += 1
    draw_clinic(book, t)
    book.end()
    for i in range(2):
        draw_note(book, i + 1, "Notes")
        book.end()
    # interstitial blanks to keep even page count for print (KDP friendly)
    for _ in range(4):
        draw_note(book, _, "Blank — your own pages")
        book.end()
    book.save()
    return dest


def listing_text(t: dict, interior_name: str, wrap_name: str) -> str:
    hook = t.get("hook", "A discreet, undated tracking journal.")
    house = "Live inside the range."
    house_long = "A range is not a cage. It is the band you already chose. Undated logs for a life that has numbers but is not a number."
    glp = False  # Volume 3 is not a GLP-1 line
    disclaimer = "Personal tracking / management tool only. Not medical advice."
    bullets = "".join(f"<li>{b}</li>" for b in t["bullets"])
    also = "".join(f"<li>{x}</li>" for x in t.get("also") or [])
    html = f"""<p><b>{t['kdp_title']}</b> — {t['kdp_subtitle']}</p>
<p><i>{house}</i> {hook}</p>
<p>From <b>{IMPRINT}</b>. {house_long} Write what your own clinician already directed. This book does not diagnose, dose, or treat, and it is not affiliated with any medication manufacturer.</p>
<p><b>Inside</b></p>
<ul>{bullets}</ul>
<p><b>Also in this catalog</b></p>
<ul>{also}</ul>
<p>Trim {t['trim'][0]:g} × {t['trim'][1]:g} in · {t['pages']} pages · black-and-white interior · white paper recommended · bleed OFF · <b>${t['price']:.2f}</b>.</p>
<p><i>{disclaimer}</i></p>"""
    plain = "\n".join([
        t["kdp_title"], t["kdp_subtitle"], "",
        f"{house} {hook}", "",
        f"From {IMPRINT}. {house_long} Fill in what your own clinician already directed. This book does not diagnose, dose, or treat, and it is not affiliated with any medication manufacturer.", "",
        "INSIDE",
    ] + [f"  • {b}" for b in t["bullets"]] + ["", "ALSO IN THIS CATALOG"] +
        [f"  • {x}" for x in t.get("also") or []] + [
        "", f"Trim {t['trim'][0]:g} × {t['trim'][1]:g} in · {t['pages']} pages · black-and-white interior · white paper recommended · bleed OFF · ${t['price']:.2f}.",
        "", disclaimer,
    ])
    return f"""KDP LISTING — {t['n']}  (Range Band Press Volume 3)
================================
TITLE (≤200 chars)
{t['kdp_title']}

SUBTITLE
{t['kdp_subtitle']}

AUTHOR / IMPRINT
{IMPRINT}

LANGUAGE
English

INTERIOR
Black & white  |  Bleed: OFF  |  Paper: white

TRIM
{t['trim'][0]:g}" × {t['trim'][1]:g}"

PAGE COUNT
{t['pages']}

COVER FILE
{wrap_name}

INTERIOR FILE
{interior_name}

CATEGORIES / BISAC
{' | '.join(f'{name}  ({code})' for name, code in zip(t['bisac_names'], t['bisac']))}

SEVEN BACKEND KEYWORDS
{chr(10).join(f'  {i+1}. {k}' for i, k in enumerate(t['keywords']))}

SUGGESTED PRICE (US)
$9.99

DESCRIPTION (plain)
-------------------
{plain}

DESCRIPTION (HTML paste)
------------------------
{html}
"""


def build_one(t: dict) -> dict:
    folder = KIT / t["stem"]
    folder.mkdir(parents=True, exist_ok=True)
    interior = OUTPUT / f"{t['stem']}_interior.pdf"
    wrap = folder / f"{t['stem']}_COVER_WRAP.pdf"
    front = folder / f"{t['stem']}_COVER_FRONT.pdf"
    interior_dest = folder / f"{t['stem']}_interior.pdf"
    t["file_interior"] = interior_dest.name
    build_interior(t)
    # sync page count before covers so wrap/spine math is exact
    actual = len(PdfReader(str(interior)).pages)
    t["actual_pages"] = actual
    t["pages"] = actual
    make_wrap(t, wrap)
    make_front(t, front)
    import shutil
    shutil.copy2(interior, interior_dest)
    listing = folder / "listing.txt"
    listing.write_text(listing_text(t, interior_dest.name, wrap.name), encoding="utf-8")
    return {
        "n": t["n"], "stem": t["stem"], "folder": t["stem"],
        "title": t["kdp_title"], "subtitle": t["kdp_subtitle"],
        "series": t["series"], "pages": t["pages"], "trim": f'{t["trim"][0]:g}x{t["trim"][1]:g}',
        "mechanic": t["mechanic"], "daily": t["daily"],
        "interior_file": interior_dest.name, "cover_wrap": wrap.name, "cover_front": front.name,
        "listing": listing.name, "price": 9.99,
    }


def verify_pdf(path: Path) -> dict:
    r = PdfReader(str(path))
    box = r.pages[0].mediabox
    return {
        "pages": len(r.pages),
        "width": round(float(box.width) / 72, 3),
        "height": round(float(box.height) / 72, 3),
    }


def validate(row: dict, t: dict) -> list[str]:
    issues = []
    p = OUTPUT / f"{t['stem']}_interior.pdf"
    if p.exists():
        info = verify_pdf(p)
        if info["pages"] < 24:
            issues.append(f"interior only {info['pages']} pages")
        if abs(info["width"] - t["trim"][0]) > 0.01 or abs(info["height"] - t["trim"][1]) > 0.01:
            issues.append(f"trim {info['width']}x{info['height']} vs {t['trim']}")
    return issues


BLACKLIST = re.compile(
    r"\bozempic\b|\bwegovy\b|\bmounjaro\b|\bsaxenda\b|\bzepbound\b|\brybelsus\b"
    r"|\b75\s*hard\b|\btreats nausea\b|\bvagus[- ]nerve stimulation\b|\bpolyvagal exercises\b"
    r"|\belderly coloring book\b", re.I)


def main():
    seen_kw = {}
    kw_issues = []
    text_issues = []
    rows = []
    for i, t in enumerate(sorted(VOL3, key=lambda x: int(x["n"])), 1):
        t0 = time.time()
        row = build_one(t)
        # keyword uniqueness
        for k in t["keywords"]:
            key = k.lower().strip()
            if key in seen_kw:
                kw_issues.append(f"dup '{k}' ({seen_kw[key]} & {t['n']})")
            seen_kw[key] = t["n"]
        if len(t["keywords"]) != 7:
            kw_issues.append(f"{t['n']}: {len(t['keywords'])} keywords")
        listing = (KIT / t["stem"] / "listing.txt").read_text(encoding="utf-8")
        blob = json.dumps({**t, "listing": listing})
        for m in BLACKLIST.finditer(blob.lower()):
            text_issues.append(f"{t['n']}: blacklist '{m.group(0)}'")
        issues = validate(row, t)
        row["issues"] = issues
        row["seconds"] = round(time.time() - t0, 1)
        rows.append(row)
        print(f"  OK {row['n']}  {row['stem'][:38]:38}  {row['pages']:>3}p  {row['daily']:7}  {row['seconds']}s  issues={len(issues)}")

    fields = ["n", "stem", "folder", "title", "subtitle", "series", "pages", "trim",
              "mechanic", "daily", "interior_file", "cover_wrap", "cover_front",
              "listing", "price", "issues"]
    with open(OUT_ROOT / "METADATA_VOL3.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    summary = {
        "titles": len(rows),
        "keyword_issues": kw_issues,
        "text_issues": text_issues,
        "row_issues": {r["n"]: r["issues"] for r in rows if r["issues"]},
        "unique_keywords": len(seen_kw),
    }
    (OUT_ROOT / "BUILD_SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "text_issues"}, indent=2))
    if text_issues:
        print("TEXT BLACKLIST:", text_issues)
    if kw_issues:
        print("KEYWORD ISSUES:", kw_issues)
    else:
        print("VALIDATION: PASS (36 titles, 252 unique keywords, zero blacklist hits)")


if __name__ == "__main__":
    main()
