#!/usr/bin/env python3
"""ART KIT — batch 4 smooth/elegant drawing infrastructure.

Everything here draws with smooth mathematics rather than polyline approximations:
  catmull_rom_path  — cubic Bezier spline through control points (C1 continuous)
  log_spiral_path   — logarithmic/golden spiral (nautilus)
  nautilus          — chambered shell: spiral + septa + membrane
  phyllotaxis       — golden-angle dot packing (sunflower/seed heads)
  moon              — true terminator (half-ellipse), 8 phases
  catenary          — hanging chain / string-light curves
  spike_star        — star with 4-point diffraction spikes
  wave_field_smooth — overlapping smooth ocean swells with foam claws
Journal typographic system: eyebrow / display / ornament_rule / date_slot /
dots_scale / check_row / leaf_rule — shared by all five journals.
"""
from __future__ import annotations
import math
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch

INK = HexColor("#1A1A1A")
MUTED = HexColor("#5C5C5C")
SOFT = HexColor("#8A8A8A")
RULE = HexColor("#C5C5C5")
GUIDE_CREAM = HexColor("#B4B4B4")   # dark-tint guides for cream paper (v1 lesson)
GUIDE_WHITE = HexColor("#C8C8C8")   # slightly lighter ok on white paper


# ─────────────────────────────────────────────
# SMOOTH CURVES
# ─────────────────────────────────────────────
def catmull_rom_path(c, pts, closed=False, tension=1.0):
    """Draw a smooth curve through pts via Catmull-Rom converted to cubic Beziers."""
    p = c.beginPath()
    P = list(pts)
    if len(P) < 3:
        p.moveTo(*P[0]); p.lineTo(*P[-1]); c.drawPath(p, stroke=1, fill=0); return
    if closed:
        P = [P[-1]] + P + [P[0], P[1]]
    else:
        P = [P[0]] + P + [P[-1]]
    p.moveTo(P[1][0], P[1][1])
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        k = tension / 6.0
        c1 = (p1[0] + k * (p2[0] - p0[0]), p1[1] + k * (p2[1] - p0[1]))
        c2 = (p2[0] - k * (p3[0] - p1[0]), p2[1] - k * (p3[1] - p1[1]))
        p.curveTo(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    if closed:
        p.close()
    c.drawPath(p, stroke=1, fill=0)
    return p


def log_spiral_points(cx, cy, r0, growth, theta_start, theta_end, steps=220, dir=1):
    """Points along r = r0 * e^(growth*theta). Returns list of (x,y)."""
    pts = []
    if theta_end < theta_start: theta_end = theta_start
    for i in range(steps + 1):
        t = theta_start + (theta_end - theta_start) * i / steps
        r = r0 * math.exp(growth * t)
        pts.append((cx + r * math.cos(dir * t), cy + r * math.sin(dir * t)))
    return pts


def draw_smooth_polyline(c, pts, step=2):
    p = c.beginPath(); p.moveTo(*pts[0])
    for pt in pts[1:]: p.lineTo(*pt)
    c.drawPath(p, stroke=1, fill=0)


def nautilus(c, cx, cy, R, growth=0.18, chambers=9, lw=1.1, dir=1):
    """Chambered nautilus: septa walls + inner spiral + outer membrane."""
    import random as _r
    rng = _r.Random(int(R * 1000 + chambers))
    th_max = math.log(R / (R * 0.04)) / growth
    # septa
    c.setLineWidth(lw)
    for i in range(1, chambers + 1):
        t = th_max * i / (chambers + 1)
        r = R * 0.04 * math.exp(growth * t)
        pts = log_spiral_points(cx, cy, R * 0.04, growth, t - 0.16, t + 0.16, 12, dir)
        inner = []
        for (x, y) in pts:
            f = 0.62
            inner.append((cx + (x - cx) * f, cy + (y - cy) * f))
        catmull_rom_path(c, pts + inner[::-1], closed=True)
    # spiral spine
    spine = log_spiral_points(cx, cy, R * 0.04, growth, 0, th_max, 260, dir)
    draw_smooth_polyline(c, spine)
    # outer membrane = offset spiral
    mem = []
    for (x, y) in spine:
        ang = math.atan2(y - cy, x - cx)
        rr = math.hypot(x - cx, y - cy) + R * 0.055
        mem.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    catmull_rom_path(c, mem)
    # aperture lip
    ex, ey = mem[-1]
    c.setLineWidth(lw + 0.3)
    p = c.beginPath()
    p.moveTo(ex - R * 0.02 * dir, ey)
    p.curveTo(ex + R * 0.10, ey - R * 0.02, ex + R * 0.10, ey + R * 0.10, ex - R * 0.01, ey + R * 0.09)
    c.drawPath(p, stroke=1, fill=0)
    c.setLineWidth(lw)


def phyllotaxis(c, cx, cy, n, r_max, dot_r=None, angle=137.508, lw=None, dots=True):
    """Golden-angle packing. dots=True fills small circles; else returns points."""
    pts = []
    for i in range(n):
        t = i / max(1, n - 1)
        r = r_max * math.sqrt(t)
        a = math.radians(angle) * i
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    if dots:
        for i, (x, y) in enumerate(pts):
            t = i / max(1, n - 1)
            rr = dot_r if dot_r else r_max * 0.055 * (1.15 - 0.5 * t)
            c.circle(x, y, rr, stroke=1, fill=0)
    return pts


def moon(c, cx, cy, r, phase, lw=1.0):
    """phase 0=new .. 0.5=full .. 1=new. True terminator via half-ellipse."""
    c.setLineWidth(lw)
    c.circle(cx, cy, r, stroke=1, fill=0)
    k = math.cos(2 * math.pi * phase)          # 1 new, -1 full
    rx = abs(k) * r
    p = c.beginPath()
    if 0 <= phase < 0.25 or 0.75 < phase <= 1:  # crescent: terminator bulges toward lit side
        side = 1 if phase < 0.5 else -1
        p.moveTo(cx, cy - r)
        p.curveTo(cx - side * rx * 1.3333, cy - r / 3, cx - side * rx * 1.3333, cy + r / 3, cx, cy + r)
    else:                                       # gibbous: terminator bulges away
        side = -1 if phase < 0.5 else 1
        p.moveTo(cx, cy - r)
        p.curveTo(cx - side * rx * 1.3333, cy - r / 3, cx - side * rx * 1.3333, cy + r / 3, cx, cy + r)
    c.drawPath(p, stroke=1, fill=0)


def catenary(c, x0, x1, y_anchor, depth, lw=1.0, segments=60):
    """Hanging-chain curve between two points."""
    import random as _r
    p = c.beginPath()
    for i in range(segments + 1):
        t = i / segments
        x = x0 + (x1 - x0) * t
        y = y_anchor - depth * (1 - (2 * t - 1) ** 2)
        if i == 0: p.moveTo(x, y)
        else: p.lineTo(x, y)
    c.setLineWidth(lw)
    c.drawPath(p, stroke=1, fill=0)


def spike_star(c, x, y, r, spike=2.6, lw=0.6):
    """Star circle with 4-point diffraction spikes."""
    c.setLineWidth(lw)
    c.circle(x, y, r, stroke=1, fill=0)
    s = r * spike
    for dx, dy in ((1, 0), (0, 1)):
        c.line(x - s * dx, y - s * dy, x + s * dx, y + s * dy)


def wave_field_smooth(c, cx, cy, w, h, rows, rng, lw=1.1):
    """Overlapping smooth swells; each crest ends in a curling foam claw."""
    for i in range(rows):
        y0 = cy - h / 2 + h * (i + 0.5) / rows
        amp = h / rows * (0.55 if i % 2 else 0.8)
        pts = []
        for s in range(46):
            t = s / 45
            x = cx - w / 2 + w * t
            env = math.sin(math.pi * min(1, max(0, (t - 0.04) / 0.92)))
            y = y0 + amp * 0.5 * math.sin(t * math.pi * (2.2 + (i % 3)) + i) * env
            pts.append((x, y))
        catmull_rom_path(c, pts)
        # foam claw at crest
        px, py = pts[10 + (i * 7) % 20]
        pts2 = [(px - w * 0.010, py), (px - w * 0.004, py + h * 0.012),
                (px + w * 0.006, py + h * 0.016), (px + w * 0.010, py + h * 0.004)]
        catmull_rom_path(c, pts2)
        for d in range(3):
            qx = px + w * 0.012 + d * w * 0.008
            qy = py + h * 0.010 - d * h * 0.004
            c.circle(qx, qy, w * 0.0022, stroke=1, fill=0)


# ─────────────────────────────────────────────
# JOURNAL TYPOGRAPHIC SYSTEM
# ─────────────────────────────────────────────
def eyebrow(c, x, y, text, tracking=2.4, color=SOFT, size=6.5, font="Inter-Light"):
    c.setFont(font, size); c.setFillColor(color)
    widths = [c.stringWidth(ch, font, size) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    sx = x - total / 2
    for ch, w in zip(text, widths):
        c.drawString(sx, y, ch); sx += w + tracking
    return total

def eyebrow_left(c, x, y, text, tracking=2.4, color=SOFT, size=6.5, font="Inter-Light"):
    c.setFont(font, size); c.setFillColor(color)
    for ch in text:
        c.drawString(x, y, ch)
        x += c.stringWidth(ch, font, size) + tracking

def display(c, x, y, text, size=15, color=INK, font="Cormorant-Light", centered=True):
    c.setFont(font, size); c.setFillColor(color)
    (c.drawCentredString if centered else c.drawString)(x, y, text)

def diamond(c, x, y, s=2.2, color=INK):
    p = c.beginPath()
    p.moveTo(x, y + s); p.lineTo(x + s, y); p.lineTo(x, y - s); p.lineTo(x - s, y)
    p.close()
    c.setFillColor(color)
    c.drawPath(p, stroke=0, fill=1)

def ornament_rule(c, x1, x2, y, color=RULE, with_diamond=True):
    c.setStrokeColor(color); c.setLineWidth(0.5)
    c.line(x1, y, x2, y)
    if with_diamond:
        mid = (x1 + x2) / 2
        c.setFillColor(color)
        diamond(c, mid, y, 2.0, color)
        c.setFillColor(INK)

def date_slot(c, x_right, y, label="DATE"):
    eyebrow_left(c, x_right - 1.55 * inch, y + 2, label, size=5.5)
    c.setStrokeColor(GUIDE_CREAM); c.setLineWidth(0.5)
    c.line(x_right - 1.05 * inch, y, x_right, y)
    for i in (0.38, 0.72):
        c.line(x_right - 1.05 * inch + i * 1.05 * inch, y, x_right - 1.05 * inch + i * 1.05 * inch + 8, y)

def dots_scale(c, x_left, y, n=5, r=5.2, gap=13, end_labels=None, color=None):
    c.setStrokeColor(color or SOFT); c.setLineWidth(0.9)
    for i in range(n):
        c.circle(x_left + i * gap + r, y, r, stroke=1, fill=0)
    if end_labels:
        c.setFont("Inter-Light", 5.5); c.setFillColor(SOFT)
        c.drawString(x_left - 4, y - 8, end_labels[0])
        c.drawRightString(x_left + n * gap + r + 4, y - 8, end_labels[1])

def check_row(c, x, y, items, size=7.5, gap=None, box=7, color=SOFT, col_w=None):
    c.setFont("Inter", size); c.setFillColor(INK)
    step = gap or col_w
    for i, it in enumerate(items):
        c.setStrokeColor(color); c.setLineWidth(0.7)
        c.rect(x + i * step, y - 1, box, box, stroke=1, fill=0)
        c.setFillColor(INK)
        c.drawString(x + i * step + box + 5, y, it)

def write_lines(c, x0, x1, y_top, n, gap=20, color=GUIDE_CREAM, weight=0.45):
    c.setStrokeColor(color); c.setLineWidth(weight)
    y = y_top
    for _ in range(n):
        c.line(x0, y, x1, y); y -= gap
    return y

def leaf_rule(c, x1, x2, y, color=RULE):
    """Hairline that thins visually via a tiny center gap flanked by diamonds."""
    mid = (x1 + x2) / 2; half = (x2 - x1) / 2
    c.setStrokeColor(color); c.setLineWidth(0.5)
    c.line(x1, y, mid - 6, y); c.line(mid + 6, y, x2, y)
    diamond(c, mid, y, 1.8, color); c.setFillColor(INK)

def margins(w, h, page_num, top=0.78, bottom=0.72, inner=0.72, outer=0.55):
    """Recto/verso-aware margins. page_num is 1-based folio."""
    recto = page_num % 2 == 1
    left = inner if recto else outer
    right = outer if recto else inner
    return left * inch, w - right * inch, h - top * inch, bottom * inch   # L R T B in points


# ─────────────────────────────────────────────
# CONSTELLATIONS (approximate real positions; y-up, 0..1; mag = brightness)
# ─────────────────────────────────────────────
CONSTELLATIONS = [
    ("URSA MAJOR", "the great bear", [
        (0.98, 0.88, 1.8), (0.90, 0.62, 2.4), (0.66, 0.58, 2.4), (0.58, 0.72, 3.3),
        (0.46, 0.76, 1.8), (0.32, 0.84, 2.2), (0.10, 0.96, 1.9)],
     [(0,1),(1,2),(2,3),(3,0),(3,4),(4,5),(5,6)],
     [("Dubhe",0),("Merak",1),("Alioth",4),("Alkaid",6)]),
    ("ORION", "the hunter", [
        (0.24, 0.94, 0.5), (0.66, 0.92, 1.6), (0.44, 0.62, 1.7), (0.50, 0.60, 1.7),
        (0.56, 0.58, 2.2), (0.42, 0.24, 2.1), (0.72, 0.22, 0.2), (0.45, 1.08, 3.4)],
     [(0,2),(0,3),(1,4),(2,3),(3,4),(2,5),(4,6),(0,7),(1,7)],
     [("Betelgeuse",0),("Rigel",6),("belt",3)]),
    ("CASSIOPEIA", "the queen", [
        (0.10, 0.60, 3.4), (0.30, 0.38, 2.7), (0.50, 0.60, 2.4), (0.70, 0.36, 2.2), (0.90, 0.56, 2.3)],
     [(0,1),(1,2),(2,3),(3,4)],
     [("Caph",4),("Schedar",3),("Ruchbah",1)]),
    ("CYGNUS", "the swan", [
        (0.50, 0.96, 1.2), (0.50, 0.62, 2.2), (0.50, 0.10, 3.0), (0.16, 0.72, 2.9), (0.84, 0.70, 3.8)],
     [(0,1),(1,2),(3,1),(1,4)],
     [("Deneb",0),("Albireo",2)]),
    ("SCORPIUS", "the scorpion", [
        (0.86, 0.92, 2.6), (0.82, 0.80, 2.3), (0.88, 0.68, 2.9), (0.74, 0.58, 1.1),
        (0.62, 0.50, 2.8), (0.52, 0.40, 2.3), (0.42, 0.30, 3.0), (0.32, 0.22, 3.6),
        (0.24, 0.14, 3.3), (0.14, 0.08, 1.6), (0.08, 0.04, 2.7)],
     [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10)],
     [("Antares",3),("Shaula",9)]),
    ("LYRA", "the lyre", [
        (0.50, 0.92, 0.6), (0.42, 0.60, 3.5), (0.44, 0.48, 3.1), (0.58, 0.46, 4.0), (0.60, 0.58, 3.1), (0.47, 0.76, 4.2)],
     [(0,5),(5,1),(1,2),(2,3),(3,4),(4,1)],
     [("Vega",0)]),
    ("CRUX", "the southern cross", [
        (0.50, 0.10, 0.8), (0.50, 0.92, 1.6), (0.82, 0.48, 1.3), (0.28, 0.38, 2.8)],
     [(0,1),(2,3)],
     [("Acrux",0),("Gacrux",1)]),
    ("LEO", "the lion", [
        (0.24, 0.22, 1.4), (0.28, 0.42, 3.5), (0.34, 0.55, 2.0), (0.38, 0.68, 3.4),
        (0.47, 0.74, 3.9), (0.56, 0.70, 3.0), (0.54, 0.36, 3.3), (0.63, 0.44, 2.6), (0.88, 0.52, 2.1)],
     [(0,1),(1,2),(2,3),(3,4),(4,5),(5,8),(8,7),(7,6),(6,0)],
     [("Regulus",0),("Denebola",8),("Algieba",2)]),
    ("GEMINI", "the twins", [
        (0.34, 0.90, 1.6), (0.54, 0.86, 1.2), (0.40, 0.62, 3.0), (0.48, 0.44, 3.0),
        (0.74, 0.28, 1.9), (0.28, 0.34, 2.9), (0.22, 0.26, 3.3)],
     [(0,2),(2,3),(3,1),(3,4),(2,5),(5,6)],
     [("Castor",0),("Pollux",1),("Alhena",4)]),
    ("TAURUS", "the bull", [
        (0.56, 0.42, 0.9), (0.64, 0.60, 3.5), (0.48, 0.58, 3.7), (0.68, 0.50, 3.8),
        (0.60, 0.34, 3.4), (0.86, 0.74, 1.7), (0.28, 0.16, 3.0), (0.76, 0.30, 3.6)],
     [(0,1),(1,5),(0,2),(0,3),(3,7),(2,6),(0,4)],
     [("Aldebaran",0),("El Nath",5),("M45 Pleiades",7)]),
    ("URSA MINOR", "the little bear", [
        (0.50, 0.96, 2.0), (0.48, 0.80, 4.3), (0.42, 0.68, 4.2), (0.50, 0.56, 3.0),
        (0.58, 0.46, 4.3), (0.66, 0.34, 4.4), (0.76, 0.26, 4.3)],
     [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6)],
     [("Polaris",0)]),
    ("AQUILA", "the eagle", [
        (0.50, 0.50, 0.8), (0.50, 0.64, 2.7), (0.50, 0.36, 3.7), (0.24, 0.72, 3.0), (0.76, 0.70, 3.5)],
     [(0,1),(0,2),(0,3),(0,4)],
     [("Altair",0),("Tarazed",1)]),
]

def draw_constellation(c, cx, cy, size, idx, lw=0.8):
    """Render one constellation plate: magnitude stars, thin lines, tracked labels."""
    name, latin, stars, lines, labels = CONSTELLATIONS[idx % len(CONSTELLATIONS)]
    span = size * 0.78
    x0, y0 = cx - span / 2, cy - span / 2
    pts = [(x0 + sx * span, y0 + sy * span) for (sx, sy, m) in stars]
    mags = [m for (_, _, m) in stars]
    c.setStrokeColor(INK)
    # faint coordinate ring
    c.setLineWidth(0.4); c.setFillColor(INK)
    c.circle(cx, cy, size * 0.46, stroke=1, fill=0)
    for t in range(12):
        a = math.pi * t / 6
        c.line(cx + size * 0.44 * math.cos(a), cy + size * 0.44 * math.sin(a),
               cx + size * 0.46 * math.cos(a), cy + size * 0.46 * math.sin(a))
    # lines
    c.setLineWidth(lw * 0.8)
    for i, j in lines:
        c.line(pts[i][0], pts[i][1], pts[j][0], pts[j][1])
    # stars
    for (x, y), m in zip(pts, mags):
        r = max(1.5, 8.2 - m * 1.7) * size / 300
        if m <= 1.6:
            spike_star(c, x, y, r, spike=2.4, lw=0.55)
        else:
            c.setLineWidth(0.7)
            c.circle(x, y, r, stroke=1, fill=0)
    # labels
    c.setFont("Inter-Light", 5.5); c.setFillColor(MUTED)
    for text, i in labels:
        c.drawString(pts[i][0] + 6, pts[i][1] + 4, text)
    # title
    eyebrow(c, cx, y0 - 16, name, size=7)
    display(c, cx, y0 - 29, latin, size=10, color=MUTED)
