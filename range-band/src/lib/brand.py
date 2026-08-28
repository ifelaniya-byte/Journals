"""Range Band Press — house mark, color, and voice.

A range is not a cage. It is the band you already chose.
"""

from __future__ import annotations

from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

IMPRINT = "Range Band Press"
IMPRINT_TRACKED = "RANGE BAND PRESS"
HOUSE = "Live inside the range."
HOUSE_LONG = (
    "A range is not a cage. It is the band you already chose — protein, sleep, "
    "a shot day, a quiet Tuesday. Undated logs for a life that has numbers "
    "but is not a number."
)
BACK_BLURB = (
    "Range Band Press makes undated tracking journals for the middle of the work: "
    "the week after the start, the month you keep. Fill in what your own clinician "
    "already directed. This book does not diagnose, dose, or treat."
)
FOOT = "Undated  ·  Personal tracking  ·  Not medical advice"
YEAR = "2026"

# Series accents (print-safe, not neon). Dark covers use copper sand.
ACCENT = {
    "GLP-1 TRACKING SERIES": (0.36, 0.54, 0.38),
    "WELLNESS TRACKING SERIES": (0.24, 0.42, 0.48),
    "GLP-1 COMPANION SERIES": (0.77, 0.47, 0.29),
    "WELLNESS COMPANION SERIES": (0.42, 0.31, 0.45),
}
ACCENT_DARK = (0.86, 0.70, 0.48)


def C(rgb) -> Color:
    return Color(*rgb)


def accent_rgb(t: dict) -> tuple[float, float, float]:
    if t.get("dark"):
        return ACCENT_DARK
    return ACCENT.get(t.get("series", ""), (0.45, 0.42, 0.36))


def mix(a, b, t: float):
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))


def draw_range_band(
    c: canvas.Canvas,
    cx: float,
    cy: float,
    width: float,
    ink: Color,
    accent: Color | None = None,
    tick: float = 7.0,
    band_h: float = 6.4,
    weight: float = 1.35,
):
    """Two posts, a rail, a living band, a pip. The house mark."""
    x0 = cx - width / 2
    x1 = cx + width / 2
    c.setStrokeColor(ink)
    c.setLineWidth(weight)
    c.line(x0, cy - tick, x0, cy + tick)
    c.line(x1, cy - tick, x1, cy + tick)
    c.setLineWidth(0.65)
    c.line(x0, cy, x1, cy)
    bw = width * 0.44
    bx = x0 + width * 0.20
    fill = accent or ink
    c.setFillColor(fill)
    c.roundRect(bx, cy - band_h / 2, bw, band_h, min(2.0, band_h / 2), stroke=0, fill=1)
    pip = bx + bw * 0.78
    c.setFillColor(ink)
    c.circle(pip, cy, max(2.1, band_h * 0.38), stroke=0, fill=1)


def spaced(c, text, x, y, font, size, tracking, align, color):
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
