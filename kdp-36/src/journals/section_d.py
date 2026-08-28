"""Volume 2 — nine premium wellness interiors (28–36)."""

from __future__ import annotations

from reportlab.lib.units import inch

from lib.kit import (
    HAIR,
    INK,
    INK2,
    MID,
    MUTED,
    OUTPUT,
    PALE,
    RULE,
    SIX_NINE,
    WASH,
    Book,
    section_opener,
    standard_front,
)
from lib.prompts import ANXIETY_90, CLINIC_Q, GRIEF_90, HABIT_OS
from journals.section_c import _clinic, _toc

WELL = (
    "This journal is a personal tracking tool. It is not therapy, diagnosis, or treatment. "
    "Seek urgent care for chest pain, fainting, thoughts of harm, or a sudden change you cannot explain."
)


def _mini(b, x, y, n=10, gap=12, r=3.8):
    for i in range(n):
        b.set_stroke(INK2, 0.6)
        b.c.circle(x + i * gap, y, r, stroke=1, fill=0)


# ===================================================================== 28 anxiety
def build_28(path=None):
    path = path or OUTPUT / "28_Anxiety_and_Panic_Sensation_Log_6x9.pdf"
    b = Book(path, SIX_NINE, running="ANXIETY & PANIC LOG")
    standard_front(
        b, "WELLNESS COMPANION SERIES", "Anxiety & Panic Sensation Log",
        "Ninety unique prompts, body maps of sensation, peak-and-pass timing",
        "Undated  ·  6 × 9 in  ·  Not a treatment program",
        extra_disclaimer=WELL + " If you might be in medical danger, treat it as medical until a clinician says otherwise.",
        how_to=[("Sensation first, story second", [
            "Name where it started in the body. Time the peak if you can. Then the prompt.",
            "Checking, googling, and reassurance-seeking get a checkbox so you can see the loop.",
            "This is not CBT homework assigned by a book. If you have a therapist, bring pages they ask for.",
        ])],
        legend=[("Peak minutes", "How long the worst of it lasted"), ("Check", "Phone, portal, person, mirror")],
        goals=["My usual first sensation", "2 a.m. plan I already like", "Who I can text without a novel"],
    )
    _toc(b, [("90 days", "unique prompts"), ("Weekly", ""), ("Clinician / therapist brief", "")])
    for d in range(1, 91):
        b.begin()
        y = b.header_bar("ANXIETY & PANIC LOG", f"Day {d}")
        b.date_line(b.x0, y, b.cw)
        y -= 18
        b.field("First sensation (where)", b.x0, y, b.cw)
        y -= 16
        b.field("Peak time / minutes", b.x0, y, 180)
        b.field("Sleep (h)", b.x0 + 200, y, 120)
        y -= 16
        b.text("Loops I used", b.x0, y, "Sans-Semi", 7.4, MID)
        y -= 14
        for i, lab in enumerate(["Googled", "Checked", "Asked twice", "Avoided", "Breathed", "Walked", "Stayed", "Other"]):
            b.checkbox(b.x0 + (i % 4) * (b.cw / 4), y - (i // 4) * 15, lab, fs=7.2)
        y -= 40
        b.scale_row("Intensity", b.x0, y, b.cw)
        y -= 46
        prompt = ANXIETY_90[(d - 1) % 90]
        b.rect(b.x0, y - 70, b.cw, 70, stroke=RULE, sw=0.55, r=3)
        b.paragraph(prompt, b.x0 + 8, y - 18, b.cw - 16, "Cormorant-Italic", 11, 14, INK)
        y -= 80
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "What was actually true an hour later", lines=True)
        b.footer()
        b.end()
        if d % 7 == 0:
            b.begin()
            y = b.header_bar("ANXIETY & PANIC LOG", f"Week {d // 7}")
            for p in ["Most common first sensation", "Loop I used most", "What actually helped", "What I need next week (smaller)"]:
                b.text(p, b.x0, y, "Sans-Semi", 8, MID)
                y = b.writing_lines(y - 14, 3, gap=16) - 10
            b.footer()
            b.end()
    _clinic(b, "Therapist / clinician brief")
    return b.save()


# ===================================================================== 29 sleep
def build_29(path=None):
    path = path or OUTPUT / "29_Sleep_Window_and_Wind_Down_Diary_6x9.pdf"
    b = Book(path, SIX_NINE, running="SLEEP WINDOW DIARY")
    standard_front(
        b, "WELLNESS COMPANION SERIES", "Sleep Window & Wind-Down Diary",
        "Twelve weeks of classic sleep-diary fields: bed, latency, WASO, rise, wind-down",
        "Tracking only — not a sleep-restriction protocol  ·  6 × 9 in",
        extra_disclaimer=WELL + " Loud snoring, witnessed apneas, chest pain, or falling asleep while driving need a clinician.",
        how_to=[("Fill it in the morning", [
            "Bed time, how long to fall asleep (latency), times you woke (WASO), rise time, how you feel.",
            "Wind-down: screens, caffeine, alcohol as you already use them — copy, don't start a protocol from a book.",
            "Weekly page looks for pattern, not a grade.",
        ])],
        legend=[("Latency", "Minutes to fall asleep, guess honestly"), ("WASO", "Wake after sleep onset, minutes")],
        goals=["Window I am aiming for", "Caffeine cutoff I already try", "What 'good enough sleep' means"],
    )
    _toc(b, [("84 nightly pages", "12 weeks"), ("Weekly pattern", ""), ("Clinic brief", "")])
    day = 1
    for w in range(1, 13):
        for _ in range(7):
            b.begin()
            y = b.header_bar("SLEEP WINDOW DIARY", f"Week {w}  ·  night {day}")
            b.date_line(b.x0, y, b.cw)
            y -= 20
            b.field("Lights out", b.x0, y, 100)
            b.field("Latency (min)", b.x0 + 120, y, 90)
            b.field("Rise", b.x0 + 230, y, 90)
            y -= 16
            b.field("WASO (min)", b.x0, y, 100)
            b.field("Hours (guess)", b.x0 + 120, y, 90)
            b.field("Naps", b.x0 + 230, y, 90)
            y -= 18
            b.scale_row("How I feel at rise", b.x0, y, b.cw, left="wrecked", right="ok")
            y -= 48
            b.text("Wind-down", b.x0, y, "Sans-Semi", 8, MID)
            y -= 14
            for i, lab in enumerate(["Screen in bed", "Caffeine after 2", "Alcohol", "Worry loop", "Read / paper", "Other"]):
                b.checkbox(b.x0 + (i % 3) * (b.cw / 3), y - (i // 3) * 15, lab, fs=7.3)
            y -= 42
            b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "What I did that helped or didn't", lines=True)
            b.footer()
            b.end()
            day += 1
        b.begin()
        y = b.header_bar("SLEEP WINDOW DIARY", f"Week {w} pattern")
        for p in ["Average rise / bed (eyeball it)", "Nights that felt human", "Caffeine / screen pattern", "One experiment next week (small)"]:
            b.text(p, b.x0, y, "Sans-Semi", 8, MID)
            y = b.writing_lines(y - 14, 3, gap=16) - 10
        b.footer()
        b.end()
    _clinic(b)
    return b.save()


# ===================================================================== 30 PMDD
def build_30(path=None):
    path = path or OUTPUT / "30_PMDD_and_Cycle_Mood_Chart_6x9.pdf"
    b = Book(path, SIX_NINE, running="CYCLE & PMDD CHART")
    standard_front(
        b, "WELLNESS COMPANION SERIES", "PMDD & Cycle Mood Chart",
        "Six undated cycles of daily mood/irritability/energy with luteal flags",
        "Tracking to share — not a diagnosis  ·  6 × 9 in",
        extra_disclaimer=WELL + " Thoughts of harm, especially cyclically, need urgent care. This chart cannot diagnose PMDD.",
        how_to=[("Daily, then look at the luteal week later", [
            "You do not have to know your cycle day. Mark bleed when it happens. Patterns show up in hindsight.",
            "Score mood, irritability, energy, sleep, breast/bloat 0–5. Flag days you would not trust a big decision.",
            "Bring two cycles to a clinician if that is your goal. One cycle is a weather report; two is a climate hint.",
        ])],
        legend=[("0–5", "0 none · 5 worst / strongest"), ("Flag", "Would not make a life decision today")],
        goals=["Why I want a chart", "Usual cycle length if I know it", "Clinician I might bring this to"],
    )
    _toc(b, [("6 cycles", "28 daily pages + review each"), ("Clinic brief", "")])
    for cyc in range(1, 7):
        section_opener(b, f"CYCLE {cyc}", "Daily chart")
        for d in range(1, 29):
            b.begin()
            y = b.header_bar("CYCLE & PMDD CHART", f"Cycle {cyc}  ·  day {d}")
            b.date_line(b.x0, y, b.cw)
            y -= 18
            b.checkbox(b.x0, y, "Bleed / spotting", fs=8)
            b.checkbox(b.x0 + 120, y, "Flag day", fs=8)
            b.field("Cycle day if known", b.x0 + 200, y, 120)
            y -= 20
            for lab in ["Mood dip", "Irritability", "Anxiety", "Energy crash", "Sleep off", "Breast / bloat", "Rage", "Hopeless"]:
                b.text(lab, b.x0, y, "Sans", 8, INK2)
                _mini(b, b.x0 + 110, y + 3, n=6, gap=14, r=3.6)
                y -= 16
            y -= 6
            b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Notes / what I need from people", lines=True)
            b.footer()
            b.end()
        b.begin()
        y = b.header_bar("CYCLE & PMDD CHART", f"Cycle {cyc} review")
        for p in ["When did the worst cluster (count backward from bleed if you can)", "What I need people to know next luteal week", "Sleep / caffeine / alcohol confounders", "Questions for clinic"]:
            b.text(p, b.x0, y, "Sans-Semi", 8, MID)
            y = b.writing_lines(y - 14, 3, gap=16) - 10
        b.footer()
        b.end()
    _clinic(b)
    return b.save()


# ===================================================================== 31 glucose
def build_31(path=None):
    path = path or OUTPUT / "31_Glucose_and_Meal_Timing_Log_6x9.pdf"
    b = Book(path, SIX_NINE, running="GLUCOSE & MEAL TIMING")
    standard_front(
        b, "WELLNESS COMPANION SERIES", "Glucose & Meal Timing Log",
        "Ninety days to copy meter / CGM readings and meal times as directed",
        "Not a dosing protocol  ·  6 × 9 in",
        extra_disclaimer=WELL + " Do not change insulin or other medication from a paper log. Lows, confusion, or fainting need urgent care.",
        how_to=[("Copy the meter, don't interpret a career", [
            "Write the number, the time, and what you had eaten if that is how you were taught to log.",
            "Targets belong to your clinician. This book leaves them blank on purpose.",
            "CGM graphs live in the app. This is the paper trail for a visit.",
        ])],
        legend=[("As directed", "The schedule you were given"), ("Note", "Exercise, illness, extra food")],
        goals=["Meter / CGM I use", "Check times I was given", "Clinic / educator contact"],
    )
    _toc(b, [("90 daily logs", ""), ("Weekly", ""), ("Clinic brief", "")])
    for d in range(1, 91):
        b.begin()
        y = b.header_bar("GLUCOSE & MEAL TIMING", f"Day {d}")
        b.date_line(b.x0, y, b.cw)
        y -= 16
        rh = 18
        heads = ["Time", "Reading (copy)", "Meal / context", "Note"]
        ws = [0.16, 0.22, 0.36, 0.26]
        b.c.setFillColor(PALE)
        b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
        x = b.x0
        for lab, w in zip(heads, ws):
            b.rect(x, y - rh, w * b.cw, rh, stroke=HAIR, sw=0.35)
            b.text(lab, x + 3, y - 12, "Sans-Semi", 6.6, MID)
            x += w * b.cw
        y -= rh
        for i in range(10):
            x = b.x0
            for w in ws:
                b.rect(x, y - rh, w * b.cw, rh, stroke=HAIR, sw=0.3)
                x += w * b.cw
            y -= rh
        y -= 8
        b.field("Meds as prescribed (tick / time)", b.x0, y, b.cw)
        y -= 16
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Illness / exercise / extra food", lines=True)
        b.footer()
        b.end()
        if d % 7 == 0:
            b.begin()
            y = b.header_bar("GLUCOSE & MEAL TIMING", f"Week {d // 7}")
            for p in ["Pattern I notice (not a diagnosis)", "Lows / highs I will mention", "Meals that sat with steadier numbers", "Questions"]:
                b.text(p, b.x0, y, "Sans-Semi", 8, MID)
                y = b.writing_lines(y - 14, 3, gap=16) - 10
            b.footer()
            b.end()
    _clinic(b)
    return b.save()


# ===================================================================== 32 pain
def build_32(path=None):
    path = path or OUTPUT / "32_Chronic_Pain_Body_Map_and_Flare_Diary_6x9.pdf"
    b = Book(path, SIX_NINE, running="PAIN & FLARE DIARY")
    standard_front(
        b, "WELLNESS COMPANION SERIES", "Chronic Pain Body-Map Diary",
        "Forty flare pages with front/back mark-up, plus twelve monthly dashboards",
        "Undated  ·  6 × 9 in",
        extra_disclaimer=WELL + " New 'worst pain of my life', chest pain, weakness, or loss of bowel/bladder control needs urgent care.",
        how_to=[("Mark two spots, not a novel", [
            "Circle regions on the simple front/back map. Score 0–10. Note what you already use (heat, meds as prescribed, rest).",
            "Monthly dashboard: count flares, sleep, function (what you could still do).",
        ])],
        legend=[("0–10", "0 none · 10 worst imaginable"), ("Function", "What I could still do, not what I failed")],
        goals=["Usual regions", "Meds / devices I already have", "Function that matters (walk, work, sleep)"],
    )
    _toc(b, [("12 monthly dashboards", ""), ("40 flare pages", ""), ("Clinic brief", "")])

    def body(b, x, y):
        # simple front/back rectangles with head circles
        b.set_stroke(INK2, 0.8)
        b.c.circle(x + 24, y + 88, 10, stroke=1, fill=0)
        b.c.rect(x + 10, y + 20, 28, 56, stroke=1, fill=0)
        b.c.rect(x + 4, y + 50, 10, 28, stroke=1, fill=0)
        b.c.rect(x + 34, y + 50, 10, 28, stroke=1, fill=0)
        b.c.rect(x + 12, y, 10, 22, stroke=1, fill=0)
        b.c.rect(x + 26, y, 10, 22, stroke=1, fill=0)
        b.text("Front", x + 24, y - 12, "Sans", 6.5, MUTED, "center")
        x2 = x + 70
        b.c.circle(x2 + 24, y + 88, 10, stroke=1, fill=0)
        b.c.rect(x2 + 10, y + 20, 28, 56, stroke=1, fill=0)
        b.c.rect(x2 + 12, y, 10, 22, stroke=1, fill=0)
        b.c.rect(x2 + 26, y, 10, 22, stroke=1, fill=0)
        b.text("Back", x2 + 24, y - 12, "Sans", 6.5, MUTED, "center")

    ep = 1
    for m in range(1, 13):
        b.begin()
        y = b.header_bar("PAIN & FLARE DIARY", f"Month {m} dashboard")
        b.field("Month / year", b.x0, y, 160)
        y -= 18
        b.text("Flare tally", b.x0, y, "Sans-Semi", 8, MID)
        y -= 14
        for i in range(14):
            b.rect(b.x0 + i * 20, y - 14, 16, 16, stroke=INK2, sw=0.6)
        y -= 32
        for p in ["Function I kept", "Sleep pattern", "What I already used that helped", "Questions"]:
            b.text(p, b.x0, y, "Sans-Semi", 8, MID)
            y = b.writing_lines(y - 14, 2, gap=16) - 10
        b.footer()
        b.end()
        for _ in range(6):
            b.begin()
            y = b.header_bar("PAIN & FLARE DIARY", f"Flare {ep}")
            b.date_line(b.x0, y, b.cw)
            y -= 18
            b.text("Pain 0–10", b.x0, y, "Sans-Semi", 7.4, MID)
            _mini(b, b.x0 + 70, y + 3, n=11, gap=11.2, r=3.6)
            y -= 22
            body(b, b.x0, y - 100)
            b.text("Mark 1–3 regions.", b.x0, y - 118, "Sans", 6.5, MUTED)
            bx = b.x0 + 175
            b.text("Associated", bx, y, "Sans-Semi", 7.4, MID)
            for i, lab in enumerate(["Ache", "Sharp", "Burn", "Nerve-ish", "Swell", "Fatigue", "Fog", "Mood", "Sleep loss", "Other"]):
                b.checkbox(bx + (i % 2) * 80, y - 16 - (i // 2) * 14, lab, fs=7)
            y -= 130
            b.field("What I used (as already directed)", b.x0, y, b.cw)
            y -= 16
            b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Function I still did / did not", lines=True)
            b.footer()
            b.end()
            ep += 1
    _clinic(b)
    return b.save()


# ===================================================================== 33 grief
def build_33(path=None):
    path = path or OUTPUT / "33_Grief_and_Loss_90_Day_Journal_6x9.pdf"
    b = Book(path, SIX_NINE, running="GRIEF & LOSS")
    standard_front(
        b, "WELLNESS COMPANION SERIES", "Grief & Loss 90-Day Journal",
        "Ninety unique prompts. No timeline, no 'stages', no silver lining required.",
        "Gender-neutral  ·  6 × 9 in",
        extra_disclaimer=WELL + " If you are thinking of joining the dead, call emergency services or a crisis line. This book cannot keep you safe alone.",
        how_to=[("No arc required", [
            "One prompt a day. Skip any that are too sharp. Write 'not today'.",
            "This is not a religious text and not a five-stages worksheet.",
            "Weekly page is optional. Grief does not owe the calendar.",
        ])],
        legend=[("Not today", "A complete page"), ("Name", "You may write it as often as you need")],
        goals=["Who or what this volume is for (only if I want it on paper)", "Who can hear the true version", "A 2 a.m. plan"],
    )
    _toc(b, [("90 prompts", "none repeated"), ("Weekly optional", ""), ("Notes", "")])
    for d in range(1, 91):
        b.begin()
        y = b.header_bar("GRIEF & LOSS", f"Day {d} of 90")
        b.date_line(b.x0, y, b.cw)
        y -= 18
        prompt = GRIEF_90[(d - 1) % 90]
        b.rect(b.x0, y - 88, b.cw, 88, stroke=RULE, sw=0.6, r=3)
        b.paragraph(prompt, b.x0 + 8, y - 22, b.cw - 16, "Cormorant-Italic", 12, 15, INK)
        y -= 100
        b.scale_row("Intensity", b.x0, y, b.cw * 0.48, left="low", right="wave")
        b.scale_row("Support I used", b.x0 + b.cw * 0.52, y, b.cw * 0.48, left="none", right="enough")
        y -= 50
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Write  (or: not today)", lines=True)
        b.footer()
        b.end()
        if d % 7 == 0:
            b.begin()
            y = b.header_bar("GRIEF & LOSS", f"Week {d // 7}  (optional)")
            for p in ["What was true", "What I needed and did not get", "A concrete help I will ask for", "A small living thing I did"]:
                b.text(p, b.x0, y, "Sans-Semi", 8, MID)
                y = b.writing_lines(y - 14, 3, gap=16) - 10
            b.footer()
            b.end()
    for _ in range(8):
        b.notes_page()
    return b.save()


# ===================================================================== 34 habit OS
def build_34(path=None):
    path = path or OUTPUT / "34_Twelve_Week_Habit_Operating_System_6x9.pdf"
    b = Book(path, SIX_NINE, running="HABIT OS")
    standard_front(
        b, "WELLNESS COMPANION SERIES", "12-Week Habit Operating System",
        "Identity, environment, minimum versions, weekly contracts — not a 75-hard clone",
        "Undated  ·  6 × 9 in",
        extra_disclaimer=WELL,
        how_to=[("One operating system, not twelve personalities", [
            "Pick at most three habits. Write a minimum version for bad days.",
            "Weekly contract: what you will do, what you will not track, the repair if you miss two days.",
            "Daily page is a tick + one line. If you want a moral essay, you are doing it wrong.",
        ])],
        legend=[("Min", "The version you can do when life is loud"), ("Repair", "After two misses, not a rebirth")],
        goals=["Three habits, not ten", "Bad-day minimums", "A witness who is not a jury"],
    )
    _toc(b, [("Operating rules", "once"), ("12 weeks", "contract + 7 days + review"), ("Quarter debrief", "")])
    b.begin()
    y = b.header_bar("HABIT OS", "Operating rules")
    for i, p in enumerate(HABIT_OS):
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 2, gap=15) - 8
        if y < b.y0 + 50:
            break
    b.footer()
    b.end()
    for w in range(1, 13):
        b.begin()
        y = b.header_bar("HABIT OS", f"Week {w}  ·  contract")
        b.field("Week of", b.x0, y, 160)
        y -= 18
        for i in range(1, 4):
            b.field(f"Habit {i}", b.x0, y, b.cw * 0.62)
            b.field("Min version", b.x0 + b.cw * 0.64, y, b.cw * 0.36)
            y -= 16
        b.field("I will not track this week", b.x0, y, b.cw)
        y -= 16
        b.field("Repair if I miss two days", b.x0, y, b.cw)
        y -= 18
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Environment change (friction up / down)", lines=True)
        b.footer()
        b.end()
        for d in range(1, 8):
            b.begin()
            y = b.header_bar("HABIT OS", f"Week {w}  ·  day {d}")
            b.date_line(b.x0, y, b.cw)
            y -= 20
            for i in range(1, 4):
                b.checkbox(b.x0, y, f"Habit {i}  (min counts)", fs=8)
                b.dotted_field(b.x0 + 160, y, 170)
                y -= 18
            b.scale_row("Follow-through", b.x0, y, b.cw)
            y -= 48
            b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "One line  (what made it easy or expensive)", lines=True)
            b.footer()
            b.end()
        b.begin()
        y = b.header_bar("HABIT OS", f"Week {w}  ·  review")
        for p in ["What the ticks actually say", "Which minimum saved me", "Environment tweak", "Keep / drop / shrink"]:
            b.text(p, b.x0, y, "Sans-Semi", 8, MID)
            y = b.writing_lines(y - 14, 3, gap=16) - 10
        b.footer()
        b.end()
    b.begin()
    y = b.header_bar("HABIT OS", "12-week debrief")
    for p in ["What is identity now", "What was theater", "What I will run again", "What I forgive"]:
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 4, gap=16) - 10
    b.footer()
    b.end()
    return b.save()


# ===================================================================== 35 burnout
def build_35(path=None):
    path = path or OUTPUT / "35_Burnout_and_Energy_Budget_Journal_6x9.pdf"
    b = Book(path, SIX_NINE, running="BURNOUT ENERGY BUDGET")
    standard_front(
        b, "WELLNESS COMPANION SERIES", "Burnout & Energy Budget",
        "Twelve weeks for knowledge-work humans: meetings, recovery, resentment, sleep",
        "Not a productivity system  ·  6 × 9 in",
        extra_disclaimer=WELL + " Collapse, chest pain, or inability to get out of bed needs a clinician, not a better budget.",
        how_to=[("Budget, not a grind", [
            "Daily: energy in the morning, meetings that took more than they gave, one recovery, resentment tick.",
            "Weekly: what to decline, what to delegate, what is not yours.",
            "This is not a hustle journal. If a page makes you add more, you are misusing it.",
        ])],
        legend=[("Resentment", "A useful signal, not a personality"), ("Recovery", "Something that actually returns energy")],
        goals=["Work shape I have (not the one I pretend)", "Recovery that works in 20 minutes", "A no I need to say"],
    )
    _toc(b, [("84 days", ""), ("Weekly budget", ""), ("Clinic / manager notes", "")])
    day = 1
    for w in range(1, 13):
        for _ in range(7):
            b.begin()
            y = b.header_bar("BURNOUT ENERGY BUDGET", f"Week {w}  ·  day {day}")
            b.date_line(b.x0, y, b.cw)
            y -= 20
            b.scale_row("Energy at start", b.x0, y, b.cw * 0.48)
            b.scale_row("Energy at close", b.x0 + b.cw * 0.52, y, b.cw * 0.48)
            y -= 48
            b.field("Meetings / deep work that cost extra", b.x0, y, b.cw)
            y -= 16
            b.field("Recovery I actually took", b.x0, y, b.cw)
            y -= 16
            b.checkbox(b.x0, y, "Resentment showed up", fs=8)
            b.checkbox(b.x0 + 160, y, "I said no", fs=8)
            b.checkbox(b.x0 + 240, y, "I should have", fs=8)
            y -= 20
            b.field("Sleep (h)", b.x0, y, 120)
            b.field("Last screen", b.x0 + 140, y, 180)
            y -= 18
            b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "What was not mine to carry", lines=True)
            b.footer()
            b.end()
            day += 1
        b.begin()
        y = b.header_bar("BURNOUT ENERGY BUDGET", f"Week {w}  ·  budget")
        for p in ["Decline / delegate next week", "Recovery that actually returned energy", "Resentment pattern", "A conversation I owe or don't"]:
            b.text(p, b.x0, y, "Sans-Semi", 8, MID)
            y = b.writing_lines(y - 14, 3, gap=16) - 10
        b.footer()
        b.end()
    _clinic(b, "Clinician or (optional) manager notes — you choose who sees this")
    return b.save()


# ===================================================================== 36 bladder
def build_36(path=None):
    path = path or OUTPUT / "36_Bladder_and_Pelvic_Symptom_Diary_6x9.pdf"
    b = Book(path, SIX_NINE, running="BLADDER & PELVIC DIARY")
    standard_front(
        b, "WELLNESS COMPANION SERIES", "Bladder & Pelvic Symptom Diary",
        "Sixteen three-day diaries in the format clinicians actually ask for",
        "Tracking only  ·  6 × 9 in",
        extra_disclaimer=WELL + " Blood in urine, fever with back pain, sudden inability to void, or new incontinence after trauma needs urgent care. This is not a Kegel program.",
        how_to=[("Three days in a row, then rest the book", [
            "A bladder diary is usually 2–3 consecutive days: drink time/amount, void time/amount if you measure, leaks, urgency, pads.",
            "Do not invent pelvic-floor exercises. If a PT gave you homework, there is a line to tick it.",
            "Bring a completed three-day block to clinic. Sixteen blocks so you can repeat after a change.",
        ])],
        legend=[("Urgency 0–5", "0 none · 5 had to run"), ("Leak", "Tick if it happened")],
        goals=["Why I was asked to keep a diary", "PT / uro / GP contact", "Whether I measure volumes (only if I was asked)"],
    )
    _toc(b, [("16 blocks of 3 days", ""), ("Block reviews", ""), ("Clinic brief", "")])
    for blk in range(1, 17):
        section_opener(b, f"BLOCK {blk}", "Three consecutive days")
        for d in range(1, 4):
            b.begin()
            y = b.header_bar("BLADDER & PELVIC DIARY", f"Block {blk}  ·  day {d}")
            b.date_line(b.x0, y, b.cw)
            y -= 16
            rh = 16
            heads = ["Time", "Drink", "Void", "Urg 0–5", "Leak", "Pad / note"]
            ws = [0.12, 0.16, 0.16, 0.16, 0.12, 0.28]
            b.c.setFillColor(PALE)
            b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
            x = b.x0
            for lab, w in zip(heads, ws):
                b.rect(x, y - rh, w * b.cw, rh, stroke=HAIR, sw=0.3)
                b.text(lab, x + 2, y - 11, "Sans-Semi", 6.2, MID)
                x += w * b.cw
            y -= rh
            for i in range(14):
                x = b.x0
                for w in ws:
                    b.rect(x, y - rh, w * b.cw, rh, stroke=HAIR, sw=0.28)
                    x += w * b.cw
                y -= rh
                if y < b.y0 + 70:
                    break
            b.field("PT homework as assigned (tick only those)", b.x0, y, b.cw)
            y -= 16
            b.box(b.x0, b.y0 + 14, b.cw, max(30, y - (b.y0 + 14)), "Night voids / pain / notes", lines=True, line_gap=14)
            b.footer()
            b.end()
        b.begin()
        y = b.header_bar("BLADDER & PELVIC DIARY", f"Block {blk} review")
        for p in ["Day vs night pattern", "Drinks that seemed to matter", "Leaks / urgency cluster", "Questions for PT or clinic"]:
            b.text(p, b.x0, y, "Sans-Semi", 8, MID)
            y = b.writing_lines(y - 14, 3, gap=16) - 10
        b.footer()
        b.end()
    _clinic(b)
    return b.save()


BUILDERS_D = [build_28, build_29, build_30, build_31, build_32, build_33, build_34, build_35, build_36]
