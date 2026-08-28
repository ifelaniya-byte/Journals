"""Section B — nine high-growth wellness journal interiors."""

from __future__ import annotations

import math

from reportlab.lib.units import inch

from lib.kit import (
    FIVE_EIGHT,
    HAIR,
    INK,
    INK2,
    LETTER,
    MID,
    MUTED,
    OUTPUT,
    PALE,
    RULE,
    SIX_NINE,
    WASH,
    GHOST,
    Book,
    G,
    section_opener,
    standard_front,
)

WELL_EXTRA = (
    "This journal is a personal tracking and management tool. It is not treatment, therapy, "
    "or a diagnosis. It does not replace a clinician, counselor, pelvic-floor physical therapist, "
    "registered dietitian, or other licensed professional."
)


def _mini_scale(b: Book, x, y, n=10, gap=11.2, r=3.8):
    for i in range(n):
        b.set_stroke(INK2, 0.6)
        b.c.circle(x + i * gap, y, r, stroke=1, fill=0)


# ===================================================================== 10 sobriety
SOBER_PROMPTS = [
    "What was the first fork in the road today?",
    "Which feeling arrived before the craving, if any?",
    "Where was I, and who was I with, when it got loud?",
    "What did I do in the ten minutes after the urge peaked?",
    "A version of me from 90 days ago would notice what?",
    "What am I proud of that has nothing to do with not drinking?",
    "Which people, rooms, or apps make this easier?",
    "Which people, rooms, or apps make this harder — without villain stories?",
    "What did I eat, and did it change the volume of the day?",
    "Sleep last night, in honest hours.",
    "If I could borrow one skill from tomorrow-me, what is it?",
    "A craving is weather. What was the forecast and what was the sky?",
    "Where did I tell the truth today?",
    "Where did I go quiet when I needed a sentence?",
    "What would a kind witness say about this particular day?",
    "Did I confuse 'bored' with 'in danger'?",
    "A ritual that is replacing the old one — even a small one.",
    "Money, morning, or memory: which benefit showed up?",
    "What I will do with my hands at the usual witching hour.",
    "If I slipped in thought but not in action, what did I learn?",
    "Body notes: gut, head, skin, energy — no drama, just data.",
    "One boundary I kept.",
    "One boundary I need.",
    "A pleasure that is not a substance.",
    "Who can I text before I negotiate with myself?",
    "What did 'enough' feel like tonight?",
    "The story I almost told myself, and the shorter true one.",
    "How I will make tomorrow morning kinder than today's.",
    "A song, walk, shower, or show that helped.",
    "I am allowed to have a boring sober day. What was quietly good?",
]


def _10_day(b: Book, day: int):
    b.begin()
    y = b.header_bar("SOBER / SOBER-CURIOUS", f"Day {day} of 90")
    b.date_line(b.x0, y, b.cw)
    y -= 20
    # day badge
    b.rect(b.x0, y - 36, 54, 36, stroke=INK, sw=0.8, fill=PALE)
    b.text(str(day), b.x0 + 27, y - 26, "Cormorant-Bold", 18, INK, "center")
    b.field("Wake mood", b.x0 + 64, y - 12, 140)
    b.field("Sleep (h)", b.x0 + 220, y - 12, 90)
    b.field("I stayed aligned with my aim", b.x0 + 64, y - 30, 240)
    y -= 48

    h = 78
    b.box(b.x0, y - h, b.cw, h, "Trigger log  (place, people, time, body cue)")
    b.writing_lines(y - 28, 3, gap=15, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8

    b.text("Craving intensity  (peak)", b.x0, y, "Sans-Semi", 7.4, MID)
    _mini_scale(b, b.x0 + 4, y - 16, n=10, gap=14, r=4.2)
    b.text("none", b.x0 + 4, y - 30, "Sans", 6, MUTED)
    b.text("strongest", b.x0 + 4 + 9 * 14, y - 30, "Sans", 6, MUTED)
    b.text("Minutes it lasted", b.x0 + 230, y, "Sans", 7.2, MID)
    b.dotted_field(b.x0 + 310, y, 40)
    y -= 42

    prompt = SOBER_PROMPTS[(day - 1) % len(SOBER_PROMPTS)]
    h = 88
    b.box(b.x0, y - h, b.cw, h, "Reflection")
    b.paragraph(prompt, b.x0 + 8, y - 28, b.cw - 16, "Cormorant-Italic", 10, 13, INK)
    b.writing_lines(y - 56, 2, gap=15, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8

    h = 56
    b.box(b.x0, y - h, b.cw, h, "Gratitude  (one true line)")
    b.writing_lines(y - 28, 1, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8

    b.text("Protective moves I used", b.x0, y, "Sans-Semi", 7.4, MID)
    y -= 16
    for i, lab in enumerate(["Walked", "Ate", "Texted", "Left", "Waited 20", "Meeting / call", "Water", "Other"]):
        b.checkbox(b.x0 + (i % 4) * (b.cw / 4), y - (i // 4) * 16, lab, fs=7.4)
    y -= 40
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "If I struggled: what I need tonight, without a speech", lines=True)
    b.footer()
    b.end()


def _10_week(b: Book, week: int):
    b.begin()
    y = b.header_bar("SOBER / SOBER-CURIOUS", f"Week {week} of 13")
    for p in [
        "Days that matched my aim  (tick)",
        "The loudest trigger, in one sentence",
        "Skills that actually worked",
        "Support I used — and support I still need",
        "A pleasure I want more of next week",
    ]:
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        if "tick" in p:
            b.day_pills(b.x0 + 170, y + 2)
            y -= 28
        else:
            y = b.writing_lines(y - 14, 3, gap=16) - 12
    b.footer()
    b.end()


def build_10(path=None):
    path = path or OUTPUT / "10_Sobriety_and_Sober_Curious_Journal_90_Day_6x9.pdf"
    b = Book(path, SIX_NINE, running="SOBER / SOBER-CURIOUS")
    standard_front(
        b,
        "WELLNESS TRACKING SERIES",
        "Sobriety & Sober-Curious Journal",
        "Ninety undated days: trigger log, craving slider, gratitude, weekly review",
        "Gender-neutral  ·  Not twelve-step branded  ·  6 × 9 in",
        extra_disclaimer=WELL_EXTRA + " If you are physically dependent on alcohol, stopping suddenly can be dangerous. Seek medical care for detox. This book is not a detox protocol.",
        how_to=[
            (
                "One page, one day",
                [
                    "Write the peak craving, not a moral essay. Triggers are logistics (place, time, body) more than identity.",
                    "Protective moves are checkboxes so you can see which skills you actually use.",
                    "This interior is gender-neutral and not affiliated with AA or any recovery brand. Use whatever support system you already have.",
                ],
            )
        ],
        legend=[
            ("Craving 1-10", "Peak intensity"),
            ("Aligned with my aim", "Your definition — abstinence, a pause, or a rule you chose"),
        ],
        goals=[
            "My aim for these 90 days, in one sentence",
            "People I can contact before I negotiate",
            "Rooms and hours that need a plan",
        ],
    )
    section_opener(b, "BEGIN", "90 days", "One page. One honest day.")
    for d in range(1, 91):
        _10_day(b, d)
        if d % 7 == 0:
            _10_week(b, d // 7)
    for _ in range(4):
        b.notes_page()
    return b.save()


# ===================================================================== 11 IF
def _hour_bar(b: Book, x, y, w, h=26):
    b.rect(x, y - h, w, h, stroke=INK2, sw=0.7)
    # 24 ticks
    for i in range(25):
        tx = x + w * i / 24
        tall = h if i % 6 == 0 else (12 if i % 3 == 0 else 7)
        b.line(tx, y - h, tx, y - h + tall, INK2 if i % 6 == 0 else HAIR, 0.5 if i % 6 else 0.35)
        if i % 6 == 0 and i < 24:
            b.text(f"{i:02d}", tx + 2, y - h - 10, "Sans", 5.5, MUTED)
    b.text("24", x + w - 10, y - h - 10, "Sans", 5.5, MUTED)


def _11_day(b: Book, day: int, week: int):
    b.begin()
    y = b.header_bar("FASTING WINDOW TRACKER", f"Week {week}  ·  day {day}")
    b.date_line(b.x0, y, b.cw)
    y -= 20
    b.text("Window I intended", b.x0, y, "Sans-Semi", 7.4, MID)
    for i, lab in enumerate(["12/12", "14/10", "16/8", "18/6", "20/4", "Custom"]):
        b.checkbox(b.x0 + i * 52, y - 16, lab, fs=6.6, size=7.5)
    y -= 36
    b.text("Fast / feed timeline  (shade or tick the hours you fasted)", b.x0, y, "Sans-Semi", 7.4, MID)
    y -= 8
    _hour_bar(b, b.x0, y, b.cw, 28)
    y -= 50
    b.field("Fast started", b.x0, y, 150)
    b.field("First meal", b.x0 + 170, y, 150)
    y -= 18
    b.field("Last meal", b.x0, y, 150)
    b.field("Hours fasted (count)", b.x0 + 170, y, 150)
    y -= 22
    b.text("Water / black coffee / tea / electrolytes  (as you already use them)", b.x0, y, "Sans", 7, MUTED)
    y -= 14
    b.water_row(b.x0, y, n=8, gap=18)
    y -= 28
    b.scale_row("Energy", b.x0, y, b.cw * 0.48, n=10)
    b.scale_row("Mood", b.x0 + b.cw * 0.52, y, b.cw * 0.48, n=10)
    y -= 56
    b.text("Mood mark", b.x0, y, "Sans-Semi", 7.2, MID)
    y -= 16
    for i, lab in enumerate(["Steady", "Irritable", "Foggy", "Clear", "Low", "Fine"]):
        b.checkbox(b.x0 + i * 54, y, lab, fs=6.5, size=7.5)
    y -= 22
    h = 70
    b.box(b.x0, y - h, b.cw, h, "Eating window notes  (protein, how the first meal sat)")
    b.writing_lines(y - 28, 2, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8
    # sparkline box
    h = 56
    b.box(b.x0, y - h, b.cw, h, "Optional weight / measurement sparkline  (one point; skip if unhelpful)")
    b.line(b.x0 + 12, y - 40, b.x1 - 12, y - 40, HAIR, 0.4)
    y -= h + 8
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Tomorrow's window (intention, not a vow)")
    b.footer()
    b.end()


def _11_week(b: Book, week: int):
    b.begin()
    y = b.header_bar("FASTING WINDOW TRACKER", f"Week {week} review")
    # 7 x 24 mini bars conceptually as a table
    b.text("Hours fasted  (write a number in each day)", b.x0, y, "Sans-Semi", 8, MID)
    y -= 16
    rh = 22
    cw = b.cw / 8
    b.c.setFillColor(PALE)
    b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
    for i, d in enumerate(["", "M", "T", "W", "T", "F", "S", "S"]):
        b.rect(b.x0 + i * cw, y - rh, cw, rh, stroke=HAIR, sw=0.4)
        b.text(d, b.x0 + i * cw + cw / 2, y - 14, "Sans-Semi", 8, MID, "center")
    y -= rh
    b.rect(b.x0, y - rh, cw, rh, stroke=HAIR, sw=0.4)
    b.text("Hours", b.x0 + 4, y - 14, "Sans", 7, INK2)
    for i in range(7):
        b.rect(b.x0 + (i + 1) * cw, y - rh, cw, rh, stroke=HAIR, sw=0.4)
    y -= rh + 16
    for p in [
        "Window that felt sustainable",
        "Sleep and energy pattern",
        "Social / work days that need a different shape",
        "Keep / drop / tweak",
    ]:
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 3, gap=16) - 10
    b.footer()
    b.end()


def build_11(path=None):
    path = path or OUTPUT / "11_Intermittent_Fasting_Window_Tracker_12_Week_6x9.pdf"
    b = Book(path, SIX_NINE, running="FASTING WINDOW TRACKER")
    standard_front(
        b,
        "WELLNESS TRACKING SERIES",
        "Intermittent Fasting Window Tracker",
        "Twelve weeks of 24-hour timeline bars, hydration, mood, and weekly reviews",
        "Undated  ·  6 × 9 in",
        extra_disclaimer=WELL_EXTRA + " Fasting is not appropriate for everyone (pregnancy, some medical conditions, history of disordered eating, certain medications). Ask a clinician before you change eating windows.",
        how_to=[
            (
                "Shade the bar, do not chase a brand of fasting",
                [
                    "Tick the window you intended, then shade hours you actually fasted on the 24-hour bar.",
                    "Hydration row is for water and whatever non-caloric drinks you already use. This book does not tell you to black-coffee your way through a morning.",
                    "Skip the weight sparkline if weighing is unhelpful. The window is the point.",
                ],
            )
        ],
        legend=[
            ("24-hour bar", "00 at left, 24 at right. Shade fasted hours."),
            ("Window labels", "Your choice to record — not a prescription"),
        ],
        goals=[
            "Window I am testing, and why",
            "Days of the week that cannot be identical",
            "Stop-rules (dizziness, missed period, obsession) I will not ignore",
        ],
    )
    section_opener(b, "BEGIN", "12 weeks")
    day = 1
    for w in range(1, 13):
        for _ in range(7):
            _11_day(b, day, w)
            day += 1
        _11_week(b, w)
    for _ in range(4):
        b.notes_page()
    return b.save()


# ===================================================================== 12 migraine
def _head_map(b: Book, x, y, s=70):
    """Simple front + right-side head outlines."""
    c = b.c
    # front
    c.setStrokeColor(INK2)
    c.setLineWidth(0.9)
    c.ellipse(x, y, x + s * 0.7, y + s, stroke=1, fill=0)
    c.line(x + s * 0.2, y + s * 0.28, x + s * 0.5, y + s * 0.28)  # mouth-ish
    c.circle(x + s * 0.25, y + s * 0.58, 2.2, stroke=1, fill=1)
    c.circle(x + s * 0.45, y + s * 0.58, 2.2, stroke=1, fill=1)
    b.text("Front", x + s * 0.35, y - 12, "Sans", 6.5, MUTED, "center")
    # zones faint
    b.text("L", x + 4, y + s * 0.7, "Sans", 6, GHOST)
    b.text("R", x + s * 0.55, y + s * 0.7, "Sans", 6, GHOST)
    # side
    x2 = x + s * 0.95
    c.ellipse(x2, y, x2 + s * 0.62, y + s, stroke=1, fill=0)
    c.arc(x2 + s * 0.05, y + s * 0.35, x2 + s * 0.55, y + s * 0.95, 200, 140)
    b.text("Side", x2 + s * 0.31, y - 12, "Sans", 6.5, MUTED, "center")
    b.text("Mark the area. 1-3 spots is enough.", x, y - 24, "Sans", 6.5, MUTED)


def _12_episode(b: Book, n: int):
    b.begin()
    y = b.header_bar("MIGRAINE WEATHER DIARY", f"Episode {n}")
    b.field("Date", b.x0, y, 110)
    b.field("Start time", b.x0 + 125, y, 90)
    b.field("End / still on", b.x0 + 230, y, 100)
    y -= 20
    b.text("Pain 0-10", b.x0, y, "Sans-Semi", 7.4, MID)
    _mini_scale(b, b.x0 + 70, y + 3, n=11, gap=11.5, r=3.8)
    y -= 22
    _head_map(b, b.x0, y - 88, 78)
    # aura / associated
    x = b.x0 + 175
    b.text("Aura / associated", x, y, "Sans-Semi", 7.4, MID)
    items = [
        "Visual aura",
        "Sensory aura",
        "Speech change",
        "Nausea",
        "Light",
        "Sound",
        "Smell",
        "Neck",
        "One-sided",
        "Both sides",
        "Throbbing",
        "Pressure",
    ]
    for i, lab in enumerate(items):
        b.checkbox(x + (i % 2) * 90, y - 18 - (i // 2) * 15, lab, fs=7, size=7.5)
    y -= 110
    # weather
    b.rect(b.x0, y - 52, b.cw, 52, stroke=RULE, sw=0.55, r=3)
    b.text("Weather / pressure  (copy from your app)", b.x0 + 8, y - 14, "Sans-Semi", 7.2, MID)
    b.field("Pressure", b.x0 + 8, y - 32, 90)
    b.field("Temp", b.x0 + 110, y - 32, 70)
    b.field("Humidity", b.x0 + 195, y - 32, 70)
    b.field("Storm / front", b.x0 + 280, y - 32, 50)
    y -= 64
    b.rect(b.x0, y - 52, b.cw, 52, stroke=RULE, sw=0.55, r=3)
    b.text("Possible triggers I noticed  (sleep, food, cycle, screen, stress, skip-meal)", b.x0 + 8, y - 14, "Sans-Semi", 7, MID)
    b.writing_lines(y - 32, 1, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= 62
    b.field("Medication / device used (as already prescribed)", b.x0, y, b.cw)
    y -= 18
    b.field("Response 1h / 2h / next day", b.x0, y, b.cw)
    y -= 18
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Notes for my clinician")
    b.footer()
    b.end()


def _12_month(b: Book, m: int):
    b.begin()
    y = b.header_bar("MIGRAINE WEATHER DIARY", f"Month {m} dashboard")
    b.field("Month / year", b.x0, y, 160)
    y -= 18
    b.text("Episode tally  (shade a box per episode)", b.x0, y, "Sans-Semi", 8, MID)
    y -= 16
    for i in range(16):
        b.rect(b.x0 + i * 20, y - 14, 16, 16, stroke=INK2, sw=0.6)
    y -= 36
    # mini calendar heat
    b.text("Calendar  (write episode numbers on days)", b.x0, y, "Sans-Semi", 8, MID)
    y -= 8
    cell = 28
    for i, d in enumerate("SMTWTFS"):
        b.text(d, b.x0 + i * cell + 10, y - 10, "Sans-Semi", 7, MID, "center")
    y -= 14
    for r in range(5):
        for c in range(7):
            b.rect(b.x0 + c * cell, y - (r + 1) * cell, cell, cell, stroke=HAIR, sw=0.4)
    y -= 5 * cell + 16
    for p in ["Weather pattern I notice", "Sleep / cycle / work pattern", "Treatment pattern (what I already use)", "Questions for clinic"]:
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 2, gap=16) - 10
    b.footer()
    b.end()


def build_12(path=None):
    path = path or OUTPUT / "12_Migraine_Weather_and_Trigger_Diary_6x9.pdf"
    b = Book(path, SIX_NINE, running="MIGRAINE WEATHER DIARY")
    standard_front(
        b,
        "WELLNESS TRACKING SERIES",
        "Migraine Weather & Trigger Diary",
        "Episode pages with pain maps, aura checklists, barometric fields, monthly dashboards",
        "Seventy-two episode pages  ·  twelve monthly dashboards  ·  6 × 9 in",
        extra_disclaimer=WELL_EXTRA + " Sudden 'worst headache of my life,' weakness, vision loss, fever, or a changed pattern needs urgent medical care — not a diary entry.",
        how_to=[
            (
                "Log the episode while it is still true",
                [
                    "Mark the head map with one or two spots. Score peak pain 0-10.",
                    "Copy pressure and weather from any weather app. You are looking for clusters, not proving a theory.",
                    "Monthly dashboards turn scattered episodes into something you can show a clinician.",
                ],
            )
        ],
        legend=[
            ("Pain 0-10", "0 none · 10 worst imaginable"),
            ("Aura boxes", "Tick only what you noticed"),
            ("Front / side map", "Your marks, not a diagnostic diagram"),
        ],
        goals=[
            "My usual warning signs, if any",
            "Medications / devices I already have prescribed",
            "Clinic / headache specialist contact",
        ],
    )
    section_opener(b, "BEGIN", "Episodes & months")
    ep = 1
    for m in range(1, 13):
        _12_month(b, m)
        for _ in range(6):
            _12_episode(b, ep)
            ep += 1
    for _ in range(6):
        b.notes_page()
    return b.save()


# ===================================================================== 13 ADHD
def _13_day(b: Book, day: int):
    b.begin()
    y = b.header_bar("ADHD MEDICATION & FOCUS", f"Day {day}")
    b.date_line(b.x0, y, b.cw)
    y -= 20
    # dose grid
    b.text("Doses as prescribed  (copy time and amount — do not invent)", b.x0, y, "Sans-Semi", 7.3, MID)
    y -= 8
    rh = 18
    headers = ["Time", "Med (name as on bottle)", "Amount as Rx", "Taken?"]
    ws = [0.18, 0.42, 0.24, 0.16]
    b.c.setFillColor(PALE)
    b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
    x = b.x0
    for lab, w in zip(headers, ws):
        b.rect(x, y - rh, w * b.cw, rh, stroke=HAIR, sw=0.4)
        b.text(lab, x + 4, y - 12, "Sans-Semi", 6.5, MID)
        x += w * b.cw
    y -= rh
    for i in range(4):
        x = b.x0
        if i % 2 == 0:
            b.c.setFillColor(WASH)
            b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
        for w in ws:
            b.rect(x, y - rh, w * b.cw, rh, stroke=HAIR, sw=0.35)
            x += w * b.cw
        y -= rh
    y -= 10
    b.text("Side-effect notes today", b.x0, y, "Sans-Semi", 7.3, MID)
    y -= 14
    for i, lab in enumerate(["Appetite", "Sleep", "Mood", "Headache", "Jitters", "Crash", "GI", "Other"]):
        b.checkbox(b.x0 + (i % 4) * (b.cw / 4), y - (i // 4) * 16, lab, fs=7.3)
    y -= 40
    b.field("Crash / wear-off time (if any)", b.x0, y, b.cw)
    y -= 20
    # pomodoros
    b.text("Focus blocks  (fill a box per 25-min block you actually started)", b.x0, y, "Sans-Semi", 7.3, MID)
    y -= 16
    for i in range(10):
        b.rect(b.x0 + i * 28, y - 18, 22, 18, stroke=INK2, sw=0.7, r=2)
    y -= 34
    b.scale_row("Focus quality", b.x0, y, b.cw * 0.48, n=10, left="scattered", right="locked in")
    b.scale_row("Restlessness", b.x0 + b.cw * 0.52, y, b.cw * 0.48, n=10)
    y -= 44
    h = 64
    b.box(b.x0, y - h, b.cw, h, "What the meds did / did not cover today  (observation, not a verdict)")
    b.writing_lines(y - 28, 2, gap=15, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8
    # dopamine stamp
    h = 70
    b.rect(b.x0, y - h, b.cw, h, stroke=RULE, sw=0.6, r=3)
    b.text("Dopamine-reward stamp box", b.x0 + 8, y - 14, "Sans-Semi", 7.2, MID)
    b.text("A sticker, tally, or tiny drawing for a finished block — not for a perfect day.", b.x0 + 8, y - 28, "Sans", 6.8, MUTED)
    for i in range(6):
        b.rect(b.x0 + 8 + i * 48, y - h + 8, 40, 28, stroke=HAIR, sw=0.45, r=2)
    y -= h + 8
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Tomorrow's first block (task + start time)", lines=True)
    b.footer()
    b.end()


def _13_week(b: Book, week: int):
    b.begin()
    y = b.header_bar("ADHD MEDICATION & FOCUS", f"Week {week}")
    for p in [
        "Days the schedule matched the prescription  (tick)",
        "Wear-off / crash pattern",
        "Sleep and appetite pattern",
        "Focus-block average (honest)",
        "Questions for my prescriber",
    ]:
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        if "tick" in p:
            b.day_pills(b.x0 + 210, y + 2)
            y -= 28
        else:
            y = b.writing_lines(y - 14, 3, gap=16) - 10
    b.footer()
    b.end()


def build_13(path=None):
    path = path or OUTPUT / "13_ADHD_Medication_and_Focus_Log_6x9.pdf"
    b = Book(path, SIX_NINE, running="ADHD MEDICATION & FOCUS")
    standard_front(
        b,
        "WELLNESS TRACKING SERIES",
        "ADHD Medication & Focus Log",
        "Dose/time grids, side-effect columns, Pomodoro stamps, weekly reviews",
        "Ninety undated days  ·  6 × 9 in",
        extra_disclaimer=WELL_EXTRA + " Never change a stimulant or non-stimulant dose because a journal 'looks like' it is time. Shortages, crashes, and sleep problems belong in a clinic conversation. This book is not a prescribing guide.",
        how_to=[
            (
                "Record the bottle, not a theory",
                [
                    "Copy the name, amount, and time you were directed to take. Tick 'taken' when you take it.",
                    "Fill a focus box only for a block you started. Empty boxes are information.",
                    "The stamp box is a cheap dopamine close-the-loop. Use stickers or scribbles.",
                ],
            )
        ],
        legend=[
            ("Focus boxes", "One box ≈ one started 25-minute block"),
            ("Crash line", "When the day fell off, if it did"),
        ],
        goals=[
            "Current prescription (copied from the bottle)",
            "Usual start time of the first dose",
            "Sleep cutoff I was given, if any",
        ],
    )
    section_opener(b, "BEGIN", "Daily log")
    for d in range(1, 91):
        _13_day(b, d)
        if d % 7 == 0:
            _13_week(b, d // 7)
    for _ in range(4):
        b.notes_page()
    return b.save()


# ===================================================================== 14 peri
def _wheel(b: Book, cx, cy, r=52, n=5, title="Sleep"):
    b.set_stroke(INK2, 0.8)
    b.c.circle(cx, cy, r, stroke=1, fill=0)
    for i in range(n):
        ang = math.radians(90 - i * (360 / n))
        b.line(cx, cy, cx + r * math.cos(ang), cy + r * math.sin(ang), HAIR, 0.5)
        lab_ang = math.radians(90 - (i + 0.5) * (360 / n))
        b.text(str(i + 1), cx + (r + 10) * math.cos(lab_ang), cy + (r + 10) * math.sin(lab_ang) - 3, "Sans", 6.5, MUTED, "center")
    b.text(title, cx, cy - r - 16, "Sans-Semi", 7, MID, "center")


def _14_day(b: Book, day: int):
    b.begin()
    y = b.header_bar("PERIMENOPAUSE CHART", f"Day {day}")
    b.date_line(b.x0, y, b.cw)
    y -= 18
    b.field("Cycle day (if known)", b.x0, y, 130)
    b.field("Spotting / flow", b.x0 + 170, y, 150)
    y -= 20
    # hot flashes
    b.text("Hot flashes / night sweats  (tally marks)", b.x0, y, "Sans-Semi", 7.4, MID)
    y -= 8
    rh = 20
    for lab in ["Day flashes", "Night sweats"]:
        b.rect(b.x0, y - rh, 80, rh, stroke=HAIR, sw=0.4, fill=WASH)
        b.text(lab, b.x0 + 4, y - 14, "Sans", 7, INK2)
        b.rect(b.x0 + 80, y - rh, b.cw - 80, rh, stroke=HAIR, sw=0.4)
        y -= rh
    y -= 10
    b.text("Peak intensity", b.x0, y, "Sans-Semi", 7.2, MID)
    b.slider(b.x0 + 90, y + 3, 200, ticks=5, labels=["1", "2", "3", "4", "5"])
    y -= 28
    # wheel + mood
    _wheel(b, b.x0 + 58, y - 58, 48, 5, "Sleep quality")
    b.text("Mood / mind", b.x0 + 130, y, "Sans-Semi", 7.4, MID)
    items = ["Even", "Low", "Rage", "Fog", "Anxious", "Tearful", "Wired-tired", "OK"]
    for i, lab in enumerate(items):
        b.checkbox(b.x0 + 130 + (i % 2) * 100, y - 18 - (i // 2) * 15, lab, fs=7.2)
    y -= 158
    b.text("Other observations", b.x0, y, "Sans-Semi", 7.4, MID)
    y -= 14
    for i, lab in enumerate(["Heart notice", "Joint", "Libido change", "Headache", "Bloat", "Itch / skin", "UTI-ish", "Other"]):
        b.checkbox(b.x0 + (i % 4) * (b.cw / 4), y - (i // 4) * 16, lab, fs=7)
    y -= 42
    h = 70
    b.box(b.x0, y - h, b.cw, h, "What actually helped today  (layer, fan, walk, food, rest — your list)")
    b.writing_lines(y - 28, 2, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Note for my clinician  (if I would mention this day)")
    b.footer()
    b.end()


def _14_month(b: Book, m: int):
    b.begin()
    y = b.header_bar("PERIMENOPAUSE CHART", f"Month {m}  ·  cycle timeline")
    b.field("Month / year", b.x0, y, 160)
    y -= 18
    b.text("Bleed / spotting timeline  (mark days 1-31)", b.x0, y, "Sans-Semi", 8, MID)
    y -= 16
    cell = 18
    for i in range(31):
        col = i % 16
        row = i // 16
        x = b.x0 + col * (cell + 2)
        yy = y - row * 36
        b.rect(x, yy - cell, cell, cell, stroke=HAIR, sw=0.45)
        b.text(str(i + 1), x + cell / 2, yy - 12, "Sans", 6, MUTED, "center")
    y -= 84
    for p in [
        "Cycle length this month (if any period started)",
        "Hot-flash pattern (day vs night, week-by-week)",
        "Sleep pattern",
        "Questions for my clinician",
        "What I want from the next visit",
    ]:
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 2, gap=16) - 10
    b.footer()
    b.end()


def build_14(path=None):
    path = path or OUTPUT / "14_Perimenopause_Symptom_and_Mood_Chart_6x9.pdf"
    b = Book(path, SIX_NINE, running="PERIMENOPAUSE CHART")
    standard_front(
        b,
        "WELLNESS TRACKING SERIES",
        "Perimenopause Symptom & Mood Chart",
        "Daily hot-flash tallies, sleep wheels, cycle timelines, clinic question lists",
        "Ninety undated days  ·  six monthly reviews  ·  6 × 9 in",
        extra_disclaimer=WELL_EXTRA + " Chest pain, fainting, flooding that soaks protection hourly, or sudden one-sided weakness needs urgent care.",
        how_to=[
            (
                "Tally, do not diagnose",
                [
                    "Use tally marks for flashes and sweats. Intensity is the peak, 1-5.",
                    "Shade a slice of the sleep wheel (1 poor - 5 restored).",
                    "Monthly timeline is for spotting cycle length when cycles are chaotic — which they often are.",
                ],
            )
        ],
        legend=[
            ("Sleep wheel", "Circle a number 1-5 or shade a slice"),
            ("Cycle day", "Leave blank if you cannot number it. That is data too."),
        ],
        goals=[
            "What I most want to understand (sleep, mood, cycle, heat)",
            "Clinician I will bring this to",
        ],
    )
    section_opener(b, "BEGIN", "Daily chart")
    for d in range(1, 91):
        _14_day(b, d)
        if d % 15 == 0:
            _14_month(b, d // 15)
    for _ in range(4):
        b.notes_page()
    return b.save()


# ===================================================================== 15 FODMAP
BRISTOL = [
    ("1", "Hard"),
    ("2", "Lumpy"),
    ("3", "Cracked"),
    ("4", "Smooth"),
    ("5", "Soft"),
    ("6", "Mushy"),
    ("7", "Watery"),
]


def _15_day(b: Book, day: int, week: int):
    b.begin()
    y = b.header_bar("GUT & LOW-FODMAP DIARY", f"Week {week}  ·  day {day}")
    b.date_line(b.x0, y, b.cw)
    y -= 18
    b.text("Phase", b.x0, y, "Sans-Semi", 7.4, MID)
    for i, lab in enumerate(["Baseline", "Elimination", "Reintroduce", "Personalize"]):
        b.checkbox(b.x0 + 40 + i * 72, y, lab, fs=6.8, size=7.5)
    y -= 18
    # meals
    for name in ["Breakfast", "Lunch", "Dinner", "Extras"]:
        h = 52
        b.rect(b.x0, y - h, b.cw, h, stroke=RULE, sw=0.5, r=2)
        b.text(name, b.x0 + 6, y - 12, "Sans-Semi", 7.2, MID)
        b.field("Time", b.x0 + 70, y - 12, 70)
        b.writing_lines(y - 28, 2, gap=13, x0=b.x0 + 6, x1=b.x1 - 6)
        y -= h + 5
    y -= 4
    b.text("Symptoms  ·  latency from last meal", b.x0, y, "Sans-Semi", 7.4, MID)
    y -= 14
    for i, lab in enumerate(["Pain", "Bloat", "Gas", "Reflux", "Urgency", "Fatigue", "Fog", "Other"]):
        b.checkbox(b.x0 + (i % 4) * (b.cw / 4), y - (i // 4) * 15, lab, fs=7)
    y -= 40
    b.field("Latency (minutes)", b.x0, y, 120)
    b.field("Severity 1-5", b.x0 + 160, y, 80)
    y -= 18
    b.text("Stool  (Bristol 1-7)  — tracking only", b.x0, y, "Sans-Semi", 7.2, MID)
    y -= 14
    cell_w = b.cw / 7
    for i, (n, desc) in enumerate(BRISTOL):
        x = b.x0 + i * cell_w
        b.rect(x, y - 36, cell_w - 3, 36, stroke=HAIR, sw=0.4, r=2)
        b.text(n, x + (cell_w - 3) / 2, y - 14, "Sans-Semi", 9, INK, "center")
        b.text(desc, x + (cell_w - 3) / 2, y - 28, "Sans", 6, MUTED, "center")
    y -= 48
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Notes  (oil, garlic, wheat, polyols, stress, cycle)", lines=True)
    b.footer()
    b.end()


def _15_week(b: Book, week: int):
    b.begin()
    y = b.header_bar("GUT & LOW-FODMAP DIARY", f"Week {week}  ·  review")
    b.field("Phase this week", b.x0, y, 200)
    y -= 20
    b.box(b.x0, y - 70, b.cw, 70, "Weekly gut goal  (one behavior, not a personality rebuild)")
    b.writing_lines(y - 28, 2, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= 82
    for p in [
        "Foods that seemed quiet",
        "Foods that seemed noisy",
        "Reintroduction candidate (only if my dietitian / plan says so)",
        "Stress / sleep / cycle confounders",
    ]:
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 2, gap=16) - 10
    b.footer()
    b.end()


def _15_reintro(b: Book, n: int):
    b.begin()
    y = b.header_bar("GUT & LOW-FODMAP DIARY", f"Reintroduction card {n}")
    b.paragraph(
        "Only reintroduce when your clinician or dietitian has you in that phase. This card records their plan, not a protocol from a book.",
        b.x0,
        y,
        b.cw,
        "Sans",
        8.3,
        12,
        INK2,
    )
    y -= 40
    b.field("Food / group", b.x0, y, b.cw)
    y -= 20
    b.field("Amount / day 1-3  (as directed)", b.x0, y, b.cw)
    y -= 20
    for p in ["Day 1 observations", "Day 2 observations", "Day 3 observations", "Decision (keep / pause / retry later)"]:
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 3, gap=16) - 10
    b.footer()
    b.end()


def build_15(path=None):
    path = path or OUTPUT / "15_Gut_Health_and_Low_FODMAP_Symptom_Diary_6x9.pdf"
    b = Book(path, SIX_NINE, running="GUT & LOW-FODMAP DIARY")
    standard_front(
        b,
        "WELLNESS TRACKING SERIES",
        "Gut Health & Low-FODMAP Symptom Diary",
        "Meal columns, symptom latency, Bristol chart, reintroduction cards",
        "Eight weeks of daily pages  ·  6 × 9 in",
        extra_disclaimer=WELL_EXTRA + " A low-FODMAP elimination is meant to be short and supervised. This book does not put you on a diet. Blood in stool, black stool, fever, or unexplained weight loss needs a clinician.",
        how_to=[
            (
                "Meals on the left of the day, body on the bottom",
                [
                    "Write ingredients, not brand slogans. Garlic, onion, wheat, milk, polyols are the usual suspects — tick them in notes if they showed up.",
                    "Latency is minutes from the last meal to the first symptom.",
                    "Bristol types are a tracking shorthand, not a diagnosis. Circle one.",
                    "Reintroduction cards are blank on purpose. Fill them from a dietitian's plan.",
                ],
            )
        ],
        legend=[("Bristol 1-7", "1 hard lumps · 4 smooth · 7 watery"), ("Phase ticks", "Where you are in YOUR plan")],
        goals=[
            "Who is supervising this (RD / GI / none yet)",
            "Foods I already know are loud",
            "My one weekly gut goal",
        ],
    )
    section_opener(b, "BEGIN", "Daily food & symptom pages")
    day = 1
    for w in range(1, 9):
        for _ in range(7):
            _15_day(b, day, w)
            day += 1
        _15_week(b, w)
    section_opener(b, "PHASE", "Reintroduction cards", "Use only if your own plan says so.")
    for n in range(1, 13):
        _15_reintro(b, n)
    for _ in range(4):
        b.notes_page()
    return b.save()


# ===================================================================== 16 digital detox
DETOX_PROMPTS = [
    "Which app did I open without deciding to?",
    "What feeling did I reach for a screen to skip?",
    "Where did my thumb go first this morning?",
    "A notification I do not actually need.",
    "What did boredom feel like in my body?",
    "One conversation that deserved my whole face.",
    "The time of day the pull is strongest.",
    "What I would do with 20 uncaptured minutes.",
    "A comparison spiral I can name without shame.",
    "Which room in my home should be screen-quiet?",
    "Did I sleep next to a phone? What did that cost?",
    "A creator or feed that leaves me worse.",
    "A tool that is actually a tool.",
    "Who benefits from my extra hour of scroll?",
    "What I missed because I was half-there.",
    "A rule that is kind, not punitive.",
    "How I will charge the phone tonight.",
    "A paper, walk, or sink of dishes that is the real world.",
    "The story I tell about 'I have to be reachable.'",
    "One app I can delete for 24 hours as an experiment.",
    "What did I look up that I already know?",
    "A craving for news versus a need for news.",
    "How my neck and eyes feel right now.",
    "A person I could text instead of a feed I could scroll.",
    "What 'enough internet' would look like today.",
    "The last beautiful unphotographed thing I saw.",
    "A boundary I can keep on a workday.",
    "If my home screen were honest, what would it show?",
    "What I want my attention to be for.",
    "How I will close this 30-day experiment without a binge.",
]


def _16_left(b: Book, day: int):
    b.begin()
    y = b.header_bar("DIGITAL DETOX 30", f"Day {day} of 30")
    b.date_line(b.x0, y, b.cw)
    y -= 20
    b.rect(b.x0, y - 48, 58, 48, stroke=INK, sw=0.8, fill=PALE)
    b.text(str(day), b.x0 + 29, y - 34, "Cormorant-Bold", 22, INK, "center")
    b.field("Phone pickup intent", b.x0 + 70, y - 14, 240)
    b.field("First app", b.x0 + 70, y - 34, 240)
    y -= 60
    b.text("App-usage bar  (shade hours of recreational screen time, 0-12)", b.x0, y, "Sans-Semi", 7.3, MID)
    y -= 10
    bw = b.cw
    bh = 22
    b.rect(b.x0, y - bh, bw, bh, stroke=INK2, sw=0.7)
    for i in range(13):
        tx = b.x0 + bw * i / 12
        b.line(tx, y - bh, tx, y, HAIR, 0.35)
        b.text(str(i), tx, y - bh - 10, "Sans", 5.5, MUTED, "center")
    y -= 42
    b.field("Hours (from Screen Time / Digital Wellbeing)", b.x0, y, b.cw)
    y -= 18
    b.field("Pickups / unlocks", b.x0, y, b.cw * 0.48)
    b.field("Notifications I allowed", b.x0 + b.cw * 0.52, y, b.cw * 0.48)
    y -= 22
    h = 80
    b.box(b.x0, y - h, b.cw, h, "Dopamine trigger  (boredom, anxiety, envy, habit, loneliness, work-avoidance)")
    b.writing_lines(y - 28, 3, gap=15, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8
    prompt = DETOX_PROMPTS[(day - 1) % 30]
    h = 88
    b.box(b.x0, y - h, b.cw, h, "Today's question")
    b.paragraph(prompt, b.x0 + 8, y - 28, b.cw - 16, "Cormorant-Italic", 11, 14, INK)
    b.writing_lines(y - 58, 2, gap=15, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "One sentence I want to remember", lines=True)
    b.footer()
    b.end()


def _16_right(b: Book, day: int):
    b.begin()
    y = b.header_bar("DIGITAL DETOX 30", f"Day {day}  ·  real world")
    h = 110
    b.box(b.x0, y - h, b.cw, h, "Real-world substitutions I used")
    for i, lab in enumerate(
        ["Walk", "Paper book", "Cook", "Call / voice", "Analog hobby", "Nap / rest", "Body / stretch", "People in a room", "Chore", "Outside", "Journal", "Other"]
    ):
        b.checkbox(b.x0 + 10 + (i % 3) * (b.cw / 3), y - 36 - (i // 3) * 16, lab, fs=7.4)
    y -= h + 10
    h = 80
    b.box(b.x0, y - h, b.cw, h, "When I reached and then stopped — what I did with my hands")
    b.writing_lines(y - 28, 3, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 10
    b.scale_row("Presence", b.x0, y, b.cw * 0.48, left="split", right="here")
    b.scale_row("Urge strength", b.x0 + b.cw * 0.52, y, b.cw * 0.48)
    y -= 46
    h = 80
    b.box(b.x0, y - h, b.cw, h, "Night  (charge location, last pickup, sleep)")
    b.writing_lines(y - 28, 3, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 10
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Rule I will keep tomorrow  (small enough to keep)")
    b.footer()
    b.end()


def build_16(path=None):
    path = path or OUTPUT / "16_Digital_Detox_Screen_Time_Workbook_30_Day_6x9.pdf"
    b = Book(path, SIX_NINE, running="DIGITAL DETOX 30")
    standard_front(
        b,
        "WELLNESS TRACKING SERIES",
        "Digital Detox Screen-Time Workbook",
        "Thirty two-page days: usage bars, dopamine notes, substitution lists",
        "Plus a 20-day maintenance coda  ·  6 × 9 in  ·  Minimalist interior",
        extra_disclaimer=WELL_EXTRA,
        how_to=[
            (
                "Measure, then substitute",
                [
                    "Copy hours from iOS Screen Time or Android Digital Wellbeing. Shade the 0-12 hour bar.",
                    "Name the trigger in plain language. Then tick a real-world substitution you actually did.",
                    "After 30 days, use the maintenance pages so the rebound binge has somewhere honest to go.",
                ],
            )
        ],
        legend=[("Usage bar", "Recreational hours, 0-12"), ("Presence scale", "How split-brained the day felt")],
        goals=[
            "Why I want my attention back",
            "Apps that are tools vs slots",
            "Charge-the-phone-outside-the-bedroom rule (yes/no)",
        ],
    )
    section_opener(b, "BEGIN", "30-day experiment")
    for d in range(1, 31):
        _16_left(b, d)
        _16_right(b, d)
        if d % 7 == 0:
            b.begin()
            y = b.header_bar("DIGITAL DETOX 30", f"Week {d//7} review")
            for p in ["Average hours", "Strongest trigger", "Substitution that stuck", "Rule for next week"]:
                b.text(p, b.x0, y, "Sans-Semi", 8, MID)
                y = b.writing_lines(y - 14, 3, gap=16) - 12
            b.footer()
            b.end()
    section_opener(b, "AFTER", "Maintenance days", "Lighter pages so the experiment does not cliff.")
    for d in range(1, 21):
        b.begin()
        y = b.header_bar("DIGITAL DETOX 30", f"Maintenance {d}")
        b.date_line(b.x0, y, b.cw)
        y -= 22
        b.field("Hours", b.x0, y, 120)
        b.field("First app", b.x0 + 140, y, 180)
        y -= 22
        b.scale_row("Presence", b.x0, y, b.cw)
        y -= 40
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Notes")
        b.footer()
        b.end()
    for _ in range(4):
        b.notes_page()
    return b.save()


# ===================================================================== 17 postpartum
def _17_day(b: Book, day: int, week: int):
    b.begin()
    y = b.header_bar("POSTPARTUM RECOVERY PLANNER", f"Week {week}  ·  day {day}")
    b.date_line(b.x0, y, b.cw)
    y -= 18
    b.field("Weeks postpartum", b.x0, y, 100)
    b.field("Baby sleep (rough)", b.x0 + 140, y, 180)
    y -= 20
    b.text("Only movements and checks your own clinician / pelvic-floor PT has cleared.", b.x0, y, "Sans", 7, MUTED)
    y -= 14
    b.text("PT homework I was given  (tick if I did the assigned items — not extra)", b.x0, y, "Sans-Semi", 7.2, MID)
    y -= 14
    for i in range(6):
        b.checkbox(b.x0, y - i * 16, f"Assigned item {i+1}:", fs=7.5)
        b.dotted_field(b.x0 + 118, y - i * 16, 200)
    y -= 6 * 16 + 10
    b.text("Body notes  (tracking, not diagnosing)", b.x0, y, "Sans-Semi", 7.3, MID)
    y -= 14
    for i, lab in enumerate(["Bleeding", "Stitches / incision", "Pelvic pressure", "Leak with cough", "Back / SI", "Headache", "Mood dip", "Anxiety spike", "Feverish", "Breast / chest", "Bowel", "Other"]):
        b.checkbox(b.x0 + (i % 3) * (b.cw / 3), y - (i // 3) * 15, lab, fs=6.8, size=7.5)
    y -= 15 * 4 + 8
    h = 60
    b.box(b.x0, y - h, b.cw, h, "Stitches / incision care I was already taught  (what I did today)")
    b.writing_lines(y - 28, 2, gap=14, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8
    b.scale_row("Mood", b.x0, y, b.cw * 0.48, n=10)
    b.scale_row("Energy", b.x0 + b.cw * 0.52, y, b.cw * 0.48, n=10)
    y -= 44
    h = 56
    b.box(b.x0, y - h, b.cw, h, "Partner / support prompt  (what I needed, what I asked for, what landed)")
    b.writing_lines(y - 28, 2, gap=14, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 6
    rh = max(48, y - (b.y0 + 16))
    b.rect(b.x0, b.y0 + 16, b.cw, rh, stroke=INK, sw=0.7, fill=PALE, r=3)
    b.paragraph(
        "Red-flag: heavy bleeding, fever, chest pain, or thoughts of harm. Call emergency / your clinician now — do not wait to journal it.",
        b.x0 + 8,
        b.y0 + 16 + rh - 16,
        b.cw - 16,
        "Sans-Semi",
        7.4,
        11,
        INK,
    )
    b.footer()
    b.end()


def build_17(path=None):
    path = path or OUTPUT / "17_Postpartum_Core_and_Pelvic_Floor_Recovery_Planner_6x9.pdf"
    b = Book(path, SIX_NINE, running="POSTPARTUM RECOVERY PLANNER")
    standard_front(
        b,
        "WELLNESS TRACKING SERIES",
        "Postpartum Core & Pelvic-Floor Recovery Planner",
        "Six-week daily pages plus weeks 7-12: PT homework ticks, mood, stitches care, support prompts",
        "Not an exercise program  ·  6 × 9 in",
        extra_disclaimer=(
            WELL_EXTRA
            + " This is not a physiotherapy protocol and contains no QR workout videos. "
            "Do not begin core or pelvic-floor loading until your own clinician has cleared you. "
            "Heavy bleeding, fever, calf pain, chest pain, shortness of breath, or thoughts of harming yourself or the baby require urgent care."
        ),
        how_to=[
            (
                "Track the plan you were given",
                [
                    "Write the homework your pelvic-floor PT or obstetric clinician assigned. Tick only those items.",
                    "Stitches / incision notes are for what you were taught to do (clean, air, position), not new medical steps.",
                    "The partner prompt exists because recovery is logistical. Ask for one concrete thing.",
                    "Weeks 7-12 are lighter on purpose. Healing is not a six-week cliff.",
                ],
            )
        ],
        legend=[
            ("Assigned item lines", "Copy from your PT sheet"),
            ("Mood 1-10", "A check-in, not a diagnosis of postpartum depression"),
        ],
        goals=[
            "Delivery date / weeks postpartum when I start this book",
            "PT / OB contacts",
            "One person I will ask for help",
        ],
    )
    section_opener(b, "WEEKS 1-6", "Daily recovery pages")
    day = 1
    for w in range(1, 7):
        for _ in range(7):
            _17_day(b, day, w)
            day += 1
        b.begin()
        y = b.header_bar("POSTPARTUM RECOVERY PLANNER", f"Week {w} review")
        for p in ["What felt stronger or quieter", "What still needs a clinician", "Support that worked", "One ask for next week"]:
            b.text(p, b.x0, y, "Sans-Semi", 8, MID)
            y = b.writing_lines(y - 14, 2, gap=16) - 10
        side = 56
        b.rect(b.x0, b.y0 + 18, side, side, stroke=HAIR, sw=0.6, r=2)
        b.text("Optional QR / URL from my PT", b.x0 + side + 10, b.y0 + 50, "Sans-Semi", 7.2, MID)
        b.text("Paste only a link your own clinician sent. This book has no videos.", b.x0 + side + 10, b.y0 + 36, "Sans", 7, MUTED)
        b.footer()
        b.end()
    section_opener(b, "WEEKS 7-12", "Lighter follow-along")
    for w in range(7, 13):
        for d in range(1, 8):
            b.begin()
            y = b.header_bar("POSTPARTUM RECOVERY PLANNER", f"Week {w}  ·  day {d}")
            b.date_line(b.x0, y, b.cw)
            y -= 20
            b.field("PT / movement as cleared", b.x0, y, b.cw)
            y -= 18
            b.scale_row("Mood", b.x0, y, b.cw * 0.48)
            b.scale_row("Energy", b.x0 + b.cw * 0.52, y, b.cw * 0.48)
            y -= 44
            b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Notes / support / clinic")
            b.footer()
            b.end()
    for _ in range(4):
        b.notes_page()
    return b.save()


# ===================================================================== 18 autoimmune
def _spoons(b: Book, x, y, n=12, gap=22):
    for i in range(n):
        cx = x + i * gap
        b.set_stroke(INK2, 0.7)
        b.c.ellipse(cx - 5, y + 4, cx + 5, y + 16, stroke=1, fill=0)
        b.line(cx, y + 4, cx, y - 10, INK2, 0.7)
        b.text(str(i + 1), cx, y - 20, "Sans", 5.5, MUTED, "center")


def _18_day(b: Book, day: int):
    b.begin()
    y = b.header_bar("AUTOIMMUNE FLARE JOURNAL", f"Day {day}")
    b.date_line(b.x0, y, b.cw)
    y -= 20
    b.text("Spoons today  (fill or tick how many you actually have)", b.x0, y, "Sans-Semi", 7.4, MID)
    y -= 8
    _spoons(b, b.x0 + 8, y - 8, 12, gap=26)
    y -= 44
    b.field("Spoons spent", b.x0, y, 120)
    b.field("Spoons left this evening", b.x0 + 160, y, 150)
    y -= 20
    b.text("Symptom severity  0 none  ·  5 worst", b.x0, y, "Sans-Semi", 7.3, MID)
    y -= 8
    rows = ["Pain", "Fatigue", "Brain fog", "GI", "Skin / rash", "Swell", "Feverish", "Mood"]
    lab_w = 78
    cell = (b.cw - lab_w) / 6
    rh = 16
    b.c.setFillColor(PALE)
    b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
    b.text(" ", b.x0 + 4, y - 11, "Sans", 6.5, MID)
    for i in range(6):
        b.text(str(i), b.x0 + lab_w + i * cell + cell / 2, y - 11, "Sans-Semi", 7, MID, "center")
    y -= rh
    for i, lab in enumerate(rows):
        if i % 2 == 0:
            b.c.setFillColor(WASH)
            b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
        b.rect(b.x0, y - rh, lab_w, rh, stroke=HAIR, sw=0.35)
        b.text(lab, b.x0 + 4, y - 11, "Sans", 7, INK2)
        for c in range(6):
            b.rect(b.x0 + lab_w + c * cell, y - rh, cell, rh, stroke=HAIR, sw=0.35)
        y -= rh
    y -= 10
    b.text("Medication as prescribed  (copy from bottles / clinic list)", b.x0, y, "Sans-Semi", 7.3, MID)
    y -= 8
    rh = 17
    headers = ["Time", "Name as labeled", "Amount as Rx", "Taken"]
    ws = [0.16, 0.44, 0.24, 0.16]
    x = b.x0
    b.c.setFillColor(PALE)
    b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
    for lab, w in zip(headers, ws):
        b.rect(x, y - rh, w * b.cw, rh, stroke=HAIR, sw=0.35)
        b.text(lab, x + 3, y - 12, "Sans-Semi", 6.3, MID)
        x += w * b.cw
    y -= rh
    for i in range(4):
        x = b.x0
        for w in ws:
            b.rect(x, y - rh, w * b.cw, rh, stroke=HAIR, sw=0.35)
            x += w * b.cw
        y -= rh
    y -= 10
    h = 56
    b.box(b.x0, y - h, b.cw, h, "What used spoons  /  what gave one back")
    b.writing_lines(y - 28, 2, gap=14, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8
    h = 48
    b.box(b.x0, y - h, b.cw, h, "Gratitude micro-moment")
    b.writing_lines(y - 28, 1, gap=14, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 6
    b.box(b.x0, b.y0 + 16, b.cw, max(36, y - (b.y0 + 16)), "Flare watch  (what I will tell clinic if this stacks)")
    b.footer()
    b.end()


def build_18(path=None):
    path = path or OUTPUT / "18_Autoimmune_Flare_and_Energy_Level_Journal_6x9.pdf"
    b = Book(path, SIX_NINE, running="AUTOIMMUNE FLARE JOURNAL")
    standard_front(
        b,
        "WELLNESS TRACKING SERIES",
        "Autoimmune Flare & Energy-Level Journal",
        "Daily spoon counts, severity grids, medication-as-prescribed tables, gratitude micro-moments",
        "Ninety undated days  ·  6 × 9 in",
        extra_disclaimer=WELL_EXTRA + " Flares, fever, chest pain, or sudden neurological change need clinical care. Do not adjust immune-modulating medication from a paper journal.",
        how_to=[
            (
                "Spoons are a budget, not a personality test",
                [
                    "Tick how many spoons you have at the start of the day. Write how many you spent. This is pacing, not a dare.",
                    "Shade 0-5 for each observation. Blank means you did not notice it.",
                    "Copy medications from the label. The gratitude line is one true thing, not a toxic-positivity tax.",
                ],
            )
        ],
        legend=[
            ("Spoons", "Energy units for the day — your definition"),
            ("0-5 grid", "0 none · 5 worst"),
        ],
        goals=[
            "Conditions I am tracking (my names for them)",
            "Clinician / rheumatology contacts",
            "Early flare signs I already know",
        ],
    )
    section_opener(b, "BEGIN", "Daily pages")
    for d in range(1, 91):
        _18_day(b, d)
        if d % 7 == 0:
            b.begin()
            y = b.header_bar("AUTOIMMUNE FLARE JOURNAL", f"Week {d//7}")
            for p in ["Average spoons", "Flare days (tick)", "Meds as prescribed?", "Rest that helped", "Clinic notes"]:
                b.text(p, b.x0, y, "Sans-Semi", 8, MID)
                if "tick" in p:
                    b.day_pills(b.x0 + 130, y + 2)
                    y -= 26
                else:
                    y = b.writing_lines(y - 14, 3, gap=16) - 10
            b.footer()
            b.end()
    for _ in range(4):
        b.notes_page()
    return b.save()


BUILDERS_B = [
    build_10,
    build_11,
    build_12,
    build_13,
    build_14,
    build_15,
    build_16,
    build_17,
    build_18,
]
