#!/usr/bin/env python3
"""
NINE NEW PRODUCTS — production build

JOURNALS (3):
  A. "The 5-Minute Dump" — micro-journal, 5.5×8.5, 200pp
  B. "Parallel Lives" — side-by-side journal, 7×10, 160pp
  C. "The Night Pages" — insomnia journal, 5×8, 120pp

COLORING BOOKS (6):
  D. "First Strokes" — BEGINNER, super simple, 8.5×11, 100pp
  E. "Easy Garden" — BEGINNER, simple botanical, 8.5×11, 100pp
  F. "Mosaic Mind" — AMATEUR, geometric mosaics, 8.5×11, 120pp
  G. "Woodland Wonders" — AMATEUR, nature scenes, 8.5×11, 120pp
  H. "Fractal Dreams" — ADVANCED, mathematical fractals, 8.5×11, 140pp
  I. "Architectural Visions" — ADVANCED, intricate buildings, 8.5×11, 140pp

    python build_nine_products.py
    python build_nine_products.py --product dump
    python build_nine_products.py --product parallel
    python build_nine_products.py --product night
    python build_nine_products.py --product firststroke
    python build_nine_products.py --product garden
    python build_nine_products.py --product mosaic
    python build_nine_products.py --product woodland
    python build_nine_products.py --product fractal
    python build_nine_products.py --product architect
"""

from __future__ import annotations
import argparse, math, os, random, zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "fonts"
RELEASE = ROOT / "release3"
ASSETS = ROOT / "assets3"

INK = HexColor("#1A1A1A")
MUTED = HexColor("#5C5C5C")
SOFT = HexColor("#8A8A8A")
RULE = HexColor("#C5C5C5")
CREAM = HexColor("#F7F1E6")
GOLD = HexColor("#D4B56A")
WARM_WHITE = HexColor("#FAF8F5")

YEAR = 2026
AUTHOR = "Quiet Mind Press"
BLEED = 0.125 * inch
CREAM_PPI = 0.0025
WHITE_PPI = 0.002252


# ══════════════════════════════════════════════
# FONTS
# ══════════════════════════════════════════════
def register_fonts():
    mapping = {
        "Inter": FONTS / "Inter-Regular.ttf",
        "Inter-Light": FONTS / "Inter-Light.ttf",
        "Inter-Medium": FONTS / "Inter-Medium.ttf",
        "Inter-SemiBold": FONTS / "Inter-SemiBold.ttf",
        "Cormorant-Light": FONTS / "CormorantGaramond-Light.ttf",
        "Cormorant": FONTS / "CormorantGaramond-Regular.ttf",
        "Cormorant-Medium": FONTS / "CormorantGaramond-Medium.ttf",
        "Cormorant-SemiBold": FONTS / "CormorantGaramond-SemiBold.ttf",
    }
    for name, path in mapping.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing font: {path}")
        pdfmetrics.registerFont(TTFont(name, str(path)))


# ══════════════════════════════════════════════
# DRAWING HELPERS
# ══════════════════════════════════════════════
def draw_centered(c, text, x, y, font, size, color=INK):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawCentredString(x, y, text)

def draw_tracked(c, text, x, y, font, size, tracking=1.4, color=INK):
    c.setFont(font, size)
    c.setFillColor(color)
    widths = [c.stringWidth(ch, font, size) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1 if text else 0)
    sx = x - total / 2
    for ch, w in zip(text, widths):
        c.drawString(sx, y, ch)
        sx += w + tracking

def draw_hairline(c, x1, y, x2, color=GOLD, weight=0.6):
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    c.line(x1, y, x2, y)

def wrap_text(c, text, font, size, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if c.stringWidth(trial, font, size) <= max_width:
            line = trial
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def draw_paragraph(c, text, x, y, font, size, max_width, leading, color=INK, align="left"):
    c.setFillColor(color)
    c.setFont(font, size)
    for line in wrap_text(c, text, font, size, max_width):
        if align == "center": c.drawCentredString(x, y, line)
        else: c.drawString(x, y, line)
        y -= leading
    return y

def draw_checkbox(c, x, y, size=8, tint=INK):
    c.setStrokeColor(tint)
    c.setLineWidth(0.7)
    c.rect(x, y, size, size, stroke=1, fill=0)

def draw_dot_grid(c, x0, y0, x1, y1, color, spacing=5*mm, radius=0.4):
    c.setFillColor(color)
    x = x0
    while x <= x1 + 0.1:
        y = y0
        while y <= y1 + 0.1:
            c.circle(x, y, radius, stroke=0, fill=1)
            y += spacing
        x += spacing

def draw_lined_area(c, x0, y0, x1, y1, color, spacing=20):
    c.setStrokeColor(color)
    c.setLineWidth(0.4)
    y = y1
    while y >= y0:
        c.line(x0, y, x1, y)
        y -= spacing

def page_folio(c, w, num, color=SOFT):
    c.setFillColor(color)
    c.setFont("Inter-Light", 7)
    c.drawCentredString(w / 2, 18, str(num))

def title_page(c, w, h, title, subtitle, edition=""):
    draw_tracked(c, title.upper(), w/2, h*0.58, "Cormorant-Light", 22, tracking=2.8)
    draw_hairline(c, w/2-42, h*0.55, w/2+42, RULE, 0.5)
    draw_centered(c, subtitle, w/2, h*0.52, "Inter-Light", 9, MUTED)
    if edition:
        draw_centered(c, edition, w/2, 48, "Inter-Light", 7.5, SOFT)
    draw_centered(c, AUTHOR.upper(), w/2, 32, "Inter-Light", 6.5, SOFT)
    c.showPage()

def copyright_page(c, w, h, title, blurb):
    y = h * 0.62
    draw_centered(c, title, w/2, y, "Cormorant", 14, INK)
    y -= 28
    y = draw_paragraph(c, blurb, w/2, y, "Inter-Light", 8.5, w*0.62, 13, MUTED, align="center")
    y -= 18
    draw_paragraph(c, f"© {YEAR} {AUTHOR}. All rights reserved.",
                   w/2, y, "Inter-Light", 8, w*0.6, 12, SOFT, align="center")
    c.showPage()

def begin_page(c, w, h, text="whenever you're ready"):
    draw_tracked(c, "BEGIN", w/2, h*0.52, "Cormorant-Light", 18, tracking=6)
    draw_centered(c, text, w/2, h*0.48, "Inter-Light", 9, MUTED)
    c.showPage()

def closing_page(c, w, h, line1, line2):
    draw_centered(c, line1, w/2, h*0.54, "Cormorant-Light", 20, INK)
    draw_centered(c, line2, w/2, h*0.50, "Inter-Light", 10, MUTED)
    draw_centered(c, f"— {AUTHOR}", w/2, 0.55*inch, "Inter-Light", 8, SOFT)
    c.showPage()


# ══════════════════════════════════════════════
# JOURNAL A: THE 5-MINUTE DUMP
# 5.5×8.5, 200 pages, micro-journaling
# ══════════════════════════════════════════════

DUMP_TRIM = (5.5 * inch, 8.5 * inch)
DUMP_PAGES = 200

DUMP_MICROS = [
    ("Brain temperature", "Circle one:", ["Frozen", "Cold", "Lukewarm", "Warm", "Boiling"]),
    ("One word for today", "Write it big:", []),
    ("The thing I keep avoiding", "", []),
    ("Energy audit", "Shade the battery:", []),
    ("If I could only do ONE thing today", "", []),
    ("What's actually urgent vs what feels urgent", "", []),
    ("Body check", "Circle what hurts:", ["Head", "Neck", "Shoulders", "Chest", "Stomach", "Back", "Everything", "Nothing"]),
    ("Permission slip", "Today I give myself permission to:", []),
    ("The smallest possible next step", "", []),
    ("Done list", "Things I already did (even tiny):", []),
    ("Emotional weather", "Draw it:", []),
    ("What would make today 1% better", "", []),
    ("Sensory inventory", "Right now I can:", []),
    ("The thought that keeps looping", "Write it once. Then cross it out:", []),
    ("Capacity check", "Circle one:", ["Empty", "Running on fumes", "Half tank", "Enough", "Full"]),
    ("Three things within arm's reach", "Name them:", []),
    ("What I need but won't ask for", "", []),
    ("Am I hungry? Thirsty? Tired?", "Circle all that apply. Fix one.", []),
    ("The win from yesterday", "Even tiny:", []),
    ("Inbox zero for my brain", "Dump everything here:", []),
    ("What am I performing right now?", "For whom?", []),
    ("Rate the noise level in my head", "1–10:", []),
    ("If this day were a color", "What color and why:", []),
    ("One thing I'm grateful for", "Not because I should be. Because I am.", []),
    ("What would I tell my friend in my situation?", "", []),
    ("The thing I finished today", "Or the thing I started. Both count:", []),
    ("Where does my body hold stress?", "Point to it. Breathe into it.", []),
    ("What's one thing I can control right now?", "", []),
    ("What's one thing I need to let go of?", "", []),
    ("End of dump", "Close the book. You did enough.", []),
]


def draw_dump_page(c, w, h, page_num, micro_idx):
    m = 0.55 * inch
    micro = DUMP_MICROS[micro_idx % len(DUMP_MICROS)]
    title, subtitle, options = micro

    y = h - m
    # page number top corner
    c.setFillColor(RULE)
    c.setFont("Inter-Light", 7)
    c.drawRightString(w - m, y + 8, str(page_num))

    # timer icon — 5 small dots in a row
    c.setFillColor(SOFT)
    for i in range(5):
        c.circle(m + i * 8, y + 10, 2, stroke=0, fill=1)
    c.setFont("Inter-Light", 6)
    c.drawString(m + 48, y + 7, "5 min")

    y -= 12
    # title
    c.setFillColor(INK)
    c.setFont("Cormorant-Medium", 16)
    c.drawString(m, y, title)
    y -= 18

    if subtitle:
        c.setFillColor(MUTED)
        c.setFont("Inter-Light", 9)
        c.drawString(m, y, subtitle)
        y -= 16

    # options as circles to fill
    if options:
        y -= 8
        for opt in options:
            c.setStrokeColor(RULE)
            c.setLineWidth(1.0)
            c.circle(m + 6, y + 3, 5, stroke=1, fill=0)
            c.setFillColor(INK)
            c.setFont("Inter", 9)
            c.drawString(m + 18, y, opt)
            y -= 20
        y -= 8

    # writing space — light lines
    y -= 10
    draw_lined_area(c, m, m + 0.15*inch, w - m, y, HexColor("#E8E8E8"), spacing=24)

    # bottom affirmation
    c.setFillColor(SOFT)
    c.setFont("Inter-Light", 6.5)
    c.drawCentredString(w/2, m - 8, "You don't have to finish. You just have to dump.")

    c.showPage()


def generate_dump(path: Path):
    w, h = DUMP_TRIM
    c = canvas.Canvas(str(path), pagesize=(w, h))
    c.setTitle("The 5-Minute Dump")
    c.setAuthor(AUTHOR)
    pn = 0

    title_page(c, w, h, "The 5-Minute Dump", "Micro-journaling for people who hate journaling", "200 undated pages")
    pn += 1
    copyright_page(c, w, h, "The 5-Minute Dump",
        "Each page takes five minutes or less. No long prompts. No pressure. "
        "Just brain dumps, body checks, and tiny wins. For ADHD, anxiety, depression, "
        "or anyone who wants to journal but can't commit to paragraphs.")
    pn += 1

    # How to use
    y = h - 0.7*inch
    draw_centered(c, "How to use this book", w/2, y, "Cormorant-Light", 16)
    y -= 22
    draw_hairline(c, w/2-28, y, w/2+28, RULE, 0.5)
    y -= 26
    tips = [
        "Open to any page. They're not in order.",
        "Set a timer for 5 minutes. Stop when it rings.",
        "Circle, scribble, write one word, or fill the whole page.",
        "Some pages repeat. That's on purpose. Your answer changes.",
        "There's no wrong way to dump.",
    ]
    for tip in tips:
        c.setFillColor(INK)
        c.setFont("Inter", 8.5)
        c.drawString(0.7*inch, y, "·  " + tip)
        y -= 18
    c.showPage()
    pn += 1

    begin_page(c, w, h, "set a timer. go.")
    pn += 1

    micro_idx = 0
    while pn < DUMP_PAGES - 1:
        pn += 1
        draw_dump_page(c, w, h, pn, micro_idx)
        micro_idx += 1

    closing_page(c, w, h, "You dumped it.", "Now let it go.")
    pn += 1

    c.save()
    print(f"   wrote {path} ({pn} pages)")
    return pn


# ══════════════════════════════════════════════
# JOURNAL B: PARALLEL LIVES
# 7×10, 160 pages, side-by-side comparison
# ══════════════════════════════════════════════

PARALLEL_TRIM = (7 * inch, 10 * inch)
PARALLEL_PAGES = 160

PARALLEL_PAIRS = [
    ("What happened", "How it felt"),
    ("What I said", "What I meant"),
    ("What they said", "What I heard"),
    ("The plan", "What actually happened"),
    ("What I wanted to do", "What I did instead"),
    ("The expectation", "The reality"),
    ("What I showed people", "What was underneath"),
    ("Before", "After"),
    ("The fear", "The evidence"),
    ("What I thought I needed", "What I actually needed"),
    ("The criticism", "The translation"),
    ("What I'm doing", "Why I'm really doing it"),
    ("The should", "The want"),
    ("How I see myself", "How others probably see me"),
    ("The problem", "The smallest solution"),
    ("What exhausts me", "What restores me"),
    ("The loud thought", "The quiet truth"),
    ("My version", "Their version"),
    ("What I lost", "What I gained"),
    ("Today's mask", "Today's face"),
]


def draw_parallel_spread(c, w, h, page_num, pair_idx):
    pair = PARALLEL_PAIRS[pair_idx % len(PARALLEL_PAIRS)]
    left_title, right_title = pair
    m = 0.6 * inch
    mid = w / 2

    # dividing line
    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    c.line(mid, m + 0.1*inch, mid, h - m - 0.1*inch)

    y_top = h - m

    # left header
    c.setFillColor(INK)
    c.setFont("Cormorant-Medium", 13)
    c.drawString(m, y_top, left_title)

    # right header
    c.drawString(mid + 0.2*inch, y_top, right_title)

    y_top -= 14
    c.setStrokeColor(RULE)
    c.setLineWidth(0.4)
    c.line(m, y_top, mid - 0.1*inch, y_top)
    c.line(mid + 0.1*inch, y_top, w - m, y_top)

    # lined areas on both sides
    draw_lined_area(c, m, m + 0.1*inch, mid - 0.15*inch, y_top - 10, HexColor("#E4E4E4"), spacing=22)
    draw_lined_area(c, mid + 0.15*inch, m + 0.1*inch, w - m, y_top - 10, HexColor("#E4E4E4"), spacing=22)

    # folio
    page_folio(c, w, page_num)

    # subtle prompt at bottom
    c.setFillColor(SOFT)
    c.setFont("Inter-Light", 6.5)
    c.drawCentredString(w/2, m - 10, "Write both sides. See what you learn.")

    c.showPage()


def draw_parallel_reflection(c, w, h, page_num):
    m = 0.65 * inch
    y = h - m
    draw_tracked(c, "REFLECTION", w/2, y, "Inter-Light", 7, tracking=2.2, color=SOFT)
    y -= 22
    draw_centered(c, "What pattern do you see?", w/2, y, "Cormorant-Light", 14)
    y -= 14
    draw_hairline(c, w/2-30, y, w/2+30, RULE, 0.4)
    y -= 20

    questions = [
        "Which side was easier to write?",
        "Where did the two sides disagree most?",
        "What surprised you?",
        "What would a compassionate observer say about the gap?",
    ]
    for q in questions:
        c.setFillColor(INK)
        c.setFont("Inter-Medium", 9)
        c.drawString(m, y, q)
        y -= 16
        for _ in range(4):
            c.setStrokeColor(HexColor("#E0E0E0"))
            c.setLineWidth(0.4)
            c.line(m, y, w - m, y)
            y -= 20
        y -= 12

    page_folio(c, w, page_num)
    c.showPage()


def generate_parallel(path: Path):
    w, h = PARALLEL_TRIM
    c = canvas.Canvas(str(path), pagesize=(w, h))
    c.setTitle("Parallel Lives")
    c.setAuthor(AUTHOR)
    pn = 0

    title_page(c, w, h, "Parallel Lives", "A side-by-side journal for divided minds", "160 undated pages")
    pn += 1
    copyright_page(c, w, h, "Parallel Lives",
        "Every spread splits the page in two. Left and right. What happened and how it felt. "
        "What you said and what you meant. The gap between the two sides is where the insight lives. "
        "Undated. Start anywhere. 7 × 10 in.")
    pn += 1

    y = h - 0.7*inch
    draw_centered(c, "How to use this journal", w/2, y, "Cormorant-Light", 16)
    y -= 22
    draw_hairline(c, w/2-28, y, w/2+28, RULE, 0.5)
    y -= 26
    tips = [
        "Each spread has two columns with complementary prompts.",
        "Write in the left column first. Then the right. Or switch.",
        "Every 10 spreads, a reflection page asks what you noticed.",
        "The point isn't balance. It's awareness.",
    ]
    for tip in tips:
        c.setFillColor(INK)
        c.setFont("Inter", 8.5)
        c.drawString(0.8*inch, y, "·  " + tip)
        y -= 18
    c.showPage()
    pn += 1

    begin_page(c, w, h, "pick a side")
    pn += 1

    pair_idx = 0
    spread_count = 0
    while pn < PARALLEL_PAGES - 1:
        if spread_count > 0 and spread_count % 10 == 0 and pn < PARALLEL_PAGES - 3:
            pn += 1
            draw_parallel_reflection(c, w, h, pn)

        pn += 1
        draw_parallel_spread(c, w, h, pn, pair_idx)
        pair_idx += 1
        spread_count += 1

    while pn < PARALLEL_PAGES - 1:
        c.showPage()
        pn += 1

    closing_page(c, w, h, "Both sides are true.", "That's the whole lesson.")
    pn += 1

    c.save()
    print(f"   wrote {path} ({pn} pages)")
    return pn


# ══════════════════════════════════════════════
# JOURNAL C: THE NIGHT PAGES
# 5×8, 120 pages, insomnia journal
# ══════════════════════════════════════════════

NIGHT_TRIM = (5 * inch, 8 * inch)
NIGHT_PAGES = 120

NIGHT_PROMPTS = [
    "It's 3am. What woke you up?",
    "Write the thought that won't stop looping.",
    "List every sound you can hear right now.",
    "What are you afraid will happen tomorrow?",
    "Describe the darkness in your room.",
    "What does your body feel like right now?",
    "Write the conversation you keep replaying.",
    "What do you wish you could turn off?",
    "If sleep were a place, what does yours look like?",
    "Name five things that are true right now.",
    "What would morning-you say to right-now-you?",
    "Describe the weight of the blanket.",
    "What's the thing you didn't say today?",
    "Write until your hand slows down. Then stop.",
    "List three things that went fine today. They don't have to be impressive.",
    "What does tired feel like in your specific body?",
    "Write a boring list. Groceries. Tasks. Anything mundane.",
    "What year does 3am feel like?",
    "Describe the last time you slept well.",
    "Write the worry. Then write its expiration date.",
]

BODY_SCAN = [
    "Unclench your jaw.",
    "Drop your shoulders.",
    "Soften your forehead.",
    "Release your fists.",
    "Ungrip your toes.",
    "Breathe into your stomach.",
    "Let your tongue rest.",
    "Close your eyes between sentences.",
]

def draw_night_writing_page(c, w, h, page_num, prompt):
    m = 0.48 * inch
    y = h - m

    # moon phase dots — decorative
    c.setFillColor(HexColor("#D8D8D8"))
    for i in range(5):
        c.circle(m + i * 10, y + 8, 2.5, stroke=0, fill=1)
    c.setFillColor(HexColor("#B0B0B0"))
    c.circle(m + 20, y + 8, 2.5, stroke=0, fill=1)  # current phase highlight

    y -= 8
    c.setFillColor(INK)
    c.setFont("Cormorant-Medium", 12)
    lines = wrap_text(c, prompt, "Cormorant-Medium", 12, w - 2*m)
    for line in lines:
        c.drawString(m, y, line)
        y -= 16
    y -= 6
    draw_hairline(c, m, y, w - m, RULE, 0.4)
    y -= 12

    draw_lined_area(c, m, m + 0.1*inch, w - m, y, HexColor("#EBEBEB"), spacing=22)

    page_folio(c, w, page_num, SOFT)
    c.showPage()


def draw_body_scan_page(c, w, h, page_num):
    m = 0.55 * inch
    y = h - m
    draw_tracked(c, "BODY SCAN", w/2, y, "Inter-Light", 7, tracking=2.2, color=SOFT)
    y -= 22
    draw_centered(c, "Before you write, arrive.", w/2, y, "Cormorant-Light", 14)
    y -= 14
    draw_hairline(c, w/2-24, y, w/2+24, RULE, 0.4)
    y -= 28

    rng = random.Random(page_num)
    items = rng.sample(BODY_SCAN, min(5, len(BODY_SCAN)))

    for item in items:
        draw_checkbox(c, m, y - 1, 9, SOFT)
        c.setFillColor(INK)
        c.setFont("Inter", 9.5)
        c.drawString(m + 18, y, item)
        y -= 32

    y -= 20
    draw_centered(c, "Now breathe. In 4, hold 4, out 6.", w/2, y, "Inter-Light", 8.5, MUTED)
    y -= 14
    draw_centered(c, "Repeat three times.", w/2, y, "Inter-Light", 8.5, MUTED)

    y -= 36
    # three breathing circles
    c.setStrokeColor(SOFT)
    c.setLineWidth(1.0)
    spacing = (w - 2*m) / 4
    for i in range(3):
        cx = m + spacing * (i + 1)
        c.circle(cx, y, 16, stroke=1, fill=0)
        c.circle(cx, y, 10, stroke=1, fill=0)
        c.circle(cx, y, 4, stroke=1, fill=0)

    page_folio(c, w, page_num, SOFT)
    c.showPage()


def generate_night(path: Path):
    w, h = NIGHT_TRIM
    c = canvas.Canvas(str(path), pagesize=(w, h))
    c.setTitle("The Night Pages")
    c.setAuthor(AUTHOR)
    pn = 0

    title_page(c, w, h, "The Night Pages", "A journal for when you can't sleep", "120 undated pages")
    pn += 1
    copyright_page(c, w, h, "The Night Pages",
        "This journal lives on your nightstand. When your brain won't shut up at 3am, "
        "open it. Write until your hand slows. Body scan pages help you land back in your body. "
        "No rules about length, quality, or making sense. 5 × 8 in. Pocket-sized for dark rooms.")
    pn += 1

    y = h - 0.6*inch
    draw_centered(c, "For the 3am brain", w/2, y, "Cormorant-Light", 14)
    y -= 22
    draw_hairline(c, w/2-24, y, w/2+24, RULE, 0.4)
    y -= 24
    tips = [
        "Keep this next to your bed.",
        "When you can't sleep, open to any page.",
        "Write in the dark if you want. It doesn't have to be legible.",
        "Body scan pages are rest stops. Use them when the thoughts are too fast.",
        "Close the book when your hand slows. That's the signal.",
    ]
    for tip in tips:
        c.setFillColor(INK)
        c.setFont("Inter", 8)
        c.drawString(0.6*inch, y, "·  " + tip)
        y -= 16
    c.showPage()
    pn += 1

    begin_page(c, w, h, "it's okay to be awake")
    pn += 1

    prompt_idx = 0
    count = 0
    while pn < NIGHT_PAGES - 1:
        if count > 0 and count % 8 == 0 and pn < NIGHT_PAGES - 3:
            pn += 1
            draw_body_scan_page(c, w, h, pn)

        pn += 1
        draw_night_writing_page(c, w, h, pn, NIGHT_PROMPTS[prompt_idx % len(NIGHT_PROMPTS)])
        prompt_idx += 1
        count += 1

    while pn < NIGHT_PAGES - 1:
        c.showPage()
        pn += 1

    closing_page(c, w, h, "The night will end.", "It always does.")
    pn += 1

    c.save()
    print(f"   wrote {path} ({pn} pages)")
    return pn


# ══════════════════════════════════════════════
# COLORING BOOK SHARED INFRASTRUCTURE
# ══════════════════════════════════════════════

COLOR_TRIM = (8.5 * inch, 11 * inch)

def coloring_title(c, w, h, title, subtitle, seed=0):
    draw_tracked(c, title.upper(), w/2, h*0.58, "Cormorant-Light", 26, tracking=3.5, color=INK)
    draw_hairline(c, w/2-48, h*0.55, w/2+48, RULE, 0.7)
    draw_centered(c, subtitle, w/2, h*0.52, "Inter-Light", 10, MUTED)
    draw_centered(c, AUTHOR.upper(), w/2, 0.55*inch, "Inter-Light", 7, SOFT)
    c.showPage()


def coloring_copyright_blurb(level, page_count):
    """Copyright blurb without a second © — copyright_page already adds one."""
    lv = level.lower()
    if lv == "beginner":
        label, outlines = "beginner", "Thick outlines for markers, colored pencils, or crayons."
    elif lv in ("amateur", "intermediate"):
        label, outlines = "intermediate", "Comfortable outlines for markers, colored pencils, or crayons."
    elif lv == "advanced":
        label, outlines = "advanced", "Fine outlines for colored pencils and fine-tip markers."
    elif "fine" in lv:
        label, outlines = "fine-line", "Fine outlines for colored pencils and fine-tip markers."
    elif "cozy" in lv:
        label, outlines = "cozy", "Soft outlines for markers, colored pencils, or crayons."
    else:
        label, outlines = level, "Outlines for markers, colored pencils, or crayons."
    return f"{page_count} pages of {label} designs. {outlines} Single-sided printing."

def coloring_howto(c, w, h, level, tips):
    y = h - 0.8*inch
    draw_centered(c, "How to use this book", w/2, y, "Cormorant-Light", 18)
    y -= 26
    draw_tracked(c, level.upper(), w/2, y, "Inter-Light", 7, tracking=2.5, color=SOFT)
    y -= 22
    draw_hairline(c, w/2-30, y, w/2+30, RULE, 0.5)
    y -= 26
    for t, b in tips:
        c.setFillColor(INK)
        c.setFont("Inter-Medium", 9)
        c.drawString(1.1*inch, y, t)
        c.setFillColor(MUTED)
        c.setFont("Inter-Light", 8)
        c.drawString(1.1*inch, y - 13, b)
        y -= 36
    c.showPage()

def coloring_folio(c, w, num):
    c.setFillColor(RULE)
    c.setFont("Inter-Light", 7)
    c.drawCentredString(w/2, 22, str(num))

def coloring_border(c, cx, cy, size, weight=2.5):
    c.setStrokeColor(INK)
    c.setLineWidth(weight)
    m = size * 0.02
    c.rect(cx - size/2 + m, cy - size/2 + m, size - 2*m, size - 2*m, stroke=1, fill=0)

def build_coloring_book(path, title, subtitle, level, tips, page_count, draw_fn, paper_ppi=WHITE_PPI):
    w, h = COLOR_TRIM
    c = canvas.Canvas(str(path), pagesize=(w, h))
    c.setTitle(title)
    c.setAuthor(AUTHOR)

    margin = 0.6 * inch
    art_size = min(w - 2*margin, h - 2*margin - 0.3*inch)
    cx, cy = w/2, h/2 + 0.1*inch
    pn = 0

    coloring_title(c, w, h, title, subtitle)
    pn += 1

    copyright_page(c, w, h, title, coloring_copyright_blurb(level, page_count))
    pn += 1

    coloring_howto(c, w, h, level, tips)
    pn += 1

    begin_page(c, w, h, "pick any page")
    pn += 1

    rng = random.Random(sum(ord(ch) for ch in title))  # PATCH 2: deterministic seed (was hash(title))
    while pn < page_count - 2:  # PATCH 1: was page_count - 1 (off-by-one: art/blank pairs overran by 2, closing page pushed total to N+1)
        # art page
        draw_fn(c, cx, cy, art_size, seed=pn * 17 + 5, rng=rng)
        coloring_folio(c, w, pn + 1)
        c.showPage()
        pn += 1
        # blank back
        c.showPage()
        pn += 1
        if pn % 20 == 0:
            print(f"   {title} page {pn}/{page_count}")

    while pn < page_count - 1:
        c.showPage()
        pn += 1

    closing_page(c, w, h, "You colored.", "That counts.")
    pn += 1

    c.save()
    print(f"   wrote {path} ({pn} pages)")
    return pn


# ══════════════════════════════════════════════
# BEGINNER 1: FIRST STROKES
# Super simple shapes, very thick lines, max 3-5 elements
# ══════════════════════════════════════════════

def draw_beginner_simple(c, cx, cy, size, seed, rng=None):
    if not rng: rng = random.Random(seed)
    c.setStrokeColor(INK)
    c.setLineCap(1)
    c.setLineJoin(1)

    page_type = rng.choice(["circles", "stars", "hearts", "fish", "houses", "trees", "cats", "butterflies"])

    if page_type == "circles":
        # nested circles with thick lines
        c.setLineWidth(4.0)
        count = rng.randint(3, 5)
        for i in range(count):
            r = size * (0.1 + i * 0.08)
            c.circle(cx, cy, r, stroke=1, fill=0)
        # big center dot
        c.setFillColor(INK)
        c.circle(cx, cy, size * 0.03, stroke=0, fill=1)

    elif page_type == "stars":
        c.setLineWidth(3.8)
        points = rng.choice([4, 5, 6])
        r_outer = size * 0.35
        r_inner = size * 0.15
        p = c.beginPath()
        for i in range(points * 2):
            angle = (math.pi / points) * i - math.pi / 2
            r = r_outer if i % 2 == 0 else r_inner
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            if i == 0: p.moveTo(x, y)
            else: p.lineTo(x, y)
        p.close()
        c.drawPath(p, stroke=1, fill=0)
        # decorative circle around
        c.setLineWidth(3.0)
        c.circle(cx, cy, r_outer * 1.15, stroke=1, fill=0)

    elif page_type == "hearts":
        c.setLineWidth(4.0)
        count = rng.randint(1, 3)
        for h_i in range(count):
            hcx = cx + rng.uniform(-size*0.15, size*0.15)
            hcy = cy + rng.uniform(-size*0.1, size*0.15)
            hr = size * (0.15 - h_i * 0.03)
            p = c.beginPath()
            p.moveTo(hcx, hcy - hr * 0.4)
            p.curveTo(hcx + hr, hcy + hr * 0.6, hcx + hr * 0.4, hcy + hr * 1.2, hcx, hcy + hr * 0.8)
            p.curveTo(hcx - hr * 0.4, hcy + hr * 1.2, hcx - hr, hcy + hr * 0.6, hcx, hcy - hr * 0.4)
            c.drawPath(p, stroke=1, fill=0)

    elif page_type == "fish":
        c.setLineWidth(3.5)
        # body
        c.ellipse(cx - size*0.22, cy - size*0.1, cx + size*0.12, cy + size*0.1, stroke=1, fill=0)
        # tail
        p = c.beginPath()
        p.moveTo(cx + size*0.12, cy + size*0.06)
        p.lineTo(cx + size*0.25, cy + size*0.14)
        p.lineTo(cx + size*0.25, cy - size*0.14)
        p.lineTo(cx + size*0.12, cy - size*0.06)
        c.drawPath(p, stroke=1, fill=0)
        # eye
        c.setLineWidth(2.5)
        c.circle(cx - size*0.12, cy + size*0.02, size*0.025, stroke=1, fill=0)
        c.setFillColor(INK)
        c.circle(cx - size*0.12, cy + size*0.02, size*0.01, stroke=0, fill=1)
        # fin
        c.setLineWidth(3.0)
        p = c.beginPath()
        p.moveTo(cx - size*0.05, cy + size*0.1)
        p.curveTo(cx - size*0.02, cy + size*0.22, cx + size*0.05, cy + size*0.2, cx + size*0.05, cy + size*0.1)
        c.drawPath(p, stroke=1, fill=0)

    elif page_type == "houses":
        c.setLineWidth(4.0)
        bw, bh = size*0.3, size*0.22
        # body
        c.rect(cx - bw/2, cy - bh/2, bw, bh, stroke=1, fill=0)
        # roof
        p = c.beginPath()
        p.moveTo(cx - bw/2 - size*0.04, cy + bh/2)
        p.lineTo(cx, cy + bh/2 + size*0.18)
        p.lineTo(cx + bw/2 + size*0.04, cy + bh/2)
        p.close()
        c.drawPath(p, stroke=1, fill=0)
        # door
        c.setLineWidth(3.0)
        c.rect(cx - size*0.04, cy - bh/2, size*0.08, size*0.12, stroke=1, fill=0)
        # windows
        ws = size * 0.06
        c.rect(cx - bw/2 + size*0.04, cy + size*0.02, ws, ws, stroke=1, fill=0)
        c.rect(cx + bw/2 - size*0.04 - ws, cy + size*0.02, ws, ws, stroke=1, fill=0)

    elif page_type == "trees":
        c.setLineWidth(4.0)
        # trunk
        tw = size * 0.06
        c.rect(cx - tw/2, cy - size*0.2, tw, size*0.2, stroke=1, fill=0)
        # canopy circles
        c.setLineWidth(3.5)
        for angle_i in range(3):
            angle = (2 * math.pi / 3) * angle_i + math.pi/6
            tr = size * 0.12
            tx = cx + tr * 0.5 * math.cos(angle)
            ty = cy + size*0.05 + tr * 0.5 * math.sin(angle)
            c.circle(tx, ty, tr, stroke=1, fill=0)
        c.circle(cx, cy + size*0.15, size*0.1, stroke=1, fill=0)

    elif page_type == "cats":
        c.setLineWidth(3.5)
        # body
        c.ellipse(cx - size*0.14, cy - size*0.15, cx + size*0.14, cy + size*0.05, stroke=1, fill=0)
        # head
        c.circle(cx, cy + size*0.14, size*0.09, stroke=1, fill=0)
        # ears
        for side in [-1, 1]:
            p = c.beginPath()
            ex = cx + side * size*0.06
            p.moveTo(ex - size*0.025, cy + size*0.2)
            p.lineTo(ex, cy + size*0.28)
            p.lineTo(ex + size*0.025, cy + size*0.2)
            c.drawPath(p, stroke=1, fill=0)
        # eyes
        c.setLineWidth(2.5)
        for side in [-1, 1]:
            c.circle(cx + side*size*0.035, cy + size*0.15, size*0.015, stroke=1, fill=0)
        # tail
        c.setLineWidth(3.0)
        p = c.beginPath()
        p.moveTo(cx + size*0.14, cy - size*0.08)
        p.curveTo(cx + size*0.28, cy - size*0.05, cx + size*0.25, cy + size*0.1, cx + size*0.2, cy + size*0.12)
        c.drawPath(p, stroke=1, fill=0)

    elif page_type == "butterflies":
        c.setLineWidth(3.5)
        # body
        c.ellipse(cx - size*0.015, cy - size*0.12, cx + size*0.015, cy + size*0.12, stroke=1, fill=0)
        # wings — large simple ovals
        for side in [-1, 1]:
            # upper wing
            c.saveState()
            c.translate(cx + side * size*0.01, cy + size*0.04)
            c.rotate(side * 25)
            c.ellipse(-size*0.02, -size*0.02, side * size*0.18, size*0.14, stroke=1, fill=0)
            c.restoreState()
            # lower wing
            c.saveState()
            c.translate(cx + side * size*0.01, cy - size*0.04)
            c.rotate(side * -15)
            c.ellipse(-size*0.015, -size*0.1, side * size*0.14, size*0.02, stroke=1, fill=0)
            c.restoreState()
        # antennae
        c.setLineWidth(2.5)
        for side in [-1, 1]:
            p = c.beginPath()
            p.moveTo(cx, cy + size*0.12)
            p.curveTo(cx + side*size*0.06, cy + size*0.2, cx + side*size*0.08, cy + size*0.22, cx + side*size*0.07, cy + size*0.24)
            c.drawPath(p, stroke=1, fill=0)
            c.setFillColor(INK)
            c.circle(cx + side*size*0.07, cy + size*0.24, size*0.01, stroke=0, fill=1)

    coloring_border(c, cx, cy, size, weight=3.5)


# ══════════════════════════════════════════════
# BEGINNER 2: EASY GARDEN
# Simple flowers, leaves, bugs — large shapes
# ══════════════════════════════════════════════

def draw_beginner_garden(c, cx, cy, size, seed, rng=None):
    if not rng: rng = random.Random(seed)
    c.setStrokeColor(INK)
    c.setLineCap(1)
    c.setLineJoin(1)

    page_type = rng.choice(["sunflower", "tulip", "daisy", "ladybug", "mushroom", "cactus", "snail", "bee"])

    if page_type == "sunflower":
        c.setLineWidth(3.5)
        # center
        c.circle(cx, cy, size*0.1, stroke=1, fill=0)
        c.circle(cx, cy, size*0.06, stroke=1, fill=0)
        # petals
        petals = 10
        for i in range(petals):
            angle = (2*math.pi/petals) * i
            c.saveState()
            c.translate(cx, cy)
            c.rotate(math.degrees(angle))
            c.ellipse(-size*0.04, size*0.1, size*0.04, size*0.26, stroke=1, fill=0)
            c.restoreState()
        # stem
        c.setLineWidth(4.0)
        c.line(cx, cy - size*0.1, cx, cy - size*0.38)
        # leaves
        c.setLineWidth(3.0)
        for side in [-1, 1]:
            c.saveState()
            c.translate(cx, cy - size*0.25)
            c.rotate(side * 35)
            c.ellipse(-size*0.03, 0, size*0.03, size*0.1, stroke=1, fill=0)
            c.restoreState()

    elif page_type == "tulip":
        c.setLineWidth(3.5)
        # petals — 3 overlapping U shapes
        for offset in [-size*0.04, 0, size*0.04]:
            p = c.beginPath()
            p.moveTo(cx + offset - size*0.06, cy)
            p.curveTo(cx + offset - size*0.06, cy + size*0.22, cx + offset + size*0.06, cy + size*0.22, cx + offset + size*0.06, cy)
            c.drawPath(p, stroke=1, fill=0)
        # stem
        c.setLineWidth(4.0)
        c.line(cx, cy, cx, cy - size*0.35)
        # leaf
        c.setLineWidth(3.0)
        p = c.beginPath()
        p.moveTo(cx, cy - size*0.2)
        p.curveTo(cx + size*0.12, cy - size*0.15, cx + size*0.1, cy - size*0.08, cx + size*0.04, cy - size*0.12)
        c.drawPath(p, stroke=1, fill=0)

    elif page_type == "daisy":
        c.setLineWidth(3.5)
        c.circle(cx, cy, size*0.06, stroke=1, fill=0)
        petals = 8
        for i in range(petals):
            angle = (2*math.pi/petals) * i
            c.saveState()
            c.translate(cx, cy)
            c.rotate(math.degrees(angle))
            c.ellipse(-size*0.025, size*0.06, size*0.025, size*0.2, stroke=1, fill=0)
            c.restoreState()
        c.setLineWidth(4.0)
        c.line(cx, cy - size*0.06, cx, cy - size*0.35)

    elif page_type == "ladybug":
        c.setLineWidth(3.5)
        # body
        c.ellipse(cx - size*0.16, cy - size*0.12, cx + size*0.16, cy + size*0.12, stroke=1, fill=0)
        # head
        c.circle(cx, cy + size*0.18, size*0.07, stroke=1, fill=0)
        # center line
        c.line(cx, cy + size*0.12, cx, cy - size*0.12)
        # spots
        c.setLineWidth(2.5)
        spots = [(cx-size*0.07, cy+size*0.04), (cx+size*0.07, cy+size*0.04),
                 (cx-size*0.05, cy-size*0.06), (cx+size*0.05, cy-size*0.06)]
        for sx, sy in spots:
            c.circle(sx, sy, size*0.025, stroke=1, fill=0)
        # antennae
        c.setLineWidth(3.0)
        for side in [-1, 1]:
            p = c.beginPath()
            p.moveTo(cx + side*size*0.03, cy + size*0.23)
            p.curveTo(cx + side*size*0.08, cy + size*0.32, cx + side*size*0.1, cy + size*0.32, cx + side*size*0.09, cy + size*0.3)
            c.drawPath(p, stroke=1, fill=0)

    elif page_type == "mushroom":
        c.setLineWidth(4.0)
        # stem
        c.rect(cx - size*0.06, cy - size*0.2, size*0.12, size*0.2, stroke=1, fill=0)
        # cap
        p = c.beginPath()
        p.moveTo(cx - size*0.2, cy)
        p.curveTo(cx - size*0.2, cy + size*0.25, cx + size*0.2, cy + size*0.25, cx + size*0.2, cy)
        p.close()
        c.drawPath(p, stroke=1, fill=0)
        # spots
        c.setLineWidth(2.5)
        c.circle(cx - size*0.06, cy + size*0.12, size*0.03, stroke=1, fill=0)
        c.circle(cx + size*0.08, cy + size*0.1, size*0.025, stroke=1, fill=0)
        c.circle(cx, cy + size*0.18, size*0.02, stroke=1, fill=0)

    elif page_type == "cactus":
        c.setLineWidth(4.0)
        # main body
        c.roundRect(cx - size*0.06, cy - size*0.2, size*0.12, size*0.35, size*0.06, stroke=1, fill=0)
        # arms
        for side, y_off in [(-1, 0.05), (1, -0.02)]:
            arm_x = cx + side * size*0.06
            c.setLineWidth(3.5)
            p = c.beginPath()
            p.moveTo(arm_x, cy + y_off*size)
            p.lineTo(arm_x + side*size*0.1, cy + y_off*size)
            p.lineTo(arm_x + side*size*0.1, cy + y_off*size + size*0.12)
            c.drawPath(p, stroke=1, fill=0)
        # pot
        c.setLineWidth(4.0)
        p = c.beginPath()
        p.moveTo(cx - size*0.1, cy - size*0.2)
        p.lineTo(cx - size*0.08, cy - size*0.32)
        p.lineTo(cx + size*0.08, cy - size*0.32)
        p.lineTo(cx + size*0.1, cy - size*0.2)
        p.close()
        c.drawPath(p, stroke=1, fill=0)

    elif page_type == "snail":
        c.setLineWidth(3.5)
        # body
        p = c.beginPath()
        p.moveTo(cx - size*0.2, cy - size*0.08)
        p.curveTo(cx - size*0.2, cy - size*0.14, cx + size*0.12, cy - size*0.14, cx + size*0.12, cy - size*0.08)
        c.drawPath(p, stroke=1, fill=0)
        # shell spiral
        c.circle(cx - size*0.02, cy + size*0.02, size*0.12, stroke=1, fill=0)
        c.circle(cx - size*0.02, cy + size*0.04, size*0.07, stroke=1, fill=0)
        c.circle(cx - size*0.02, cy + size*0.055, size*0.03, stroke=1, fill=0)
        # eye stalks
        c.setLineWidth(3.0)
        for side in [-1, 1]:
            ex = cx + size*0.12 + side*size*0.02
            c.line(ex, cy - size*0.08, ex + side*size*0.02, cy + size*0.04)
            c.circle(ex + side*size*0.02, cy + size*0.04, size*0.012, stroke=1, fill=0)

    elif page_type == "bee":
        c.setLineWidth(3.5)
        # body
        c.ellipse(cx - size*0.14, cy - size*0.08, cx + size*0.14, cy + size*0.08, stroke=1, fill=0)
        # stripes
        c.setLineWidth(2.5)
        for i in range(3):
            sx = cx - size*0.06 + i * size*0.06
            c.line(sx, cy - size*0.075, sx, cy + size*0.075)
        # head
        c.setLineWidth(3.5)
        c.circle(cx - size*0.18, cy, size*0.055, stroke=1, fill=0)
        # wings
        c.setLineWidth(2.5)
        for side in [-1, 1]:
            c.saveState()
            c.translate(cx, cy + side*size*0.08)
            c.rotate(side * 15)
            c.ellipse(-size*0.08, 0, size*0.08, side*size*0.15, stroke=1, fill=0)
            c.restoreState()
        # stinger
        c.setLineWidth(3.0)
        c.line(cx + size*0.14, cy, cx + size*0.2, cy)

    coloring_border(c, cx, cy, size, weight=3.5)


# ══════════════════════════════════════════════
# AMATEUR 1: MOSAIC MIND
# Medium-complexity geometric mosaics and tessellations
# ══════════════════════════════════════════════

def draw_amateur_mosaic(c, cx, cy, size, seed, rng=None):
    if not rng: rng = random.Random(seed)
    c.setStrokeColor(INK)
    c.setLineCap(1)
    c.setLineJoin(1)

    page_type = rng.choice(["hex_mosaic", "triangle_grid", "islamic_star", "celtic_knot",
                            "op_art_circles", "chevron_field", "diamond_lattice", "pinwheel"])

    half = size * 0.45

    if page_type == "hex_mosaic":
        r = size * 0.04
        c.setLineWidth(2.0)
        for row in range(-10, 11):
            for col in range(-8, 9):
                offset = r * 1.5 * (row % 2)
                hx = cx + col * r * 1.74 + offset
                hy = cy + row * r * 1.52
                if abs(hx - cx) > half or abs(hy - cy) > half: continue
                p = c.beginPath()
                for i in range(7):
                    a = math.pi/6 + i * math.pi/3
                    px = hx + r * math.cos(a)
                    py = hy + r * math.sin(a)
                    if i == 0: p.moveTo(px, py)
                    else: p.lineTo(px, py)
                c.drawPath(p, stroke=1, fill=0)
                # inner star
                if rng.random() > 0.5:
                    c.setLineWidth(1.0)
                    ir = r * 0.5
                    for i in range(6):
                        a1 = math.pi/6 + i * math.pi/3
                        a2 = math.pi/6 + ((i+2) % 6) * math.pi/3
                        c.line(hx + ir*math.cos(a1), hy + ir*math.sin(a1),
                               hx + ir*math.cos(a2), hy + ir*math.sin(a2))
                    c.setLineWidth(2.0)

    elif page_type == "triangle_grid":
        c.setLineWidth(1.8)
        spacing = size * 0.05
        rows = int(size * 0.9 / (spacing * 0.866))
        for row in range(rows):
            for col in range(int(size * 0.9 / spacing) + 1):
                x = cx - half + col * spacing + (row % 2) * spacing/2
                y = cy - half + row * spacing * 0.866
                if abs(x - cx) > half or abs(y - cy) > half: continue
                # upward triangle
                p = c.beginPath()
                p.moveTo(x, y)
                p.lineTo(x + spacing, y)
                p.lineTo(x + spacing/2, y + spacing * 0.866)
                p.close()
                c.drawPath(p, stroke=1, fill=0)
                # optional inner circle
                if rng.random() > 0.6:
                    c.setLineWidth(0.8)
                    c.circle(x + spacing/2, y + spacing*0.289, spacing*0.18, stroke=1, fill=0)
                    c.setLineWidth(1.8)

    elif page_type == "islamic_star":
        c.setLineWidth(2.2)
        # 8-pointed star tiling
        unit = size * 0.08
        for row in range(-6, 7):
            for col in range(-6, 7):
                sx = cx + col * unit * 2
                sy = cy + row * unit * 2
                if abs(sx - cx) > half or abs(sy - cy) > half: continue
                # draw 8-pointed star
                p = c.beginPath()
                for i in range(8):
                    a1 = (math.pi/4) * i
                    a2 = a1 + math.pi/8
                    r1 = unit * 0.9
                    r2 = unit * 0.45
                    x1 = sx + r1 * math.cos(a1)
                    y1 = sy + r1 * math.sin(a1)
                    x2 = sx + r2 * math.cos(a2)
                    y2 = sy + r2 * math.sin(a2)
                    if i == 0:
                        p.moveTo(x1, y1)
                    else:
                        p.lineTo(x1, y1)
                    p.lineTo(x2, y2)
                p.close()
                c.drawPath(p, stroke=1, fill=0)

    elif page_type == "celtic_knot":
        c.setLineWidth(2.5)
        # simplified interlaced circles
        spacing = size * 0.1
        for row in range(-5, 6):
            for col in range(-5, 6):
                kcx = cx + col * spacing
                kcy = cy + row * spacing
                if abs(kcx - cx) > half or abs(kcy - cy) > half: continue
                c.circle(kcx, kcy, spacing*0.42, stroke=1, fill=0)
                if (row + col) % 2 == 0:
                    c.setLineWidth(1.2)
                    c.circle(kcx, kcy, spacing*0.22, stroke=1, fill=0)
                    c.setLineWidth(2.5)

    elif page_type == "op_art_circles":
        c.setLineWidth(1.8)
        rings = rng.randint(12, 20)
        for i in range(rings):
            r = size * 0.02 * (i + 1)
            c.circle(cx, cy, r, stroke=1, fill=0)
        # offset circles
        offsets = [(size*0.15, 0), (-size*0.15, 0), (0, size*0.15), (0, -size*0.15)]
        for ox, oy in offsets:
            c.setLineWidth(1.2)
            for i in range(8):
                c.circle(cx + ox, cy + oy, size*0.02*(i+1), stroke=1, fill=0)

    elif page_type == "chevron_field":
        c.setLineWidth(2.0)
        ch_h = size * 0.04
        ch_w = size * 0.08
        rows = int(size * 0.9 / ch_h)
        cols = int(size * 0.9 / ch_w) + 1
        for row in range(rows):
            for col in range(cols):
                x = cx - half + col * ch_w + (row % 2) * ch_w/2
                y = cy - half + row * ch_h
                if abs(x - cx) > half or abs(y - cy) > half: continue
                p = c.beginPath()
                p.moveTo(x, y)
                p.lineTo(x + ch_w/2, y + ch_h)
                p.lineTo(x + ch_w, y)
                c.drawPath(p, stroke=1, fill=0)

    elif page_type == "diamond_lattice":
        c.setLineWidth(2.0)
        ds = size * 0.06
        for row in range(-12, 13):
            for col in range(-12, 13):
                dx = cx + col * ds + (row % 2) * ds/2
                dy = cy + row * ds * 0.7
                if abs(dx - cx) > half or abs(dy - cy) > half: continue
                p = c.beginPath()
                p.moveTo(dx, dy - ds*0.35)
                p.lineTo(dx + ds/2, dy)
                p.lineTo(dx, dy + ds*0.35)
                p.lineTo(dx - ds/2, dy)
                p.close()
                c.drawPath(p, stroke=1, fill=0)

    elif page_type == "pinwheel":
        c.setLineWidth(2.2)
        blades = rng.choice([6, 8, 10, 12])
        layers = rng.randint(3, 5)
        for layer in range(layers):
            r = size * (0.08 + layer * 0.08)
            for i in range(blades):
                a1 = (2*math.pi/blades) * i
                a2 = a1 + math.pi/blades * 0.8
                x1 = cx + r * math.cos(a1)
                y1 = cy + r * math.sin(a1)
                x2 = cx + (r + size*0.06) * math.cos(a2)
                y2 = cy + (r + size*0.06) * math.sin(a2)
                c.line(x1, y1, x2, y2)
            c.setLineWidth(1.5)
            c.circle(cx, cy, r, stroke=1, fill=0)
            c.setLineWidth(2.2)

    coloring_border(c, cx, cy, size, weight=2.5)


# ══════════════════════════════════════════════
# AMATEUR 2: WOODLAND WONDERS
# Medium-detail forest animals and nature scenes
# ══════════════════════════════════════════════

def draw_amateur_woodland(c, cx, cy, size, seed, rng=None):
    if not rng: rng = random.Random(seed)
    c.setStrokeColor(INK)
    c.setLineCap(1)
    c.setLineJoin(1)
    half = size * 0.45  # PATCH 4: 'half' was used below but never defined (NameError on tree/grass scenes)

    page_type = rng.choice(["owl", "fox", "deer", "mushroom_scene", "tree_scene", "fern_pattern", "pine_forest", "acorn_wreath"])

    if page_type == "owl":
        c.setLineWidth(2.5)
        # body
        c.ellipse(cx - size*0.14, cy - size*0.22, cx + size*0.14, cy + size*0.08, stroke=1, fill=0)
        # head
        c.circle(cx, cy + size*0.16, size*0.1, stroke=1, fill=0)
        # ears
        for side in [-1, 1]:
            p = c.beginPath()
            p.moveTo(cx + side*size*0.07, cy + size*0.23)
            p.lineTo(cx + side*size*0.1, cy + size*0.32)
            p.lineTo(cx + side*size*0.04, cy + size*0.25)
            c.drawPath(p, stroke=1, fill=0)
        # eyes — large concentric circles
        c.setLineWidth(2.0)
        for side in [-1, 1]:
            ex = cx + side*size*0.04
            ey = cy + size*0.17
            c.circle(ex, ey, size*0.04, stroke=1, fill=0)
            c.circle(ex, ey, size*0.025, stroke=1, fill=0)
            c.setFillColor(INK)
            c.circle(ex, ey, size*0.01, stroke=0, fill=1)
        # beak
        c.setLineWidth(2.0)
        p = c.beginPath()
        p.moveTo(cx - size*0.015, cy + size*0.12)
        p.lineTo(cx, cy + size*0.1)
        p.lineTo(cx + size*0.015, cy + size*0.12)
        c.drawPath(p, stroke=1, fill=0)
        # feather details on body
        c.setLineWidth(1.2)
        for row in range(5):
            for col in range(3):
                fx = cx - size*0.06 + col * size*0.06
                fy = cy + size*0.02 - row * size*0.05
                # PATCH 3: reportlab 5 removed stroke kwarg from Canvas.arc — use path arc
                fp = c.beginPath()
                fp.arc(fx - size*0.02, fy - size*0.015, fx + size*0.02, fy + size*0.015, 0, 180)
                c.drawPath(fp, stroke=1, fill=0)
        # branch
        c.setLineWidth(2.5)
        c.line(cx - size*0.25, cy - size*0.22, cx + size*0.25, cy - size*0.2)
        # feet
        c.setLineWidth(2.0)
        for side in [-1, 1]:
            fx = cx + side * size*0.06
            c.line(fx, cy - size*0.18, fx, cy - size*0.22)
            for t in [-1, 0, 1]:
                c.line(fx, cy - size*0.22, fx + t*size*0.015, cy - size*0.25)

    elif page_type == "fox":
        c.setLineWidth(2.5)
        # body
        c.ellipse(cx - size*0.18, cy - size*0.12, cx + size*0.1, cy + size*0.08, stroke=1, fill=0)
        # head
        p = c.beginPath()
        p.moveTo(cx + size*0.1, cy + size*0.04)
        p.curveTo(cx + size*0.22, cy + size*0.15, cx + size*0.22, cy + size*0.2, cx + size*0.16, cy + size*0.22)
        p.curveTo(cx + size*0.14, cy + size*0.16, cx + size*0.1, cy + size*0.14, cx + size*0.1, cy + size*0.04)
        c.drawPath(p, stroke=1, fill=0)
        # ears
        c.setLineWidth(2.0)
        for offset in [0.01, 0.06]:
            p = c.beginPath()
            p.moveTo(cx + size*(0.12+offset), cy + size*0.2)
            p.lineTo(cx + size*(0.13+offset), cy + size*0.3)
            p.lineTo(cx + size*(0.16+offset), cy + size*0.22)
            c.drawPath(p, stroke=1, fill=0)
        # eye
        c.circle(cx + size*0.15, cy + size*0.16, size*0.012, stroke=1, fill=0)
        # nose
        c.setFillColor(INK)
        c.circle(cx + size*0.2, cy + size*0.14, size*0.008, stroke=0, fill=1)
        # tail
        c.setLineWidth(2.5)
        p = c.beginPath()
        p.moveTo(cx - size*0.18, cy - size*0.05)
        p.curveTo(cx - size*0.32, cy - size*0.02, cx - size*0.3, cy + size*0.12, cx - size*0.22, cy + size*0.1)
        c.drawPath(p, stroke=1, fill=0)
        # legs
        c.setLineWidth(2.0)
        for lx in [cx - size*0.1, cx + size*0.04]:
            c.line(lx, cy - size*0.12, lx, cy - size*0.25)

    elif page_type == "deer":
        c.setLineWidth(2.5)
        # body
        c.ellipse(cx - size*0.18, cy - size*0.1, cx + size*0.14, cy + size*0.1, stroke=1, fill=0)
        # neck
        p = c.beginPath()
        p.moveTo(cx + size*0.12, cy + size*0.08)
        p.curveTo(cx + size*0.14, cy + size*0.2, cx + size*0.12, cy + size*0.25, cx + size*0.1, cy + size*0.28)
        c.drawPath(p, stroke=1, fill=0)
        # head
        c.ellipse(cx + size*0.06, cy + size*0.26, cx + size*0.16, cy + size*0.34, stroke=1, fill=0)
        # antlers
        c.setLineWidth(2.0)
        for side in [-1, 1]:
            ax = cx + size*0.11 + side*size*0.02
            ay = cy + size*0.34
            c.line(ax, ay, ax + side*size*0.06, ay + size*0.12)
            c.line(ax + side*size*0.03, ay + size*0.06, ax + side*size*0.08, ay + size*0.08)
            c.line(ax + side*size*0.05, ay + size*0.1, ax + side*size*0.1, ay + size*0.14)
        # eye
        c.setLineWidth(1.5)
        c.circle(cx + size*0.12, cy + size*0.3, size*0.008, stroke=1, fill=0)
        # legs
        c.setLineWidth(2.0)
        for lx in [cx - size*0.12, cx - size*0.04, cx + size*0.04, cx + size*0.1]:
            c.line(lx, cy - size*0.1, lx, cy - size*0.28)
        # tail
        c.setLineWidth(2.5)
        p = c.beginPath()
        p.moveTo(cx - size*0.18, cy + size*0.06)
        p.curveTo(cx - size*0.22, cy + size*0.1, cx - size*0.21, cy + size*0.12, cx - size*0.19, cy + size*0.1)
        c.drawPath(p, stroke=1, fill=0)

    elif page_type in ("mushroom_scene", "tree_scene", "fern_pattern", "pine_forest", "acorn_wreath"):
        # generic nature scenes with medium detail
        c.setLineWidth(2.2)
        if page_type == "mushroom_scene":
            # 3 mushrooms of different sizes
            for i, (mx, ms) in enumerate([(cx-size*0.15, 0.8), (cx+size*0.05, 1.0), (cx+size*0.2, 0.6)]):
                sw = size * 0.05 * ms
                sh = size * 0.15 * ms
                c.rect(mx - sw/2, cy - size*0.15, sw, sh, stroke=1, fill=0)
                p = c.beginPath()
                cap_w = size * 0.12 * ms
                p.moveTo(mx - cap_w, cy - size*0.15 + sh)
                p.curveTo(mx - cap_w, cy + size*0.08*ms, mx + cap_w, cy + size*0.08*ms, mx + cap_w, cy - size*0.15 + sh)
                p.close()
                c.drawPath(p, stroke=1, fill=0)
                # spots
                c.setLineWidth(1.2)
                for _ in range(rng.randint(2, 4)):
                    c.circle(mx + rng.uniform(-cap_w*0.6, cap_w*0.6),
                             cy - size*0.15 + sh + rng.uniform(size*0.01, size*0.06*ms),
                             size*0.012*ms, stroke=1, fill=0)
                c.setLineWidth(2.2)
            # grass
            c.setLineWidth(1.5)
            for g in range(20):
                gx = cx + rng.uniform(-half*0.8, half*0.8)
                c.line(gx, cy - size*0.2, gx + rng.uniform(-3, 3), cy - size*0.2 + rng.uniform(size*0.03, size*0.06))
        else:
            # tree scene — multiple trees
            c.setLineWidth(2.5)
            for i in range(rng.randint(3, 5)):
                tx = cx + rng.uniform(-half*0.7, half*0.7)
                trunk_h = rng.uniform(size*0.12, size*0.25)
                trunk_w = size * 0.03
                base_y = cy - size*0.2
                c.rect(tx - trunk_w, base_y, trunk_w*2, trunk_h, stroke=1, fill=0)
                # canopy
                canopy_r = rng.uniform(size*0.06, size*0.12)
                c.circle(tx, base_y + trunk_h + canopy_r*0.7, canopy_r, stroke=1, fill=0)
                # additional canopy circles
                for _ in range(rng.randint(1, 3)):
                    c.circle(tx + rng.uniform(-canopy_r*0.6, canopy_r*0.6),
                             base_y + trunk_h + canopy_r*0.7 + rng.uniform(-canopy_r*0.3, canopy_r*0.3),
                             canopy_r * rng.uniform(0.5, 0.8), stroke=1, fill=0)

    coloring_border(c, cx, cy, size, weight=2.5)


# ══════════════════════════════════════════════
# ADVANCED 1: FRACTAL DREAMS
# Complex mathematical fractals and detailed mandalas
# ══════════════════════════════════════════════

def draw_advanced_fractal(c, cx, cy, size, seed, rng=None):
    if not rng: rng = random.Random(seed)
    c.setStrokeColor(INK)
    c.setLineCap(1)
    c.setLineJoin(1)

    page_type = rng.choice(["sierpinski", "koch_mandala", "fractal_tree", "julia_dots",
                            "dragon_curve", "spiral_fractal", "nested_polygon", "recursive_star"])

    half = size * 0.44

    if page_type == "sierpinski":
        c.setLineWidth(1.2)
        def sierpinski(x, y, s, depth):
            if depth == 0:
                p = c.beginPath()
                p.moveTo(x, y)
                p.lineTo(x + s, y)
                p.lineTo(x + s/2, y + s * 0.866)
                p.close()
                c.drawPath(p, stroke=1, fill=0)
                return
            sierpinski(x, y, s/2, depth-1)
            sierpinski(x + s/2, y, s/2, depth-1)
            sierpinski(x + s/4, y + s*0.433, s/2, depth-1)
        sierpinski(cx - size*0.35, cy - size*0.3, size*0.7, 5)

    elif page_type == "koch_mandala":
        c.setLineWidth(1.0)
        def koch_line(x1, y1, x2, y2, depth):
            if depth == 0:
                c.line(x1, y1, x2, y2)
                return
            dx = (x2 - x1) / 3
            dy = (y2 - y1) / 3
            ax, ay = x1 + dx, y1 + dy
            bx, by = x1 + 2*dx, y1 + 2*dy
            mx = (ax + bx)/2 - (by - ay) * 0.866
            my = (ay + by)/2 + (bx - ax) * 0.866
            koch_line(x1, y1, ax, ay, depth-1)
            koch_line(ax, ay, mx, my, depth-1)
            koch_line(mx, my, bx, by, depth-1)
            koch_line(bx, by, x2, y2, depth-1)

        sides = 6
        r = size * 0.35
        for i in range(sides):
            a1 = (2*math.pi/sides)*i - math.pi/2
            a2 = (2*math.pi/sides)*(i+1) - math.pi/2
            x1 = cx + r*math.cos(a1)
            y1 = cy + r*math.sin(a1)
            x2 = cx + r*math.cos(a2)
            y2 = cy + r*math.sin(a2)
            koch_line(x1, y1, x2, y2, 3)

    elif page_type == "fractal_tree":
        c.setLineWidth(1.0)
        def branch(x, y, length, angle, depth):
            if depth == 0 or length < 2: return
            x2 = x + length * math.cos(angle)
            y2 = y + length * math.sin(angle)
            c.setLineWidth(max(0.5, depth * 0.3))
            c.line(x, y, x2, y2)
            branch(x2, y2, length * 0.7, angle + 0.45, depth-1)
            branch(x2, y2, length * 0.7, angle - 0.45, depth-1)
            if depth > 3:
                branch(x2, y2, length * 0.5, angle + 0.9, depth-2)
        branch(cx, cy - size*0.35, size*0.18, math.pi/2, 10)

    elif page_type == "julia_dots":
        c.setLineWidth(0.8)
        # Julia-set-inspired dot pattern
        scale = size * 0.0035
        cr, ci = -0.7, 0.27
        for px in range(int(-half/scale), int(half/scale)):
            for py in range(int(-half/scale), int(half/scale)):
                zr, zi = px * 0.01, py * 0.01
                iteration = 0
                while zr*zr + zi*zi < 4 and iteration < 20:
                    zr, zi = zr*zr - zi*zi + cr, 2*zr*zi + ci
                    iteration += 1
                if 5 < iteration < 18:
                    dot_r = max(0.3, (iteration - 5) * 0.15)
                    dx = cx + px * scale
                    dy = cy + py * scale
                    if abs(dx - cx) < half and abs(dy - cy) < half:
                        c.circle(dx, dy, dot_r, stroke=1, fill=0)

    elif page_type == "dragon_curve":
        c.setLineWidth(1.0)
        # generate dragon curve sequence
        seq = [0]
        for _ in range(12):
            seq = seq + [1] + [1-x for x in reversed(seq)]
        # draw
        x, y = cx - size*0.1, cy
        angle = 0
        step = size * 0.006
        for turn in seq:
            x2 = x + step * math.cos(angle)
            y2 = y + step * math.sin(angle)
            if abs(x2 - cx) < half and abs(y2 - cy) < half:
                c.line(x, y, x2, y2)
            x, y = x2, y2
            angle += math.pi/2 if turn == 1 else -math.pi/2

    elif page_type == "spiral_fractal":
        c.setLineWidth(1.0)
        # golden ratio spiral with fractal branches
        phi = (1 + math.sqrt(5)) / 2
        for arm in range(rng.randint(3, 6)):
            arm_offset = arm * 2 * math.pi / 6
            for t in range(300):
                angle = t * 0.08 + arm_offset
                r = size * 0.003 * t
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                if abs(x - cx) > half or abs(y - cy) > half: continue
                dot_r = max(0.3, min(1.5, t * 0.005))
                c.circle(x, y, dot_r, stroke=1, fill=0)
                # branches at intervals
                if t > 20 and t % 15 == 0:
                    br = r * 0.3
                    ba = angle + math.pi/2
                    bx = x + br * math.cos(ba)
                    by = y + br * math.sin(ba)
                    if abs(bx - cx) < half and abs(by - cy) < half:
                        c.line(x, y, bx, by)
                        c.circle(bx, by, dot_r * 1.5, stroke=1, fill=0)

    elif page_type == "nested_polygon":
        c.setLineWidth(1.0)
        sides_list = [3, 4, 5, 6, 7, 8, 9, 10, 12]
        for layer, sides in enumerate(sides_list):
            r = size * (0.04 + layer * 0.04)
            rotation = layer * math.pi / (sides * 2)
            c.setLineWidth(max(0.6, 1.5 - layer * 0.1))
            p = c.beginPath()
            for i in range(sides + 1):
                angle = (2*math.pi/sides) * i + rotation
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                if i == 0: p.moveTo(x, y)
                else: p.lineTo(x, y)
            c.drawPath(p, stroke=1, fill=0)
            # connect vertices to center
            if layer < 5:
                c.setLineWidth(0.5)
                for i in range(sides):
                    angle = (2*math.pi/sides) * i + rotation
                    x = cx + r * math.cos(angle)
                    y = cy + r * math.sin(angle)
                    ir = size * 0.03
                    c.line(cx + ir*math.cos(angle), cy + ir*math.sin(angle), x, y)

    elif page_type == "recursive_star":
        c.setLineWidth(1.2)
        def recursive_star(cx, cy, r, points, depth):
            if depth == 0 or r < 2: return
            p = c.beginPath()
            for i in range(points * 2):
                angle = (math.pi / points) * i - math.pi/2
                rad = r if i % 2 == 0 else r * 0.4
                x = cx + rad * math.cos(angle)
                y = cy + rad * math.sin(angle)
                if i == 0: p.moveTo(x, y)
                else: p.lineTo(x, y)
            p.close()
            c.drawPath(p, stroke=1, fill=0)
            # recurse at each point
            for i in range(points):
                angle = (2*math.pi / points) * i - math.pi/2
                nx = cx + r * 0.85 * math.cos(angle)
                ny = cy + r * 0.85 * math.sin(angle)
                recursive_star(nx, ny, r * 0.35, points, depth-1)
        recursive_star(cx, cy, size * 0.35, rng.choice([5, 6]), 3)

    coloring_border(c, cx, cy, size, weight=1.5)


# ══════════════════════════════════════════════
# ADVANCED 2: ARCHITECTURAL VISIONS
# Intricate buildings, cityscapes, architectural details
# ══════════════════════════════════════════════

def draw_advanced_architect(c, cx, cy, size, seed, rng=None):
    if not rng: rng = random.Random(seed)
    c.setStrokeColor(INK)
    c.setLineCap(1)
    c.setLineJoin(1)

    page_type = rng.choice(["cathedral", "cityscape", "arch_detail", "staircase",
                            "dome_interior", "bridge", "tower_row", "window_wall"])

    half = size * 0.44

    if page_type == "cathedral":
        c.setLineWidth(1.5)
        # main structure
        bw, bh = size*0.5, size*0.55
        bx, by = cx - bw/2, cy - size*0.3
        c.rect(bx, by, bw, bh, stroke=1, fill=0)
        # pointed arch entrance
        c.setLineWidth(1.8)
        aw, ah = bw*0.3, bh*0.4
        ax = cx - aw/2
        ay = by
        c.rect(ax, ay, aw, ah*0.6, stroke=1, fill=0)
        p = c.beginPath()
        p.moveTo(ax, ay + ah*0.6)
        p.curveTo(ax, ay + ah, ax + aw, ay + ah, ax + aw, ay + ah*0.6)
        c.drawPath(p, stroke=1, fill=0)
        # rose window
        c.setLineWidth(1.2)
        rw_r = bw * 0.15
        rw_y = by + bh * 0.72
        c.circle(cx, rw_y, rw_r, stroke=1, fill=0)
        c.circle(cx, rw_y, rw_r*0.7, stroke=1, fill=0)
        c.circle(cx, rw_y, rw_r*0.4, stroke=1, fill=0)
        # spokes
        c.setLineWidth(0.8)
        for i in range(12):
            a = (2*math.pi/12) * i
            c.line(cx + rw_r*0.4*math.cos(a), rw_y + rw_r*0.4*math.sin(a),
                   cx + rw_r*math.cos(a), rw_y + rw_r*math.sin(a))
        # towers
        c.setLineWidth(1.5)
        for side in [-1, 1]:
            tx = cx + side * (bw/2 + size*0.04)
            tw, th = size*0.08, bh + size*0.12
            c.rect(tx - tw/2, by, tw, th, stroke=1, fill=0)
            # spire
            p = c.beginPath()
            p.moveTo(tx - tw/2, by + th)
            p.lineTo(tx, by + th + size*0.1)
            p.lineTo(tx + tw/2, by + th)
            p.close()
            c.drawPath(p, stroke=1, fill=0)
            # tower windows
            c.setLineWidth(0.8)
            for wi in range(4):
                wy = by + size*0.04 + wi * th*0.2
                c.rect(tx - tw*0.2, wy, tw*0.4, th*0.08, stroke=1, fill=0)
            c.setLineWidth(1.5)
        # flying buttresses
        c.setLineWidth(1.0)
        for side in [-1, 1]:
            for bi in range(2):
                bby = by + bh * (0.3 + bi * 0.3)
                bbx = cx + side * bw/2
                bbx2 = cx + side * (bw/2 + size*0.12)
                p = c.beginPath()
                p.moveTo(bbx, bby)
                p.curveTo(bbx + side*size*0.04, bby + size*0.08, bbx2, bby + size*0.02, bbx2, bby - size*0.02)
                c.drawPath(p, stroke=1, fill=0)

    elif page_type == "cityscape":
        c.setLineWidth(1.2)
        base_y = cy - size*0.25
        # ground line
        c.setLineWidth(1.5)
        c.line(cx - half, base_y, cx + half, base_y)
        # buildings
        c.setLineWidth(1.2)
        x = cx - half * 0.85
        while x < cx + half * 0.85:
            bw = rng.uniform(size*0.04, size*0.1)
            bh = rng.uniform(size*0.15, size*0.55)
            c.rect(x, base_y, bw, bh, stroke=1, fill=0)
            # windows
            c.setLineWidth(0.6)
            w_cols = max(1, int(bw / (size*0.025)))
            w_rows = max(1, int(bh / (size*0.04)))
            ww = bw * 0.5 / w_cols
            wh = size * 0.015
            for wr in range(w_rows):
                for wc in range(w_cols):
                    wx = x + bw*0.15 + wc * (bw*0.7/max(1, w_cols-1)) if w_cols > 1 else x + bw/2 - ww/2
                    wy = base_y + bh*0.08 + wr * (bh*0.85/w_rows)
                    c.rect(wx, wy, ww, wh, stroke=1, fill=0)
            c.setLineWidth(1.2)
            # roof detail
            roof_type = rng.choice(["flat", "peak", "dome"])
            if roof_type == "peak":
                p = c.beginPath()
                p.moveTo(x, base_y + bh)
                p.lineTo(x + bw/2, base_y + bh + size*0.03)
                p.lineTo(x + bw, base_y + bh)
                c.drawPath(p, stroke=1, fill=0)
            elif roof_type == "dome":
                # PATCH 3: reportlab 5 removed stroke kwarg from Canvas.arc — use path arc
                dp = c.beginPath()
                dp.arc(x, base_y + bh - size*0.01, x + bw, base_y + bh + size*0.03, 0, 180)
                c.drawPath(dp, stroke=1, fill=0)
            x += bw + rng.uniform(size*0.005, size*0.02)

    elif page_type == "arch_detail":
        c.setLineWidth(1.5)
        # series of ornate arches
        arch_count = 3
        aw = size * 0.25
        spacing = (size * 0.8) / arch_count
        for ai in range(arch_count):
            acx = cx - size*0.35 + ai * spacing + spacing/2
            aby = cy - size*0.2
            ah = size * 0.45
            # pillars
            pw = size * 0.025
            c.rect(acx - aw/2, aby, pw, ah*0.7, stroke=1, fill=0)
            c.rect(acx + aw/2 - pw, aby, pw, ah*0.7, stroke=1, fill=0)
            # pointed arch
            c.setLineWidth(1.8)
            p = c.beginPath()
            p.moveTo(acx - aw/2, aby + ah*0.7)
            p.curveTo(acx - aw/2, aby + ah, acx + aw/2, aby + ah, acx + aw/2, aby + ah*0.7)
            c.drawPath(p, stroke=1, fill=0)
            # inner arch
            c.setLineWidth(1.0)
            iw = aw * 0.7
            p = c.beginPath()
            p.moveTo(acx - iw/2, aby + ah*0.6)
            p.curveTo(acx - iw/2, aby + ah*0.9, acx + iw/2, aby + ah*0.9, acx + iw/2, aby + ah*0.6)
            c.drawPath(p, stroke=1, fill=0)
            # keystone detail
            c.setLineWidth(0.8)
            for spoke in range(7):
                sa = math.pi * spoke / 6
                c.line(acx + iw*0.05*math.cos(sa), aby + ah*0.75 + iw*0.05*math.sin(sa),
                       acx + iw*0.4*math.cos(sa), aby + ah*0.75 + iw*0.35*math.sin(sa))
            # column details
            c.setLineWidth(0.6)
            for pi_side in [-1, 1]:
                px = acx + pi_side * (aw/2 - pw/2)
                for li in range(8):
                    ly = aby + li * (ah*0.7/8)
                    c.line(px - pw*0.4, ly, px + pw*0.4, ly)

    elif page_type in ("staircase", "dome_interior", "bridge", "tower_row", "window_wall"):
        c.setLineWidth(1.5)
        if page_type == "staircase":
            # grand spiral staircase
            steps = 40
            c.setLineWidth(1.2)
            for i in range(steps):
                angle = (math.pi * 2) * i / 12
                r = size * 0.08 + i * size*0.008
                x = cx + r * math.cos(angle)
                y = cy - size*0.3 + i * size*0.015
                sw = size * 0.06
                sh = size * 0.01
                c.saveState()
                c.translate(x, y)
                c.rotate(math.degrees(angle))
                c.rect(0, 0, sw, sh, stroke=1, fill=0)
                c.restoreState()
            # central column
            c.setLineWidth(1.8)
            c.line(cx, cy - size*0.3, cx, cy + size*0.35)
            # railing
            c.setLineWidth(0.8)
            for i in range(steps):
                angle = (math.pi * 2) * i / 12
                r = size * 0.08 + i * size * 0.008 + size*0.06
                x = cx + r * math.cos(angle)
                y = cy - size*0.3 + i * size*0.015
                c.line(x, y, x, y + size*0.025)
        else:
            # window wall — grid of ornate windows
            c.setLineWidth(1.0)
            cols, rows = 4, 5
            ww = size * 0.16
            wh = size * 0.13
            gap_x = (size * 0.8 - cols * ww) / (cols + 1)
            gap_y = (size * 0.8 - rows * wh) / (rows + 1)
            for row in range(rows):
                for col in range(cols):
                    wx = cx - size*0.38 + gap_x + col * (ww + gap_x)
                    wy = cy - size*0.35 + gap_y + row * (wh + gap_y)
                    c.rect(wx, wy, ww, wh*0.7, stroke=1, fill=0)
                    # arch top
                    p = c.beginPath()
                    p.moveTo(wx, wy + wh*0.7)
                    p.curveTo(wx, wy + wh, wx + ww, wy + wh, wx + ww, wy + wh*0.7)
                    c.drawPath(p, stroke=1, fill=0)
                    # cross bars
                    c.setLineWidth(0.6)
                    c.line(wx + ww/2, wy, wx + ww/2, wy + wh*0.7)
                    c.line(wx, wy + wh*0.35, wx + ww, wy + wh*0.35)
                    # inner details
                    c.circle(wx + ww/2, wy + wh*0.78, ww*0.15, stroke=1, fill=0)
                    c.setLineWidth(1.0)

    coloring_border(c, cx, cy, size, weight=1.5)


# ══════════════════════════════════════════════
# TEXTURE + COVER + METADATA INFRASTRUCTURE
# ══════════════════════════════════════════════

def make_texture(path: Path, w_px, h_px, rgb, seed=7):
    random.seed(seed)
    img = Image.new("RGB", (w_px, h_px), rgb)
    noise = Image.effect_noise((w_px, h_px), 16).convert("L")
    noise = ImageEnhance.Contrast(noise).enhance(1.4)
    dark = ImageEnhance.Brightness(img).enhance(0.90)
    light = ImageEnhance.Brightness(img).enhance(1.08)
    img = Image.composite(light, dark, noise)
    overlay = Image.new("RGBA", (w_px, h_px), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    r, g, b = rgb
    for y in range(0, h_px, 3):
        d.line([(0, y), (w_px, y)], fill=(min(r+14,255),min(g+14,255),min(b+14,255),22))
    for x in range(0, w_px, 3):
        d.line([(x, 0), (x, h_px)], fill=(max(r-12,0),max(g-12,0),max(b-12,0),18))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img = img.filter(ImageFilter.GaussianBlur(0.35))
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "JPEG", quality=88, optimize=True)  # PATCH 5: JPEG texture (lossless PNG made each wrap 7-16MB)
    return path

def kdp_wrap_size(trim, page_count, ppi=CREAM_PPI):
    tw, th = trim
    spine = page_count * ppi * inch
    return BLEED + tw + spine + tw + BLEED, BLEED + th + BLEED, spine

def back_blurb(desc, limit=250):
    """Back-cover blurb: the longest clean prefix of desc that fits.

    Cut at a sentence boundary when one exists in the back half of the
    budget; otherwise cut at a word boundary and end with "...".
    Replaces the old desc[:250] slice, which chopped words mid-letter
    on the printed back cover ("...portioned desse", "...one sitti").
    """
    d = " ".join(desc.split())
    if len(d) <= limit:
        return d
    seg = d[:limit]
    best = max(seg.rfind(". "), seg.rfind("! "), seg.rfind("? "))
    if best >= limit // 2:
        return seg[:best + 1]
    sp = seg.rfind(" ")
    if sp < limit // 4:
        return seg.rstrip(" ,;:-") + "..."
    return seg[:sp].rstrip(" ,;:-") + "..."

def generate_wrap(path, trim, pages, texture, title_lines, subtitle, blurb, features, ppi=CREAM_PPI):
    tw, th = trim
    wrap_w, wrap_h, spine = kdp_wrap_size(trim, pages, ppi)
    c = canvas.Canvas(str(path), pagesize=(wrap_w, wrap_h))
    c.drawImage(str(texture), 0, 0, wrap_w, wrap_h, preserveAspectRatio=False, mask="auto")
    front_x = BLEED + tw + spine
    cream = CREAM

    # front
    fx = front_x + tw/2
    y = BLEED + th*0.58 + (len(title_lines)-1)*13
    for line in title_lines:
        draw_tracked(c, line, fx, y, "Cormorant-Light", 22, tracking=3.0, color=cream)
        y -= 26
    y -= 6
    draw_hairline(c, fx-42, y, fx+42, GOLD, 0.7)
    y -= 18
    draw_centered(c, subtitle, fx, y, "Inter-Light", 8.5, cream)
    draw_centered(c, AUTHOR.upper(), fx, BLEED+0.5*inch, "Inter-Light", 6.5, cream)

    # back
    bx = BLEED + tw/2
    y = wrap_h - BLEED - 1.2*inch
    draw_paragraph(c, blurb, bx, y, "Inter-Light", 8, tw-inch, 12, cream, align="center")
    y -= 18
    if features:
        c.setFont("Inter-Light", 7.5)
        c.setFillColor(cream)
        for f in features:
            c.drawCentredString(bx, y, f)
            y -= 12

    # barcode
    spine_x = BLEED + tw
    bbx = spine_x - 2.05*inch
    c.setFillColor(HexColor("#FFFFFF"))
    c.rect(bbx, BLEED+0.08*inch, 2*inch, 1.2*inch, stroke=0, fill=1)

    # spine text
    if spine > 0.35*inch:
        c.saveState()
        c.translate(spine_x + spine/2, wrap_h/2)
        c.rotate(-90)
        c.setFillColor(cream)
        c.setFont("Cormorant-Light", 9)
        c.drawCentredString(0, -3, " ".join(title_lines))
        c.restoreState()

    c.save()
    print(f"   wrote {path} ({wrap_w/inch:.3f}\" × {wrap_h/inch:.3f}\", spine {spine/inch:.3f}\")")
    return wrap_w, wrap_h, spine

def generate_png(path, texture, title_lines, subtitle, badge=None):
    W, H = 1800, 2700
    tex = ImageOps.fit(Image.open(texture).convert("RGB"), (W, H), Image.Resampling.LANCZOS)
    veil = Image.new("RGBA", (W, H), (20, 15, 30, 55))
    img = Image.alpha_composite(tex.convert("RGBA"), veil)
    draw = ImageDraw.Draw(img)
    try:
        ft = ImageFont.truetype(str(FONTS/"CormorantGaramond-Light.ttf"), 88)
        fs = ImageFont.truetype(str(FONTS/"Inter-Light.ttf"), 28)
        fb = ImageFont.truetype(str(FONTS/"Inter-Light.ttf"), 22)
    except: ft = fs = fb = ImageFont.load_default()

    def ct(text, y, font, fill=(247,241,230,255), tr=8):
        chars = [(ch, draw.textbbox((0,0), ch, font=font)[2] - draw.textbbox((0,0), ch, font=font)[0]) for ch in text]
        total = sum(w for _,w in chars) + tr*(len(chars)-1)
        x = (W - total)/2
        for ch, cw in chars:
            draw.text((x, y), ch, font=font, fill=fill)
            x += cw + tr

    y = 980
    for line in title_lines:
        ct(line, y, ft, tr=10)
        y += 110
    draw.rectangle([W//2-90, y+30, W//2+90, y+33], fill=(212,181,106,255))
    bbox = draw.textbbox((0,0), subtitle, font=fs)
    draw.text(((W-(bbox[2]-bbox[0]))//2, y+60), subtitle, font=fs, fill=(247,241,230,220))
    if badge:
        bbox = draw.textbbox((0,0), badge, font=fb)
        bw = bbox[2]-bbox[0]+60
        draw.rounded_rectangle([W//2-bw//2, H-350, W//2+bw//2, H-310], radius=10, fill=(255,255,255,35))
        draw.text(((W-(bbox[2]-bbox[0]))//2, H-346), badge, font=fb, fill=(247,241,230,210))
    img.convert("RGB").save(path, "PNG", optimize=True)
    print(f"   wrote {path}")

def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip()+"\n", encoding="utf-8")
    print(f"   wrote {path}")

def zip_pkg(zpath, files):
    zpath.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for f in files:
            f = Path(f)
            if f.exists(): z.write(f, f.name)
    print(f"   packed {zpath}")


# ══════════════════════════════════════════════
# PRODUCT CONFIGS
# ══════════════════════════════════════════════

PRODUCTS = {
    "dump": {
        "title": "The 5-Minute Dump",
        "subtitle": "200 Pages of Rotating Five-Minute Prompts, Undated",
        "trim": DUMP_TRIM, "pages": 200, "paper": "cream", "price": "$9.99",
        "dir": "dump", "tex_rgb": (82, 68, 56), "tex_seed": 21,
        "title_lines": ["THE 5-MINUTE", "DUMP"],
        "categories": "Self-Help > Journaling | Health > ADHD",
        "keywords": "5 minute journal, adhd micro journal, quick journal for anxiety, brain dump notebook, "
                    "low effort journal, journaling for beginners, tiny prompts journal",
        "desc": "Each page takes five minutes or less. No long prompts. No essays. Just brain dumps, body checks, "
                "mood circles, and tiny wins. 30 rotating micro-prompts designed for people who want to journal "
                "but can't commit to paragraphs. Undated. Start anywhere. 5.5 × 8.5 in. 200 pages. Cream paper. "
                "For ADHD, anxiety, depression, and anyone who needs less, not more.",
        "features": ["200 undated pages  ·  5.5 × 8.5 in", "30 rotating micro-prompts",
                     "Circle-and-go format  ·  no paragraphs required", "For people who hate journaling"],
        "badge": "200 PAGES  ·  5 MINUTES  ·  ZERO PRESSURE",
    },
    "parallel": {
        "title": "Parallel Lives",
        "subtitle": "160 Pages of Side-by-Side Prompts: What Happened and How It Felt",
        "trim": PARALLEL_TRIM, "pages": 160, "paper": "cream", "price": "$9.99",
        "dir": "parallel", "tex_rgb": (62, 52, 78), "tex_seed": 23,
        "title_lines": ["PARALLEL", "LIVES"],
        "categories": "Self-Help > Journaling | Self-Help > Personal Transformation",
        "keywords": "side by side journal, parallel journal prompts, therapy journal adults, self awareness notebook, "
                    "cognitive behavioral journal, dual perspective journal, overthinking journal",
        "desc": "Every spread splits the page in two. What happened and how it felt. What you said and what you meant. "
                "The gap between the two sides is where the insight lives. 20 paired prompt themes with reflection "
                "pages every 10 spreads. 7 × 10 in. 160 pages. Cream paper. For divided minds that need to see both sides.",
        "features": ["20 paired prompt themes", "Reflection pages every 10 spreads",
                     "7 × 10 in  ·  160 pages", "For therapy, self-awareness, and overthinking"],
        "badge": "SIDE-BY-SIDE  ·  160 PAGES  ·  SEE BOTH SIDES",
    },
    "night": {
        "title": "The Night Pages",
        "subtitle": "A 5 by 8 Pocket Nightstand Journal for Racing Thoughts",
        "trim": NIGHT_TRIM, "pages": 120, "paper": "cream", "price": "$9.99",
        "dir": "night", "tex_rgb": (28, 32, 48), "tex_seed": 25,
        "title_lines": ["THE NIGHT", "PAGES"],
        "categories": "Self-Help > Journaling | Health > Sleep Disorders",
        "keywords": "insomnia journal, 3am journal, anxiety night journal, cant sleep notebook, "
                    "sleep anxiety journal, nighttime writing journal, worry dump journal",
        "desc": "This journal lives on your nightstand. When your brain won't shut up at 3am, open it. "
                "20 prompts written for the dark. Body scan pages between sections to land you back in your body. "
                "5 × 8 in. 120 pages. Pocket-sized for dark rooms. For insomnia, night anxiety, and 3am brains.",
        "features": ["20 prompts for the 3am brain", "Body scan rest stops",
                     "5 × 8 in pocket size  ·  120 pages", "For insomnia and night anxiety"],
        "badge": "3AM BRAIN  ·  120 PAGES  ·  POCKET SIZE",
    },
    "firststroke": {
        "title": "First Strokes",
        "subtitle": "37 Super Simple Designs with 3 to 5 Large Shapes per Page",
        "trim": COLOR_TRIM, "pages": 100, "paper": "white", "price": "$9.99",
        "dir": "firststroke", "tex_rgb": (172, 88, 52), "tex_seed": 31,
        "title_lines": ["FIRST", "STROKES"],
        "categories": "Crafts > Coloring Books > Easy & Simple | Health > Stress Management",
        "keywords": "easy coloring book adults, beginner coloring book, simple coloring pages, "
                    "large print coloring book, thick lines coloring, first coloring book adults, elderly coloring book",
        "desc": "The simplest coloring book you'll find. 3–5 shapes per page. Lines so thick a marker can't miss. "
                "Stars, hearts, fish, cats, butterflies, houses — nothing intimidating, everything satisfying. "
                "Single-sided. 8.5 × 11 in. 100 pages. For absolute beginners, seniors, kids, and anyone who "
                "wants to color without frustration.",
        "features": ["Super thick lines  ·  3–5 shapes per page", "Stars, hearts, animals, houses",
                     "Single-sided  ·  8.5 × 11", "For beginners, seniors, and stress relief"],
        "badge": "BEGINNER  ·  37 DESIGNS  ·  LARGE SHAPES",
    },
    "garden": {
        "title": "Easy Garden",
        "subtitle": "47 Big and Simple Designs with Thick Lines",
        "trim": COLOR_TRIM, "pages": 100, "paper": "white", "price": "$9.99",
        "dir": "garden", "tex_rgb": (46, 102, 58), "tex_seed": 33,
        "title_lines": ["EASY", "GARDEN"],
        "categories": "Crafts > Coloring Books > Flowers & Botanical | Health > Stress Management",
        "keywords": "easy flower coloring book, simple garden coloring, botanical coloring beginners, "
                    "flower coloring book adults, nature coloring easy, plant coloring book, relaxing coloring flowers",
        "desc": "Sunflowers, tulips, daisies, mushrooms, ladybugs, snails, and bees, all drawn with thick, "
                "forgiving lines. One big subject per page, large fill areas, no tiny gaps. "
                "47 single-sided designs. 8.5 × 11 in. 100 pages.",
        "features": ["Bold botanical illustrations", "One subject per page  ·  large fill areas",
                     "Single-sided  ·  8.5 × 11", "Flowers, bugs, and garden friends"],
        "badge": "BEGINNER  ·  100 PAGES  ·  BOLD BOTANICALS",
    },
    "mosaic": {
        "title": "Mosaic Mind",
        "subtitle": "57 Stained-Glass Mosaics, Tessellations and Islamic Stars",
        "trim": COLOR_TRIM, "pages": 120, "paper": "white", "price": "$9.99",
        "dir": "mosaic", "tex_rgb": (48, 72, 108), "tex_seed": 35,
        "title_lines": ["MOSAIC", "MIND"],
        "categories": "Crafts > Coloring Books > Geometric & Patterns | Crafts > Coloring Books > Mandalas",
        "keywords": "geometric coloring book, mosaic coloring adults, tessellation coloring, "
                    "pattern coloring book, islamic pattern coloring, celtic coloring book, op art coloring",
        "desc": "Hexagonal mosaics, Islamic stars, Celtic knots, op-art circles, chevron fields, and pinwheel "
                "patterns. Tile by tile, each page builds like stained glass. Medium complexity: enough detail "
                "to stay engaged, never overwhelming. 57 single-sided designs. 8.5 × 11 in. 120 pages.",
        "features": ["8 distinct geometric pattern types", "Medium complexity  ·  satisfying detail",
                     "Single-sided  ·  120 pages", "For intermediate colorists"],
        "badge": "INTERMEDIATE  ·  57 DESIGNS  ·  STAINED-GLASS STYLE",
    },
    "woodland": {
        "title": "Woodland Wonders",
        "subtitle": "57 Cottagecore Designs: Owls, Foxes, Mushrooms and Ferns",
        "trim": COLOR_TRIM, "pages": 120, "paper": "white", "price": "$9.99",
        "dir": "woodland", "tex_rgb": (42, 82, 52), "tex_seed": 37,
        "title_lines": ["WOODLAND", "WONDERS"],
        "categories": "Crafts > Coloring Books > Animals | Crafts > Coloring Books > Nature",
        "keywords": "woodland coloring book, forest animal coloring, owl coloring book adults, "
                    "fox deer coloring, nature scenes coloring, wildlife coloring book, mushroom coloring adults",
        "desc": "Owls, foxes, deer, mushroom villages, pine forests, and fern patterns — medium-detail nature "
                "scenes with character details, feather textures, and enough background elements to reward "
                "patient coloring. Single-sided. 8.5 × 11 in. 120 pages. The forest, flattened.",
        "features": ["Owls, foxes, deer, mushrooms, and more", "Medium detail with texture elements",
                     "Single-sided  ·  120 pages", "For nature lovers and intermediate colorists"],
        "badge": "INTERMEDIATE  ·  57 DESIGNS  ·  COTTAGECORE FOREST",
    },
    "fractal": {
        "title": "Fractal Dreams",
        "subtitle": "67 Real Fractals: Sierpinski, Julia Sets and Golden Spirals",
        "trim": COLOR_TRIM, "pages": 140, "paper": "white", "price": "$9.99",
        "dir": "fractal", "tex_rgb": (22, 22, 38), "tex_seed": 39,
        "title_lines": ["FRACTAL", "DREAMS"],
        "categories": "Crafts > Coloring Books > Mandalas & Patterns | Science & Math > Mathematics",
        "keywords": "fractal coloring book, advanced coloring adults, complex coloring patterns, "
                    "mathematical coloring book, sierpinski coloring, sacred geometry coloring advanced, intricate coloring book",
        "desc": "Sierpinski triangles, Koch snowflake mandalas, fractal trees, Julia set dot fields, dragon curves, "
                "golden spirals, nested polygons, and recursive stars — generated from real mathematics. Every page "
                "is unique. Thin precise lines with hundreds of fill regions. Single-sided. 8.5 × 11 in. 140 pages. "
                "Not for beginners. For the colorist who has done everything else.",
        "features": ["8 fractal algorithm types", "Thin precise lines  ·  hundreds of fill areas",
                     "Single-sided  ·  140 pages", "For advanced colorists and math lovers"],
        "badge": "ADVANCED  ·  67 DESIGNS  ·  REAL MATHEMATICS",
    },
    "architect": {
        "title": "Architectural Visions",
        "subtitle": "67 Intricate Cathedrals, Cityscapes and Rose Windows",
        "trim": COLOR_TRIM, "pages": 140, "paper": "white", "price": "$9.99",
        "dir": "architect", "tex_rgb": (54, 60, 94), "tex_seed": 41,
        "title_lines": ["ARCHITECTURAL", "VISIONS"],
        "categories": "Crafts > Coloring Books > Architecture | Crafts > Coloring Books > Cities & Buildings",
        "keywords": "architecture coloring book, building coloring adults, cathedral coloring, "
                    "cityscape coloring book, intricate coloring detailed, advanced coloring buildings, stained glass coloring",
        "desc": "Gothic cathedrals with flying buttresses and rose windows. Dense cityscapes with hundreds of windows. "
                "Ornate arched doorways. Grand spiral staircases. Every page rewards patience with architectural detail "
                "you can get lost in. 67 single-sided designs. 8.5 × 11 in. 140 pages.",
        "features": ["Cathedrals, cityscapes, arches, staircases", "Fine detail with hundreds of fill regions",
                     "Single-sided  ·  140 pages", "For advanced colorists who love architecture"],
        "badge": "ADVANCED  ·  67 DESIGNS  ·  GOTHIC DETAIL",
    },
}

DRAW_FN_MAP = {
    "firststroke": draw_beginner_simple,
    "garden": draw_beginner_garden,
    "mosaic": draw_amateur_mosaic,
    "woodland": draw_amateur_woodland,
    "fractal": draw_advanced_fractal,
    "architect": draw_advanced_architect,
}

COLORING_TIPS = {
    "firststroke": ("beginner", [
        ("Super thick lines", "Every outline is 3-4 points wide. Markers can't miss."),
        ("3–5 shapes per page", "Simple enough to finish in one sitting."),
        ("Single-sided", "Remove and frame your favorites."),
        ("No rules", "There is no wrong color."),
    ]),
    "garden": ("beginner", [
        ("Bold botanicals", "One flower, one bug, one garden scene per page."),
        ("Large fill areas", "Big petals, big leaves, easy to stay inside."),
        ("Single-sided", "The back is blank. Frame what you love."),
        ("Any medium", "Markers, pencils, crayons — all work."),
    ]),
    "mosaic": ("intermediate", [
        ("Medium complexity", "More detail than beginner, less than advanced."),
        ("8 pattern types", "Hexagons, stars, Celtic knots, op-art, and more."),
        ("Satisfying repetition", "Tessellations reward patience with rhythm."),
        ("Single-sided", "120 pages, each one unique."),
    ]),
    "woodland": ("intermediate", [
        ("Forest creatures", "Owls, foxes, deer — with feather and fur detail."),
        ("Nature scenes", "Mushroom villages, pine forests, fern patterns."),
        ("Medium detail", "Enough texture to stay engaged, not enough to frustrate."),
        ("Single-sided", "120 unique pages."),
    ]),
    "fractal": ("advanced", [
        ("Mathematical art", "Sierpinski, Koch, Julia, dragon curves — real algorithms."),
        ("Thin precise lines", "Fine detail with hundreds of tiny fill regions."),
        ("Hours per page", "These are meant to take a long time. That's the point."),
        ("Single-sided", "140 unique fractal pages."),
    ]),
    "architect": ("advanced", [
        ("Architectural detail", "Cathedrals, cityscapes, arches, staircases."),
        ("Hundreds of windows", "Dense urban scenes reward close attention."),
        ("Fine lines", "Precise outlines for colored pencils and fine-tip markers."),
        ("Single-sided", "140 unique architectural pages."),
    ]),
}


# ══════════════════════════════════════════════
# MAIN BUILD
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser()
    all_keys = list(PRODUCTS.keys())
    parser.add_argument("--product", choices=["all"] + all_keys, default="all")
    args = parser.parse_args()

    register_fonts()

    build_list = all_keys if args.product == "all" else [args.product]

    for key in build_list:
        prod = PRODUCTS[key]
        d = RELEASE / prod["dir"]
        d.mkdir(parents=True, exist_ok=True)

    (RELEASE / "packages").mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("NINE PRODUCTS — production build")
    print("=" * 60)

    for key in build_list:
        prod = PRODUCTS[key]
        d = RELEASE / prod["dir"]
        prefix = prod["dir"]

        print(f"\n▸ [{key}] {prod['title']}")

        # texture
        tex_path = ASSETS / f"{prefix}_linen.png"
        make_texture(tex_path, 3900, 3375, prod["tex_rgb"], prod["tex_seed"])

        # interior
        interior_path = d / f"{prefix}_interior.pdf"
        ppi = WHITE_PPI if prod["paper"] == "white" else CREAM_PPI

        if key == "dump":
            actual_pages = generate_dump(interior_path)
        elif key == "parallel":
            actual_pages = generate_parallel(interior_path)
        elif key == "night":
            actual_pages = generate_night(interior_path)
        elif key in DRAW_FN_MAP:
            level, tips = COLORING_TIPS[key]
            actual_pages = build_coloring_book(
                interior_path, prod["title"], prod["subtitle"],
                level, tips, prod["pages"], DRAW_FN_MAP[key], ppi)
        else:
            print(f"   SKIP — unknown key {key}")
            continue

        # cover
        generate_wrap(d / f"{prefix}_cover_wrap.pdf", prod["trim"], actual_pages, tex_path,
                      prod["title_lines"], prod["subtitle"],
                      back_blurb(prod["desc"]), prod["features"], ppi)

        generate_png(d / f"{prefix}_cover.png", tex_path,
                     prod["title_lines"], prod["subtitle"], prod.get("badge"))

        # metadata
        write_text(d / "metadata.txt", f"""TITLE: {prod['title']}
SUBTITLE: {prod['subtitle']}
AUTHOR: {AUTHOR}
FORMAT: Paperback, {prod['trim'][0]/inch}×{prod['trim'][1]/inch} in, {prod['pages']} pages, B&W interior, {prod['paper']} paper, matte, no bleed
PRICE: {prod['price']}
CATEGORIES: {prod['categories']}
KEYWORDS: {prod['keywords']}

DESCRIPTION:
{prod['desc']}""")

        # zip
        zip_pkg(RELEASE / "packages" / f"{prefix}_KDP.zip", [
            d / f"{prefix}_interior.pdf",
            d / f"{prefix}_cover_wrap.pdf",
            d / "metadata.txt",
        ])

    # upload checklist
    write_text(RELEASE / "UPLOAD_CHECKLIST.md", "\n".join([
        "# Upload checklist — 9 products", ""] +
        [f"""## {PRODUCTS[k]['title']}
1. KDP → Create Paperback
2. Title: {PRODUCTS[k]['title']} | Subtitle: {PRODUCTS[k]['subtitle']} | Author: {AUTHOR}
3. Settings: B&W interior, {PRODUCTS[k]['paper'].upper()} paper, {PRODUCTS[k]['trim'][0]/inch}×{PRODUCTS[k]['trim'][1]/inch}, NO bleed, matte
4. Upload {PRODUCTS[k]['dir']}_interior.pdf + {PRODUCTS[k]['dir']}_cover_wrap.pdf
5. Price: {PRODUCTS[k]['price']} | Expanded distribution: OFF
6. Preview → approve → order proof → publish
""" for k in all_keys]))

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)
    for p in sorted(RELEASE.rglob("*")):
        if p.is_file():
            print(f"  {p.relative_to(RELEASE)}  {p.stat().st_size/1024:8.1f} KB")


if __name__ == "__main__":
    main()
