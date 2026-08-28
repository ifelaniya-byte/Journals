"""KDP paperback wrap covers + front-only PDFs. Range Band Press."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import Color
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

from .brand import (
    BACK_BLURB,
    FOOT,
    HOUSE,
    IMPRINT,
    IMPRINT_TRACKED,
    accent_rgb,
    draw_range_band,
    mix,
    spaced,
)
from .kit import register_fonts
from .kit import wrap as wrap_text
from .titles import BLEED, TITLES, wrap_size
from .titles_vol2 import TITLES_VOL2

OUTPUT = Path(__file__).resolve().parent.parent / "output"


def C(rgb) -> Color:
    return Color(*rgb)


def _title_block(c, cx, y_top, title, ink, max_w, size=28):
    lines = title.split("\n")
    s = size
    while any(pdfmetrics.stringWidth(ln, "Cormorant-Semi", s) > max_w for ln in lines) and s > 16:
        s -= 1
    y = y_top
    c.setFillColor(ink)
    for ln in lines:
        c.setFont("Cormorant-Semi", s)
        c.drawCentredString(cx, y, ln)
        y -= s * 1.08
    return y, s


def draw_front_panel(c, x, y, w, h, t, ink, bg, panel, dark: bool):
    accent = C(accent_rgb(t))
    # living strip — energy without shouting
    bar_h = min(0.16 * inch, h * 0.028)
    c.setFillColor(accent)
    c.rect(x, y + h - bar_h, w, bar_h, stroke=0, fill=1)

    inset = 0.28 * inch
    c.setStrokeColor(ink)
    c.setLineWidth(0.9)
    c.rect(x + inset, y + inset, w - 2 * inset, h - 2 * inset - bar_h * 0.15, stroke=1, fill=0)
    c.setLineWidth(0.35)
    c.rect(x + inset + 5, y + inset + 5, w - 2 * inset - 10, h - 2 * inset - 10 - bar_h * 0.15, stroke=1, fill=0)

    cx = x + w / 2
    top = y + h - bar_h - 0.42 * inch
    spaced(c, IMPRINT_TRACKED, cx, top, "Sans", 6.6, 1.7, "center", ink)
    spaced(c, t["series"], cx, top - 0.22 * inch, "Sans", 6.4, 1.35, "center", ink)
    draw_range_band(c, cx, top - 0.46 * inch, min(118, w * 0.42), ink, accent)

    y_title = y + h * 0.56
    y_after, _ = _title_block(c, cx, y_title, t["cover_title"], ink, w - 1.15 * inch, size=30)

    y_after -= 8
    draw_range_band(c, cx, y_after, min(88, w * 0.32), ink, accent, tick=5.0, band_h=4.8, weight=1.1)

    sub_y = y_after - 26
    c.setFillColor(ink)
    for ln in t["subtitle"].split("\n"):
        c.setFont("Cormorant-Italic", 11)
        c.drawCentredString(cx, sub_y, ln)
        sub_y -= 15

    c.setFillColor(ink)
    c.setFont("Cormorant-Italic", 10)
    c.drawCentredString(cx, y + 0.92 * inch, HOUSE)
    c.setFont("Sans", 7.6)
    c.drawCentredString(cx, y + 0.70 * inch, t["tagline"])
    c.setFont("Sans", 6.6)
    c.drawCentredString(cx, y + 0.50 * inch, FOOT)


def draw_back_panel(c, x, y, w, h, t, ink, bg, panel, dark: bool, spine_w: float):
    accent = C(accent_rgb(t))
    bar_h = min(0.16 * inch, h * 0.028)
    c.setFillColor(accent)
    c.rect(x, y + h - bar_h, w, bar_h, stroke=0, fill=1)

    inset = 0.28 * inch
    c.setStrokeColor(ink)
    c.setLineWidth(0.9)
    c.rect(x + inset, y + inset, w - 2 * inset, h - 2 * inset - bar_h * 0.15, stroke=1, fill=0)

    left = x + 0.48 * inch
    right = x + w - 0.48 * inch
    maxw = right - left

    spaced(c, IMPRINT_TRACKED, left, y + h - bar_h - 0.38 * inch, "Sans", 6.4, 1.4, "left", ink)
    draw_range_band(c, left + 52, y + h - bar_h - 0.62 * inch, 104, ink, accent, tick=5.2, band_h=5.0, weight=1.15)

    c.setFillColor(ink)
    c.setFont("Cormorant-Semi", 16)
    c.drawString(left, y + h - bar_h - 0.98 * inch, t["cover_title_one"])

    yy = y + h - bar_h - 1.28 * inch
    c.setFont("Sans", 8.4)
    for ln in wrap_text(BACK_BLURB, "Sans", 8.4, maxw):
        c.drawString(left, yy, ln)
        yy -= 12

    yy -= 8
    c.setFont("Cormorant-Italic", 10)
    c.drawString(left, yy, HOUSE)
    yy -= 16
    c.setFont("Sans-Semi", 7.5)
    c.drawString(left, yy, "INSIDE")
    yy -= 16
    for b in t["bullets"]:
        c.setFillColor(ink)
        c.circle(left + 3, yy + 3, 1.4, stroke=0, fill=1)
        lines = wrap_text(b, "Sans", 8.2, maxw - 14)
        for ln in lines:
            c.setFont("Sans", 8.2)
            c.drawString(left + 12, yy, ln)
            yy -= 11.5
        yy -= 4

    bw, bh = 2.05 * inch, 1.25 * inch
    bx = x + w - 0.22 * inch - bw
    by = y + 0.22 * inch
    c.setFillColor(Color(1, 1, 1))
    c.setStrokeColor(ink)
    c.setLineWidth(0.3)
    c.rect(bx, by, bw, bh, stroke=1, fill=1)
    c.setFillColor(ink)
    c.setFont("Sans", 6)
    c.drawCentredString(bx + bw / 2, by + bh / 2 - 3, "KDP BARCODE")

    c.setFont("Sans", 6.5)
    c.drawString(left, y + 0.42 * inch, "Not affiliated with any medication manufacturer.")
    c.setFont("Sans-Semi", 6.5)
    c.drawString(left, y + 0.28 * inch, IMPRINT)


def draw_spine(c, x, y, w, h, t, ink, dark: bool):
    if t["pages"] < 79 or w < 0.06 * inch:
        return
    accent = C(accent_rgb(t))
    c.setFillColor(accent)
    c.rect(x, y, w, 0.14 * inch, stroke=0, fill=1)
    c.rect(x, y + h - 0.14 * inch, w, 0.14 * inch, stroke=0, fill=1)
    c.saveState()
    c.translate(x + w / 2, y + h / 2)
    c.rotate(90)
    draw_range_band(c, -h * 0.36, 0, 36, ink, accent, tick=3.2, band_h=3.4, weight=0.9)
    c.setFillColor(ink)
    label = t["spine"]
    size = 8
    while pdfmetrics.stringWidth(label, "Cormorant-Semi", size) > h * 0.48 and size > 6:
        size -= 0.3
    c.setFont("Cormorant-Semi", size)
    c.drawCentredString(0, -2.5, label)
    c.setFont("Sans", 5.6)
    c.drawCentredString(h * 0.36, -2, f"{t['n']}  ·  {IMPRINT}")
    c.restoreState()
    c.setStrokeColor(ink)
    c.setLineWidth(0.35)
    c.line(x, y + 0.2 * inch, x, y + h - 0.2 * inch)
    c.line(x + w, y + 0.2 * inch, x + w, y + h - 0.2 * inch)


def make_wrap(t: dict, dest: Path) -> Path:
    register_fonts()
    tw, th = t["trim"]
    width, height, sp = wrap_size(t["trim"], t["pages"])
    dest.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(dest), pagesize=(width * inch, height * inch))
    c.setTitle(t["kdp_title"] + " — print cover")
    c.setAuthor(IMPRINT)
    W, H = width * inch, height * inch
    ink = C(t["ink"])
    bg = C(mix(t["bg"], accent_rgb(t), 0.10 if not t["dark"] else 0.06))
    panel = C(t["panel"])
    c.setFillColor(bg)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    bleed = BLEED * inch
    tw_pt, th_pt = tw * inch, th * inch
    spine_w = sp * inch
    back_x = bleed
    back_y = bleed
    spine_x = bleed + tw_pt
    front_x = spine_x + spine_w
    front_y = bleed

    draw_back_panel(c, back_x, back_y, tw_pt, th_pt, t, ink, bg, panel, t["dark"], spine_w)
    draw_spine(c, spine_x, back_y, spine_w, th_pt, t, ink, t["dark"])
    draw_front_panel(c, front_x, front_y, tw_pt, th_pt, t, ink, bg, panel, t["dark"])
    c.save()
    return dest


def make_front(t: dict, dest: Path) -> Path:
    register_fonts()
    tw, th = t["trim"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(dest), pagesize=(tw * inch, th * inch))
    c.setTitle(t["kdp_title"])
    c.setAuthor(IMPRINT)
    ink = C(t["ink"])
    bg = C(mix(t["bg"], accent_rgb(t), 0.10 if not t["dark"] else 0.06))
    panel = C(t["panel"])
    c.setFillColor(bg)
    c.rect(0, 0, tw * inch, th * inch, stroke=0, fill=1)
    draw_front_panel(c, 0, 0, tw * inch, th * inch, t, ink, bg, panel, t["dark"])
    c.save()
    return dest


def generate_all_covers(out_dir: Path | None = None, titles=None):
    out_dir = out_dir or OUTPUT
    titles = titles if titles is not None else (TITLES + TITLES_VOL2)
    rows = []
    for t in titles:
        wrap_path = out_dir / f"{t['stem']}_COVER_WRAP.pdf"
        front_path = out_dir / f"{t['stem']}_COVER_FRONT.pdf"
        make_wrap(t, wrap_path)
        make_front(t, front_path)
        w, h, sp = wrap_size(t["trim"], t["pages"])
        rows.append((t["n"], wrap_path.name, f"{w:.3f}x{h:.3f}", f"{sp:.4f}"))
        print(f"  cover {t['n']}  wrap {w:.3f}×{h:.3f}in  spine {sp:.4f}in")
    return rows
