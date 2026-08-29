#!/usr/bin/env python3
"""Regenerate listing-side files for all 18 titles + catalog formats.

Outputs:
  releaseN/<dir>/metadata.txt         paste-ready KDP listing
  releaseN/<dir>/listing_*.jpg        7 Amazon images (cover + interiors + callout + series)
  CATALOG.csv
  LOOKBOOK.pdf
  00_START_HERE.md
  MARKETING.md

Run AFTER any interior/cover rebuild:
    python gen_catalog.py
"""
from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

import build_nine_products as B
import build_batch4 as B4
import niche_upgrades as U

ROOT = Path(__file__).resolve().parent
BLEED = 0.125
COLOR_KEYS = [k for k, v in U.SERIES.items() if v == "Quiet Mind Color"]
JOURNAL_KEYS = [k for k, v in U.SERIES.items() if v == "Quiet Mind Journals"]


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


def listing(p):
    key = p["key"]
    return {
        "title": U.TITLES[key],
        "cover_title": p["title"],
        "subtitle": U.SUBTITLES[key],
        "keywords": U.KEYWORDS[key],
        "price": U.PRICES.get(key) or U.cap_price(p["price"]),
        "categories": U.CATEGORIES[key],
        "series": U.SERIES[key],
        "difficulty": U.DIFFICULTY.get(key),
        "hook": U.HOOKS[key],
        "desc": p["desc"] + U.DESC_APPEND.get(key, ""),
        "stack": U.JOURNAL_STACKS.get(key, ""),
    }


def ladder_line(key):
    keys = [k for k, _ in U.LADDER]
    if key not in keys:
        return ""
    i = keys.index(key)
    names = dict(U.LADDER)
    prev_ = names[keys[i - 1]] if i else None
    next_ = names[keys[i + 1]] if i < len(keys) - 1 else None
    bits = [f"Quiet Mind Color ladder: {U.DIFFICULTY.get(key)}."]
    if prev_:
        bits.append(f"Too hard? Try {prev_}.")
    if next_:
        bits.append(f"Too easy? Try {next_}.")
    return " ".join(bits)


def html_desc(p, L):
    key = p["key"]
    bullets = []
    if L["difficulty"]:
        bullets.append(f"Difficulty: {L['difficulty']} · single-sided pages")
        bullets.append("Quiet Mind Color — interiors first, then the cover")
    else:
        bullets.append("Undated — start any day")
        if L["stack"]:
            bullets.append(L["stack"])
    bullets.append(
        f"{p['pages']} pages · {p['trim'][0]/inch:g}×{p['trim'][1]/inch:g} in · "
        f"{p['paper']} paper · black & white · bleed OFF · matte"
    )
    extra = ladder_line(key)
    li = "".join(f"<li>{b}</li>" for b in bullets)
    parts = [
        f"<p><b>{L['title']}</b> — {L['subtitle']}</p>",
        f"<p>{L['hook']}</p>",
        f"<p><b>Inside</b></p><ul>{li}</ul>",
        f"<p>{L['desc']}</p>",
    ]
    if extra:
        parts.append(f"<p><i>{extra}</i></p>")
    parts.append(
        "<p><i>Personal use. Not medical advice, not a treatment protocol, "
        "not affiliated with any challenge brand or manufacturer.</i></p>"
    )
    return "\n".join(parts)


def write_metadata(p, L):
    key = p["key"]
    extra = ladder_line(key)
    images = [
        f"{p['dir']}_cover.jpg  (1 — main)",
        "listing_02_interior.jpg",
        "listing_03_interior.jpg",
        "listing_04_interior.jpg",
        "listing_05_interior.jpg",
        "listing_06_callout.jpg",
        "listing_07_series.jpg",
    ]
    img_block = "\n".join(f"  {i}. {n}" for i, n in enumerate(images, 1))
    B.write_text(
        p["release"] / p["dir"] / "metadata.txt",
        f"""KDP LISTING — {p['n']:02d}  {p['dir']}
================================
AMAZON TITLE (≤200) — paste this, not the short cover word
{L['title']}

SUBTITLE
{L['subtitle']}

COVER TITLE (already printed; do not change the PDF)
{L['cover_title']}

AUTHOR / IMPRINT
{B.AUTHOR}

SERIES (create these two series on KDP — do not mix)
{L['series']}

LANGUAGE
English

INTERIOR
Black & white  |  Bleed: OFF  |  Paper: {p['paper']}  |  Cover: matte

TRIM
{p['trim'][0]/inch:g}\" × {p['trim'][1]/inch:g}\"

PAGE COUNT
{p['pages']}

COVER FILE
{p['dir']}_cover_wrap.pdf

INTERIOR FILE
{p['dir']}_interior.pdf

SEVEN LISTING IMAGES (Amazon order)
{img_block}

CATEGORIES
{L['categories']}

SEVEN BACKEND KEYWORDS
{chr(10).join(f'  {i}. {k.strip()}' for i, k in enumerate(L['keywords'].split(','), 1))}

SUGGESTED PRICE (US)
{L['price']}

DIFFICULTY / LADDER
{L['difficulty'] or 'n/a (journal)'}
{extra or L['stack']}

DESCRIPTION (plain)
-------------------
{L['title']}
{L['subtitle']}

{L['hook']}

{L['desc']}
{extra}

Trim: {p['trim'][0]/inch:g} × {p['trim'][1]/inch:g} in
Pages: {p['pages']}
Paper: {p['paper']}  ·  B&W  ·  bleed OFF  ·  matte
Price: {L['price']}
Series: {L['series']}

Personal use. Not medical advice. Not a treatment protocol.

DESCRIPTION (HTML paste)
------------------------
{html_desc(p, L)}
""",
    )


def font(size, bold=False):
    for path in (
        str(ROOT / "fonts" / ("Inter-SemiBold.ttf" if bold else "Inter-Regular.ttf")),
        str(ROOT / "fonts" / "Inter-Medium.ttf"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrapped(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def render_interiors(p, dest: Path):
    import pymupdf

    pdf = p["release"] / p["dir"] / f"{p['dir']}_interior.pdf"
    doc = pymupdf.open(pdf)
    n = doc.page_count
    # skip front matter; coloring books have blank backs so prefer odd 1-index pages
    if p["key"] in COLOR_KEYS:
        candidates = [i for i in range(2, n) if i % 2 == 0]  # 0-index even = 1-index odd designs
    else:
        candidates = list(range(4, n - 2, max(1, (n - 8) // 5)))
    picks = []
    for i in candidates:
        if len(picks) >= 4:
            break
        picks.append(i)
    while len(picks) < 4 and picks:
        picks.append(picks[-1])
    out = []
    for idx, pi in enumerate(picks[:4], start=2):
        page = doc[min(pi, n - 1)]
        pix = page.get_pixmap(matrix=pymupdf.Matrix(1.35, 1.35), alpha=False)
        path = dest / f"listing_{idx:02d}_interior.jpg"
        pix.save(str(path))
        # shrink if huge
        im = Image.open(path)
        im.thumbnail((1400, 2000))
        im.convert("RGB").save(path, "JPEG", quality=82)
        out.append(path)
    doc.close()
    return out


def make_callout(p, L, dest: Path):
    W, H = 1400, 1800
    bg = (250, 247, 241) if p["paper"] == "cream" else (252, 252, 252)
    ink, muted = (28, 28, 26), (110, 108, 102)
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    d.rectangle([48, 48, W - 48, H - 48], outline=ink, width=2)
    y = 120
    f_k = font(22)
    f_t = font(48, bold=True)
    f_b = font(28)
    f_s = font(24)
    series = L["series"].upper()
    d.text((W / 2, y), series, fill=muted, font=f_k, anchor="mt")
    y += 70
    for line in wrapped(d, L["cover_title"], f_t, W - 180):
        d.text((W / 2, y), line, fill=ink, font=f_t, anchor="mt")
        y += 58
    y += 20
    specs = [
        f"{p['pages']} pages",
        f"{p['trim'][0]/inch:g} × {p['trim'][1]/inch:g} in",
        f"{p['paper'].title()} paper · B&W · bleed OFF",
        f"Matte cover · {L['price']}",
    ]
    if L["difficulty"]:
        specs.insert(0, f"Difficulty: {L['difficulty']}")
        specs.append("Single-sided pages")
    else:
        specs.append("Undated journal")
    for s in specs:
        d.text((W / 2, y), s, fill=ink, font=f_b, anchor="mt")
        y += 48
    y += 30
    extra = ladder_line(p["key"]) or L["stack"]
    if extra:
        for line in wrapped(d, extra, f_s, W - 200):
            d.text((W / 2, y), line, fill=muted, font=f_s, anchor="mt")
            y += 36
    d.text((W / 2, H - 110), "Quiet Mind Press", fill=muted, font=f_k, anchor="mt")
    path = dest / "listing_06_callout.jpg"
    im.save(path, "JPEG", quality=85)
    return path


def make_series_cards():
    """Two shared series images reused as listing_07."""
    out = {}
    for series, keys, subtitle in (
        (
            "Quiet Mind Journals",
            JOURNAL_KEYS,
            "Eight undated journals. Same imprint. Do not mix with coloring.",
        ),
        (
            "Quiet Mind Color",
            COLOR_KEYS,
            "Beginner → advanced ladder. Single-sided. 8.5 × 11.",
        ),
    ):
        W, H = 1400, 1800
        im = Image.new("RGB", (W, H), (250, 247, 241))
        d = ImageDraw.Draw(im)
        d.rectangle([48, 48, W - 48, H - 48], outline=(28, 28, 26), width=2)
        f_k, f_t, f_b, f_s = font(22), font(44, bold=True), font(28), font(22)
        d.text((W / 2, 120), "QUIET MIND PRESS", fill=(110, 108, 102), font=f_k, anchor="mt")
        d.text((W / 2, 180), series, fill=(28, 28, 26), font=f_t, anchor="mt")
        y = 260
        for line in wrapped(d, subtitle, f_s, W - 200):
            d.text((W / 2, y), line, fill=(110, 108, 102), font=f_s, anchor="mt")
            y += 32
        y += 24
        if series.endswith("Color"):
            rows = U.LADDER
            d.text((W / 2, y), "If this felt too easy, go down. Too hard, go up.", fill=(28, 28, 26), font=f_s, anchor="mt")
            y += 50
            for k, name in rows:
                diff = U.DIFFICULTY[k]
                d.text((160, y), name, fill=(28, 28, 26), font=f_b, anchor="lt")
                d.text((W - 160, y), diff, fill=(110, 108, 102), font=f_s, anchor="rt")
                y += 42
        else:
            names = [
                ("dump", "The 5-Minute Dump — ADHD micro-journal"),
                ("dopamine", "The Dopamine Menu — stimulation orders"),
                ("night", "The Night Pages — 3 a.m. pocket"),
                ("settle", "Settle — body tracking, no protocol"),
                ("middle", "The Middle Season — perimenopause"),
                ("parallel", "Parallel Lives — split-page therapy"),
                ("slow", "The Slow Page — four seasons"),
                ("soft", "The 75 Soft Journal — gentler 75 days"),
            ]
            for k, label in names:
                d.text((W / 2, y), label, fill=(28, 28, 26), font=f_b, anchor="mt")
                y += 48
            y += 20
            d.text((W / 2, y), "Launch ads first: Dopamine Menu, 75 Soft,", fill=(110, 108, 102), font=f_s, anchor="mt")
            y += 32
            d.text((W / 2, y), "Middle Season, Cozy Corners (Color).", fill=(110, 108, 102), font=f_s, anchor="mt")
        path = Path("/tmp") / ("_series_journals.jpg" if "Journals" in series else "_series_color.jpg")
        im.save(path, "JPEG", quality=85)
        out[series] = path
    return out


def listing_images(p, L, series_card: Path):
    dest = p["release"] / p["dir"]
    render_interiors(p, dest)
    make_callout(p, L, dest)
    (dest / "listing_07_series.jpg").write_bytes(series_card.read_bytes())
    # listing_01 is the existing cover.jpg — documented, not duplicated


def keyword_guard(items):
    seen, errors = {}, []
    for p in items:
        L = listing(p)
        kw = [k.strip() for k in L["keywords"].split(",")]
        if len(kw) != 7:
            errors.append(f"{p['key']}: {len(kw)} keywords")
        for w in kw:
            wl = w.lower()
            if wl in seen:
                errors.append(f"duplicate keyword '{w}' ({seen[wl]} & {p['key']})")
            seen[wl] = p["key"]
        blob = (L["keywords"] + " " + L["desc"] + " " + L["categories"]).lower()
        for bad in U.BANNED_FRAGMENTS:
            if bad in blob:
                errors.append(f"{p['key']} banned fragment: {bad}")
    assert not errors, f"keyword guard failed: {errors}"
    print(f"keyword guard: {len(items)} titles × 7 keywords, all unique — OK")


def write_marketing(items):
    lines = [
        "# Quiet Mind Press — how to market this catalog",
        "",
        "Two Amazon **series**. Create both. Do not mix SKUs.",
        "",
        "1. **Quiet Mind Journals** — dump, parallel, night, settle, middle, dopamine, slow, soft",
        "2. **Quiet Mind Color** — firststroke → garden → cozy → woodland → mosaic → botanical → tidal → celestial → fractal → architect",
        "",
        "## Launch ads only on four titles",
        "",
        "| Key | Amazon title | Why |",
        "|---|---|---|",
        "| dopamine | The Dopamine Menu | TikTok search term, ADHD |",
        "| soft | The 75 Soft Journal | January + anti-grind fitness |",
        "| middle | The Middle Season: Perimenopause… | high-intent, title now searchable |",
        "| cozy | Cozy Corners: Cozy Spaces… | Pinterest / cottagecore coloring |",
        "",
        "Everything else rides also-bought and the color ladder. Do not ads-blast 18.",
        "",
        "## Amazon image order (7)",
        "",
        "1. `*_cover.jpg` (main)",
        "2–5. `listing_02`–`05` interior spreads (coloring: designs, not blank backs)",
        "6. `listing_06_callout.jpg` — trim, paper, difficulty, price",
        "7. `listing_07_series.jpg` — journal stack or color ladder",
        "",
        "Coloring buyers decide from interiors. If you only upload the cover, the book dies.",
        "",
        "## Title rule",
        "",
        "Paste **AMAZON TITLE** from `metadata.txt`, not the short word on the cover.",
        "`Settle` on the cover is fine. `Settle: A Somatic Journal for a Wired Nervous System` is the listing.",
        "",
        "## Claims we stripped",
        "",
        "- No vagus-nerve stimulation, no polyvagal *exercises*",
        "- No Sleep Disorders / ADHD-as-disease browse nodes",
        "- No “elderly coloring book”",
        "- No 75 Hard in copy or ads",
        "- 75 Soft subtitle stays “gentler 75-day”; do not bid on 75 Hard",
        "",
        "## Channels",
        "",
        "| Title | Channel |",
        "|---|---|",
        "| Dopamine Menu, 5-Minute Dump | TikTok ADHD, r/adhdwomen |",
        "| 75 Soft | TikTok 75 Soft. Launch January. |",
        "| Middle Season | Midlife IG / peri Facebook. Mother’s Day. |",
        "| Night Pages, Settle | Insomnia/anxiety TikTok — tracking language only |",
        "| Slow Page, Cozy Corners | Pinterest hygge / cottagecore. Q4. |",
        "| All coloring | Pinterest first, then Facebook coloring groups. UGC of finished pages. |",
        "",
        "Expanded distribution: OFF (IngramSpark in Wave 2 — PLATFORM_DECISIONS.md).",
        "",
    ]
    (ROOT / "MARKETING.md").write_text("\n".join(lines) + "\n")
    print("wrote MARKETING.md")


def main():
    B.register_fonts()
    items = all_products()
    keyword_guard(items)

    series_cards = make_series_cards()
    for p in items:
        L = listing(p)
        write_metadata(p, L)
        listing_images(p, L, series_cards[L["series"]])
        print(f"   images {p['dir']}")

    rows = []
    for p in items:
        L = listing(p)
        ppi = B.WHITE_PPI if p["paper"] == "white" else B.CREAM_PPI
        spine = p["pages"] * ppi
        wrap_w = 2 * BLEED + 2 * (p["trim"][0] / inch) + spine
        wrap_h = 2 * BLEED + p["trim"][1] / inch
        rows.append(
            {
                "n": p["n"],
                "batch": p["batch"],
                "amazon_title": L["title"],
                "cover_title": L["cover_title"],
                "subtitle": L["subtitle"],
                "pages": p["pages"],
                "trim": f"{p['trim'][0]/inch:g}x{p['trim'][1]/inch:g}",
                "paper": p["paper"],
                "spine_in": f"{spine:.4f}",
                "wrap_w": f"{wrap_w:.3f}",
                "wrap_h": f"{wrap_h:.3f}",
                "price": L["price"],
                "interior_file": f"{p['dir']}/{p['dir']}_interior.pdf",
                "cover_file": f"{p['dir']}/{p['dir']}_cover_wrap.pdf",
                "marketing_image": f"{p['dir']}/{p['dir']}_cover.jpg",
                "keywords": " | ".join(k.strip() for k in L["keywords"].split(",")),
                "categories": L["categories"],
                "series": L["series"],
                "difficulty": L["difficulty"] or "",
            }
        )
    with open(ROOT / "CATALOG.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote CATALOG.csv ({len(rows)} rows)")

    # LOOKBOOK
    W, H = 6 * inch, 9 * inch
    c = canvas.Canvas(str(ROOT / "LOOKBOOK.pdf"), pagesize=(W, H))
    c.setTitle("Quiet Mind Press — Catalog Lookbook")
    from art_kit import eyebrow, display, ornament_rule

    eyebrow(c, W / 2, H * 0.62, "QUIET MIND PRESS")
    display(c, W / 2, H * 0.56, "The Catalog", size=30)
    display(c, W / 2, H * 0.50, "18 paperbacks · 2 series · 2026", size=11, color=B.MUTED)
    ornament_rule(c, W / 2 - 50, W / 2 + 50, H * 0.46)
    B.draw_paragraph(
        c,
        "Quiet Mind Journals (8) and Quiet Mind Color (10). "
        "Amazon titles carry the search phrase; covers keep the short brand name. "
        "Color ladder is on every coloring listing. Ads: Dopamine Menu, 75 Soft, "
        "Middle Season, Cozy Corners only.",
        W / 2,
        H * 0.40,
        "Inter-Light",
        8.5,
        W - 1.2 * inch,
        13,
        B.MUTED,
        align="center",
    )
    c.showPage()
    for p in items:
        L = listing(p)
        img = Image.open(p["release"] / p["dir"] / f"{p['dir']}_cover.jpg")
        img.thumbnail((600, 900))
        tpath = Path("/tmp") / f"thumb_{p['dir']}.jpg"
        img.convert("RGB").save(tpath, "JPEG", quality=82)
        tw, th = 2.1 * inch, 3.15 * inch
        c.drawImage(str(tpath), (W - tw) / 2, H - th - 0.55 * inch, tw, th, mask="auto")
        y = H - th - 0.85 * inch
        eyebrow(c, W / 2, y, f"{L['series']} · {p['n']:02d}", size=6)
        y -= 15
        display(c, W / 2, y, L["cover_title"], size=15)
        y -= 14
        display(c, W / 2, y, L["subtitle"][:62], size=8, color=B.MUTED)
        y -= 16
        ppi = B.WHITE_PPI if p["paper"] == "white" else B.CREAM_PPI
        spine = p["pages"] * ppi
        display(
            c,
            W / 2,
            y,
            f"{p['pages']} pages · {p['trim'][0]/inch:g}×{p['trim'][1]/inch:g} in · "
            f"{p['paper']} paper · spine {spine:.3f} in",
            size=7.5,
            color=B.SOFT,
        )
        y -= 12
        display(
            c,
            W / 2,
            y,
            L["price"] + "  ·  matte · no bleed · B&W interior",
            size=7.5,
            color=B.SOFT,
        )
        y -= 14
        if L["difficulty"]:
            display(c, W / 2, y, "Difficulty: " + L["difficulty"], size=7.5, color=B.SOFT)
            y -= 16
        B.draw_paragraph(
            c,
            "Amazon title: " + L["title"],
            W / 2,
            y,
            "Inter-Light",
            6.5,
            W - 0.7 * inch,
            9,
            B.SOFT,
            align="center",
        )
        c.showPage()
    c.save()
    print("wrote LOOKBOOK.pdf")

    write_marketing(items)

    start = f"""# Quiet Mind Press — start here

SELLING: read PLATFORM_DECISIONS.md (what lists where) then PLATFORM_PLAYBOOK.md (how) — every sales platform, zero-upfront-fee verified 2026-08-28, exact file packages per site.

18 paperbacks on branch `ADHD-Journals`. Two Amazon series. Built {B.YEAR}.

**Paste the AMAZON TITLE from each `metadata.txt`, not the short word on the cover.**

## Two series (create both on KDP)

| Series | Titles |
|---|---|
| Quiet Mind Journals | 5-Minute Dump, Parallel Lives, Night Pages, Settle, Middle Season, Dopamine Menu, Slow Page, 75 Soft |
| Quiet Mind Color | First Strokes → Easy Garden → Cozy Corners → Woodland → Mosaic → Botanical Ink → Tidal Ink → Celestial Atlas → Fractal Dreams → Architectural Visions |

## Format inventory (per title)

| File | Purpose |
|---|---|
| `*_interior.pdf` | KDP interior |
| `*_cover_wrap.pdf` | KDP cover (full wrap) |
| `*_cover.jpg` | listing image 1 |
| `listing_02`–`05_interior.jpg` | listing images 2–5 (interiors first for coloring) |
| `listing_06_callout.jpg` | trim / paper / difficulty / price |
| `listing_07_series.jpg` | series card (journals stack or color ladder) |
| `metadata.txt` | title, HTML description, 7 keywords, BISAC, price |
| `CATALOG.csv` / `LOOKBOOK.pdf` / `MARKETING.md` | catalog + ads plan |

## Upload settings

Paperback · B&W · **bleed OFF** · matte · expanded distribution OFF  
Paper: cream (journals) / white (coloring + Middle Season grids)

## Staging (account health)

1. **Ads launch (week 1):** Dopamine Menu, 75 Soft, Middle Season, Cozy Corners
2. Week 2: Dump, Night Pages, Settle
3. Week 3: remaining journals
4. Week 4+: color ladder in order, interiors on the listing before the cover

## Pricing

**Every KDP title is $9.99 US** (catalog-wide cap, 60% royalty floor). Other stores: `MARKETS/PLAYBOOK.md`. Do not put B&N prices on KDP.

## Rebuild

```
python build_nine_products.py
python build_batch4.py
python gen_catalog.py          # ALWAYS last
python make_zips.py all        # optional
```

Do not merge this branch with `Range-Band` (Range Band Press, the GLP-1 36).
"""
    (ROOT / "00_START_HERE.md").write_text(start)
    print("wrote 00_START_HERE.md")


if __name__ == "__main__":
    main()
