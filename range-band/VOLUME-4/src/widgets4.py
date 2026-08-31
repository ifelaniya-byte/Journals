"""Extra page widgets for Volume 4 — capacity bands, grounding field, blotter.
Reuses Drawing helpers patterned on widgets.py (lib.kit Book).
"""
from __future__ import annotations

from reportlab.lib.colors import Color
from reportlab.lib.units import inch

from lib.kit import sw
from widgets import _bub, _fieldline, _header, INKK, INK2, MID, RULE, HAIR, WASH


def draw_capacity(book, day, spec):
    y = _header(book, day, "Capacity bands — today is a color, not a grade")
    fields = spec.get("capacity_fields") or ["Capacity band", "Sensory load", "One recovery act", "What changed"]
    # three band boxes
    bw = (book.x1 - book.x0 - 16) / 3
    by = y - 24
    names = [("GREEN", "full engine"), ("YELLOW", "half power"), ("RED", "rest day")]
    for i, (name, sub) in enumerate(names):
        x = book.x0 + i * (bw + 8)
        _bub(book, x, by, bw, 54)
        book.text(name, x + 8, by + 30, "Sans", 9, INK2)
        book.text(sub, x + 8, by + 16, "Sans", 6.6, MID)
        book.c.setStrokeColor(RULE)
        book.c.rect(x + 8, by + 4, 12, 12, stroke=1, fill=0)
    yy = by - 70
    for f in fields:
        _fieldline(book, book.x0, yy, book.x1 - book.x0 - 10, f)
        yy -= 22
    book.text("Bands are information, not failure. A red day is still a day.", book.x0, yy - 6, "Sans", 6.6, MID)
    book.footer()


def draw_ground(book, day, spec):
    y = _header(book, day, "Grounding field — write the anchors before the moment")
    fields = spec.get("ground_fields") or ["See (5)", "Hear (4)", "Touch (3)", "Smell (2)", "Taste (1)"]
    yy = y - 26
    for f in fields:
        book.text(f, book.x0, yy, "Sans", 8, INK2)
        book.dotted_field(book.x0 + 90, yy, book.x1 - book.x0 - 110)
        yy -= 28
    _fieldline(book, book.x0, yy - 6, book.x1 - book.x0, "Trigger / time")
    _fieldline(book, book.x0, yy - 28, book.x1 - book.x0, "What made me safe")
    book.text("Preparatory anchors beat mid-freeze invention.", book.x0, yy - 50, "Sans", 6.6, MID)
    book.footer()


def draw_blotter(book, day, spec):
    y = _header(book, day, "Blotter — quick entries, honest facts")
    fields = spec.get("blotter_fields") or ["Time", "What", "Length", "Felt"]
    # time axis
    book.text("clock", book.x0, y - 16, "Sans", 6.6, MID)
    bx = book.x0 + 40
    bw = book.x1 - book.x0 - 50
    book.c.setStrokeColor(HAIR)
    book.c.setLineWidth(0.6)
    book.c.line(bx, y - 16, bx + bw, y - 16)
    for h in range(0, 25, 2):
        xx = bx + bw * h / 24
        book.c.setStrokeColor(RULE)
        book.c.line(xx, y - 12, xx, y - 20)
        if h % 4 == 0:
            book.text(str(h), xx - 4, y - 30, "Sans", 5.6, MID)
    # blot bullets
    yy = y - 52
    for i in range(5):
        _bub(book, book.x0, yy, book.x1 - book.x0, 52)
        cy = yy + 42
        xoff = book.x0 + 10
        for f in fields:
            book.text(f, xoff, cy, "Sans", 6.8, MID)
            book.dotted_field(xoff + sw(f, "Sans", 6.8) + 8, cy, 60)
            xoff += 110
            if xoff > book.x1 - 40:
                break
        yy -= 58
    _fieldline(book, book.x0, yy - 4, book.x1 - book.x0, "Pattern note")
    book.footer()
