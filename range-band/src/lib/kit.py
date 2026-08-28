"""Grayscale drawing kit for print-ready KDP journal interiors."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import Color, white
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "fonts"
OUTPUT = ROOT / "output"

INK = Color(0.10, 0.10, 0.10)
INK2 = Color(0.22, 0.22, 0.22)
MID = Color(0.42, 0.42, 0.42)
MUTED = Color(0.55, 0.55, 0.55)
RULE = Color(0.70, 0.70, 0.70)
HAIR = Color(0.80, 0.80, 0.80)
PALE = Color(0.93, 0.93, 0.93)
WASH = Color(0.96, 0.96, 0.96)
GHOST = Color(0.88, 0.88, 0.88)

SIX_NINE = (6 * inch, 9 * inch)
FIVE_EIGHT = (5 * inch, 8 * inch)
LETTER = (8.5 * inch, 11 * inch)

_FONTS_READY = False


def G(v: float) -> Color:
    return Color(v, v, v)


def register_fonts() -> None:
    global _FONTS_READY
    if _FONTS_READY:
        return
    mapping = {
        "Cormorant": "cormorant-400.ttf",
        "Cormorant-Med": "cormorant-500.ttf",
        "Cormorant-Semi": "cormorant-600.ttf",
        "Cormorant-Bold": "cormorant-700.ttf",
        "Cormorant-Italic": "cormorant-400i.ttf",
        "Cormorant-SemiItalic": "cormorant-600i.ttf",
        "Sans": "sourcesans-400.ttf",
        "Sans-Light": "sourcesans-300.ttf",
        "Sans-Semi": "sourcesans-600.ttf",
        "Sans-Bold": "sourcesans-700.ttf",
        "Sans-Italic": "sourcesans-400i.ttf",
        "Serif": "librebaskerville-400.ttf",
        "Serif-Bold": "librebaskerville-700.ttf",
        "Serif-Italic": "librebaskerville-400i.ttf",
    }
    for name, fn in mapping.items():
        pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / fn)))
    _FONTS_READY = True


def sw(text: str, font: str, size: float) -> float:
    return pdfmetrics.stringWidth(text, font, size)


def wrap(text: str, font: str, size: float, max_width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if sw(test, font, size) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def draw_spaced(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    font: str = "Sans",
    size: float = 7.5,
    tracking: float = 1.15,
    align: str = "left",
    color: Color = MUTED,
) -> float:
    text = text.upper()
    widths = [sw(ch, font, size) for ch in text]
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


class Book:
    def __init__(
        self,
        path: str | Path,
        pagesize=SIX_NINE,
        gutter: float = 0.72 * inch,
        outer: float = 0.50 * inch,
        top: float = 0.46 * inch,
        bottom: float = 0.50 * inch,
        running: str = "",
    ):
        register_fonts()
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.w, self.h = pagesize
        self.gutter = gutter
        self.outer = outer
        self.top = top
        self.bottom = bottom
        self.running = running
        self.c = canvas.Canvas(str(self.path), pagesize=pagesize)
        self.c.setTitle(running or self.path.stem)
        self.c.setAuthor("Range Band Press")
        self.c.setSubject("Personal tracking / management journal (not medical advice)")
        self.page_num = 0
        self.ml = self.mr = outer

    # --- page lifecycle -------------------------------------------------
    def begin(self) -> None:
        self.page_num += 1
        odd = self.page_num % 2 == 1  # right-hand page in a bound book
        if odd:
            self.ml, self.mr = self.gutter, self.outer
        else:
            self.ml, self.mr = self.outer, self.gutter
        self.c.setFillColor(white)
        self.c.rect(0, 0, self.w, self.h, stroke=0, fill=1)

    def end(self) -> None:
        self.c.showPage()

    def save(self) -> Path:
        self.c.save()
        return self.path

    def page(self):
        """Context manager-ish: call begin, yield, caller must end. Kept simple."""
        self.begin()
        return self

    @property
    def odd(self) -> bool:
        return self.page_num % 2 == 1

    @property
    def x0(self) -> float:
        return self.ml

    @property
    def x1(self) -> float:
        return self.w - self.mr

    @property
    def y0(self) -> float:
        return self.bottom

    @property
    def y1(self) -> float:
        return self.h - self.top

    @property
    def cw(self) -> float:
        return self.x1 - self.x0

    @property
    def ch(self) -> float:
        return self.y1 - self.y0

    def ensure_left(self, filler=None) -> None:
        """Next page should be a left (even) page. If not, consume a right-hand filler."""
        if self.page_num % 2 == 0:
            # last finished even -> next is odd (right). Insert filler.
            if filler:
                filler()
            else:
                self.blank_with_ornament()

    def ensure_right(self) -> None:
        if self.page_num % 2 == 1:
            self.blank_with_ornament()

    # --- primitives -----------------------------------------------------
    def set_stroke(self, color=INK, width=0.6):
        self.c.setStrokeColor(color)
        self.c.setLineWidth(width)

    def line(self, x1, y1, x2, y2, color=HAIR, width=0.5):
        self.set_stroke(color, width)
        self.c.line(x1, y1, x2, y2)

    def hline(self, y, x0=None, x1=None, color=HAIR, width=0.5):
        self.line(x0 if x0 is not None else self.x0, y, x1 if x1 is not None else self.x1, y, color, width)

    def double_rule(self, y, x0=None, x1=None, color=INK, gap=2.2):
        x0 = self.x0 if x0 is None else x0
        x1 = self.x1 if x1 is None else x1
        self.line(x0, y, x1, y, color, 0.9)
        self.line(x0, y - gap, x1, y - gap, color, 0.35)

    def rect(self, x, y, w, h, stroke=INK, fill=None, sw=0.7, r=0):
        self.c.setStrokeColor(stroke)
        self.c.setLineWidth(sw)
        if fill is not None:
            self.c.setFillColor(fill)
            if r:
                self.c.roundRect(x, y, w, h, r, stroke=1, fill=1)
            else:
                self.c.rect(x, y, w, h, stroke=1, fill=1)
        else:
            if r:
                self.c.roundRect(x, y, w, h, r, stroke=1, fill=0)
            else:
                self.c.rect(x, y, w, h, stroke=1, fill=0)

    def box(
        self,
        x,
        y,
        w,
        h,
        title: str | None = None,
        fill=None,
        stroke=RULE,
        sw=0.6,
        r=3,
        title_size=7.2,
        lines=False,
        line_gap=16,
    ):
        self.rect(x, y, w, h, stroke=stroke, fill=fill, sw=sw, r=r)
        if title:
            self.c.setFillColor(MID)
            self.c.setFont("Sans-Semi", title_size)
            t = title
            maxw = w - 16
            while pdfmetrics.stringWidth(t, "Sans-Semi", title_size) > maxw and len(t) > 6:
                t = t[:-1]
            if t != title:
                t = t.rstrip() + "..."
            self.c.drawString(x + 7, y + h - 12, t)
            self.line(x + 6, y + h - 16, x + w - 6, y + h - 16, HAIR, 0.4)
        if lines:
            top = y + h - (22 if title else 10)
            n = max(1, int((top - (y + 8)) / line_gap))
            self.writing_lines(top, n, gap=line_gap, x0=x + 8, x1=x + w - 8)
        return y + h - (20 if title else 8)

    def text(self, s, x, y, font="Sans", size=9, color=INK, align="left"):
        self.c.setFillColor(color)
        self.c.setFont(font, size)
        if align == "center":
            self.c.drawCentredString(x, y, s)
        elif align == "right":
            self.c.drawRightString(x, y, s)
        else:
            self.c.drawString(x, y, s)

    def paragraph(self, text, x, y, w, font="Sans", size=9, leading=13, color=INK2, align="left") -> float:
        lines = wrap(text, font, size, w)
        self.c.setFillColor(color)
        self.c.setFont(font, size)
        for i, ln in enumerate(lines):
            yy = y - i * leading
            if align == "center":
                self.c.drawCentredString(x + w / 2, yy, ln)
            else:
                self.c.drawString(x, yy, ln)
        return y - len(lines) * leading

    def writing_lines(self, y_top, n, gap=16, x0=None, x1=None, color=HAIR):
        x0 = self.x0 if x0 is None else x0
        x1 = self.x1 if x1 is None else x1
        y = y_top
        for _ in range(n):
            self.line(x0, y, x1, y, color, 0.4)
            y -= gap
        return y

    def dotted_field(self, x, y, w, color=RULE):
        self.set_stroke(color, 0.5)
        self.c.setDash(1, 2)
        self.c.line(x, y, x + w, y)
        self.c.setDash()

    def checkbox(self, x, y, label="", size=8.5, font="Sans", fs=8, color=INK2):
        self.rect(x, y, size, size, stroke=INK2, sw=0.7, r=1)
        if label:
            self.text(label, x + size + 5, y + 1.2, font, fs, color)

    def check_row(self, items, x, y, col_w, cols, size=8.5, fs=8) -> float:
        """items: list of labels. Returns y of last row (bottom)."""
        row_h = 16
        for i, lab in enumerate(items):
            c = i % cols
            r = i // cols
            self.checkbox(x + c * col_w, y - r * row_h, lab, size=size, fs=fs)
        rows = (len(items) + cols - 1) // cols
        return y - (rows - 1) * row_h

    def circles(self, x, y, n=10, r=5.2, gap=15.5, start=1, labels=True, fs=6.5):
        for i in range(n):
            cx = x + i * gap
            self.set_stroke(INK2, 0.7)
            self.c.circle(cx, y, r, stroke=1, fill=0)
            if labels:
                self.text(str(start + i), cx, y - r - 9, "Sans", fs, MUTED, "center")

    def scale_row(self, label, x, y, w, n=10, left="low", right="high"):
        """Draw a labeled 1–n circle scale. `y` is the label baseline; graphics hang below."""
        self.text(label, x, y, "Sans-Semi", 7.2, MID)
        gap = min(16.5, max(11.0, (w - 16) / n))
        self.circles(x + 6, y - 16, n=n, gap=gap, r=4.6)
        self.text(left, x + 6, y - 36, "Sans", 6, MUTED)
        lastx = x + 6 + (n - 1) * gap
        self.text(right, lastx, y - 36, "Sans", 6, MUTED, "center")

    def slider(self, x, y, w, ticks=5, labels=None):
        self.line(x, y, x + w, y, INK2, 0.8)
        for i in range(ticks):
            tx = x + (w * i / (ticks - 1) if ticks > 1 else 0)
            self.line(tx, y - 4, tx, y + 4, INK2, 0.7)
            self.set_stroke(INK2, 0.7)
            self.c.circle(tx, y, 4.2, stroke=1, fill=0)
            if labels and i < len(labels):
                self.text(str(labels[i]), tx, y - 13, "Sans", 6.2, MUTED, "center")

    def water_row(self, x, y, n=8, r=5.5, gap=16):
        for i in range(n):
            cx = x + i * gap
            # simple droplet: circle + triangle-ish
            self.set_stroke(INK2, 0.7)
            self.c.circle(cx, y - 2, r * 0.72, stroke=1, fill=0)
            p = self.c.beginPath()
            p.moveTo(cx, y + r * 1.15)
            p.curveTo(cx + r * 0.7, y + r * 0.2, cx + r * 0.7, y - 2, cx, y - 2)
            p.curveTo(cx - r * 0.7, y - 2, cx - r * 0.7, y + r * 0.2, cx, y + r * 1.15)
            self.c.drawPath(p, stroke=1, fill=0)

    def day_pills(self, x, y, days="MTWTFSS", gap=18):
        for i, d in enumerate(days):
            cx = x + i * gap
            self.set_stroke(INK2, 0.6)
            self.c.circle(cx, y, 7.2, stroke=1, fill=0)
            self.text(d, cx, y - 2.6, "Sans-Semi", 7, INK2, "center")

    def date_line(self, x, y, w=None):
        self.text("Date", x, y, "Sans-Semi", 7.5, MID)
        self.dotted_field(x + 26, y, 78)
        self.text("Day", x + 112, y, "Sans-Semi", 7.5, MID)
        self.day_pills(x + 138, y + 2, gap=16.5)

    def field(self, label, x, y, w, label_w=None):
        self.text(label, x, y, "Sans", 8, MID)
        lw = label_w if label_w is not None else sw(label, "Sans", 8) + 6
        self.dotted_field(x + lw, y, w - lw)

    def footer(self, show_number=True):
        y = 0.30 * inch
        self.line(self.x0, self.bottom - 10, self.x1, self.bottom - 10, HAIR, 0.35)
        # page number on the outer edge; running foot on the inner edge
        if self.odd:
            if self.running:
                self.text(self.running, self.x0, y, "Sans", 6.2, MUTED)
            if show_number:
                self.text(str(self.page_num), self.x1, y, "Sans", 7.5, MID, "right")
        else:
            if show_number:
                self.text(str(self.page_num), self.x0, y, "Sans", 7.5, MID)
            if self.running:
                self.text(self.running, self.x1, y, "Sans", 6.2, MUTED, "right")

    def header_bar(self, kicker: str, title: str):
        draw_spaced(self.c, kicker, self.x0, self.y1 - 2, "Sans", 6.6, 1.2, "left", MUTED)
        self.text(title, self.x0, self.y1 - 20, "Cormorant-Semi", 16, INK)
        self.double_rule(self.y1 - 26)
        return self.y1 - 40

    def ornament(self, cx, y, w=86):
        self.line(cx - w, y, cx - 8, y, RULE, 0.5)
        self.line(cx + 8, y, cx + w, y, RULE, 0.5)
        self.set_stroke(INK2, 0.7)
        self.c.saveState()
        self.c.translate(cx, y)
        self.c.rotate(45)
        self.c.rect(-3.2, -3.2, 6.4, 6.4, stroke=1, fill=0)
        self.c.restoreState()

    def blank_with_ornament(self, caption: str | None = None):
        self.begin()
        self.ornament(self.w / 2, self.h / 2, 70)
        if caption:
            self.text(caption, self.w / 2, self.h / 2 - 22, "Cormorant-Italic", 11, MUTED, "center")
        self.footer(show_number=False)
        self.end()

    def notes_page(self, title="Notes"):
        self.begin()
        y = self.header_bar(self.running or "JOURNAL", title)
        self.writing_lines(y - 8, 28, gap=18)
        self.footer()
        self.end()

    def lined_page(self, title="Notes", n=26, gap=18):
        self.notes_page(title)


# ---------------------------------------------------------------------------
# Shared front matter
# ---------------------------------------------------------------------------

DISCLAIMER = (
    "This journal is a personal tracking and management tool only. "
    "It is not medical advice, diagnosis, or treatment, and it is not a substitute "
    "for care from a licensed clinician. It is not affiliated with, endorsed by, or "
    "sponsored by any medication manufacturer or healthcare brand. "
    "Do not start, stop, or change a medication, meal plan, or activity based on this book. "
    "Record only what your own prescriber has directed. If you notice concerning symptoms, "
    "seek professional medical care promptly."
)

COPYRIGHT = (
    "Copyright (c) 2026. All rights reserved. For personal use by the purchaser. "
    "No part of this interior may be reproduced for resale. First undated edition."
)


def title_page(book: Book, series: str, title: str, subtitle: str, tagline: str):
    from .brand import HOUSE, IMPRINT_TRACKED, draw_range_band

    b = book
    b.begin()
    inset = 0.38 * inch
    b.rect(inset, inset, b.w - 2 * inset, b.h - 2 * inset, stroke=INK, sw=0.9, r=0)
    b.rect(inset + 5, inset + 5, b.w - 2 * inset - 10, b.h - 2 * inset - 10, stroke=INK, sw=0.35, r=0)
    draw_spaced(b.c, IMPRINT_TRACKED, b.w / 2, b.h * 0.78, "Sans", 7.0, 1.8, "center", MID)
    draw_spaced(b.c, series, b.w / 2, b.h * 0.74, "Sans", 7.2, 1.5, "center", MID)
    draw_range_band(b.c, b.w / 2, b.h * 0.74 - 20, 96, INK, INK, tick=5.5, band_h=5.2, weight=1.15)
    y = b.h * 0.56
    for ln in wrap(title, "Cormorant-Semi", 28, b.w - 1.5 * inch):
        b.text(ln, b.w / 2, y, "Cormorant-Semi", 28, INK, "center")
        y -= 32
    y -= 6
    for ln in wrap(subtitle, "Cormorant-Italic", 12, b.w - 1.7 * inch):
        b.text(ln, b.w / 2, y, "Cormorant-Italic", 12, INK2, "center")
        y -= 16
    draw_range_band(b.c, b.w / 2, y - 8, 72, INK, INK, tick=4.5, band_h=4.4, weight=1.0)
    b.text(HOUSE, b.w / 2, 1.32 * inch, "Cormorant-Italic", 11, INK2, "center")
    b.text(tagline, b.w / 2, 1.08 * inch, "Sans", 8.5, MID, "center")
    b.text("Undated  ·  Personal use  ·  Not medical advice", b.w / 2, 0.84 * inch, "Sans", 7, MUTED, "center")
    b.end()


def copyright_page(book: Book, extra: str = ""):
    b = book
    b.begin()
    y = b.y1 - 10
    b.text("A note before you begin", b.x0, y, "Cormorant-Semi", 16, INK)
    b.double_rule(y - 8)
    y = b.paragraph(DISCLAIMER, b.x0, y - 28, b.cw, "Sans", 8.7, 12.5, INK2)
    if extra:
        y = b.paragraph(extra, b.x0, y - 10, b.cw, "Sans", 8.7, 12.5, INK2)
    y -= 18
    b.text("Copyright", b.x0, y, "Sans-Semi", 8, MID)
    y = b.paragraph(COPYRIGHT, b.x0, y - 14, b.cw, "Sans", 8, 12, MUTED)
    y -= 16
    b.text("Edition", b.x0, y, "Sans-Semi", 8, MID)
    y = b.paragraph(
        "First undated edition, 2026. Printed for personal use. This is a tracking journal, not a clinical record.",
        b.x0,
        y - 14,
        b.cw,
        "Sans",
        8,
        12,
        MUTED,
    )
    b.footer(show_number=False)
    b.end()


def belongs_page(book: Book, fields: list[str] | None = None):
    b = book
    b.begin()
    y = b.header_bar(b.running or "JOURNAL", "This journal belongs to")
    fields = fields or [
        "Name",
        "Year I started this volume",
        "Care team / clinic (optional)",
        "Emergency contact",
        "If found, please return to",
    ]
    for lab in fields:
        b.text(lab, b.x0, y, "Sans-Semi", 8, MID)
        b.writing_lines(y - 14, 2, gap=18)
        y -= 52
    b.rect(b.x0, b.y0 + 8, b.cw, 78, stroke=HAIR, sw=0.5, r=3)
    b.text("Intention for this volume", b.x0 + 8, b.y0 + 70, "Sans-Semi", 7.5, MID)
    b.writing_lines(b.y0 + 54, 3, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    b.footer()
    b.end()


def how_to_page(book: Book, title: str, sections: list[tuple[str, list[str]]]):
    """One or two pages of how-to copy. sections = [(heading, [bullets])]."""
    b = book
    b.begin()
    y = b.header_bar(b.running or "JOURNAL", title)
    for heading, bullets in sections:
        if y < b.y0 + 90:
            b.footer()
            b.end()
            b.begin()
            y = b.header_bar(b.running or "JOURNAL", title + "  (continued)")
        b.text(heading, b.x0, y, "Cormorant-Semi", 13, INK)
        y -= 16
        for bullet in bullets:
            # hanging indent
            b.c.setFillColor(INK)
            b.c.circle(b.x0 + 3.5, y + 3, 1.3, stroke=0, fill=1)
            lines = wrap(bullet, "Sans", 8.6, b.cw - 16)
            for i, ln in enumerate(lines):
                b.text(ln, b.x0 + 12, y, "Sans", 8.6, INK2)
                y -= 12.2
            y -= 4
        y -= 10
    b.footer()
    b.end()


def goals_page(book: Book, title: str, prompts: list[str]):
    b = book
    b.begin()
    y = b.header_bar(b.running or "JOURNAL", title)
    for p in prompts:
        if y < b.y0 + 56:
            break
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 3, gap=16) - 14
    b.footer()
    b.end()


def legend_page(book: Book, title: str, rows: list[tuple[str, str]]):
    b = book
    b.begin()
    y = b.header_bar(b.running or "JOURNAL", title)
    b.paragraph(
        "Use these marks consistently so patterns are easy to see later — and easy to share with your care team.",
        b.x0,
        y,
        b.cw,
        "Sans",
        8.5,
        12,
        INK2,
    )
    y -= 28
    col_l = b.cw * 0.34
    for i, (mark, meaning) in enumerate(rows):
        b.rect(b.x0, y - 6, b.cw, 22, stroke=HAIR, sw=0.35, fill=WASH if i % 2 == 0 else None, r=0)
        b.text(mark, b.x0 + 8, y, "Sans-Semi", 8, INK)
        b.text(meaning, b.x0 + col_l, y, "Sans", 8, INK2)
        y -= 24
    b.footer()
    b.end()


def section_opener(book: Book, kicker: str, title: str, blurb: str = ""):
    b = book
    b.begin()
    draw_spaced(b.c, kicker, b.w / 2, b.h * 0.58, "Sans", 7.2, 1.4, "center", MUTED)
    b.ornament(b.w / 2, b.h * 0.58 - 16, 60)
    b.text(title, b.w / 2, b.h * 0.48, "Cormorant-Semi", 22, INK, "center")
    if blurb:
        b.paragraph(blurb, b.x0 + 12, b.h * 0.42, b.cw - 24, "Sans", 9, 13, INK2, "center")
    b.footer(show_number=False)
    b.end()


def standard_front(
    book: Book,
    series: str,
    title: str,
    subtitle: str,
    tagline: str,
    how_to: list[tuple[str, list[str]]],
    goals: list[str],
    extra_disclaimer: str = "",
    belongs_fields: list[str] | None = None,
    legend: list[tuple[str, str]] | None = None,
    how_to_title: str = "How to use this journal",
    goals_title: str = "Where I am starting",
):
    title_page(book, series, title, subtitle, tagline)
    copyright_page(book, extra_disclaimer)
    belongs_page(book, belongs_fields)
    how_to_page(book, how_to_title, how_to)
    if legend:
        legend_page(book, "Marks & scales", legend)
    goals_page(book, goals_title, goals)
