#!/usr/bin/env python3
"""Build the complete KDP kit: interiors, wrap covers, listings, lookbook, folder, zip."""

from __future__ import annotations

import csv
import shutil
import sys
import zipfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import Color
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from lib import algorithm as A  # noqa: E402
from lib.covers import generate_all_covers, make_front, make_wrap  # noqa: E402
from lib.kit import OUTPUT, register_fonts  # noqa: E402
from lib.titles import TITLES, spine_in, wrap_size  # noqa: E402
from lib.titles_vol2 import TITLES_VOL2  # noqa: E402

ALL_TITLES = TITLES + TITLES_VOL2
A.assert_unique()
for _t in ALL_TITLES:
    _t["keywords"] = A.KEYWORDS[_t["n"]]
    _t["hook"] = A.HOOKS[_t["n"]]
    _t["also"] = A.ALSO[_t["n"]]

KIT = Path("/home/user/KDP-Complete-Kit")


def html_desc(t: dict) -> str:
    bullets = "".join(f"<li>{b}</li>" for b in t["bullets"])
    also = "".join(f"<li>{x}</li>" for x in t.get("also") or [])
    hook = t.get("hook") or "A discreet, giftable, undated tracking journal."
    return f"""<p><b>{t["kdp_title"]}</b> — {t["kdp_subtitle"]}</p>
<p>{hook}</p>
<p>A discreet, giftable, <b>undated</b> tracking journal. Write what your own clinician already directed. This book does not diagnose, dose, or treat, and it is not affiliated with any medication manufacturer.</p>
<p><b>Inside</b></p>
<ul>{bullets}</ul>
<p><b>Also in this catalog</b></p>
<ul>{also}</ul>
<p>Trim {t["trim"][0]:g} × {t["trim"][1]:g} in · {t["pages"]} pages · black-and-white interior · white paper recommended · bleed OFF · <b>$9.99</b>.</p>
<p><i>Personal tracking / management tool only. Not medical advice. GLP-1 is the stem on the cover — no manufacturer brands in the title.</i></p>"""


def plain_desc(t: dict) -> str:
    hook = t.get("hook") or "A discreet, giftable, undated tracking journal."
    lines = [
        f"{t['kdp_title']}",
        t["kdp_subtitle"],
        "",
        hook,
        "",
        "A discreet, giftable, undated tracking journal. Fill in what your own clinician already directed. This book does not diagnose, dose, or treat, and it is not affiliated with any medication manufacturer.",
        "",
        "INSIDE",
    ]
    for b in t["bullets"]:
        lines.append(f"  • {b}")
    also = t.get("also") or []
    if also:
        lines += ["", "ALSO IN THIS CATALOG"]
        for x in also:
            lines.append(f"  • {x}")
    lines += [
        "",
        f"Trim: {t['trim'][0]:g} × {t['trim'][1]:g} in",
        f"Pages: {t['pages']}",
        "Interior: black & white / grayscale, no bleed, fonts embedded",
        "Paper: white (recommended for grids and stickers)",
        f"Suggested list price: ${t['price']:.2f}",
        "",
        "Personal tracking / management tool only. Not medical advice.",
    ]
    return "\n".join(lines)


def listing_txt(t: dict, wrap_w, wrap_h, spine) -> str:
    kw = "\n".join(f"  {i}. {k}" for i, k in enumerate(t["keywords"], 1))
    return f"""KDP LISTING — {t["n"]}
================================
TITLE (≤200 chars)
{t["kdp_title"]}

SUBTITLE
{t["kdp_subtitle"]}

AUTHOR / IMPRINT
Range Band Press

LANGUAGE
English

INTERIOR
Black & white  |  Bleed: OFF  |  Paper: white

TRIM
{t["trim"][0]:g}" × {t["trim"][1]:g}"

PAGE COUNT
{t["pages"]}

COVER FILE
{t["stem"]}_COVER_WRAP.pdf
  Full wrap size: {wrap_w:.3f}" × {wrap_h:.3f}"
  Spine: {spine:.4f}"  (white paper B&W, {t["pages"]} × 0.002252)
  Spine text: {"YES" if t["pages"] >= 79 else "NO — under 79 pages, KDP forbids spine text"}
  Barcode: white 2.05 × 1.25" reserved, back cover lower-right (near spine)

INTERIOR FILE
{t["file_interior"]}

CATEGORIES / BISAC
{t["bisac_names"][0]}  ({t["bisac"][0]})
{t["bisac_names"][1]}  ({t["bisac"][1]})

SEVEN BACKEND KEYWORDS
{kw}

SUGGESTED PRICE (US)
${t["price"]:.2f}

DESCRIPTION (plain)
-------------------
{plain_desc(t)}

DESCRIPTION (HTML paste)
------------------------
{html_desc(t)}
"""


def write_csv(path: Path):
    fields = [
        "n",
        "kdp_title",
        "kdp_subtitle",
        "pages",
        "trim",
        "spine_in",
        "wrap_w",
        "wrap_h",
        "price",
        "interior_file",
        "cover_file",
        "keywords",
        "bisac",
        "series",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for t in ALL_TITLES:
            ww, hh, sp = wrap_size(t["trim"], t["pages"])
            w.writerow(
                dict(
                    n=t["n"],
                    kdp_title=t["kdp_title"],
                    kdp_subtitle=t["kdp_subtitle"],
                    pages=t["pages"],
                    trim=f"{t['trim'][0]:g}x{t['trim'][1]:g}",
                    spine_in=f"{sp:.4f}",
                    wrap_w=f"{ww:.3f}",
                    wrap_h=f"{hh:.3f}",
                    price=f"{t['price']:.2f}",
                    interior_file=t["file_interior"],
                    cover_file=f"{t['stem']}_COVER_WRAP.pdf",
                    keywords=" | ".join(t["keywords"]),
                    bisac=" | ".join(t["bisac_names"]),
                    series=t["series"],
                )
            )


def lookbook(dest: Path, front_pngs: list[tuple[dict, Path]]):
    register_fonts()
    c = canvas.Canvas(str(dest), pagesize=(8.5 * inch, 11 * inch))
    INK = Color(0.12, 0.12, 0.12)
    MUTED = Color(0.45, 0.45, 0.45)

    def page_frame(title, sub=""):
        c.setFillColor(Color(1, 1, 1))
        c.rect(0, 0, 8.5 * inch, 11 * inch, stroke=0, fill=1)
        c.setFillColor(INK)
        c.setFont("Cormorant-Semi", 22)
        c.drawString(0.7 * inch, 10.2 * inch, title)
        if sub:
            c.setFont("Sans", 9)
            c.setFillColor(MUTED)
            c.drawString(0.7 * inch, 9.95 * inch, sub)
        c.setStrokeColor(Color(0.75, 0.75, 0.75))
        c.setLineWidth(0.5)
        c.line(0.7 * inch, 9.82 * inch, 7.8 * inch, 9.82 * inch)

    # title
    c.setFillColor(Color(0.14, 0.16, 0.15))
    c.rect(0, 0, 8.5 * inch, 11 * inch, stroke=0, fill=1)
    c.setFillColor(Color(0.93, 0.91, 0.86))
    c.setFont("Sans", 8)
    c.drawCentredString(4.25 * inch, 8.4 * inch, "R A N G E   B A N D   P R E S S")
    c.setFont("Cormorant-Semi", 32)
    c.drawCentredString(4.25 * inch, 7.6 * inch, "Thirty-Six Tracking Journals")
    c.setFont("Cormorant-Italic", 13)
    c.drawCentredString(4.25 * inch, 7.2 * inch, "Undated health logs — interiors, wraps, listing copy")
    c.setFont("Sans", 8)
    c.drawCentredString(4.25 * inch, 1.4 * inch, "GLP-1 Tracking  ·  Wellness Tracking  ·  Companions")
    c.drawCentredString(4.25 * inch, 1.15 * inch, "Undated  ·  Grayscale interiors  ·  Discreet giftable covers  ·  $9.99")
    c.showPage()

    page_frame("How to upload", "One title at a time. Interior PDF + wrap cover PDF.")
    steps = [
        "1.  Create a KDP paperback. Bleed OFF. Interior type: black & white. Paper: white.",
        "2.  Set trim to the size on the title's listing sheet (6×9, 5×8, or 8.5×11).",
        "3.  Upload the interior PDF. Confirm page count matches the listing sheet.",
        "4.  Upload the COVER WRAP PDF (not the front-only file). KDP will place the barcode",
        "    in the reserved white box on the back.",
        "5.  Paste title, subtitle, HTML description, and 7 keywords from listing.txt.",
        "6.  Pick two BISAC categories. Set US price to $9.99. Order a proof before ads.",
        "7.  Author / imprint: Range Band Press. Covers are blank on purpose.",
        "",
        "Do not merge cover + interior. KDP wants two files.",
        "Do not put Ozempic in your title unless you accept Amazon's brand-name filter;",
        "GLP-1 is the safer stem. Keep claims to tracking / management.",
        "07 Titration and 25 Shot-Day are 5×8 (KDP has no 4×6). 09 Calendar is 8.5×11.",
        "Spine text is omitted under 79 pages (KDP rule) — title 07.",
    ]
    y = 9.5 * inch
    c.setFillColor(INK)
    c.setFont("Sans", 10)
    for s in steps:
        c.drawString(0.75 * inch, y, s)
        y -= 16
    c.showPage()

    def grid(subset, heading):
        page_frame(heading)
        cols, rows = 3, 3
        gap_x, gap_y = 0.22 * inch, 0.38 * inch
        cell_w = (7.1 * inch - 2 * gap_x) / cols
        origin_x, origin_y = 0.7 * inch, 9.55 * inch
        for i, (t, png) in enumerate(subset):
            col, row = i % cols, i // cols
            # fit height into cell
            tw, th = t["trim"]
            scale = min((cell_w - 8) / (tw * inch), 2.35 * inch / (th * inch))
            dw, dh = tw * inch * scale, th * inch * scale
            x = origin_x + col * (cell_w + gap_x) + (cell_w - dw) / 2
            y = origin_y - (row + 1) * (2.55 * inch) + 8
            c.drawImage(str(png), x, y, dw, dh, preserveAspectRatio=True, mask="auto")
            c.setFillColor(INK)
            c.setFont("Sans-Semi", 6.5)
            c.drawCentredString(x + dw / 2, y - 11, f"{t['n']}  {t['cover_title_one'][:32]}")
        c.showPage()

    grid(front_pngs[:9], "Vol 1  ·  GLP-1 tracking series")
    grid(front_pngs[9:18], "Vol 1  ·  Wellness tracking series")
    grid(front_pngs[18:27], "Vol 2  ·  GLP-1 premium companions")
    grid(front_pngs[27:36], "Vol 2  ·  Wellness premium companions")

    for t, png in front_pngs:
        page_frame(f"{t['n']}   {t['kdp_title']}", t["kdp_subtitle"][:90])
        tw, th = t["trim"]
        scale = min(3.1 * inch / (tw * inch), 6.6 * inch / (th * inch))
        dw, dh = tw * inch * scale, th * inch * scale
        c.drawImage(str(png), 0.65 * inch, 9.55 * inch - dh, dw, dh, preserveAspectRatio=True, mask="auto")
        x = 4.05 * inch
        y = 9.4 * inch
        ww, hh, sp = wrap_size(t["trim"], t["pages"])
        meta = [
            ("Series", t["series"]),
            ("Trim", f"{t['trim'][0]:g} × {t['trim'][1]:g} in"),
            ("Pages", str(t["pages"])),
            ("Wrap cover", f"{ww:.3f} × {hh:.3f} in"),
            ("Spine", f"{sp:.4f} in" + ("  (no spine text)" if t["pages"] < 79 else "")),
            ("Price (US)", f"${t['price']:.2f}"),
            ("Interior", t["file_interior"]),
            ("Cover", f"{t['stem']}_COVER_WRAP.pdf"),
        ]
        c.setFillColor(INK)
        for lab, val in meta:
            c.setFont("Sans-Semi", 8)
            c.drawString(x, y, lab)
            c.setFont("Sans", 8)
            c.drawString(x + 1.15 * inch, y, val[:42])
            y -= 14
        y -= 8
        c.setFont("Sans-Semi", 8)
        c.drawString(x, y, "Keywords")
        y -= 13
        c.setFont("Sans", 8)
        for k in t["keywords"]:
            c.drawString(x, y, "·  " + k)
            y -= 12
        y -= 6
        c.setFont("Sans-Semi", 8)
        c.drawString(x, y, "Inside")
        y -= 13
        c.setFont("Sans", 8)
        for b in t["bullets"]:
            c.drawString(x, y, "·  " + b[:48])
            y -= 12
        c.showPage()

    c.save()


START_HERE = """# Range Band Press — 36 tracking journals

Undated GLP-1 and wellness logs. GitHub branch: `Range-Band`. Not Quiet Mind.

**Imprint on every KDP listing: Range Band Press.** Covers stay blank — type it in the author field.

**List price for every title: $9.99 US** (KDP 60% paperback royalty floor).

Read `CASHFLOW.md` first — waves, also-bought, what not to bid against Quiet Mind.
Read `SELLING_AND_VALUATION.md` for royalties, marketplaces, and the exact files to upload.
Read `PROOF_REPORT.md` for the verification that every listing is $9.99.

## Folder map

```
KDP-Complete-Kit/
  00_START_HERE.md          ← you are here
  CASHFLOW.md               ← rank loop, waves, also-bought, ads
  SELLING_AND_VALUATION.md  ← prices, royalties, where to sell, upload files
  PROOF_REPORT.md           ← verification of files, trims, pages, $9.99
  METADATA.csv              ← titles, trims, spines, keywords, prices
  LOOKBOOK.pdf              ← all 36 covers + upload specs
  _covers/                  ← every wrap + front PDF
  _interiors/               ← every interior PDF
  01_…/ through 36_…/       ← per-title pack (interior + wrap + listing)
```

Each numbered folder contains:

| File | Upload where |
|---|---|
| `*_interior.pdf` | KDP interior |
| `*_COVER_WRAP.pdf` | KDP cover (full wrap with spine + barcode box) |
| `*_COVER_FRONT.pdf` | Mockups / ads only — do **not** upload as the cover |
| `listing.txt` | Title, subtitle, HTML description, 7 keywords, BISAC, spine math |

## Upload recipe (every title)

1. Paperback · **Bleed OFF** · Interior **black & white** · Paper **white**
2. Trim = the listing sheet (almost all **6 × 9**; **07 and 25 are 5 × 8**; **09 is 8.5 × 11**)
3. Interior PDF, then wrap cover PDF
4. Paste listing copy. Set **$9.99**. Order a proof.

## What was deliberately not invented

- No publisher name on the cover (KDP author field: **Range Band Press**)
- No live QR URLs — dashed QR boxes are on titles 03, 09, 17 so you can paste your own
- No Ozempic-as-brand in titles (GLP-1 is the stem)
- No exercise videos, dosing schedules, or treatment claims
- 4 × 6 pocket is not a KDP trim; 07 and 25 ship as **5 × 8**

## Spine math

White B&W: `spine_in = pages × 0.002252`  
Wrap width = `0.125 + trim_w + spine + trim_w + 0.125`  
Wrap height = `0.125 + trim_h + 0.125`  
Spine text only if **≥ 79 pages** (07 is 78 — no spine type)

Re-generate from source: `python3 /home/user/kdp-journals/assemble_kit.py`
"""


def copy_into_kit():
    if KIT.exists():
        shutil.rmtree(KIT)
    KIT.mkdir(parents=True)
    interiors = KIT / "_interiors"
    covers = KIT / "_covers"
    interiors.mkdir()
    covers.mkdir()
    (KIT / "00_START_HERE.md").write_text(START_HERE, encoding="utf-8")
    write_csv(KIT / "METADATA.csv")

    for t in ALL_TITLES:
        folder = KIT / f"{t['n']}_{t['stem'][3:]}"
        folder.mkdir()
        src_int = OUTPUT / t["file_interior"]
        src_wrap = OUTPUT / f"{t['stem']}_COVER_WRAP.pdf"
        src_front = OUTPUT / f"{t['stem']}_COVER_FRONT.pdf"
        shutil.copy2(src_int, folder / f"{t['stem']}_interior.pdf")
        shutil.copy2(src_int, interiors / t["file_interior"])
        shutil.copy2(src_wrap, folder / src_wrap.name)
        shutil.copy2(src_wrap, covers / src_wrap.name)
        shutil.copy2(src_front, folder / src_front.name)
        shutil.copy2(src_front, covers / src_front.name)
        ww, hh, sp = wrap_size(t["trim"], t["pages"])
        (folder / "listing.txt").write_text(listing_txt(t, ww, hh, sp), encoding="utf-8")
    shutil.copy2(OUTPUT / "LOOKBOOK.pdf", KIT / "LOOKBOOK.pdf")
    shutil.copy2(ROOT / "README.md", KIT / "INTERIORS_README.md")
    cf = ROOT / "CASHFLOW.md"
    if cf.exists():
        shutil.copy2(cf, KIT / "CASHFLOW.md")


def zip_kit():
    zpath = Path("/home/user/KDP-Complete-Kit.zip")
    if zpath.exists():
        zpath.unlink()
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for p in KIT.rglob("*"):
            if p.is_file():
                z.write(p, p.relative_to(KIT.parent))
    return zpath


def main():
    print("1/4  Covers…")
    generate_all_covers(OUTPUT, ALL_TITLES)

    print("2/4  Front PNGs for lookbook…")
    import pymupdf

    png_dir = OUTPUT / "_cover_png"
    png_dir.mkdir(exist_ok=True)
    pairs = []
    for t in ALL_TITLES:
        front = OUTPUT / f"{t['stem']}_COVER_FRONT.pdf"
        doc = pymupdf.open(front)
        pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(1.6, 1.6), alpha=False)
        png = png_dir / f"{t['n']}.png"
        pix.save(str(png))
        doc.close()
        pairs.append((t, png))

    print("3/4  Lookbook…")
    lookbook(OUTPUT / "LOOKBOOK.pdf", pairs)

    print("4/4  Assemble folder + zip…")
    copy_into_kit()
    z = zip_kit()
    print("KIT", KIT)
    print("ZIP", z, f"{z.stat().st_size/1e6:.1f} MB")
    n = sum(1 for _ in KIT.rglob("*") if _.is_file())
    print("files", n)


if __name__ == "__main__":
    main()
