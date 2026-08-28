#!/usr/bin/env python3
"""Regenerate listing-side files for all 18 titles + build catalog formats.

Outputs:
  releaseN/<dir>/metadata.txt      (upgraded keywords/prices/descriptions)
  CATALOG.csv                       (one row per title: specs, spine, wrap, price)
  LOOKBOOK.pdf                      (cover thumbnails + specs, one page per title)
  00_START_HERE.md                  (master upload guide + format inventory)

Run AFTER any interior/cover rebuild so metadata never drifts:
    python gen_catalog.py
"""
from __future__ import annotations
import csv, io
from pathlib import Path
from PIL import Image
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

import build_nine_products as B
import build_batch4 as B4
import niche_upgrades as U

ROOT = Path(__file__).resolve().parent
BLEED = 0.125
SERIES = {k: "CORE LINE (B3)" for k in B.PRODUCTS}
SERIES.update({k: "RISING NICHES (B4)" for k in B4.PRODUCTS4})


def all_products():
    items = []
    n = 0
    for src, batch in ((B.PRODUCTS, "B3"), (B4.PRODUCTS4, "B4")):
        for key in src:
            n += 1
            p = dict(src[key])
            p["batch"] = batch
            p["n"] = n
            p["key"] = key
            p["release"] = B.RELEASE if batch == "B3" else B4.RELEASE
            items.append(p)
    return items


def upgraded(p):
    key = p["key"]
    kw = U.KEYWORDS[key]
    price = U.PRICES.get(key, p["price"])
    desc = p["desc"] + U.DESC_APPEND.get(key, "")
    return kw, price, desc


def write_metadata(p):
    kw, price, desc = upgraded(p)
    d = p["release"] / p["dir"]
    B.write_text(d / "metadata.txt", f"""TITLE: {p['title']}
SUBTITLE: {p['subtitle']}
AUTHOR: {B.AUTHOR}
FORMAT: Paperback, {p['trim'][0]/inch}×{p['trim'][1]/inch} in, {p['pages']} pages, B&W interior, {p['paper']} paper, matte, no bleed
PRICE: {price}
CATEGORIES: {p['categories']}
KEYWORDS: {kw}

DESCRIPTION:
{desc}""")


def main():
    B.register_fonts()
    items = all_products()

    # ── guards: exactly 7 keywords, unique across catalog ──
    seen, errors = {}, []
    for p in items:
        kw = [k.strip() for k in upgraded(p)[0].split(",")]
        if len(kw) != 7:
            errors.append(f"{p['key']}: {len(kw)} keywords")
        for w in kw:
            w = w.lower()
            if w in seen:
                errors.append(f"duplicate keyword '{w}' ({seen[w]} & {p['key']})")
            seen[w] = p["key"]
    assert not errors, f"keyword guard failed: {errors}"
    print(f"keyword guard: {len(items)} titles × 7 keywords, all unique — OK")

    # ── metadata ──
    for p in items:
        write_metadata(p)

    # ── CATALOG.csv ──
    rows = []
    for p in items:
        kw, price, _ = upgraded(p)
        ppi = B.WHITE_PPI if p["paper"] == "white" else B.CREAM_PPI
        spine = p["pages"] * ppi
        wrap_w = 2 * BLEED + 2 * (p["trim"][0] / inch) + spine
        wrap_h = 2 * BLEED + p["trim"][1] / inch
        rows.append({
            "n": p["n"], "batch": p["batch"], "title": p["title"], "subtitle": p["subtitle"],
            "pages": p["pages"], "trim": f"{p['trim'][0]/inch:.1f}x{p['trim'][1]/inch:.0f}",
            "paper": p["paper"], "spine_in": f"{spine:.4f}", "wrap_w": f"{wrap_w:.3f}",
            "wrap_h": f"{wrap_h:.3f}", "price": price,
            "interior_file": f"{p['dir']}/{p['dir']}_interior.pdf",
            "cover_file": f"{p['dir']}/{p['dir']}_cover_wrap.pdf",
            "marketing_image": f"{p['dir']}/{p['dir']}_cover.jpg",
            "keywords": " | ".join(k.strip() for k in kw.split(",")),
            "categories": p["categories"], "series": SERIES[p["key"]],
        })
    with open(ROOT / "CATALOG.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"wrote CATALOG.csv ({len(rows)} rows)")

    # ── LOOKBOOK.pdf ──
    W, H = 6 * inch, 9 * inch
    c = canvas.Canvas(str(ROOT / "LOOKBOOK.pdf"), pagesize=(W, H))
    c.setTitle("Quiet Mind Press — Catalog Lookbook")
    from art_kit import eyebrow, display, ornament_rule
    eyebrow(c, W/2, H*0.62, "QUIET MIND PRESS")
    display(c, W/2, H*0.56, "The Catalog", size=30)
    display(c, W/2, H*0.50, "18 paperbacks · 2 lines · 2026", size=11, color=B.MUTED)
    ornament_rule(c, W/2-50, W/2+50, H*0.46)
    B.draw_paragraph(c, "Core Line (B3): three journals and six coloring books. "
                     "Rising Niches (B4): five specialist journals and four fine-line titles. "
                     "Every interior is validated (page count, trim, embedded fonts, blank backs); "
                     "every wrap is spine-math exact with barcode reserve.",
                     W/2, H*0.40, "Inter-Light", 8.5, W-1.2*inch, 13, B.MUTED, align="center")
    c.showPage()
    for p in items:
        kw, price, _ = upgraded(p)
        img = Image.open(p["release"] / p["dir"] / f"{p['dir']}_cover.jpg")
        img.thumbnail((600, 900))
        tpath = Path("/tmp") / f"thumb_{p['dir']}.jpg"
        img.convert("RGB").save(tpath, "JPEG", quality=82)
        tw, th = 2.1 * inch, 3.15 * inch
        c.drawImage(str(tpath), (W - tw) / 2, H - th - 0.55 * inch, tw, th, mask="auto")
        y = H - th - 0.85 * inch
        eyebrow(c, W/2, y, f"{SERIES[p['key']]} · {p['n']:02d}", size=6); y -= 15
        display(c, W/2, y, p["title"], size=15); y -= 14
        display(c, W/2, y, p["subtitle"], size=8, color=B.MUTED); y -= 16
        ppi = B.WHITE_PPI if p["paper"] == "white" else B.CREAM_PPI
        spine = p["pages"] * ppi
        display(c, W/2, y, f"{p['pages']} pages · {p['trim'][0]/inch:.1f}×{p['trim'][1]/inch:.0f} in · "
                           f"{p['paper']} paper · spine {spine:.3f} in", size=7.5, color=B.SOFT); y -= 12
        display(c, W/2, y, price + "  ·  matte · no bleed · B&W interior", size=7.5, color=B.SOFT); y -= 16
        B.draw_paragraph(c, "Keywords: " + ", ".join(k.strip() for k in kw.split(",")),
                         W/2, y, "Inter-Light", 6, W - 0.7 * inch, 8, B.SOFT, align="center")
        c.showPage()
    c.save()
    print("wrote LOOKBOOK.pdf (19 pages)")

    # ── 00_START_HERE.md ──
    lines = ["# Quiet Mind Press — start here", "",
             f"18 paperbacks, all validated and upload-ready. Built {B.YEAR} by the in-repo engines.", "",
             "## Format inventory (per title)", "",
             "| File | Purpose | In repo |", "|---|---|---|",
             "| `<dir>/<dir>_interior.pdf` | KDP interior upload | 18/18 |",
             "| `<dir>/<dir>_cover_wrap.pdf` | KDP cover upload (spine-exact, barcode reserved) | 18/18 |",
             "| `<dir>/<dir>_cover.jpg` | marketing image (1800×2700) for stores/social | 18/18 |",
             "| `<dir>/metadata.txt` | paste-ready listing: keywords, categories, description, price | 18/18 |",
             "| `CATALOG.csv` | whole catalog, one row per title | 1 |",
             "| `LOOKBOOK.pdf` | visual catalog with specs | 1 |",
             "| zips | on demand — `python make_zips.py all` | generated |", "",
             "## Upload settings (all titles)", "",
             "- Paperback · B&W interior · **no bleed** · matte cover · expanded distribution ON",
             "- Paper: cream (journals) / white (coloring + grid trackers) — per `CATALOG.csv`",
             "- Fonts embedded in every interior; validators: `python validate_nine.py` / `validate_batch4.py`", "",
             "## Staging plan (protects account health)", "",
             "1. Days 1–3: Core Line journals (dump, parallel, night) + Settle",
             "2. Days 4–6: Rising Niche journals (middle, dopamine, slow, soft)",
             "3. Days 7–10: coloring line B3 (firststroke → architect)",
             "4. Days 11–14: fine-line B4 (cozy, botanical, celestial, tidal)", "",
             "## Pricing", "",
             "See CATALOG.csv. Journal premiums are backed by page depth + architecture;",
             "pocket/impulse formats sit at $9.99. Reprice any time — it is listing-side only.", "",
             "## Rebuild after changes", "",
             "```",
             "python build_nine_products.py      # batch 3",
             "python build_batch4.py             # batch 4",
             "python gen_catalog.py              # ALWAYS last: metadata + CATALOG + LOOKBOOK",
             "python make_zips.py all            # optional upload zips",
             "```", ""]
    (ROOT / "00_START_HERE.md").write_text("\n".join(lines))
    print("wrote 00_START_HERE.md")


if __name__ == "__main__":
    main()
