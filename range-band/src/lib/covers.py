"""KDP paperback wrap covers + front-only PDFs."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import Color
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

from .kit import FONT_DIR, register_fonts, sw, wrap
from .titles import BLEED, TITLES, wrap_size
from .titles_vol2 import TITLES_VOL2

OUTPUT = Path(__file__).resolve().parent.parent / "output"


def C(rgb) -> Color:
    return Color(*rgb)


def _diamond(c, cx, cy, s=5.5, color=None, sw=0.8):
    c.saveState()
    if color:
        c.setStrokeColor(color)
    c.setLineWidth(sw)
    c.translate(cx, cy)
    c.rotate(45)
    c.rect(-s / 2, -s / 2, s, s, stroke=1, fill=0)
    c.restoreState()


def _spaced(c, text, x, y, font, size, tracking, align, color):
    text = text.upper()
    widths = [pdfmetrics.stringWidth(ch, font, size) for ch in text]
    total = sum(widths) + tracking * max(len(text) - 1, 0)
    if align == "center":
        cursor = x - total / 2
    elif align == "right":
        cursor = x - total
    else:
        cursor = x
    c.setFillColor(color)
    c.setFont(font, size)
    for ch, w in zip(text, widths):
        c.drawString(cursor, y, ch)
        cursor += w + tracking
    return total


def _title_block(c, cx, y_top, title, ink, max_w, size=28):
    lines = title.split("\n")
    # if a line is too wide, shrink
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
    """Front cover live area origin at bottom-left of the FRONT PANEL (including bleed on right/top/bottom)."""
    # panel fill is already on the whole page; draw a double frame inset from bleed
    inset = 0.28 * inch
    c.setStrokeColor(ink)
    c.setLineWidth(0.9)
    c.rect(x + inset, y + inset, w - 2 * inset, h - 2 * inset, stroke=1, fill=0)
    c.setLineWidth(0.35)
    c.rect(x + inset + 5, y + inset + 5, w - 2 * inset - 10, h - 2 * inset - 10, stroke=1, fill=0)

    cx = x + w / 2
    # series
    _spaced(c, t["series"], cx, y + h - 1.15 * inch, "Sans", 7.2, 1.5, "center", ink)
    _diamond(c, cx, y + h - 1.38 * inch, 6.2, ink, 0.8)
    c.setStrokeColor(ink)
    c.setLineWidth(0.45)
    c.line(cx - 70, y + h - 1.38 * inch, cx - 10, y + h - 1.38 * inch)
    c.line(cx + 10, y + h - 1.38 * inch, cx + 70, y + h - 1.38 * inch)

    y_title = y + h * 0.58
    y_after, _ = _title_block(c, cx, y_title, t["cover_title"], ink, w - 1.15 * inch, size=30)

    y_after -= 10
    _diamond(c, cx, y_after, 5, ink, 0.7)
    c.setLineWidth(0.4)
    c.line(cx - 54, y_after, cx - 9, y_after)
    c.line(cx + 9, y_after, cx + 54, y_after)

    # subtitle
    sub_y = y_after - 28
    c.setFillColor(ink)
    for ln in t["subtitle"].split("\n"):
        c.setFont("Cormorant-Italic", 11)
        c.drawCentredString(cx, sub_y, ln)
        sub_y -= 15

    # footer
    c.setFont("Sans", 8)
    c.setFillColor(ink)
    c.drawCentredString(cx, y + 0.72 * inch, t["tagline"])
    c.setFont("Sans", 6.8)
    c.drawCentredString(cx, y + 0.52 * inch, "Undated  ·  Personal tracking  ·  Not medical advice")


def draw_back_panel(c, x, y, w, h, t, ink, bg, panel, dark: bool, spine_w: float):
    inset = 0.28 * inch
    c.setStrokeColor(ink)
    c.setLineWidth(0.9)
    c.rect(x + inset, y + inset, w - 2 * inset, h - 2 * inset, stroke=1, fill=0)

    left = x + 0.48 * inch
    right = x + w - 0.48 * inch
    maxw = right - left

    _spaced(c, t["series"], left, y + h - 0.95 * inch, "Sans", 6.8, 1.3, "left", ink)
    c.setFillColor(ink)
    c.setFont("Cormorant-Semi", 16)
    c.drawString(left, y + h - 1.28 * inch, t["cover_title_one"])

    # about
    yy = y + h - 1.65 * inch
    c.setFont("Sans", 8.4)
    blurb = (
        "A discreet, undated tracking journal. Fill in what your own clinician already directed. "
        "This book does not diagnose, dose, or treat."
    )
    from .kit import wrap as wrap_text

    for ln in wrap_text(blurb, "Sans", 8.4, maxw):
        c.drawString(left, yy, ln)
        yy -= 12

    yy -= 10
    c.setFont("Sans-Semi", 7.5)
    c.drawString(left, yy, "INSIDE")
    yy -= 16
    for b in t["bullets"]:
        c.setFillColor(ink)
        c.circle(left + 3, yy + 3, 1.4, stroke=0, fill=1)
        lines = wrap_text(b, "Sans", 8.2, maxw - 14)
        for i, ln in enumerate(lines):
            c.setFont("Sans", 8.2)
            c.drawString(left + 12, yy, ln)
            yy -= 11.5
        yy -= 4

    # barcode reserve — bottom right of BACK, near spine (right edge of this panel)
    bw, bh = 2.05 * inch, 1.25 * inch
    bx = x + w - 0.22 * inch - bw  # toward spine
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


def draw_spine(c, x, y, w, h, t, ink, dark: bool):
    if t["pages"] < 79 or w < 0.06 * inch:
        return
    c.saveState()
    c.translate(x + w / 2, y + h / 2)
    c.rotate(90)
    # after rotate, x is along height
    _diamond(c, -h * 0.38, 0, 3.6, ink, 0.7)
    c.setFillColor(ink)
    c.setFont("Sans-Semi", 7)
    label = t["spine"]
    # fit
    size = 8
    while pdfmetrics.stringWidth(label, "Cormorant-Semi", size) > h * 0.55 and size > 6:
        size -= 0.3
    c.setFont("Cormorant-Semi", size)
    c.drawCentredString(0, -2.5, label)
    c.setFont("Sans", 6)
    c.drawCentredString(h * 0.38, -2, t["n"])
    c.restoreState()
    # hairlines
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
    c.setAuthor("KDP tracking series")
    W, H = width * inch, height * inch
    ink, bg, panel = C(t["ink"]), C(t["bg"]), C(t["panel"])
    c.setFillColor(bg)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    bleed = BLEED * inch
    tw_pt, th_pt = tw * inch, th * inch
    spine_w = sp * inch
    # [bleed][back trim][spine][front trim][bleed]
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
    """Front cover at trim size (no bleed) — for mockups / lookbook."""
    register_fonts()
    tw, th = t["trim"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(dest), pagesize=(tw * inch, th * inch))
    c.setTitle(t["kdp_title"])
    ink, bg, panel = C(t["ink"]), C(t["bg"]), C(t["panel"])
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
