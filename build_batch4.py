#!/usr/bin/env python3
"""
BATCH 4 — NINE RISING-NICHE PRODUCTS (elegant/smooth generation)

JOURNALS (5):
  1. Settle              — somatic / nervous-system regulation   6×9, 172pp, cream, $14.99
  2. The Middle Season   — perimenopause tracker                 6×9, 160pp, white, $16.99
  3. The Dopamine Menu   — ADHD dopamine-menu journal            6×9, 150pp, cream, $13.99
  4. The Slow Page       — slow-living seasonal journal          6×9, 144pp, cream, $15.99
  5. The 75 Soft Journal — 75 Soft challenge tracker             6×9,  96pp, cream, $12.99

COLORING (4) — smooth spline/phyllotaxis/spiral art via art_kit:
  6. Cozy Corners     — cozy spaces              8.5×11, 104pp, white, $10.99
  7. Botanical Ink    — fine-line botanicals     8.5×11, 104pp, white, $11.99
  8. Celestial Atlas  — celestial fine-line      8.5×11, 104pp, white, $11.99
  9. Tidal Ink        — oceancore / jellyfish    8.5×11, 104pp, white, $11.99

Usage:
    python build_batch4.py                 # all nine
    python build_batch4.py --product settle
"""
from __future__ import annotations
import argparse, math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

import build_nine_products as B
import art_kit as K

RELEASE = B.RELEASE.parent / "release4"
ASSETS = B.RELEASE.parent / "assets4"
AUTHOR = B.AUTHOR
INK, MUTED, SOFT, RULE = B.INK, B.MUTED, B.SOFT, B.RULE

# ══════════════════════════════════════════════
# SHARED JOURNAL FURNITURE
# ══════════════════════════════════════════════
def jheader(c, w, h, pn, kicker, title, sub=None):
    L, R, T, Bt = K.margins(w, h, pn)
    K.eyebrow(c, (L + R) / 2, T - 2, kicker)
    K.display(c, (L + R) / 2, T - 20, title, size=15)
    if sub:
        K.display(c, (L + R) / 2, T - 33, sub, size=9, color=MUTED)
    K.ornament_rule(c, (L + R) / 2 - 60, (L + R) / 2 + 60, T - (44 if sub else 32))
    return L, R, T - (62 if sub else 50), Bt

def jfolio(c, w, pn):
    c.setFillColor(SOFT); c.setFont("Inter-Light", 7)
    c.drawCentredString(w / 2, 20, str(pn))

def front_matter(c, w, h, title_lines, subtitle, edition, blurb, tips_lines, how_title, begin_note):
    pn = 0
    B.title_page(c, w, h, " ".join(title_lines).title(), subtitle, edition); pn += 1
    B.copyright_page(c, w, h, " ".join(title_lines).title(), blurb); pn += 1
    L, R, T, Bt = 0.9 * inch, w - 0.9 * inch, h - 0.85 * inch, 0.75 * inch
    K.display(c, w / 2, T, how_title, size=16); T -= 16
    K.ornament_rule(c, w / 2 - 40, w / 2 + 40, T); T -= 26
    for a, b in tips_lines:
        c.setFillColor(INK); c.setFont("Inter-Medium", 8.5); c.drawString(L, T, a)
        c.setFillColor(MUTED); c.setFont("Inter-Light", 7.8)
        lines = B.wrap_text(c, b, "Inter-Light", 7.8, R - L - 14)
        ty = T - 12
        for ln in lines:
            c.drawString(L + 12, ty, ln); ty -= 10.5
        T = ty - 13
    c.showPage(); pn += 1
    B.begin_page(c, w, h, begin_note); pn += 1
    return pn

def closing(c, w, h, l1, l2):
    K.display(c, w / 2, h * 0.55, l1, size=19)
    K.display(c, w / 2, h * 0.50, l2, size=10.5, color=MUTED)
    K.ornament_rule(c, w / 2 - 44, w / 2 + 44, h * 0.46)
    B.draw_centered(c, f"— {AUTHOR}", w / 2, 0.55 * inch, "Inter-Light", 8, SOFT)
    c.showPage()

def build_journal(path, title, N, plan_fn):
    """plan_fn(c, w, h) must draw exactly N-1 pages (incl. front matter).
       Closing page is drawn here. Asserts N before save."""
    w, h = 6 * inch, 9 * inch
    c = canvas.Canvas(str(path), pagesize=(w, h))
    c.setTitle(title); c.setAuthor(AUTHOR)
    pn = plan_fn(c, w, h)
    assert pn == N - 1, f"{title}: plan drew {pn} pages, expected {N-1}"
    closing(c, w, h, *JOURNAL_CLOSINGS[path.stem])
    pn += 1
    assert pn == N, f"{title}: total {pn} != {N}"
    c.save()
    print(f"   wrote {path} ({pn} pages)")
    return pn

JOURNAL_CLOSINGS = {
    "settle_interior": ("You settled.", "Not fixed. Settled."),
    "middle_interior": ("You kept the data.", "Now it speaks for you."),
    "dopamine_interior": ("You ordered well.", "Most days, anyway."),
    "slow_interior": ("You did it slowly.", "That was the whole point."),
    "soft_interior": ("75 days, softened.", "Stronger, and kinder."),
}


# ══════════════════════════════════════════════
# 1. SETTLE — somatic regulation (172pp)
# ══════════════════════════════════════════════
SETTLE_TOOLS = [
    ("PHYSIOLOGICAL SIGH", "Two inhales through the nose, one long exhale through the mouth. Repeat five times. The fastest known dial on the nervous system."),
    ("ORIENT: 5 · 4 · 3 · 2 · 1", "Name five things you see, four you feel, three you hear, two you smell, one you taste. Slowness is the point."),
    ("LONG EXHALE", "In for four, out for eight. Ten rounds. Exhaling longer than you inhale tells the body the danger has passed."),
    ("WEIGHT & PRESS", "Heavy blanket, hands pressed together, or back against a wall. Deep pressure invites the body to land."),
    ("BILATERAL TAP", "Alternate slow taps on left and right shoulders or thighs. Thirty seconds each side. Stay with the rhythm."),
    ("FEET ON THE FLOOR", "Both soles down. Press gently. Notice three points of contact. Feel held by the ground."),
    ("HUM & VIBRATE", "Hum one low note for ten seconds. Feel it in your chest and jaw. The vagus nerve listens."),
    ("TEMPERATURE SHIFT", "Cool water on the wrists or face, or warm tea in both hands. Temperature is a state-changer."),
]

def settle_daily(c, w, h, pn):
    L, R, T, Bt = jheader(c, w, h, pn, "TODAY'S SETTLE", "Daily page")
    K.date_slot(c, R, T + 6)
    T -= 6
    # before state
    c.setFont("Inter-Medium", 8); c.setFillColor(INK)
    c.drawString(L, T, "State before")
    K.dots_scale(c, L + 78, T - 1, 5, end_labels=("revved", "settled")); T -= 22
    # body check row
    c.setFont("Inter-Medium", 8); c.drawString(L, T, "Where I notice it")
    K.check_row(c, L + 92, T, ["jaw", "shldr", "chest", "gut", "hands"], size=6.8, gap=47); T -= 24
    K.leaf_rule(c, L, R, T + 6); T -= 8
    # sensation description
    K.eyebrow_left(c, L, T, "THE SENSATION, IN MY OWN WORDS", size=5.5); T -= 8
    T = K.write_lines(c, L, R, T - 4, 5, gap=21) - 8
    # what helped
    K.eyebrow_left(c, L, T, "WHAT HELPED (EVEN A LITTLE)", size=5.5); T -= 8
    T = K.write_lines(c, L, R, T - 4, 3, gap=21) - 8
    # after state + minutes
    c.setFont("Inter-Medium", 8); c.setFillColor(INK); c.drawString(L, T, "State after")
    K.dots_scale(c, L + 68, T - 1, 5, end_labels=("revved", "settled"))
    c.setFont("Inter-Light", 7); c.setFillColor(SOFT)
    c.drawRightString(R, T, "minutes spent:  ____")
    jfolio(c, w, pn); c.showPage()

def settle_weekly(c, w, h, pn, wk):
    L, R, T, Bt = jheader(c, w, h, pn, f"WEEK {wk} · REGULATION REVIEW", "Looking for patterns")
    for label, n in (("What dysregulated me most this week", 3),
                     ("What actually brought me back", 3),
                     ("One pattern I notice", 2)):
        K.eyebrow_left(c, L, T, label.upper(), size=5.8); T -= 8
        T = K.write_lines(c, L, R, T - 4, n, gap=20) - 9
    K.eyebrow_left(c, L, T, "MY TOP THREE TOOLS, RANKED", size=5.8); T -= 16
    for i in range(3):
        c.setFillColor(INK); c.setFont("Cormorant-Light", 13)
        c.drawString(L, T, f"{i+1}.")
        c.setStrokeColor(K.GUIDE_CREAM); c.setLineWidth(0.45); c.line(L + 18, T, R, T)
        T -= 22
    jfolio(c, w, pn); c.showPage()

def settle_tool(c, w, h, pn, idx):
    name, body = SETTLE_TOOLS[idx % len(SETTLE_TOOLS)]
    L, R, T, Bt = K.margins(w, h, pn)
    K.eyebrow(c, w / 2, T - 2, f"TOOL {idx % len(SETTLE_TOOLS) + 1:02d} · PRACTICE CARD")
    K.display(c, w / 2, T - 22, name.title(), size=16)
    K.ornament_rule(c, w / 2 - 52, w / 2 + 52, T - 34)
    T -= 56
    B.draw_paragraph(c, body, L + 6, T, "Inter-Light", 8.5, R - L - 12, 13.5, MUTED)
    T -= 16 + 13.5 * (len(B.wrap_text(c, body, "Inter-Light", 8.5, R - L - 12)) + 1)
    T -= 10
    # breathing circles ornament
    cy = T - 40
    c.setStrokeColor(SOFT); c.setLineWidth(0.9)
    for i, r in enumerate((34, 24, 14)):
        c.circle(w / 2, cy, r, stroke=1, fill=0)
    K.diamond(c, w / 2, cy, 2.0)
    T = cy - 62
    K.eyebrow_left(c, L, T, "NOTES FROM PRACTICING THIS", size=5.8); T -= 8
    K.write_lines(c, L, R, T - 4, 4, gap=21)
    jfolio(c, w, pn); c.showPage()

def plan_settle(c, w, h):
    pn = front_matter(c, w, h, ["SETTLE"],
        "A Somatic Journal for Settling Your Nervous System", "172 undated pages",
        "One settling page a day, eight practice cards, and a weekly pattern review. "
        "Somatic journaling is not about fixing feelings — it's about noticing states in the "
        "body and finding what returns you to yourself. Not a substitute for therapy or medical care.",
        [("Daily settle", "State before and after, where you feel it in the body, what helped."),
         ("Practice cards", "Eight gentle regulation tools — breath, orientation, pressure, temperature."),
         ("Weekly review", "Patterns, triggers, and your personal top three tools, ranked."),
         ("No streaks", "Miss a day, come back. The body keeps learning either way.")],
        "How to use this journal", "arrive here")
    tool_slots = {5 + 20 * k for k in range(8)}
    weekly_slots = {15 + 21 * k for k in range(8)}
    wk = 0
    for i in range(167):
        if i in tool_slots:
            settle_tool(c, w, h, pn, sorted(tool_slots).index(i)); pn += 1
        elif i in weekly_slots:
            wk += 1; settle_weekly(c, w, h, pn, wk); pn += 1
        else:
            settle_daily(c, w, h, pn); pn += 1
    return pn


# ══════════════════════════════════════════════
# 2. THE MIDDLE SEASON — perimenopause tracker (160pp, WHITE paper)
# ══════════════════════════════════════════════
MS_SYMPTOMS = ["hot flash", "night sweat", "poor sleep", "brain fog", "headache",
               "joint ache", "low energy", "irritable", "weepy", "bloating", "libido", "other:"]

def ms_daily(c, w, h, pn, day):
    L, R, T, Bt = jheader(c, w, h, pn, f"DAILY LOG · DAY {day}", "The Middle Season")
    K.date_slot(c, R, T + 6)
    c.setFont("Inter-Light", 7); c.setFillColor(SOFT)
    c.drawString(L, T + 2, "cycle day (if any):  ______")
    T -= 12
    # symptom grid — 2 columns of circles
    K.eyebrow_left(c, L, T, "SYMPTOMS TODAY (CIRCLE ALL)", size=5.8); T -= 16
    col2 = L + (R - L) / 2
    for i, s in enumerate(MS_SYMPTOMS):
        x = L if i % 2 == 0 else col2
        y = T - (i // 2) * 17
        c.setStrokeColor(SOFT); c.setLineWidth(0.8)
        c.circle(x + 4.5, y + 2.5, 4.5, stroke=1, fill=0)
        c.setFillColor(INK); c.setFont("Inter", 7.6)
        c.drawString(x + 14, y, s)
    T -= 6 * 17 + 6
    # intensity
    c.setFont("Inter-Medium", 8); c.setFillColor(INK)
    c.drawString(L, T, "Overall intensity")
    K.dots_scale(c, L + 88, T - 1, 5, end_labels=("mild", "severe")); T -= 24
    K.leaf_rule(c, L, R, T + 8); T -= 4
    # context row
    K.eyebrow_left(c, L, T, "CONTEXT", size=5.8); T -= 15
    K.check_row(c, L, T, ["slept ___ hrs", "caffeine", "alcohol", "moved", "stress"], size=6.8, gap=64); T -= 24
    # notes
    K.eyebrow_left(c, L, T, "NOTES FOR THE DOCTOR FILE", size=5.8); T -= 8
    K.write_lines(c, L, R, T - 4, 3, gap=20, color=K.GUIDE_WHITE)
    jfolio(c, w, pn); c.showPage()

def ms_weekly(c, w, h, pn, wk):
    L, R, T, Bt = jheader(c, w, h, pn, f"WEEK {wk} · PATTERN", "What the week said")
    # mini heat grid — 7 day squares to shade
    K.eyebrow_left(c, L, T, "SHADE EACH DAY'S OVERALL INTENSITY", size=5.8); T -= 8
    sq = (R - L - 6 * 8) / 7
    c.setFont("Inter-Light", 6); c.setFillColor(SOFT)
    for d in range(7):
        x = L + d * (sq + 8)
        c.setStrokeColor(K.GUIDE_WHITE); c.setLineWidth(0.7)
        c.rect(x, T - sq, sq, sq, stroke=1, fill=0)
        c.drawCentredString(x + sq / 2, T - sq - 9, "MTWTFSS"[d])
    T -= sq + 26
    for label in ("This week's dominant symptom", "Possible trigger I noticed", "What genuinely helped"):
        K.eyebrow_left(c, L, T, label.upper(), size=5.8); T -= 8
        T = K.write_lines(c, L, R, T - 4, 2, gap=20, color=K.GUIDE_WHITE) - 8
    jfolio(c, w, pn); c.showPage()

def ms_monthly(c, w, h, pn, mo):
    L, R, T, Bt = jheader(c, w, h, pn, f"MONTH {mo} · REVIEW", "Four weeks, one page")
    for label, n in (("The dominant pattern this month", 3),
                     ("Better weeks and why", 2), ("Worse weeks and why", 2)):
        K.eyebrow_left(c, L, T, label.upper(), size=5.8); T -= 8
        T = K.write_lines(c, L, R, T - 4, n, gap=20, color=K.GUIDE_WHITE) - 9
    K.eyebrow_left(c, L, T, "QUESTIONS FOR MY NEXT APPOINTMENT", size=5.8); T -= 8
    K.write_lines(c, L, R, T - 4, 4, gap=20, color=K.GUIDE_WHITE)
    jfolio(c, w, pn); c.showPage()

def plan_middle(c, w, h):
    pn = front_matter(c, w, h, ["THE MIDDLE", "SEASON"],
        "A Perimenopause Journal & Symptom Tracker", "160 undated pages",
        "A calm, private tracker for the middle season: daily symptoms, intensity, sleep, and context; "
        "weekly pattern pages; monthly reviews; and a doctor file that turns 'I've been feeling off' into data. "
        "Not medical advice — a companion for your own records and appointments.",
        [("Daily log", "Twelve common symptoms, intensity scale, sleep and context checkboxes."),
         ("Weekly pattern", "Seven shade-in squares plus triggers and what helped."),
         ("Monthly review", "Dominant patterns and questions for your next appointment."),
         ("Doctor file", "Bring the book. Let it speak in specifics.")],
        "How this tracker works", "begin anywhere")
    day = wk = mo = 0
    for i in range(155):
        day += 1
        if day % 28 == 0:
            mo += 1; ms_monthly(c, w, h, pn, mo); pn += 1
        elif day % 7 == 0:
            wk += 1; ms_weekly(c, w, h, pn, wk); pn += 1
        else:
            ms_daily(c, w, h, pn, day); pn += 1
    return pn


# ══════════════════════════════════════════════
# 3. THE DOPAMINE MENU — ADHD (150pp)
# ══════════════════════════════════════════════
DM_CATS = ["STARTERS", "MAINS", "SIDES", "SPECIALS", "DESSERTS"]

def dm_daily(c, w, h, pn, day):
    L, R, T, Bt = jheader(c, w, h, pn, f"ORDER #{day}", "Today's dopamine")
    c.setFont("Inter-Light", 7); c.setFillColor(SOFT)
    c.drawRightString(R, T + 6, "served at  ____ : ____")
    T -= 10
    K.eyebrow_left(c, L, T, "TODAY I'M ORDERING", size=5.8); T -= 8
    for i in range(3):
        c.setFillColor(SOFT); c.setFont("Inter-Light", 6.5)
        c.drawString(L, T - 9, DM_CATS[i % 5].lower())
        c.setStrokeColor(K.GUIDE_CREAM); c.setLineWidth(0.45)
        c.line(L + 52, T - 8, R, T - 8)
        T -= 24
    T -= 2
    c.setFont("Inter-Medium", 8); c.setFillColor(INK)
    c.drawString(L, T, "Appetite check")
    K.check_row(c, L + 82, T, ["under-stimulated", "just right", "overstimulated"], size=6.8, gap=84); T -= 24
    K.leaf_rule(c, L, R, T + 8); T -= 4
    K.eyebrow_left(c, L, T, "AFTER-TASTE (DID IT HIT THE SPOT?)", size=5.8); T -= 14
    K.dots_scale(c, L + 60, T, 5, end_labels=("meh", "exactly")); T -= 26
    K.eyebrow_left(c, L, T, "CRAVING I NOTICED (NOT HUNGER)", size=5.8); T -= 8
    K.write_lines(c, L, R, T - 4, 2, gap=20)
    jfolio(c, w, pn); c.showPage()

def dm_refresh(c, w, h, pn, n):
    L, R, T, Bt = jheader(c, w, h, pn, f"MENU REFRESH {n:02d}", "Rotate the offerings")
    for label in ("One item that stopped working (retire it)", "One item to promote from specials",
                  "A new starter to test this week"):
        K.eyebrow_left(c, L, T, label.upper(), size=5.8); T -= 8
        T = K.write_lines(c, L, R, T - 4, 2, gap=20) - 9
    K.eyebrow_left(c, L, T, "WHAT I LEARNED ABOUT MY BRAIN THIS CYCLE", size=5.8); T -= 8
    K.write_lines(c, L, R, T - 4, 3, gap=20)
    jfolio(c, w, pn); c.showPage()

def dm_index(c, w, h, pn, part):
    L, R, T, Bt = jheader(c, w, h, pn, "MY MENU", f"Index {part} of 2")
    cats = DM_CATS[:3] if part == 1 else DM_CATS[3:]
    for cat in cats:
        K.eyebrow_left(c, L, T, cat, size=6.5); T -= 8
        T = K.write_lines(c, L, R, T - 4, 3 if part == 1 else 4, gap=19) - 10
    jfolio(c, w, pn); c.showPage()

def dm_menu_explainer(c, w, h, part):
    L, R, T, Bt = K.margins(w, h, 3)
    K.eyebrow(c, w / 2, T, "BUILD YOUR MENU")
    K.display(c, w / 2, T - 20, "The five courses" if part == 1 else "The quiet courses", size=15)
    K.ornament_rule(c, w / 2 - 50, w / 2 + 50, T - 32); T -= 52
    cats = (DM_CATS[:3], DM_CATS[3:])[part - 1]
    blurbs = {
        "STARTERS": "Quick wins under five minutes — a song, cold water, one tidy surface, step outside.",
        "MAINS": "Deep-flow meals — the project, the gym, the hobby that eats an afternoon.",
        "SIDES": "Ten-minute fillers that go beside the hard thing — stretch, sketch, walk the block.",
        "SPECIALS": "Rare treats you deliberately ration — the nice candle, the long bath, the good chocolate.",
        "DESSERTS": "The sneaky ones — scrolling, snoozing, one more episode. Keep them on the menu, portioned.",
    }
    for cat in cats:
        K.eyebrow_left(c, L, T, cat, size=6.2); T -= 9
        B.draw_paragraph(c, blurbs[cat], L, T, "Inter-Light", 8, R - L, 11, MUTED)
        T -= 11 * len(B.wrap_text(c, blurbs[cat], "Inter-Light", 8, R - L)) + 8
        K.eyebrow_left(c, L, T, "MY " + cat, size=5.5); T -= 8
        T = K.write_lines(c, L, R, T - 4, 3, gap=19) - 10
    c.showPage()

def plan_dopamine(c, w, h):
    pn = front_matter(c, w, h, ["THE DOPAMINE", "MENU"],
        "An ADHD Journal for Ordering Your Stimulation", "150 undated pages",
        "The dopamine menu turns regulation into a restaurant you run. Build your starters, mains, sides, "
        "specials and desserts, then order from them daily — appetite check, service time, after-taste rating. "
        "For ADHD, AuDHD, and anyone whose stimulation diet needs a chef.",
        [("The menu", "Five courses, filled in by you, on pages 3–4."),
         ("Daily orders", "Three items a day with category tags, appetite check, after-taste dots."),
         ("Menu refresh", "Every twelve orders, rotate: retire what stopped working, promote what didn't."),
         ("Index", "The last two pages re-copy your working menu as a quick reference.")],
        "How to use this journal", "the kitchen is open")
    dm_menu_explainer(c, w, h, 1); pn += 1
    dm_menu_explainer(c, w, h, 2); pn += 1
    day = 0; refreshes = 0
    for i in range(143):
        if i >= 139:
            dm_index(c, w, h, pn, i - 137); pn += 1
        elif i % 12 == 11:
            refreshes += 1; dm_refresh(c, w, h, pn, refreshes); pn += 1
        else:
            day += 1; dm_daily(c, w, h, pn, day); pn += 1
    return pn


# ══════════════════════════════════════════════
# 4. THE SLOW PAGE — slow living (144pp)
# ══════════════════════════════════════════════
SLOW_SEASONS = [("SPRING", "waking"), ("SUMMER", "abundance"),
                ("AUTUMN", "release"), ("WINTER", "rest")]

def slow_season_emblem(c, w, h, T, idx):
    cx, cy = w / 2, T - 74
    c.setStrokeColor(INK)
    if idx == 0:   # spring — phyllotaxis bud
        K.phyllotaxis(c, cx, cy, 90, 52, dots=True)
    elif idx == 1: # summer — sun + rays
        c.setLineWidth(1.0); c.circle(cx, cy, 40, stroke=1, fill=0); c.circle(cx, cy, 26, stroke=1, fill=0)
        for t in range(16):
            a = math.pi * t / 8
            c.line(cx + 52 * math.cos(a), cy + 52 * math.sin(a), cx + 72 * math.cos(a), cy + 72 * math.sin(a))
    elif idx == 2: # autumn — falling leaf spline
        pts = [(cx - 6, cy + 46), (cx - 30, cy + 18), (cx - 12, cy - 6), (cx - 26, cy - 34),
               (cx + 4, cy - 12), (cx + 30, cy - 38), (cx + 22, cy - 2), (cx + 36, cy + 26), (cx + 6, cy + 8)]
        K.catmull_rom_path(c, pts, closed=True)
        c.setLineWidth(0.7); c.line(cx, cy + 30, cx, cy - 24)
    else:          # winter — moon phases row
        for i, ph in enumerate((0.5, 0.625, 0.75, 0.875, 0.0)):
            K.moon(c, cx - 88 + i * 44, cy, 15, ph)

def slow_gate(c, w, h, pn, idx):
    name, word = SLOW_SEASONS[idx]
    L, R, T, Bt = K.margins(w, h, pn)
    K.eyebrow(c, w / 2, T, "SEASON GATE")
    K.display(c, w / 2, T - 24, name, size=26)
    K.display(c, w / 2, T - 40, word, size=10.5, color=MUTED)
    K.ornament_rule(c, w / 2 - 44, w / 2 + 44, T - 56)
    slow_season_emblem(c, w, h, T - 70, idx)
    jfolio(c, w, pn); c.showPage()

def slow_intents(c, w, h, pn, idx):
    name, _ = SLOW_SEASONS[idx]
    L, R, T, Bt = jheader(c, w, h, pn, f"{name} · INTENTIONS", "This season")
    for label in ("One thing to do slowly", "One thing to keep", "One thing to let go of",
                  "A ritual for this season"):
        K.eyebrow_left(c, L, T, label.upper(), size=5.8); T -= 8
        T = K.write_lines(c, L, R, T - 4, 2, gap=20) - 9
    jfolio(c, w, pn); c.showPage()

def slow_daily(c, w, h, pn):
    L, R, T, Bt = jheader(c, w, h, pn, "SLOW PAGE", "Today")
    K.date_slot(c, R, T + 6); T -= 8
    K.eyebrow_left(c, L, T, "ONE THING, SLOWLY", size=5.8); T -= 8
    T = K.write_lines(c, L, R, T - 4, 2, gap=21) - 8
    K.eyebrow_left(c, L, T, "SENSORY DETAIL OF THE DAY", size=5.8); T -= 15
    for lab in ("sight", "sound", "smell", "texture"):
        c.setFillColor(SOFT); c.setFont("Inter-Light", 6.5)
        c.drawString(L, T - 8, lab)
        c.setStrokeColor(K.GUIDE_CREAM); c.setLineWidth(0.45)
        c.line(L + 40, T - 7, R, T - 7)
        T -= 19
    T -= 6
    K.eyebrow_left(c, L, T, "NOT DOING (AND MEANING IT)", size=5.8); T -= 8
    T = K.write_lines(c, L, R, T - 4, 3, gap=19) - 8
    c.setFont("Inter-Light", 7.5); c.setFillColor(SOFT)
    c.drawString(L, T, "tonight, this was enough:  ")
    c.setStrokeColor(SOFT); c.setLineWidth(0.8)
    c.rect(L + 92, T - 2, 8, 8, stroke=1, fill=0)
    # light dial — small arc
    c.setStrokeColor(RULE); c.setLineWidth(0.7)
    c.arc(L, T - 26, L + 40, T + 6, 0, 180)
    c.setFont("Inter-Light", 5.5); c.setFillColor(SOFT)
    c.drawString(L + 46, T - 12, "mark today's light")
    jfolio(c, w, pn); c.showPage()

def slow_sabbath(c, w, h, pn, wk):
    L, R, T, Bt = jheader(c, w, h, pn, f"WEEK {wk} · SABBATH", "A page for rest")
    for label, n in (("One walk I will take", 1), ("One meal, unhurried", 1),
                     ("One hour off screens", 1), ("What rest looked like", 2)):
        K.eyebrow_left(c, L, T, label.upper(), size=5.8); T -= 8
        T = K.write_lines(c, L, R, T - 4, n, gap=20) - 9
    jfolio(c, w, pn); c.showPage()

def plan_slow(c, w, h):
    pn = front_matter(c, w, h, ["THE SLOW", "PAGE"],
        "A Slow-Living Journal for Four Seasons", "144 undated pages",
        "One slow page a day: a single thing done slowly, sensory detail, and a list of what you're "
        "not doing. Season gates for spring, summer, autumn and winter; sabbath pages each week. "
        "Undated — enter whenever you like, in any season.",
        [("The slow page", "One thing, slowly. Four senses. A not-doing list. An enough checkbox."),
         ("Season gates", "Four elegant openers, each with intentions for the season ahead."),
         ("Sabbath pages", "A weekly page for one walk, one meal, one hour, one rest."),
         ("No dates", "The journal doesn't know what day it is. Neither should you, briefly.")],
        "How to use this journal", "unhurried")
    gates = {0: 0, 34: 1, 69: 2, 104: 3}
    wk = 0
    for i in range(135):  # 135 iterations -> 139 pages (gates draw 2 each): 8+16+115 = 139; 4 front + 139 = 143 = N-1
        if i in gates:
            idx = gates[i]
            slow_gate(c, w, h, pn, idx); pn += 1
            slow_intents(c, w, h, pn, idx); pn += 1
            if i == 0: continue
        elif (i + 1) % 7 == 0:
            wk += 1; slow_sabbath(c, w, h, pn, wk); pn += 1
            continue
        else:
            pass
        # default: daily (but gates consumed two slots on their turn)
        if i in gates:
            continue
        if (i + 1) % 7 == 0:
            continue
        slow_daily(c, w, h, pn); pn += 1
    return pn


# ══════════════════════════════════════════════
# 5. THE 75 SOFT JOURNAL (96pp)
# ══════════════════════════════════════════════
SOFT_RULES = ["Ate well (80/20)", "Moved 45 min", "3 L water", "10k steps",
              "10 pages read", "Kind to myself"]

def soft_day(c, w, h, pn, d):
    L, R, T, Bt = K.margins(w, h, pn)
    # day badge
    K.eyebrow(c, w / 2, T, "DAY")
    c.setFillColor(INK); c.setFont("Cormorant-Light", 34)
    c.drawCentredString(w / 2, T - 30, str(d))
    c.setFont("Inter-Light", 6); c.setFillColor(SOFT)
    c.drawCentredString(w / 2, T - 42, "of 75")
    K.ornament_rule(c, w / 2 - 36, w / 2 + 36, T - 52)
    T -= 68
    for r in SOFT_RULES:
        c.setStrokeColor(SOFT); c.setLineWidth(0.9)
        c.rect(L, T - 2, 9, 9, stroke=1, fill=0)
        c.setFillColor(INK); c.setFont("Inter", 8.2)
        c.drawString(L + 16, T, r)
        T -= 20
    T -= 4
    # water droplets — 8 small circles
    c.setFont("Inter-Medium", 7.5); c.setFillColor(INK)
    c.drawString(L, T, "Water glasses")
    c.setStrokeColor(SOFT); c.setLineWidth(0.8)
    for i in range(8):
        K.diamond(c, L + 78 + i * 16, T + 2.5, 3.4, SOFT)
    T -= 24
    K.eyebrow_left(c, L, T, "ONE KIND THING I DID FOR MYSELF", size=5.8); T -= 8
    T = K.write_lines(c, L, R, T - 4, 2, gap=20) - 6
    c.setFont("Inter-Medium", 8); c.setFillColor(INK); c.drawString(L, T, "Energy")
    K.dots_scale(c, L + 46, T - 1, 5, end_labels=("empty", "full"))
    jfolio(c, w, pn); c.showPage()

def soft_weekly(c, w, h, pn, wk):
    L, R, T, Bt = jheader(c, w, h, pn, f"WEEK {wk} · RECAP", "Softly does it")
    K.eyebrow_left(c, L, T, "RULES I KEPT MOST / LEAST", size=5.8); T -= 8
    T = K.write_lines(c, L, R, T - 4, 2, gap=20) - 9
    K.eyebrow_left(c, L, T, "WHAT THE 80% LOOKED LIKE", size=5.8); T -= 8
    T = K.write_lines(c, L, R, T - 4, 2, gap=20) - 9
    K.eyebrow_left(c, L, T, "NEXT WEEK, ONE GENTLE ADJUSTMENT", size=5.8); T -= 8
    K.write_lines(c, L, R, T - 4, 2, gap=20)
    jfolio(c, w, pn); c.showPage()

def soft_marker(c, w, h, pn, title, body):
    L, R, T, Bt = K.margins(w, h, pn)
    K.eyebrow(c, w / 2, T, "MILESTONE")
    K.display(c, w / 2, T - 22, title, size=17)
    K.ornament_rule(c, w / 2 - 40, w / 2 + 40, T - 34); T -= 56
    B.draw_paragraph(c, body, L + 4, T, "Inter-Light", 8.4, R - L - 8, 13, MUTED)
    T -= 34
    K.eyebrow_left(c, L, T, "NOTES", size=5.8); T -= 8
    K.write_lines(c, L, R, T - 4, 4, gap=20)
    jfolio(c, w, pn); c.showPage()

def soft_rules_card(c, w, h, pn):
    L, R, T, Bt = K.margins(w, h, pn)
    K.eyebrow(c, w / 2, T, "THE SIX RULES")
    K.display(c, w / 2, T - 24, "My 75 Soft", size=18)
    K.ornament_rule(c, w / 2 - 44, w / 2 + 44, T - 38); T -= 60
    for i, r in enumerate(SOFT_RULES):
        c.setFillColor(INK); c.setFont("Cormorant-Light", 14)
        c.drawString(L, T, f"{i+1}.")
        c.setFont("Inter", 9); c.drawString(L + 22, T, r)
        c.setStrokeColor(K.GUIDE_CREAM); c.setLineWidth(0.45)
        c.line(L + 22, T - 10, R, T - 10)
        T -= 34
    jfolio(c, w, pn); c.showPage()

def plan_soft(c, w, h):
    pn = front_matter(c, w, h, ["THE 75 SOFT", "JOURNAL"],
        "A Gentler 75-Day Challenge Tracker", "96 pages · 75 days",
        "75 Soft keeps the structure and drops the punishment: eat well 80% of the time, move 45 minutes "
        "five days a week, drink your water, get your steps, read your pages, and — the sixth rule — "
        "be kind to yourself. Track whichever version you committed to.",
        [("The six rules", "Checkboxes daily, water droplets, steps and pages."),
         ("Weekly recaps", "After every seven days, a soft review — no scores, no shame."),
         ("Milestones", "Refresher, halfway, momentum, and finish-line pages along the route."),
         ("Day 76", "The page after the challenge — because that's the real one.")],
        "How this tracker works", "day one")
    extras = {10: ("First foothills", "Ten days in, the novelty is gone and the habit is not yet yours. That gap is normal. Name what is already easier."),
              21: ("Rules refresher", "Read your six rules again. Still aligned? Adjust the wording so each one feels like a promise, not a threat."),
              38: ("Halfway", "Halfway is its own finish line. Write down what the first 37 days changed — in your body, your energy, your self-talk."),
              50: ("The quiet middle", "The unglamorous stretch. Nobody is clapping. Write what you are proving to yourself anyway."),
              60: ("Momentum", "The last stretch is where old habits whisper. Name the whisper, then name your answer."),
              70: ("Finish-line prep", "Five days left. What do you want day 76 to look like? Write the plan here, gently.")}
    soft_rules_card(c, w, h, pn); pn += 1
    wk = 0
    for d in range(1, 76):
        soft_day(c, w, h, pn, d); pn += 1
        if d in extras:
            t, b_ = extras[d]; soft_marker(c, w, h, pn, t, b_); pn += 1
        elif d % 7 == 0 and d < 75:
            wk += 1; soft_weekly(c, w, h, pn, wk); pn += 1
    soft_marker(c, w, h, pn, "Day 76",
                "The challenge ended yesterday. The practice didn't. Write the smallest version of it that you'll keep.")
    pn += 1
    return pn


# ══════════════════════════════════════════════
# COLORING ART GENERATORS
# ══════════════════════════════════════════════
def draw_cozy(c, cx, cy, size, seed, rng=None):
    if not rng: rng = random.Random(seed)
    c.setStrokeColor(INK); c.setLineCap(1); c.setLineJoin(1)
    kind = rng.choice(["nook", "window_rain", "fireplace", "lights", "teapot", "mug_books",
                       "cat", "shelf", "canopy", "record", "candle", "balcony"])
    s = size
    if kind == "nook":
        c.setLineWidth(2.6)
        K.catmull_rom_path(c, [(cx - .30*s, cy - .22*s), (cx - .34*s, cy + .10*s), (cx - .22*s, cy + .18*s),
                               (cx + .22*s, cy + .18*s), (cx + .34*s, cy + .10*s), (cx + .30*s, cy - .22*s)], closed=True)
        c.ellipse(cx - .24*s, cy - .02*s, cx + .24*s, cy + .16*s)
        c.circle(cx + .40*s, cy + .30*s, .05*s)
        c.line(cx + .40*s, cy + .25*s, cx + .40*s, cy - .18*s)
        c.circle(cx + .40*s, cy - .20*s, .025*s)
        for i, bx in enumerate((-0.13, -0.02, 0.09)):
            bw = .11*s - i * .006*s
            c.rect(cx + bx*s, cy - .34*s - i * .05*s, bw, .05*s)
    elif kind == "window_rain":
        c.setLineWidth(2.6)
        c.rect(cx - .26*s, cy - .28*s, .52*s, .56*s)
        c.line(cx, cy - .28*s, cx, cy + .28*s); c.line(cx - .26*s, cy, cx + .26*s, cy)
        c.setLineWidth(1.4)
        for _ in range(22):
            rx = rng.uniform(-.24, .24); ry = rng.uniform(-.26, .26)
            c.line(cx + rx*s, cy + ry*s, cx + rx*s - .012*s, cy + ry*s + .05*s)
        c.setLineWidth(2.2)
        c.rect(cx - .30*s, cy - .32*s, .60*s, .05*s)
        c.circle(cx - .16*s, cy - .20*s, .035*s); c.circle(cx - .16*s, cy - .28*s, .02*s)
    elif kind == "fireplace":
        c.setLineWidth(2.6)
        c.rect(cx - .32*s, cy - .30*s, .64*s, .50*s)
        c.rect(cx - .16*s, cy - .18*s, .32*s, .26*s)
        K.catmull_rom_path(c, [(cx - .07*s, cy - .02*s), (cx - .10*s, cy + .08*s), (cx, cy + .13*s),
                               (cx + .10*s, cy + .07*s), (cx + .07*s, cy - .02*s)])
        c.setLineWidth(2.0)
        c.line(cx - .12*s, cy - .16*s, cx + .12*s, cy - .16*s)
        c.rect(cx - .34*s, cy + .24*s, .68*s, .05*s)
        c.circle(cx - .22*s, cy + .30*s, .028*s); c.circle(cx + .22*s, cy + .30*s, .028*s)
    elif kind == "lights":
        c.setLineWidth(2.2)
        for row, (x0, x1, y0, dep) in enumerate(((-0.40, 0.40, 0.30, 0.16), (-0.30, 0.30, -0.06, 0.12))):
            K.catenary(c, cx + x0*s, cx + x1*s, cy + y0*s, dep*s)
            n = 7
            for i in range(1, n):
                t = i / n
                x = cx + (x0 + (x1 - x0)*t)*s
                y = cy + y0*s - dep*s*(1 - (2*t - 1)**2)
                c.circle(x, y - .018*s, .016*s)
        c.circle(cx, cy - .34*s, .04*s)
    elif kind == "teapot":
        c.setLineWidth(2.6)
        K.catmull_rom_path(c, [(cx - .18*s, cy - .12*s), (cx - .22*s, cy + .04*s), (cx - .10*s, cy + .14*s),
                               (cx + .10*s, cy + .14*s), (cx + .22*s, cy + .04*s), (cx + .18*s, cy - .12*s)], closed=True)
        c.setLineWidth(2.0)
        p = c.beginPath(); p.moveTo(cx + .20*s, cy + .02*s)
        p.curveTo(cx + .34*s, cy + .02*s, cx + .34*s, cy + .12*s, cx + .22*s, cy + .10*s); c.drawPath(p)
        c.circle(cx - .20*s, cy + .02*s, .035*s)
        c.ellipse(cx - .07*s, cy - .16*s, cx + .07*s, cy - .12*s)
        c.setLineWidth(1.4)
        for dx in (-.06, .02):
            sp = K.log_spiral_points(cx + dx*s, cy + .24*s, .008*s, .55, 0, 4.2, 60)
            K.draw_smooth_polyline(c, sp)
    elif kind == "mug_books":
        c.setLineWidth(2.6)
        for i, bw in enumerate((.30, .26, .22)):
            c.rect(cx - bw/2*s, cy - .24*s + i * .07*s, bw*s, .07*s)
        c.circle(cx + .16*s, cy + .06*s, .07*s)
        p = c.beginPath(); p.moveTo(cx + .16*s, cy + .13*s)
        p.curveTo(cx + .26*s, cy + .12*s, cx + .26*s, cy - .02*s, cx + .17*s, cy - .01*s); c.drawPath(p)
        c.setLineWidth(1.4)
        for dx in (.13, .19):
            sp = K.log_spiral_points(cx + dx*s, cy + .22*s, .007*s, .5, 0, 4.0, 50)
            K.draw_smooth_polyline(c, sp)
    elif kind == "cat":
        c.setLineWidth(2.6)
        pts = []
        for a in range(24):
            t = a / 24 * 2 * math.pi
            rr = .22 * (1 + .10 * math.sin(3 * t + 1.2))
            pts.append((cx + rr*s*math.cos(t), cy - .04*s + rr*s*.8*math.sin(t)))
        K.catmull_rom_path(c, pts, closed=True)
        c.circle(cx - .07*s, cy - .20*s, .014*s); c.circle(cx + .07*s, cy - .20*s, .014*s)
        c.setLineWidth(1.6)
        c.arc(cx - .03*s, cy - .235*s, cx + .01*s, cy - .21*s, 0, 180)
        c.arc(cx + .03*s, cy - .235*s, cx + .07*s, cy - .21*s, 0, 180)
        sp = K.log_spiral_points(cx + .20*s, cy - .12*s, .004*s, .9, 0, 5.5, 70)
        K.draw_smooth_polyline(c, sp)
        K.catmull_rom_path(c, [(cx + .22*s, cy - .04*s), (cx + .30*s, cy + .02*s), (cx + .24*s, cy + .08*s)])
    elif kind == "shelf":
        c.setLineWidth(2.4)
        for y, xp in ((.18, .36), (-.10, .30)):
            c.line(cx - xp*s, cy + y*s, cx + xp*s, cy + y*s)
        for x, y, w in ((-.28, .18, .05), (-.10, .18, .06), (.16, .18, .045), (-.20, -.10, .055), (.08, -.10, .05)):
            c.rect(cx + x*s, cy + y*s, w*s, .09*s)
        for dx in (-.25, -.06, .19):
            K.catenary(c, cx + dx*s, cx + dx*s + .02*s, cy + .20*s, -.22*s)
            c.setLineWidth(2.4)
    elif kind == "canopy":
        c.setLineWidth(2.4)
        K.catenary(c, cx - .38*s, cx + .38*s, cy + .34*s, .10*s)
        K.catenary(c, cx - .30*s, cx + .30*s, cy + .30*s, .16*s)
        c.rect(cx - .26*s, cy - .26*s, .52*s, .16*s)
        c.rect(cx - .30*s, cy - .30*s, .05*s, .52*s); c.rect(cx + .25*s, cy - .30*s, .05*s, .52*s)
        K.catmull_rom_path(c, [(cx - .16*s, cy - .10*s), (cx, cy - .02*s), (cx + .16*s, cy - .10*s)])
        K.catmull_rom_path(c, [(cx - .12*s, cy - .16*s), (cx, cy - .11*s), (cx + .12*s, cy - .16*s)])
    elif kind == "record":
        c.setLineWidth(2.4)
        c.rect(cx - .30*s, cy - .16*s, .60*s, .32*s)
        c.circle(cx - .10*s, cy, .13*s); c.circle(cx - .10*s, cy, .085*s); c.circle(cx - .10*s, cy, .012*s)
        c.setLineWidth(1.2)
        c.circle(cx - .10*s, cy, .108*s)
        c.setLineWidth(2.0)
        p = c.beginPath(); p.moveTo(cx + .16*s, cy + .10*s)
        p.curveTo(cx + .26*s, cy + .02*s, cx + .24*s, cy - .12*s, cx + .12*s, cy - .13*s); c.drawPath(p)
    elif kind == "candle":
        c.setLineWidth(2.4)
        c.rect(cx - .05*s, cy - .22*s, .10*s, .30*s)
        c.rect(cx - .055*s, cy - .24*s, .11*s, .03*s)
        K.catmull_rom_path(c, [(cx, cy + .22*s), (cx - .025*s, cy + .26*s), (cx, cy + .31*s), (cx + .025*s, cy + .26*s)], closed=True)
        c.setLineWidth(2.0)
        c.rect(cx - .26*s, cy - .02*s, .16*s, .05*s); c.rect(cx + .10*s, cy - .04*s, .16*s, .05*s)
        c.circle(cx + .18*s, cy + .05*s, .028*s)
    else:  # balcony
        c.setLineWidth(2.4)
        c.rect(cx - .32*s, cy - .26*s, .64*s, .52*s)
        for i in range(7):
            x = cx - .26*s + i * .087*s
            c.line(x, cy - .26*s, x, cy + .26*s)
        c.line(cx - .32*s, cy + .10*s, cx + .32*s, cy + .10*s)
        K.catmull_rom_path(c, [(cx - .12*s, cy + .22*s), (cx, cy + .30*s), (cx + .12*s, cy + .22*s)])
        for i in range(5):
            K.catenary(c, cx - .30*s + i * .07*s, cx - .22*s + i * .07*s, cy + .20*s, -.08*s, lw=1.2)
    B.coloring_border(c, cx, cy, size, weight=2.6)


def draw_botanical(c, cx, cy, size, seed, rng=None):
    if not rng: rng = random.Random(seed)
    c.setStrokeColor(INK); c.setLineCap(1); c.setLineJoin(1)
    kind = rng.choice(["fern", "eucalyptus", "monstera", "sunflower", "dandelion",
                       "poppy", "oak", "lavender", "bouquet", "herbarium", "ginkgo", "seedhead"])
    s = size; c.setLineWidth(1.1)
    if kind == "fern":
        rachis = K.log_spiral_points(cx, cy + .30*s, .004*s, .25, -math.pi/2, -math.pi/2 + 1.15, 40)
        K.draw_smooth_polyline(c, rachis)
        for i, (x, y) in enumerate(rachis[2:-2], 2):
            L = .16*s * (1 - i / len(rachis))
            for d in (-1, 1):
                tipx, tipy = x + d * L * .55, y + L
                K.catmull_rom_path(c, [(x, y), (x + d * L * .28, y + L * .45), (tipx, tipy)], closed=False)
                c.setLineWidth(1.1)
    elif kind == "eucalyptus":
        stem = K.log_spiral_points(cx - .06*s, cy + .34*s, .004*s, .22, -math.pi/2, -math.pi/2 + 1.0, 36)
        K.draw_smooth_polyline(c, stem)
        for i, (x, y) in enumerate(stem[1::2], 1):
            r = .045*s * (1 - i / 26)
            for d in (-1, 1):
                lx, ly = x + d * .07*s, y + .015*s
                c.circle(lx, ly, r)
                c.setLineWidth(0.7); c.line(x, y, lx - d * r * .5, ly - r * .5); c.setLineWidth(1.1)
    elif kind == "monstera":
        outer = []
        for a in range(28):
            t = a / 28 * 2 * math.pi
            rr = .30 * (1 + .07 * math.sin(2 * t))
            outer.append((cx + rr*s*math.cos(t), cy + rr*s*.78*math.sin(t) + .04*s))
        K.catmull_rom_path(c, outer, closed=True)
        c.setLineWidth(0.8); c.line(cx, cy - .20*s, cx, cy + .27*s)
        for (hx, hy, hw, hh) in ((-.13, -.02, .05, .016), (.10, .06, .045, .014), (-.04, -.12, .04, .013), (.02, .16, .035, .012)):
            c.ellipse(cx + (hx - hw)*s, cy + (hy - hh)*s, cx + (hx + hw)*s, cy + (hy + hh)*s)
            c.setLineWidth(1.1)
    elif kind == "sunflower":
        K.phyllotaxis(c, cx, cy + .02*s, 120, .13*s, dot_r=1.6)
        for ring, (n, r0, r1, wd) in enumerate(((14, .17, .26, .028), (14, .26, .33, .024))):
            for i in range(n):
                a = 2 * math.pi * i / n + ring * .22
                mx, my = cx + (r0 + (r1 - r0) / 2)*s*math.cos(a), cy + .02*s + (r0 + (r1 - r0) / 2)*s*.8*math.sin(a)
                c.saveState(); c.translate(mx, my); c.rotate(math.degrees(a))
                c.ellipse(-wd*s, -((r1 - r0)/2)*s*.5, wd*s, ((r1 - r0)/2)*s*.5)
                c.restoreState(); c.setLineWidth(1.1)
    elif kind == "dandelion":
        K.phyllotaxis(c, cx, cy + .16*s, 90, .07*s, dot_r=1.2)
        for i in range(46):
            a = math.pi * (0.08 + 0.84 * i / 45)
            x0, y0 = cx + .08*s*math.cos(a), cy + .16*s + .08*s*math.sin(a)
            x1, y1 = cx + .34*s*math.cos(a), cy + .16*s + .34*s*math.sin(a)
            c.setLineWidth(0.6); c.line(x0, y0, x1, y1)
            c.circle(x1, y1, 1.5, stroke=1, fill=0)
        c.setLineWidth(1.1); c.line(cx, cy + .08*s, cx, cy - .32*s)
    elif kind == "poppy":
        pts = []
        for a in range(20):
            t = a / 20 * 2 * math.pi
            rr = .20 * (1 + .16 * math.sin(3 * t + .4))
            pts.append((cx + rr*s*math.cos(t), cy + .10*s + rr*s*.75*math.sin(t)))
        K.catmull_rom_path(c, pts, closed=True)
        K.phyllotaxis(c, cx, cy + .10*s, 60, .055*s, dot_r=1.1)
        c.setLineWidth(1.2)
        stem = K.log_spiral_points(cx, cy - .32*s, .004*s, .18, math.pi/2, math.pi/2 + .7, 30)
        K.draw_smooth_polyline(c, stem)
    elif kind == "oak":
        pts = []
        for a in range(36):
            t = a / 36 * 2 * math.pi
            rr = .26 * (1 + .16 * math.sin(7 * t) + .05 * math.sin(3 * t))
            pts.append((cx + rr*s*math.cos(t), cy + rr*s*.85*math.sin(t)))
        K.catmull_rom_path(c, pts, closed=True)
        c.setLineWidth(0.7); c.line(cx, cy - .22*s, cx, cy + .22*s)
        for a in (-.6, -.2, .2, .6):
            c.line(cx, cy + .10*s, cx + .16*s*math.sin(a), cy + .10*s + .16*s*math.cos(a))
        c.setLineWidth(1.1)
    elif kind == "lavender":
        c.line(cx, cy + .30*s, cx, cy - .10*s)
        for i in range(16):
            y = cy + .28*s - i * .026*s
            w = .045*s * math.sin(math.pi * min(1, (i + 4) / 20))
            c.ellipse(cx - w, y - .008*s, cx + w, y + .008*s)
        c.line(cx, cy - .10*s, cx - .07*s, cy - .20*s); c.line(cx, cy - .10*s, cx + .07*s, cy - .20*s)
    elif kind == "bouquet":
        for dx, dy in ((-.10, .30), (0, .32), (.10, .30)):
            stem = K.log_spiral_points(cx + dx*s, cy + dy*s, .004*s, .16, -math.pi/2, -math.pi/2 + .8, 26)
            K.draw_smooth_polyline(c, stem)
            hx, hy = stem[-1]
            for k in range(5):
                c.saveState(); c.translate(hx, hy); c.rotate(72 * k)
                c.ellipse(-.022*s, 0, .022*s, .055*s)
                c.restoreState()
            K.phyllotaxis(c, hx, hy, 26, .030*s, dot_r=1.0)
        p = c.beginPath()
        p.moveTo(cx - .05*s, cy + .22*s); p.lineTo(cx + .05*s, cy + .22*s)
        p.lineTo(cx + .02*s, cy + .16*s); p.lineTo(cx - .02*s, cy + .16*s); p.close()
        c.drawPath(p, stroke=1, fill=0)
    elif kind == "herbarium":
        c.setLineWidth(1.0)
        c.rect(cx - .30*s, cy - .34*s, .60*s, .68*s)
        c.setLineWidth(0.5)
        c.rect(cx - .30*s, cy - .34*s, .60*s, .68*s)
        c.setLineWidth(1.0)
        stem = K.log_spiral_points(cx - .04*s, cy + .18*s, .003*s, .2, -math.pi/2, -math.pi/2 + .9, 30)
        K.draw_smooth_polyline(c, stem)
        for (x, y) in stem[2::3]:
            for d in (-1, 1):
                c.circle(x + d * .045*s, y - .01*s, .020*s)
                c.setLineWidth(0.6); c.line(x, y, x + d * .03*s, y); c.setLineWidth(1.0)
        c.rect(cx - .16*s, cy - .28*s, .32*s, .09*s)
        c.setLineWidth(0.7)
        for _ in range(3): c.line(cx - .14*s, cy - .255*s, cx + .14*s, cy - .255*s)
    elif kind == "ginkgo":
        c.setLineWidth(1.1)
        p = c.beginPath()
        p.moveTo(cx, cy - .30*s)
        p.curveTo(cx - .30*s, cy - .10*s, cx - .26*s, cy + .20*s, cx, cy + .26*s)
        p.curveTo(cx + .26*s, cy + .20*s, cx + .30*s, cy - .10*s, cx, cy - .30*s)
        c.drawPath(p, stroke=1, fill=0)
        c.line(cx, cy - .30*s, cx, cy + .24*s)
        c.setLineWidth(0.6)
        for a in (-.7, -.35, 0, .35, .7):
            c.line(cx, cy + .05*s, cx + .24*s*math.sin(a), cy + .05*s + .20*s*math.cos(a) - .02*s)
    else:  # seedhead
        K.phyllotaxis(c, cx, cy, 140, .16*s, dot_r=1.3)
        c.setLineWidth(0.6)
        for i in range(24):
            a = 2 * math.pi * i / 24
            c.line(cx + .17*s*math.cos(a), cy + .17*s*math.sin(a), cx + .23*s*math.cos(a), cy + .23*s*math.sin(a))
    B.coloring_border(c, cx, cy, size, weight=1.2)


def draw_celestial(c, cx, cy, size, seed, rng=None):
    if not rng: rng = random.Random(seed)
    c.setStrokeColor(INK); c.setLineCap(1); c.setLineJoin(1)
    kind = rng.choice(["constellation"] * 6 + ["moon_row", "full_moon", "sun", "saturn",
                                               "galaxy", "comet", "armillary", "meteor",
                                               "cluster", "nebula", "zodiac"])
    s = size
    if kind == "constellation":
        K.draw_constellation(c, cx, cy, s * .96, rng.randrange(len(K.CONSTELLATIONS)))
    elif kind == "moon_row":
        for i, ph in enumerate((0.125, 0.375, 0.5, 0.625, 0.875)):
            K.moon(c, cx - .32*s + i * .16*s, cy, .062*s, ph, lw=1.2)
        K.ornament_rule(c, cx - .30*s, cx + .30*s, cy - .18*s)
        K.eyebrow(c, cx, cy - .30*s, "THE MONTH, IN LIGHT", size=6)
    elif kind == "full_moon":
        c.setLineWidth(1.2); c.circle(cx, cy, .30*s)
        c.setLineWidth(0.7); c.circle(cx, cy, .27*s)
        for (mx, my, mr) in ((-.10, .08, .07), (.06, .14, .05), (.12, -.06, .06), (-.05, -.12, .05)):
            for k in range(14):
                a = 2 * math.pi * k / 14
                c.circle(cx + mx*s + mr*s*.6*math.cos(a), cy + my*s + mr*s*.6*math.sin(a), .006*s)
        for (fx, fy, fr) in ((-.14, -.02, .035), (.16, .10, .028), (.02, .20, .024), (-.08, .18, .02)):
            c.circle(cx + fx*s, cy + fy*s, fr*s)
    elif kind == "sun":
        c.setLineWidth(1.1); c.circle(cx, cy, .14*s); c.circle(cx, cy, .10*s)
        K.phyllotaxis(c, cx, cy, 40, .07*s, dot_r=1.0)
        for i in range(20):
            a = math.pi * i / 10
            long = i % 2 == 0
            r0, r1 = (.17*s, .30*s) if long else (.17*s, .24*s)
            c.setLineWidth(0.9 if long else 0.6)
            K.catmull_rom_path(c, [(cx + r0*math.cos(a), cy + r0*math.sin(a)),
                                   (cx + (r0+r1)/2*math.cos(a + .06), cy + (r0+r1)/2*math.sin(a + .06)),
                                   (cx + r1*math.cos(a), cy + r1*math.sin(a))])
    elif kind == "saturn":
        c.setLineWidth(1.1)
        c.ellipse(cx - .13*s, cy - .17*s, cx + .13*s, cy + .17*s)
        c.setLineWidth(0.7)
        for dy in (-.09, 0, .09):
            c.line(cx - .125*s, cy + dy*s, cx + .125*s, cy + dy*s)
        c.setLineWidth(1.0)
        c.ellipse(cx - .30*s, cy - .07*s, cx + .30*s, cy + .07*s)
        c.ellipse(cx - .26*s, cy - .055*s, cx + .26*s, cy + .055*s)
        c.circle(cx + .26*s, cy + .20*s, .018*s)
    elif kind == "galaxy":
        for arm in (1, -1):
            pts = K.log_spiral_points(cx, cy, .006*s, .34, 0, 4.6 * math.pi / 4.6 * 2.2, 90, dir=arm)
            for j, (x, y) in enumerate(pts[::2]):
                t = j / len(pts[::2])
                c.setLineWidth(0.55)
                c.circle(x, y, max(.5, 2.4 * (1 - t)), stroke=1, fill=0)
        c.circle(cx, cy, .030*s); c.circle(cx, cy, .018*s)
        for _ in range(26):
            c.setLineWidth(0.5)
            c.circle(cx + rng.uniform(-.34, .34)*s, cy + rng.uniform(-.34, .34)*s, rng.uniform(.5, 1.3))
    elif kind == "comet":
        c.setLineWidth(1.0); c.circle(cx + .18*s, cy + .18*s, .05*s)
        K.spike_star(c, cx + .18*s, cy + .18*s, .05*s)
        for i in range(26):
            t = i / 25
            x0 = cx + .13*s - t * .44*s; y0 = cy + .14*s - t * .36*s
            spread = t * .10*s
            c.setLineWidth(0.55)
            c.line(x0, y0 - spread * rng.uniform(.3, 1), x0 - .05*s, y0 - spread * rng.uniform(.3, 1))
    elif kind == "armillary":
        c.setLineWidth(0.9)
        c.circle(cx, cy, .30*s)
        for (rx, ry, rot) in ((.30, .10, 0), (.30, .10, 90), (.22, .22, 30)):
            c.saveState(); c.translate(cx, cy); c.rotate(rot)
            c.ellipse(-rx*s, -ry*s, rx*s, ry*s); c.restoreState()
        c.setLineWidth(0.6); c.line(cx, cy - .34*s, cx, cy + .34*s)
        K.spike_star(c, cx, cy + .30*s, .022*s)
    elif kind == "meteor":
        rx, ry = cx + .20*s, cy + .22*s
        K.spike_star(c, rx, ry, .026*s)
        for i in range(16):
            a = math.pi * (1.05 + .28 * i / 15)
            ln = rng.uniform(.18, .42) * s
            c.setLineWidth(rng.uniform(.5, .9))
            c.line(rx, ry, rx + ln * math.cos(a), ry + ln * math.sin(a))
    elif kind == "cluster":
        K.phyllotaxis(c, cx, cy, 150, .26*s, dot_r=1.5)
        for i in range(8):
            K.spike_star(c, cx + rng.uniform(-.2, .2)*s, cy + rng.uniform(-.2, .2)*s, rng.uniform(.010, .018)*s, lw=.5)
    elif kind == "nebula":
        for _ in range(240):
            gx = rng.gauss(0, .16); gy = rng.gauss(0, .13)
            if abs(gx) > .38 or abs(gy) > .38: continue
            c.setLineWidth(0.5)
            c.circle(cx + gx*s, cy + gy*s, rng.uniform(.4, 1.6))
        for _ in range(6):
            K.spike_star(c, cx + rng.uniform(-.22, .22)*s, cy + rng.uniform(-.18, .18)*s, rng.uniform(.012, .020)*s, lw=.5)
    else:  # zodiac wheel
        c.setLineWidth(1.0); c.circle(cx, cy, .30*s); c.circle(cx, cy, .24*s)
        for i in range(12):
            a = 2 * math.pi * i / 12
            c.setLineWidth(0.6)
            c.line(cx + .24*s*math.cos(a), cy + .24*s*math.sin(a), cx + .30*s*math.cos(a), cy + .30*s*math.sin(a))
            K.diamond(c, cx + .27*s*math.cos(a), cy + .27*s*math.sin(a), 2.2)
        K.spike_star(c, cx, cy, .035*s)
    B.coloring_border(c, cx, cy, size, weight=1.0)


def draw_tidal(c, cx, cy, size, seed, rng=None):
    if not rng: rng = random.Random(seed)
    c.setStrokeColor(INK); c.setLineCap(1); c.setLineJoin(1)
    kind = rng.choice(["jelly", "nautilus", "seahorse", "waves", "starfish",
                       "coral", "kelp", "turtle", "octo", "anemone", "shells", "porthole"])
    s = size
    if kind == "jelly":
        bell = [(cx + a * .001, cy + .10 * s - .001) for a in ()]
        pts = []
        for a in range(19):
            t = math.pi * a / 18
            pts.append((cx + .20*s*math.cos(t), cy + .12*s - .20*s*.75*math.sin(t)))
        K.catmull_rom_path(c, pts + [(cx + .10*s, cy - .06*s), (cx - .10*s, cy - .06*s)], closed=True)
        c.setLineWidth(0.7)
        for k in (-3, -1, 1, 3):
            c.arc(cx + k*.045*s - .02*s, cy - .05*s, cx + k*.045*s + .02*s, cy + .10*s, 0, 180)
        c.setLineWidth(1.0)
        for i, dx in enumerate((-0.12, -0.04, 0.04, 0.12)):
            pts = [(cx + dx*s, cy - .06*s)]
            y = cy - .06*s
            x = cx + dx*s
            for seg in range(5):
                x += (0.018 if seg % 2 == 0 else -0.018) * s * (1 if dx >= 0 else -1)
                y -= .055*s
                pts.append((x, y))
            K.catmull_rom_path(c, pts)
        c.setLineWidth(0.7)
        for _ in range(9):
            c.circle(cx + rng.uniform(-.17, .17)*s, cy + rng.uniform(-.34, -.16)*s, rng.uniform(.5, 1.4))
    elif kind == "nautilus":
        K.nautilus(c, cx, cy, .30 * s, growth=.19, chambers=8, lw=1.0)
    elif kind == "seahorse":
        c.setLineWidth(1.1)
        body = [(cx, cy + .26*s), (cx + .07*s, cy + .20*s), (cx + .09*s, cy + .10*s), (cx + .05*s, cy + .02*s),
                (cx + .08*s, cy - .08*s), (cx + .04*s, cy - .16*s)]
        K.catmull_rom_path(c, body)
        K.catmull_rom_path(c, [(cx - .06*s, cy + .24*s), (cx - .10*s, cy + .18*s), (cx - .06*s, cy + .14*s)])
        sp = K.log_spiral_points(cx + .02*s, cy - .16*s, .004*s, 1.35, math.pi/2, math.pi/2 + 3.4, 60, dir=-1)
        K.draw_smooth_polyline(c, sp)
        c.setLineWidth(0.6)
        for i in range(7):
            y = cy + .20*s - i * .045*s
            c.line(cx - .02*s, y, cx - .07*s, y - .015*s)
    elif kind == "waves":
        K.wave_field_smooth(c, cx, cy, .84*s, .56*s, 4, rng, lw=1.1)
        K.moon(c, cx + .26*s, cy + .30*s, .05*s, 0.75, lw=1.0)
    elif kind == "starfish":
        pts = []
        for a in range(15):
            t = a / 15 * 2 * math.pi
            rr = .28 if a % 3 == 0 else .13
            pts.append((cx + rr*s*math.cos(t), cy + rr*s*.9*math.sin(t)))
        K.catmull_rom_path(c, pts, closed=True)
        K.phyllotaxis(c, cx, cy, 40, .06*s, dot_r=1.0)
        c.setLineWidth(0.6)
        for k in range(5):
            a = math.pi * k / 2.5 - math.pi / 2
            for d in (.10, .16, .22):
                c.circle(cx + d*s*math.cos(a), cy + d*s*.9*math.sin(a), .008*s)
    elif kind == "coral":
        def branch(x, y, ang, ln, depth):
            if depth == 0:
                c.circle(x, y, .006*s); return
            x2, y2 = x + ln * math.cos(ang), y + ln * math.sin(ang)
            c.setLineWidth(max(.5, depth * .35))
            c.line(x, y, x2, y2)
            branch(x2, y2, ang + .5, ln * .72, depth - 1)
            branch(x2, y2, ang - .5, ln * .72, depth - 1)
            c.setLineWidth(1.0)
        branch(cx, cy - .26*s, math.pi/2, .14*s, 4)
    elif kind == "kelp":
        for dx in (-.18, 0, .18):
            K.catenary(c, cx + dx*s - .05*s, cx + dx*s + .05*s, cy + .34*s, .30*s, lw=1.0)
            for i in range(7):
                y = cy + .30*s - i * .085*s
                t = (y - (cy + .04*s)) / .30*s
                x = cx + dx*s + .05*s * math.sin(math.pi * t)
                for d in (-1, 1):
                    c.ellipse(x + d*.026*s - .012*s, y - .006*s, x + d*.026*s + .012*s, y + .006*s)
        c.setLineWidth(0.6)
        for _ in range(8):
            c.circle(cx + rng.uniform(-.3, .3)*s, cy + rng.uniform(-.3, .3)*s, rng.uniform(.8, 2.2))
    elif kind == "turtle":
        shell = []
        for a in range(22):
            t = a / 22 * 2 * math.pi
            rr = .22 * (1 + .04 * math.sin(2 * t))
            shell.append((cx + rr*s*math.cos(t), cy + rr*s*.62*math.sin(t)))
        K.catmull_rom_path(c, shell, closed=True)
        c.setLineWidth(0.7)
        for r in (.08, .14):
            c.ellipse(cx - r*s, cy - r*.62*s, cx + r*s, cy + r*.62*s)
        c.line(cx - .20*s, cy, cx + .20*s, cy); c.line(cx, cy - .13*s, cx, cy + .13*s)
        c.setLineWidth(1.0)
        c.circle(cx + .24*s, cy + .02*s, .045*s)
        for d in (-1, 1):
            K.catmull_rom_path(c, [(cx + d*.10*s, cy - .12*s), (cx + d*.22*s, cy - .20*s), (cx + d*.28*s, cy - .14*s)])
            K.catmull_rom_path(c, [(cx + d*.12*s, cy + .10*s), (cx + d*.24*s, cy + .18*s), (cx + d*.30*s, cy + .14*s)])
    elif kind == "octo":
        head = []
        for a in range(20):
            t = a / 20 * 2 * math.pi
            head.append((cx + .15*s*math.cos(t), cy + .10*s + .13*s*math.sin(t)))
        K.catmull_rom_path(c, head, closed=True)
        c.setLineWidth(1.0)
        for i, dx0 in enumerate((-0.11, -0.04, 0.04, 0.11)):
            pts = [(cx + dx0*s, cy - .01*s)]
            x, y = cx + dx0*s, cy - .01*s
            for seg in range(4):
                x += (0.05 if seg % 2 == 0 else -0.05) * s
                y -= .075*s
                pts.append((x, y))
            K.catmull_rom_path(c, pts)
            c.setLineWidth(0.6)
            for d in range(4):
                c.circle(pts[d][0] + .012*s, pts[d][1] + .012*s, .005*s)
            c.setLineWidth(1.0)
    elif kind == "anemone":
        base = []
        for a in range(16):
            t = a / 16 * 2 * math.pi
            base.append((cx + .12*s*math.cos(t), cy - .18*s + .07*s*math.sin(t)))
        K.catmull_rom_path(c, base, closed=True)
        for i in range(18):
            a = math.pi * (0.1 + 0.8 * i / 17)
            x0, y0 = cx + .10*s*math.cos(a), cy - .16*s - .06*s*math.sin(a)
            x1, y1 = cx + .30*s*math.cos(a), cy - .16*s - .26*s*math.sin(a)
            K.catmull_rom_path(c, [(x0, y0), ((x0+x1)/2 + .02*s, (y0+y1)/2 + .02*s), (x1, y1)])
        K.phyllotaxis(c, cx, cy - .17*s, 30, .05*s, dot_r=.9)
    elif kind == "shells":
        K.nautilus(c, cx - .16*s, cy + .06*s, .17*s, growth=.21, chambers=7, lw=.9)
        scallop = []
        for a in range(15):
            t = math.pi * a / 14
            scallop.append((cx + .16*s + .15*s*math.cos(t + math.pi), cy - .14*s - .15*s*math.sin(t)))
        K.catmull_rom_path(c, scallop)
        c.setLineWidth(0.7)
        for i in range(7):
            a = math.pi * i / 6
            c.line(cx + .16*s, cy - .14*s, cx + .16*s - .15*s*math.cos(a), cy - .14*s - .15*s*math.sin(a))
        K.nautilus(c, cx + .10*s, cy + .02*s, .10*s, growth=.24, chambers=5, lw=.8, dir=-1)
    else:  # porthole
        c.setLineWidth(1.6); c.circle(cx, cy, .32*s)
        c.setLineWidth(0.9); c.circle(cx, cy, .27*s)
        for i in range(10):
            a = 2 * math.pi * i / 10
            c.circle(cx + .295*s*math.cos(a), cy + .295*s*math.sin(a), .012*s)
        bell = [(cx + .10*s*math.cos(math.pi * a / 18), cy + .02*s - .10*s*.8*math.sin(math.pi * a / 18)) for a in range(19)]
        K.catmull_rom_path(c, bell + [(cx + .05*s, cy - .06*s), (cx - .05*s, cy - .06*s)], closed=True)
        c.setLineWidth(0.6)
        for _ in range(7):
            c.circle(cx + rng.uniform(-.2, .2)*s, cy + rng.uniform(-.2, 0)*s, rng.uniform(.8, 2))
    B.coloring_border(c, cx, cy, size, weight=1.1)


# ══════════════════════════════════════════════
# COVER (JPEG) + CONFIG + MAIN
# ══════════════════════════════════════════════
def generate_cover_jpg(path, texture, title_lines, subtitle, badge=None):
    W, H = 1800, 2700
    tex = ImageOps.fit(Image.open(texture).convert("RGB"), (W, H), Image.Resampling.LANCZOS)
    veil = Image.new("RGBA", (W, H), (20, 15, 30, 55))
    img = Image.alpha_composite(tex.convert("RGBA"), veil)
    draw = ImageDraw.Draw(img)
    ft = ImageFont.truetype(str(B.FONTS / "CormorantGaramond-Light.ttf"), 88)
    fs = ImageFont.truetype(str(B.FONTS / "Inter-Light.ttf"), 28)
    fb = ImageFont.truetype(str(B.FONTS / "Inter-Light.ttf"), 22)
    def ct(text, y, font, fill=(247, 241, 230, 255), tr=8):
        chars = [(ch, draw.textbbox((0, 0), ch, font=font)[2]) for ch in text]
        total = sum(w for _, w in chars) + tr * (len(chars) - 1)
        x = (W - total) / 2
        for ch, w in chars:
            draw.text((x, y), ch, font=font, fill=fill)
            x += w + tr
    y = 980
    for line in title_lines:
        ct(line, y, ft, tr=10); y += 110
    draw.rectangle([W//2 - 90, y + 30, W//2 + 90, y + 33], fill=(212, 181, 106, 255))
    bbox = draw.textbbox((0, 0), subtitle, font=fs)
    draw.text(((W - (bbox[2] - bbox[0])) // 2, y + 60), subtitle, font=fs, fill=(247, 241, 230, 220))
    if badge:
        bbox = draw.textbbox((0, 0), badge, font=fb)
        bw = bbox[2] - bbox[0] + 60
        draw.rounded_rectangle([W//2 - bw//2, H - 350, W//2 + bw//2, H - 310], radius=10, fill=(255, 255, 255, 35))
        draw.text(((W - (bbox[2] - bbox[0])) // 2, H - 346), badge, font=fb, fill=(247, 241, 230, 210))
    img.convert("RGB").save(path, "JPEG", quality=90, optimize=True)
    print(f"   wrote {path}")

PRODUCTS4 = {
    "settle": {
        "title": "Settle", "subtitle": "A Somatic Journal for Settling Your Nervous System",
        "trim": (6 * inch, 9 * inch), "pages": 172, "paper": "cream", "price": "$14.99",
        "dir": "settle", "tex_rgb": (126, 138, 120), "tex_seed": 51, "title_lines": ["SETTLE"],
        "categories": "Self-Help > Journaling | Health > Nervous System",
        "keywords": "somatic journal, nervous system regulation journal, grounding journal anxiety, "
                    "polyvagal exercises workbook, body scan journal, vagus nerve stimulation book, dysregulation workbook",
        "desc": "Settle is a somatic journal for anyone whose body holds what the mind can't talk down. "
                "Each daily page asks the same calm questions: your state before, where you notice it in the body, "
                "what helped, and your state after. Eight illustrated practice cards teach gentle regulation tools — "
                "the physiological sigh, orienting, long exhale, weight and pressure, bilateral tapping — and weekly "
                "reviews surface your personal patterns and top three tools. No streaks, no shame, no fixing. "
                "172 undated pages, 6 × 9 in, cream paper. A companion for anxiety, ADHD, trauma recovery, and "
                "anyone learning to live back in their body.",
        "features": ["172 undated pages  ·  6 × 9 in", "8 illustrated regulation practice cards",
                     "Daily before/after state tracking", "Weekly pattern reviews, zero streaks"],
        "badge": "SOMATIC  ·  172 PAGES  ·  GENTLE TOOLS",
    },
    "middle": {
        "title": "The Middle Season", "subtitle": "A Perimenopause Journal & Symptom Tracker",
        "trim": (6 * inch, 9 * inch), "pages": 160, "paper": "white", "price": "$16.99",
        "dir": "middle", "tex_rgb": (172, 116, 98), "tex_seed": 53, "title_lines": ["THE MIDDLE", "SEASON"],
        "categories": "Health > Women's Health | Self-Help > Journaling",
        "keywords": "perimenopause journal, perimenopause symptom tracker, menopause tracking journal, "
                    "hormone symptom log, hot flash tracker, brain fog journal, midlife wellness journal",
        "desc": "The Middle Season is a calm, private tracker for perimenopause — the years everyone talks around. "
                "Daily pages log twelve common symptoms with intensity scales, sleep, and context. Weekly pattern "
                "pages turn seven shaded squares into a picture. Monthly reviews name the dominant pattern, and a "
                "doctor file turns 'I've been feeling off' into specifics you can say out loud in an appointment. "
                "160 undated pages, 6 × 9 in, white paper for crisp grids. Not medical advice — a companion that "
                "keeps your records so you don't have to hold them in your head.",
        "features": ["160 undated pages  ·  6 × 9 in", "12-symptom daily log with intensity scale",
                     "Weekly shade-in pattern grids", "Monthly reviews + doctor file"],
        "badge": "PERIMENOPAUSE  ·  160 PAGES  ·  DATA THAT SPEAKS",
    },
    "dopamine": {
        "title": "The Dopamine Menu", "subtitle": "An ADHD Journal for Ordering Your Stimulation",
        "trim": (6 * inch, 9 * inch), "pages": 150, "paper": "cream", "price": "$13.99",
        "dir": "dopamine", "tex_rgb": (198, 116, 62), "tex_seed": 55, "title_lines": ["THE DOPAMINE", "MENU"],
        "categories": "Self-Help > Journaling | Health > ADHD",
        "keywords": "dopamine menu, adhd journal adults, adhd motivation planner, executive function journal, "
                    "neurodivergent journal, stimulation seeker workbook, adhd regulation tools",
        "desc": "Your brain runs on stimulation. The Dopamine Menu turns regulating it into a restaurant you run. "
                "Build your menu in five courses — starters under five minutes, mains for deep flow, sides for the "
                "ten-minute gaps, rationed specials, and portioned desserts — then order from it daily. Each order "
                "logs your appetite, what you ordered, and the after-taste rating, so you learn what actually feeds "
                "your brain versus what steals from it. Menu refreshes keep the offerings honest, and a two-page "
                "index re-copies your working menu. 150 undated pages, 6 × 9 in, cream paper. For ADHD, AuDHD, and "
                "anyone whose stimulation diet needs a chef.",
        "features": ["150 undated pages  ·  6 × 9 in", "Five-course menu you write yourself",
                     "Daily orders with appetite + after-taste", "Menu refreshes every 12 orders"],
        "badge": "ADHD  ·  150 PAGES  ·  FIVE COURSES",
    },
    "slow": {
        "title": "The Slow Page", "subtitle": "A Slow-Living Journal for Four Seasons",
        "trim": (6 * inch, 9 * inch), "pages": 144, "paper": "cream", "price": "$15.99",
        "dir": "slow", "tex_rgb": (150, 130, 104), "tex_seed": 57, "title_lines": ["THE SLOW", "PAGE"],
        "categories": "Self-Help > Journaling | Self-Help > Motivational",
        "keywords": "slow living journal, seasonal living journal, intentional living notebook, "
                    "mindful living journal, hygge journal, unplugged journal, quiet morning pages",
        "desc": "One page a day, done slowly. The Slow Page asks for less than any journal you've abandoned: one "
                "thing done slowly, four sensory details from the day, a list of what you're deliberately not "
                "doing, and a checkbox that says tonight, this was enough. Four season gates — spring, summer, "
                "autumn, winter — each with intentions and a hand-drawn emblem, plus weekly sabbath pages for one "
                "walk, one unhurried meal, and one hour off screens. 144 undated pages, 6 × 9 in, cream paper. "
                "For anyone recovering from hurry.",
        "features": ["144 undated pages  ·  6 × 9 in", "Four season gates with emblems",
                     "Weekly sabbath pages", "A not-doing list, daily"],
        "badge": "SLOW LIVING  ·  144 PAGES  ·  FOUR SEASONS",
    },
    "soft": {
        "title": "The 75 Soft Journal", "subtitle": "A Gentler 75-Day Challenge Tracker",
        "trim": (6 * inch, 9 * inch), "pages": 96, "paper": "cream", "price": "$12.99",
        "dir": "soft", "tex_rgb": (100, 130, 140), "tex_seed": 59, "title_lines": ["THE 75 SOFT", "JOURNAL"],
        "categories": "Health > Fitness & Dieting | Self-Help > Journaling",
        "keywords": "75 soft journal, 75 soft challenge tracker, 75 day challenge book, soft fitness journal, "
                    "gentle habit tracker, wellness challenge journal, 75 soft workbook women",
        "desc": "75 Soft keeps the structure of the famous challenge and drops the punishment. Eat well 80% of the "
                "time. Move 45 minutes, five days a week. Drink your water. Get your steps. Read your pages. And "
                "the sixth rule — be kind to yourself. This journal tracks all six daily with checkboxes, water "
                "droplets and energy dots, adds a soft weekly recap with no scores and no shame, and marks the "
                "route with refresher, halfway, momentum and finish-line pages. Day 76 gets its own page, because "
                "that's the one that matters. 96 pages, 6 × 9 in, cream paper.",
        "features": ["96 pages  ·  all 75 days + day 76", "Six daily rules + water droplets",
                     "Soft weekly recaps, no scores", "Milestone pages at 21, 38, 60, 70"],
        "badge": "75 SOFT  ·  96 PAGES  ·  KINDER BY DESIGN",
    },
    "cozy": {
        "title": "Cozy Corners", "subtitle": "Cozy Spaces to Color — Warm, Soft & Slow",
        "trim": (8.5 * inch, 11 * inch), "pages": 104, "paper": "white", "price": "$10.99",
        "dir": "cozy", "tex_rgb": (168, 94, 60), "tex_seed": 61, "title_lines": ["COZY", "CORNERS"],
        "categories": "Crafts & Hobbies > Coloring Books for Grown-Ups > Scenes | Self-Help > Stress Management",
        "keywords": "cozy coloring book, cozy spaces coloring book, hygge coloring book adults, "
                    "aesthetic coloring book, cute coloring book adults, reading nook coloring, fall vibes coloring book",
        "desc": "Reading nooks and rainy windows. Fireplaces, teapots, string lights, shelf plants, curled cats and "
                "canopy beds — the coziest corners, drawn with soft rounded lines that are a pleasure to fill. "
                "Every design is a small scene you can finish in one sitting, single-sided so you can frame the "
                "ones you love. 8.5 × 11 in, 104 pages, white paper. Warm drinks optional but recommended.",
        "features": ["Soft rounded one-sitting scenes", "Nooks, lights, cats, teapots, rain",
                     "Single-sided  ·  frame your favorites", "104 pages  ·  8.5 × 11 in"],
        "badge": "COZY  ·  104 PAGES  ·  SOFT LINES",
        "level": ("cozy & warm", [("Soft, rounded lines", "Thick enough for markers, gentle on the eyes."),
                   ("Small scenes", "Every page is one cozy corner, finishable in one sitting."),
                   ("Single-sided", "The back of each design is blank — remove and frame."),
                   ("No rules", "Cozy colors only. Unless you want otherwise.")]),
    },
    "botanical": {
        "title": "Botanical Ink", "subtitle": "Fine-Line Botanicals for Patient Coloring",
        "trim": (8.5 * inch, 11 * inch), "pages": 104, "paper": "white", "price": "$11.99",
        "dir": "botanical", "tex_rgb": (58, 92, 66), "tex_seed": 63, "title_lines": ["BOTANICAL", "INK"],
        "categories": "Crafts & Hobbies > Coloring Books for Grown-Ups > Flowers & Botanical | Arts & Photography > Drawing",
        "keywords": "botanical coloring book fine line, floral coloring book adults, detailed flower coloring book, "
                    "botanical line art coloring, garden coloring book, fern and leaf coloring, plant lover coloring book",
        "desc": "Fine-line botanicals drawn the old way: ferns with every pinna, monstera with true fenestrations, "
                "sunflower and dandelion heads built from real phyllotaxis spirals, herbarium plates with label "
                "boxes and tape corners. Thin, precise linework for colored pencils and fine-tip markers — the "
                "quiet, patient end of the coloring spectrum. Single-sided. 8.5 × 11 in, 104 pages, white paper. "
                "A garden that never wilts.",
        "features": ["True fine-line weight (0.7–1.3 pt)", "Phyllotaxis seed heads & spiral ferns",
                     "Herbarium plates with labels", "Single-sided  ·  104 pages"],
        "badge": "FINE LINE  ·  104 PAGES  ·  BOTANICAL",
        "level": ("fine line", [("Fine, precise lines", "Best with colored pencils and fine-tip markers."),
                   ("Real botany", "Phyllotaxis spirals, fenestrations, true leaf venation."),
                   ("Patient pages", "These reward an unhurried hand."),
                   ("Single-sided", "104 pages, each design frameable.")]),
    },
    "celestial": {
        "title": "Celestial Atlas", "subtitle": "Constellations & Night Skies in Fine Line",
        "trim": (8.5 * inch, 11 * inch), "pages": 104, "paper": "white", "price": "$11.99",
        "dir": "celestial", "tex_rgb": (24, 26, 52), "tex_seed": 65, "title_lines": ["CELESTIAL", "ATLAS"],
        "categories": "Crafts & Hobbies > Coloring Books for Grown-Ups > Mandalas & Patterns | Science > Astronomy",
        "keywords": "celestial coloring book, constellation coloring book, astronomy coloring book adults, "
                    "space coloring book fine line, moon phases coloring, galaxy coloring book, star coloring book intricate",
        "desc": "A night sky you color yourself. Twelve constellation plates drawn from real star positions with "
                "magnitude-scaled stars and diffraction spikes — Orion, Leo, Scorpius, the Dippers and more — plus "
                "moon phases with true terminators, Saturn's rings, spiral galaxies, comets, meteor showers and "
                "nebulae built from hundreds of fine dots. Thin, exact linework for pencils and fine tips. "
                "Single-sided. 8.5 × 11 in, 104 pages, white paper. For stargazers who like their skies quiet.",
        "features": ["12 real constellations, magnitude-scaled", "True-terminator moon phases",
                     "Galaxies, comets, nebulae in fine dots", "Single-sided  ·  104 pages"],
        "badge": "CELESTIAL  ·  104 PAGES  ·  REAL STAR DATA",
        "level": ("fine line", [("Real star charts", "Positions and brightness from the actual sky."),
                   ("Fine lines & dots", "Pencils and fine-tip markers recommended."),
                   ("Learn as you color", "Star names labeled on every plate."),
                   ("Single-sided", "104 pages of quiet night sky.")]),
    },
    "tidal": {
        "title": "Tidal Ink", "subtitle": "Jellyfish & Deep-Sea Life in Fine Line",
        "trim": (8.5 * inch, 11 * inch), "pages": 104, "paper": "white", "price": "$11.99",
        "dir": "tidal", "tex_rgb": (16, 66, 86), "tex_seed": 67, "title_lines": ["TIDAL", "INK"],
        "categories": "Crafts & Hobbies > Coloring Books for Grown-Ups > Animals | Crafts > Ocean & Marine",
        "keywords": "ocean coloring book adults, jellyfish coloring book, sea life coloring fine line, "
                    "underwater coloring book, shell and nautilus coloring, marine life intricate coloring, coastal coloring book",
        "desc": "Drifting jellyfish with ribbon arms, chambered nautiluses drawn from the actual logarithmic "
                "spiral, seahorses, sea turtles, coral fans, kelp forests and smooth rolling waves — the deep "
                "sea rendered in fine, unhurried line. Every curve is a true spline, every spiral real mathematics; "
                "the result pages feel like etchings. Single-sided. 8.5 × 11 in, 104 pages, white paper. "
                "Color it blue. Or don't. The ocean won't mind.",
        "features": ["True-spline jellyfish & waves", "Real logarithmic-spiral nautiluses",
                     "Turtles, seahorses, coral, kelp", "Single-sided  ·  104 pages"],
        "badge": "OCEANCORE  ·  104 PAGES  ·  FINE LINE",
        "level": ("fine line", [("Smooth spline curves", "Every outline flows — no choppy polylines."),
                   ("Real spirals", "Nautiluses follow the actual logarithmic shell curve."),
                   ("Fine tips & pencils", "Linework is delicate; patience is a feature."),
                   ("Single-sided", "104 pages of deep-sea calm.")]),
    },
}

JOURNAL_PLANS = {"settle": plan_settle, "middle": plan_middle, "dopamine": plan_dopamine,
                 "slow": plan_slow, "soft": plan_soft}
COLORING_FNS = {"cozy": draw_cozy, "botanical": draw_botanical,
                "celestial": draw_celestial, "tidal": draw_tidal}


def main():
    parser = argparse.ArgumentParser()
    keys = list(PRODUCTS4.keys())
    parser.add_argument("--product", choices=["all"] + keys, default="all")
    args = parser.parse_args()
    B.register_fonts()
    build_list = keys if args.product == "all" else [args.product]
    for k in build_list:
        (RELEASE / PRODUCTS4[k]["dir"]).mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    print("=" * 60); print("BATCH 4 — NINE RISING-NICHE PRODUCTS"); print("=" * 60)

    for key in build_list:
        p = PRODUCTS4[key]
        d = RELEASE / p["dir"]
        print(f"\n▸ [{key}] {p['title']}")
        tex = ASSETS / f"{p['dir']}_linen.jpg"
        B.make_texture(tex, 3900, 3375, p["tex_rgb"], p["tex_seed"])
        ppi = B.WHITE_PPI if p["paper"] == "white" else B.CREAM_PPI
        if key in JOURNAL_PLANS:
            pages = build_journal(d / f"{p['dir']}_interior.pdf", p["title"], p["pages"], JOURNAL_PLANS[key])
        else:
            level, tips = p["level"]
            pages = B.build_coloring_book(d / f"{p['dir']}_interior.pdf", p["title"], p["subtitle"],
                                          level, tips, p["pages"], COLORING_FNS[key], ppi)
        B.generate_wrap(d / f"{p['dir']}_cover_wrap.pdf", p["trim"], pages, tex,
                        p["title_lines"], p["subtitle"], p["desc"][:250], p["features"], ppi)
        generate_cover_jpg(d / f"{p['dir']}_cover.jpg", tex, p["title_lines"], p["subtitle"], p.get("badge"))
        B.write_text(d / "metadata.txt", f"""TITLE: {p['title']}
SUBTITLE: {p['subtitle']}
AUTHOR: {AUTHOR}
FORMAT: Paperback, {p['trim'][0]/inch}×{p['trim'][1]/inch} in, {p['pages']} pages, B&W interior, {p['paper']} paper, matte, no bleed
PRICE: {p['price']}
CATEGORIES: {p['categories']}
KEYWORDS: {p['keywords']}

DESCRIPTION:
{p['desc']}""")

    B.write_text(RELEASE / "UPLOAD_CHECKLIST_BATCH4.md", "\n".join(
        [f"""## {PRODUCTS4[k]['title']}
1. KDP → Create Paperback
2. Title: {PRODUCTS4[k]['title']} | Subtitle: {PRODUCTS4[k]['subtitle']} | Author: {AUTHOR}
3. Settings: B&W interior, {PRODUCTS4[k]['paper'].upper()} paper, {PRODUCTS4[k]['trim'][0]/inch}×{PRODUCTS4[k]['trim'][1]/inch}, NO bleed, matte
4. Upload {PRODUCTS4[k]['dir']}_interior.pdf + {PRODUCTS4[k]['dir']}_cover_wrap.pdf
5. Price: {PRODUCTS4[k]['price']} | Expanded distribution: ON
6. Preview → approve → order proof → publish
""" for k in keys]))
    print("\nDONE")
    for f in sorted(RELEASE.rglob("*")):
        if f.is_file():
            print(f"  {f.relative_to(RELEASE)}  {f.stat().st_size/1024:8.1f} KB")


if __name__ == "__main__":
    main()
