"""Page widgets for Range Band Press Volume 3 interiors.

Each widget draws one daily page with a distinct mechanic (quadrant, radar,
gauge, ledger, body map, bucket, trail, wire, ladder, wave, cards, script,
bridge, dial, court, orbit, wheel, histogram, meter). Grayscale, print-safe,
designed for the 6x9 Book from lib.kit.
"""
from __future__ import annotations

import math

from reportlab.lib.colors import Color
from reportlab.lib.units import inch

from lib.kit import sw

INKK = Color(0.10, 0.10, 0.10)
INK2 = Color(0.22, 0.22, 0.22)
MID = Color(0.42, 0.42, 0.42)
RULE = Color(0.70, 0.70, 0.70)
HAIR = Color(0.84, 0.84, 0.84)
WASH = Color(0.94, 0.94, 0.94)


def _header(book, day, title):
    book.begin()
    y = book.header_bar(f"DAY {day:02d}", title)
    return y


def _scale_row(book, x, y, w, label="0-10"):
    book.text("0", x, y, "Sans", 7, MID)
    book.text("5", x + w * 0.5 - 2, y, "Sans", 7, MID, "center")
    book.text("10", x + w - 8, y, "Sans", 7, MID, "right")
    return y - 6


def _bub(book, x, y, w, h):
    book.c.setFillColor(WASH)
    book.c.setStrokeColor(HAIR)
    book.c.setLineWidth(0.4)
    book.c.roundRect(x, y, w, h, 3, stroke=1, fill=1)


def _fieldline(book, x, y, w, label=""):
    if label:
        book.text(label, x, y, "Sans", 7.5, MID)
        lw = sw(label, "Sans", 7.5) + 6 if hasattr(book, "_sw") else 74
        book.dotted_field(x + lw, y, w - lw)
    else:
        book.dotted_field(x, y, w)


def draw_quad(book, day, spec):
    y = _header(book, day, "Four quadrants — one honest number each")
    fields = spec.get("quad_fields") or ["Energy", "Appetite", "Skin", "Mood"]
    cols, rows = 2, 2
    cw = (book.x1 - book.x0 - 10) / cols
    ch = (y - book.y0 - 26) / rows
    for i, f in enumerate(fields):
        cx = book.x0 + (i % cols) * (cw + 10)
        cy = y - 10 - (i // cols) * (ch + 12)
        _bub(book, cx, cy, cw, ch)
        book.text(f, cx + 8, cy + ch - 14, "Sans", 8.2, INK2)
        # 0-10 tick
        for t in range(11):
            bx = cx + 14 + t * (cw - 30) / 10
            book.c.setStrokeColor(RULE)
            book.c.line(bx, cy + 12, bx, cy + 20)
        book.text("0", cx + 10, cy + 6, "Sans", 6.6, MID)
        book.text("10", cx + cw - 16, cy + 6, "Sans", 6.6, MID, "right")
        _fieldline(book, cx + 10, cy + 2, cw - 20, "Note")
    book.footer()


def draw_radar(book, day, spec):
    y = _header(book, day, "Radar — five axes, one shape")
    axes = spec.get("radar_axes") or ["Energy", "Pain", "Sleep", "Food", "Mood"]
    cx, cy = (book.x0 + book.x1) / 2, y - 90
    r = 66
    for ring in (1, 2, 3):
        book.c.setStrokeColor(RULE if ring < 3 else MID)
        book.c.setLineWidth(0.5)
        book.c.circle(cx, cy, r * ring / 3, stroke=1, fill=0)
    labels = []
    for i, ax in enumerate(axes):
        ang = math.pi / 2 + (2 * math.pi * i / len(axes))
        x2 = cx + r * math.cos(ang)
        y2 = cy + r * math.sin(ang)
        book.c.setStrokeColor(HAIR)
        book.c.line(cx, cy, x2, y2)
        label = sw(ax, "Sans", 7) if hasattr(book, "_sw") else 60
        lx = cx + (r + 22) * math.cos(ang) - label / 2
        book.text(ax, lx, cy + (r + 22) * math.sin(ang) - 3, "Sans", 7, MID)
        labels.append((ax, ang))
    # value boxes below
    book.text("Score each axis 0-10 and write the value.", book.x0, y - 168, "Sans", 7.5, MID)
    yy = y - 186
    for i, (ax, _) in enumerate(labels):
        x = book.x0 + (i % 3) * ((book.x1 - book.x0) / 3)
        _fieldline(book, x, yy, (book.x1 - book.x0) / 3 - 10, f"{ax} /10")
        if i % 3 == 2:
            yy -= 18
    book.footer()


def draw_map(book, day, spec):
    y = _header(book, day, "Body map — shade the zones that speak")
    zones = spec.get("zones") or []
    cols = 4
    cw = (book.x1 - book.x0 - 12) / cols
    num = len(zones)
    rows = math.ceil(num / cols)
    ch = 30
    start = y - 20
    for i, z in enumerate(zones):
        r = i // cols
        c = i % cols
        x = book.x0 + c * (cw + 6)
        yy = start - r * (ch + 6)
        _bub(book, x, yy, cw, ch)
        book.text(z[:18], x + 6, yy + ch - 12, "Sans", 7.6, INK2)
        for t in range(4):
            bx = x + cw - 62 + t * 16
            book.c.setStrokeColor(RULE)
            book.c.rect(bx, yy + 6, 12, 12, stroke=1, fill=0)
    book.text("Shade 0 none · 1 mild · 2 steady · 3 loud", book.x0, start - rows * (ch + 6) + 2, "Sans", 6.6, MID)
    _fieldline(book, book.x0, start - rows * (ch + 6) - 18, book.x1 - book.x0, "Trigger / note")
    book.footer()


def draw_gauge(book, day, spec):
    y = _header(book, day, f"{spec.get('gauge_label', 'Battery')} — plan before you spend")
    label = spec.get("gauge_label", "Battery")
    mx = spec.get("gauge_max", 10)
    bar_w = book.x1 - book.x0 - 120
    bx, by = book.x0, y - 26
    book.text("0", bx, by + 26, "Sans", 7, MID)
    book.text("10", bx + bar_w + 44, by + 26, "Sans", 7, MID, "right")
    book.c.setStrokeColor(RULE)
    book.c.setLineWidth(0.6)
    book.c.rect(bx, by, bar_w, 18, stroke=1, fill=0)
    for i in range(1, mx):
        xx = bx + bar_w * i / mx
        book.c.setStrokeColor(HAIR)
        book.c.line(xx, by + 2, xx, by + 16)
    book.text("planned  ▮▮▮▮", bx, by - 14, "Sans", 7.5, INK2)
    book.text("actual    ▮▮▮▮", bx + bar_w / 2, by - 14, "Sans", 7.5, INK2)
    fields = spec.get("quad_fields") or []
    yy = by - 42
    for f in fields:
        _fieldline(book, bx, yy, bar_w + 60, f)
        yy -= 20
    _scale_row(book, bx, yy - 2, bar_w)
    book.footer()


def draw_gauge2(book, day, spec):
    y = _header(book, day, "Four gauges — read them, then ring the number")
    fields = spec.get("gauge_fields") or ["A", "B", "C", "D"]
    cols = 4
    cw = (book.x1 - book.x0 - 12) / cols
    top = y - 24
    h = 96
    for i, f in enumerate(fields):
        x = book.x0 + i * (cw + 8)
        book.text(f, x, top - 4, "Sans", 7.4, INK2)
        book.c.setStrokeColor(RULE)
        book.c.setLineWidth(0.6)
        book.c.rect(x, top - 24, 18, h, stroke=1, fill=0)
        for t in range(1, 10):
            yy = top - 24 + h * t / 10
            book.c.setStrokeColor(HAIR)
            book.c.line(x, yy, x + 18, yy)
        book.text("10", x - 2, top - 28, "Sans", 6.4, MID)
        book.text("0", x - 2, top - 24 + h - 6, "Sans", 6.4, MID)
        _fieldline(book, x + 24, top - 18, cw - 30, "val")
        _fieldline(book, x + 24, top - 40, cw - 30, "note")
    _fieldline(book, book.x0, top - 148, book.x1 - book.x0, "Morning context (1 line)")
    book.footer()


def draw_ledger(book, day, spec):
    y = _header(book, day, "Ledger — one row per entry")
    cols = spec.get("ledger_cols") or ["Time", "Value", "Note"]
    x = book.x0
    total_w = book.x1 - book.x0
    widths = [total_w * (0.78 ** i) for i in range(len(cols))]
    widths = [w * 0.9 for w in widths]
    widths[-1] = total_w - sum(widths[:-1]) - 8
    cx = x
    for c, w in zip(cols, widths):
        book.text(c[:16], cx + 2, y - 12, "Sans", 7.2, MID)
        cx += w + 6
    cx = x
    for w in widths:
        book.c.setStrokeColor(RULE)
        book.c.setLineWidth(0.5)
        book.c.line(cx, y - 18, cx + w, y - 18)
        cx += w + 6
    yy = y - 30
    for r in range(12):
        cx = x
        for w in widths:
            book.dotted_field(cx + 2, yy, w - 6)
            cx += w + 6
        yy -= 22
    book.footer()


def draw_bucket(book, day, spec):
    y = _header(book, day, "Bucket — how full did it get today?")
    bx, by = book.x0 + 60, y - 36
    bw = 88
    bh = 150
    book.c.setStrokeColor(INK2)
    book.c.setLineWidth(0.7)
    book.c.setStrokeColor(RULE)
    book.c.rect(bx, by, bw, bh, stroke=1, fill=0)
    for i in range(10):
        yy = by + bh * i / 10
        book.c.setStrokeColor(HAIR)
        book.c.line(bx, yy, bx + bw, yy)
    book.text("0", bx + bw + 10, by - 6, "Sans", 7, MID)
    book.text("10", bx + bw + 10, by + bh - 8, "Sans", 7, MID)
    triad = spec.get("triad") or ["Food", "Heat", "Stress"]
    tx = bx + bw + 40
    book.text("Triad ticks", tx, by + bh - 6, "Sans", 7.4, INK2)
    yy = by + bh - 28
    for t in triad:
        book.c.setStrokeColor(RULE)
        book.c.rect(tx, yy - 10, 12, 12, stroke=1, fill=0)
        book.text(t, tx + 18, yy - 8, "Sans", 7.2, MID)
        yy -= 26
    _fieldline(book, tx, yy - 8, 150, "Other")
    _fieldline(book, bx, by - 28, bw + 60, "What filled it")
    _fieldline(book, bx, by - 48, bw + 60, "What helped")
    book.text("30-day pattern → month page", bx, by - 68, "Sans", 6.6, MID)
    book.footer()


def draw_trail(book, day, spec):
    y = _header(book, day, "Contamination trail — trace the nodes")
    nodes = spec.get("trail_nodes") or []
    n = len(nodes)
    bw = (book.x1 - book.x0 - 16) / max(n - 1, 1)
    y0 = y - 22
    for i, node in enumerate(nodes):
        x = book.x0 + i * bw
        book.c.setFillColor(WASH)
        book.c.setStrokeColor(INK2)
        book.c.setLineWidth(0.6)
        book.c.setStrokeColor(RULE)
        book.c.circle(x, y0, 11, stroke=1, fill=1)
        if i < n - 1:
            book.c.setStrokeColor(HAIR)
            book.c.setLineWidth(0.6)
            book.c.line(x + 12, y0, x + bw - 12, y0)
        book.text(node[:14], x - 24, y0 - 22, "Sans", 6.6, MID)
    book.text("Tick the nodes you crossed today, then the hidden list.", book.x0, y0 - 42, "Sans", 7.2, INK2)
    hidden = ["Soups", "Sauces", "Oats", "Spice blends", "Deli slicer", "Shared jars"]
    yy = y0 - 62
    for i, h in enumerate(hidden):
        x = book.x0 + (i % 3) * ((book.x1 - book.x0) / 3)
        book.c.setStrokeColor(RULE)
        book.c.rect(x, yy - 10, 12, 12, stroke=1, fill=0)
        book.text(h[:16], x + 18, yy - 8, "Sans", 7, MID)
        if i % 3 == 2:
            yy -= 28
    _fieldline(book, book.x0, yy - 20, book.x1 - book.x0, "Symptom after (3 items max)")
    _fieldline(book, book.x0, yy - 40, book.x1 - book.x0 - 60, "Note")
    book.footer()


def draw_wire(book, day, spec):
    y = _header(book, day, "Wire — two numbers, one dot")
    rows = spec.get("wire_rows") or ["Stress 0-10", "GI 0-10", "Food note"]
    box_w = (book.x1 - book.x0 - 30) / 2
    x0, x1 = book.x0, book.x0 + box_w
    for i, r in enumerate(rows[:2]):
        yy = y - 24 - i * 60
        book.text(r, x0, yy, "Sans", 7.6, INK2)
        for t in range(11):
            bx = x0 + 14 + t * (box_w - 26) / 10
            book.c.setStrokeColor(RULE)
            book.c.line(bx, yy - 12, bx, yy - 2)
        book.text("0", x0 + 10, yy - 34, "Sans", 6.6, MID)
        book.text("10", x0 + box_w - 18, yy - 34, "Sans", 6.6, MID, "right")
        book.c.setFillColor(INKK)
        book.c.circle(x0 + box_w * 0.5, yy - 7, 2.2, stroke=0, fill=1)
    _fieldline(book, x0, y - 152, x1, rows[2] if len(rows) > 2 else "Food note")
    book.text("Join tonight's dots on the weekly wiring map.", x1 + 20, y - 24, "Sans", 7, MID)
    book.text("Same grid, different ink: the map is the month.", x1 + 20, y - 44, "Sans", 7, MID)
    book.footer()


def draw_ladder(book, day, spec):
    y = _header(book, day, "Ladder — step, note, next")
    steps = spec.get("ladder_steps") or ["Step 1", "Step 2", "Step 3"]
    yy = y - 26
    for i, s in enumerate(steps):
        book.c.setStrokeColor(RULE)
        book.c.setLineWidth(0.5)
        book.c.rect(book.x0, yy - 26, 16, 26, stroke=1, fill=0)
        book.text(str(i + 1), book.x0 + 4, yy - 12, "Sans", 8, MID)
        _fieldline(book, book.x0 + 24, yy - 10, book.x1 - book.x0 - 24, s)
        yy -= 42
    for t in range(4):
        yy -= 4
        book.text(f"Gate {'G Y R'[t]}", book.x0, yy, "Sans", 7, MID)
        book.dotted_field(book.x0 + 60, yy, book.x1 - book.x0 - 60)
        yy -= 18
    book.footer()


def draw_wave(book, day, spec):
    y = _header(book, day, "Wave — plot the reading, keep the line")
    series = spec.get("wave_series") or ["A", "B"]
    box_w = (book.x1 - book.x0 - 12)
    yy = y - 28
    for i, s in enumerate(series):
        book.text(s, book.x0, yy, "Sans", 7.6, INK2)
        book.c.setStrokeColor(RULE)
        book.c.setLineWidth(0.5)
        book.c.rect(book.x0, yy - 46, box_w, 40, stroke=1, fill=0)
        for t in range(1, 10):
            xx = book.x0 + box_w * t / 10
            book.c.setStrokeColor(HAIR)
            book.c.line(xx, yy - 46, xx, yy - 6)
            book.c.setStrokeColor(HAIR)
            book.c.line(book.x0, yy - 46 + 40 * t / 10, book.x0 + box_w, yy - 46 + 40 * t / 10)
        for pt in (0.2, 0.5, 0.8):
            book.c.setFillColor(INKK)
            book.c.circle(book.x0 + box_w * pt, yy - 26, 2.4, stroke=0, fill=1)
        _fieldline(book, book.x0, yy - 62, box_w, "Exertion window")
        yy -= 82
    book.footer()


def draw_cards(book, day, spec):
    y = _header(book, day, "Cards — one card at a time")
    fields = spec.get("card_fields") or ["Field", "Field"]
    ch = 106
    yy = y - 14
    for i in range(2):
        cy = yy - i * (ch + 14)
        _bub(book, book.x0, cy, book.x1 - book.x0, ch)
        book.text(f"Card {i + 1}", book.x0 + 10, cy + ch - 14, "Sans", 7.6, INK2)
        inner = ch - 34
        step = inner / len(fields)
        for j, f in enumerate(fields):
            _fieldline(book, book.x0 + 14, cy + ch - 34 - j * step, book.x1 - book.x0 - 34, f)
    book.footer()


def draw_script(book, day, spec):
    y = _header(book, day, "Script — four sentences before you speak")
    fields = spec.get("script_fields") or ["A", "B", "C", "D"]
    yy = y - 30
    for f in fields:
        book.text(f, book.x0, yy, "Sans", 7.6, INK2)
        book.dotted_field(book.x0 + 130, yy, book.x1 - book.x0 - 150)
        yy -= 26
    book.text("Rehearsal:", book.x0, yy - 6, "Sans", 7.4, MID)
    for t in range(5):
        xx = book.x0 + 70 + t * 20
        book.c.setStrokeColor(RULE)
        book.c.rect(xx, yy - 16, 16, 16, stroke=1, fill=0)
    yy -= 46
    _fieldline(book, book.x0, yy, book.x1 - book.x0, "Doorway used / nearly / skipped")
    book.footer()


def draw_bridge(book, day, spec):
    y = _header(book, day, "Bridge — four spans, one crossing")
    steps = spec.get("bridge_steps") or ["Trigger", "What I did", "Pause", "Repair"]
    n = len(steps)
    bw = (book.x1 - book.x0 - 30) / max(n - 1, 1)
    y0 = y - 30
    for i, s in enumerate(steps):
        x = book.x0 + i * bw
        book.c.setStrokeColor(RULE)
        book.c.setLineWidth(0.6)
        book.c.setStrokeColor(INKK)
        book.c.rect(x, y0, 54, 40, stroke=1, fill=0)
        book.text(s[:9], x + 4, y0 + 18, "Sans", 7.2, MID)
        if i < n - 1:
            book.c.setStrokeColor(HAIR)
            book.c.line(x + 56, y0 + 20, x + bw - 8, y0 + 20)
    yy = y0 - 26
    for i, s in enumerate(steps):
        x = book.x0 + i * bw
        _fieldline(book, x, yy, bw - 10, s)
    book.text("10-minute pause plan:", book.x0, yy - 40, "Sans", 7.4, MID)
    book.dotted_field(book.x0 + 110, yy - 40, book.x1 - book.x0 - 130)
    book.footer()


def draw_dial(book, day, spec):
    y = _header(book, day, "Dial — one number, three fields")
    cx, cy = (book.x0 + book.x1) / 2, y - 80
    r = 54
    book.c.setStrokeColor(RULE)
    book.c.circle(cx, cy, r, stroke=1, fill=0)
    for t in range(0, 11, 2):
        ang = math.radians(90 + t * 18 - 90)
        x1 = cx + (r - 8) * math.cos(ang)
        y1 = cy + (r - 8) * math.sin(ang)
        x2 = cx + r * math.cos(ang)
        y2 = cy + r * math.sin(ang)
        book.c.setStrokeColor(MID)
        book.c.line(x1, y1, x2, y2)
        book.text(str(t), cx + (r + 12) * math.cos(ang) - 4, cy + (r + 12) * math.sin(ang) - 4, "Sans", 6.4, MID)
    ang = math.radians(96)
    book.c.setStrokeColor(INKK)
    book.c.setLineWidth(1.2)
    book.c.line(cx, cy, cx + (r - 14) * math.cos(ang), cy + (r - 14) * math.sin(ang))
    fields = spec.get("dial_fields") or ["Field"]
    yy = y - 176
    for f in fields:
        _fieldline(book, book.x0, yy, book.x1 - book.x0 - 10, f)
        yy -= 20
    book.footer()


def draw_court(book, day, spec):
    y = _header(book, day, "Courtroom — claim, evidence, action")
    cols = spec.get("court_cols") or ["Critic says", "Evidence", "What I did"]
    cw = (book.x1 - book.x0 - 20) / 3
    x = book.x0
    for c, w in zip(cols, [cw] * 3):
        book.text(c, x, y - 14, "Sans", 7.2, MID)
        book.c.setStrokeColor(RULE)
        book.c.line(x, y - 20, x + w, y - 20)
        x += w + 10
    yy = y - 32
    for r in range(11):
        x = book.x0
        for w in [cw] * 3:
            book.dotted_field(x + 2, yy, w - 8)
            x += w + 10
        yy -= 22
    book.text("Cross-exam: what would I say if a friend did this?", book.x0, yy - 8, "Sans", 7, MID)
    book.footer()


def draw_orbit(book, day, spec):
    y = _header(book, day, "Orbit — rings around the launch")
    rings = spec.get("orbit_rings") or ["A", "B", "C"]
    cx, cy = (book.x0 + book.x1) / 2, y - 88
    for i, ring in enumerate(rings):
        rr = 30 + i * 24
        book.c.setStrokeColor(RULE if i < 2 else INKK)
        book.c.setLineWidth(0.5)
        book.c.circle(cx, cy, rr, stroke=1, fill=0)
        book.text(ring[:16], cx + rr + 8, cy - 4, "Sans", 6.8, MID)
    book.c.setFillColor(INKK)
    book.c.circle(cx, cy, 3, stroke=0, fill=1)
    yy = y - 190
    _fieldline(book, book.x0, yy, book.x1 - book.x0 - 10, "This week's launch action")
    _fieldline(book, book.x0, yy - 22, book.x1 - book.x0 - 10, "What I learned")
    book.footer()


def draw_wheel(book, day, spec):
    y = _header(book, day, "Wheel — four quarters of the day")
    rings = spec.get("wheel_rings") or ["Morning", "Midday", "Afternoon", "Night"]
    cx, cy = (book.x0 + book.x1) / 2, y - 84
    r = 66
    for i, ring in enumerate(rings):
        a0 = math.radians(90 - i * 90)
        a1 = math.radians(90 - (i + 1) * 90)
        pts = [(cx, cy)]
        for t in range(0, 21):
            a = a0 + (a1 - a0) * t / 20
            pts.append((cx + (r - 12) * math.cos(a), cy + (r - 12) * math.sin(a)))
        book.c.setFillColor(WASH if i % 2 == 0 else Color(0.90, 0.90, 0.90))
        book.c.setStrokeColor(RULE)
        book.c.setLineWidth(0.5)
        book.c.setFillColor(WASH if i % 2 == 0 else Color(0.90, 0.90, 0.90))
        path = book.c.beginPath()
        path.moveTo(*pts[0])
        for p in pts[1:]:
            path.lineTo(*p)
        path.close()
        book.c.drawPath(path, stroke=1, fill=1)
        mid = (a0 + a1) / 2
        book.text(ring[:10], cx + (r - 34) * math.cos(mid) - 20, cy + (r - 34) * math.sin(mid) - 4, "Sans", 6.8, MID)
    book.c.setStrokeColor(RULE)
    book.c.circle(cx, cy, r, stroke=1, fill=0)
    _fieldline(book, book.x0, y - 176, book.x1 - book.x0 - 10, "Where you are in the cycle")
    _fieldline(book, book.x0, y - 198, book.x1 - book.x0 - 10, "Note")
    book.footer()


def draw_hist(book, day, spec):
    y = _header(book, day, "Timeline — one bar per day")
    rows = spec.get("hist_rows") or ["Severity", "Bristol", "Ease", "Med (as directed)"]
    bw = (book.x1 - book.x0 - 40)
    book.c.setStrokeColor(RULE)
    book.c.rect(book.x0, y - 120, bw, 100, stroke=1, fill=0)
    for t in range(1, 10):
        xx = book.x0 + bw * t / 10
        book.c.setStrokeColor(HAIR)
        book.c.line(xx, y - 120, xx, y - 20)
    # severity bar drawn as filled column at a pseudo position
    book.c.setFillColor(INK2)
    book.c.rect(book.x0 + bw * 0.5 - 8, y - 112, 16, 60, stroke=0, fill=1)
    book.text("0", book.x0, y - 118, "Sans", 6.6, MID)
    book.text("10", book.x0 + bw - 8, y - 118, "Sans", 6.6, MID, "right")
    yy = y - 140
    for i, f in enumerate(rows):
        _fieldline(book, book.x0, yy, book.x1 - book.x0 - 10, f)
        yy -= 22
    book.footer()


def draw_meter(book, day, spec):
    y = _header(book, day, "Meter — how much did today cost?")
    fields = spec.get("meter_fields") or ["Decision load", "Tier", "One action", "Note"]
    box_w = book.x1 - book.x0
    book.text("Decision load", book.x0, y - 18, "Sans", 7.6, INK2)
    for t in range(11):
        bx = book.x0 + 14 + t * (box_w - 26) / 10
        book.c.setStrokeColor(RULE)
        book.c.line(bx, y - 32, bx, y - 22)
    book.c.setFillColor(INKK)
    book.c.circle(book.x0 + 14 + 6 * (box_w - 26) / 10, y - 27, 2.4, stroke=0, fill=1)
    book.text("0", book.x0 + 8, y - 50, "Sans", 6.6, MID)
    book.text("10", book.x0 + box_w - 16, y - 50, "Sans", 6.6, MID, "right")
    yy = y - 72
    for f in fields[1:]:
        _fieldline(book, book.x0, yy, box_w - 10, f)
        yy -= 22
    # tier chips
    for i, tier in enumerate(["T1 auto", "T2 one-look", "T3 big + 24h"]):
        x = book.x0 + i * (box_w / 3)
        book.c.setStrokeColor(RULE)
        book.c.rect(x, yy - 8, box_w / 3 - 8, 20, stroke=1, fill=0)
        book.text(tier, x + 4, yy, "Sans", 6.6, MID)
    book.footer()


def draw_note(book, day, title="Notes"):
    book.begin()
    book.header_bar("NOTES", title)
    yy = book.y1 - 40
    while yy > book.y0 + 20:
        book.c.setStrokeColor(HAIR)
        book.c.line(book.x0, yy, book.x1, yy)
        yy -= 26
    book.footer()


def draw_review(book, title, rows, blurb=""):
    book.begin()
    y = book.header_bar("REVIEW", title)
    if blurb:
        book.paragraph(blurb, book.x0, y - 8, book.x1 - book.x0, "Sans", 8.5, 12, INK2)
        y -= 40
    yy = y - 10
    for r in rows:
        _fieldline(book, book.x0, yy, book.x1 - book.x0 - 10, r)
        yy -= 26
    book.footer()


def draw_clinic(book, spec):
    book.begin()
    y = book.header_bar("CLINIC BRIEF", "What the record shows")
    rows = [
        "What felt most consistent:",
        "What changed this month:",
        "What I want to ask (1-3 questions):",
        "Comments from my care team:",
    ]
    yy = y - 10
    for r in rows:
        _fieldline(book, book.x0, yy, book.x1 - book.x0 - 10, r)
        yy -= 30
    book.text("Records only. This book gives no advice, interpretation, or treatment plan.", book.x0, yy - 6, "Sans", 7, MID)
    book.footer()
