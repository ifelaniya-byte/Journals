"""Volume 2 — nine premium GLP-1 companion interiors (19–27)."""

from __future__ import annotations

from reportlab.lib.units import inch

from lib.kit import (
    FIVE_EIGHT,
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
from lib.prompts import BODY_IMAGE_90, CLINIC_Q

GLP_EXTRA = (
    "If you use a GLP-1 or similar medication as prescribed, treat this book as a log of your own observations. "
    "It does not set doses, grocery medical diets, or lab ranges. Those belong to you and your care team."
)


def _mini(b, x, y, n=10, gap=12, r=3.8):
    for i in range(n):
        b.set_stroke(INK2, 0.6)
        b.c.circle(x + i * gap, y, r, stroke=1, fill=0)


def _toc(b, rows):
    b.begin()
    y = b.header_bar(b.running or "", "Contents")
    b.paragraph("Undated. Start anywhere. Skip what is not yours.", b.x0, y, b.cw, "Sans", 8.5, 12, INK2)
    y -= 28
    for title, note in rows:
        b.text(title, b.x0, y, "Cormorant-Semi", 12, INK)
        b.text(note, b.x0, y - 12, "Sans", 8, MUTED)
        b.hline(y - 18, color=HAIR)
        y -= 36
        if y < b.y0 + 40:
            b.footer()
            b.end()
            b.begin()
            y = b.header_bar(b.running or "", "Contents  (continued)")
    b.footer()
    b.end()


def _clinic(b, title="One-page clinic brief"):
    b.begin()
    y = b.header_bar(b.running or "", title)
    b.field("Date", b.x0, y, 140)
    b.field("Clinician / clinic", b.x0 + 160, y, 170)
    y -= 22
    for p in CLINIC_Q:
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 3, gap=15) - 10
    b.footer()
    b.end()


# ===================================================================== 19 grocery
def build_19(path=None):
    path = path or OUTPUT / "19_GLP1_Protein_Grocery_and_Prep_Planner_6x9.pdf"
    b = Book(path, SIX_NINE, running="PROTEIN GROCERY & PREP")
    standard_front(
        b, "GLP-1 COMPANION SERIES", "High-Protein Grocery & Prep",
        "Twelve weeks of shopping lists, batch-cook logs, and fridge maps",
        "Undated  ·  6 × 9 in  ·  Companion to the Meal & Satiety Journal",
        extra_disclaimer=GLP_EXTRA,
        how_to=[("How this book earns its keep", [
            "Each week: a shop list (protein / produce / extras), a prep session log, then seven 'what's in the fridge' days.",
            "Copy protein targets your clinician or dietitian already gave you. This is not a meal plan.",
            "If appetite is low, prep smaller. Leftovers are a kindness, not a test.",
        ])],
        legend=[("P", "Protein staple"), ("F", "Fiber / produce"), ("E", "Extra / condiment")],
        goals=["Protein target I was given (g/day)", "Stores I actually use", "Batch-cook window in my week"],
    )
    _toc(b, [
        ("Pantry & freezer inventory", "Once, then update"),
        ("Twelve weekly cycles", "Shop · prep · seven days"),
        ("Clinic brief", "If nutrition comes up"),
    ])
    section_opener(b, "ONCE", "Pantry & freezer")
    b.begin()
    y = b.header_bar("PROTEIN GROCERY & PREP", "What I already have")
    for lab in ["Proteins on hand", "Frozen backup meals", "Fiber staples", "Emergency low-effort foods"]:
        b.text(lab, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 4, gap=16) - 12
    b.footer()
    b.end()
    for w in range(1, 13):
        section_opener(b, f"WEEK {w}", "Shop · prep · days")
        # shop
        b.begin()
        y = b.header_bar("PROTEIN GROCERY & PREP", f"Week {w}  ·  shop")
        b.field("Shop day", b.x0, y, 140)
        b.field("Budget note", b.x0 + 160, y, 160)
        y -= 18
        for col, title in enumerate(["Protein", "Produce / fiber", "Dairy / alt", "Extras"]):
            x = b.x0 + col * (b.cw / 4)
            b.text(title, x, y, "Sans-Semi", 7.2, MID)
            for i in range(12):
                b.checkbox(x, y - 16 - i * 14, "", size=7)
                b.dotted_field(x + 12, y - 16 - i * 14, b.cw / 4 - 20)
        b.footer()
        b.end()
        # prep
        b.begin()
        y = b.header_bar("PROTEIN GROCERY & PREP", f"Week {w}  ·  prep session")
        b.field("When", b.x0, y, 140)
        b.field("Minutes I actually had", b.x0 + 160, y, 160)
        y -= 20
        b.box(b.x0, y - 90, b.cw, 90, "What I cooked / portioned")
        b.writing_lines(y - 28, 4, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
        y -= 102
        b.box(b.x0, y - 80, b.cw, 80, "Fridge map  (what's where, eat-first)")
        b.writing_lines(y - 28, 3, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
        y -= 92
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "If appetite is low this week, the smallest useful prep is…", lines=True)
        b.footer()
        b.end()
        for d in range(1, 8):
            b.begin()
            y = b.header_bar("PROTEIN GROCERY & PREP", f"Week {w}  ·  day {d}")
            b.date_line(b.x0, y, b.cw)
            y -= 20
            b.field("Protein at meal 1", b.x0, y, b.cw)
            y -= 16
            b.field("Protein at meal 2", b.x0, y, b.cw)
            y -= 16
            b.field("Protein at meal 3", b.x0, y, b.cw)
            y -= 16
            b.field("Backup if I couldn't cook", b.x0, y, b.cw)
            y -= 20
            b.text("Used leftovers?", b.x0, y, "Sans-Semi", 8, MID)
            b.checkbox(b.x0 + 110, y, "Yes", fs=8)
            b.checkbox(b.x0 + 160, y, "No", fs=8)
            b.checkbox(b.x0 + 210, y, "Threw out (note)", fs=8)
            y -= 22
            b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Notes / shop for tomorrow", lines=True)
            b.footer()
            b.end()
    _clinic(b)
    for _ in range(6):
        b.notes_page()
    return b.save()


# ===================================================================== 20 restaurant / travel
def build_20(path=None):
    path = path or OUTPUT / "20_GLP1_Restaurant_Travel_and_Social_Log_6x9.pdf"
    b = Book(path, SIX_NINE, running="OUT & ABOUT")
    standard_front(
        b, "GLP-1 COMPANION SERIES", "Restaurant, Travel & Social",
        "Event pages, trip kits, and 'my usual order' cards — undated",
        "Sixty events  ·  twelve trips  ·  6 × 9 in",
        extra_disclaimer=GLP_EXTRA,
        how_to=[("Use it when life is not your kitchen", [
            "Event page: what you ordered, how fullness showed up, what you'd repeat.",
            "Trip kit: refill, time zones, protein backups in a bag.",
            "This is not a restaurant ranking. It is a memory aid so you are not starting from zero every time.",
        ])],
        legend=[("Repeat", "I'd order this again"), ("Skip", "Not worth it on a quiet-appetite day")],
        goals=["Cuisines I actually eat", "Travel month coming up", "My protein backup in a bag"],
    )
    _toc(b, [("My usual orders", "Fill once"), ("40 event pages", ""), ("12 trip kits", ""), ("Clinic brief", "")])
    b.begin()
    y = b.header_bar("OUT & ABOUT", "My usual orders")
    for i in range(8):
        b.rect(b.x0, y - 48, b.cw, 48, stroke=HAIR, sw=0.45, r=2)
        b.field("Place", b.x0 + 8, y - 14, 200)
        b.field("Order", b.x0 + 8, y - 32, 300)
        y -= 54
    b.footer()
    b.end()
    for n in range(1, 61):
        b.begin()
        y = b.header_bar("OUT & ABOUT", f"Event {n}")
        b.date_line(b.x0, y, b.cw)
        y -= 18
        b.field("Place / host", b.x0, y, b.cw)
        y -= 16
        b.field("What I ordered / brought", b.x0, y, b.cw)
        y -= 16
        b.field("Protein I could actually see", b.x0, y, b.cw)
        y -= 18
        b.scale_row("Fullness after", b.x0, y, b.cw * 0.48, left="still hungry", right="too much")
        b.scale_row("Ease", b.x0 + b.cw * 0.52, y, b.cw * 0.48, left="braced", right="fine")
        y -= 50
        b.checkbox(b.x0, y, "Alcohol / not", fs=8)
        b.checkbox(b.x0 + 110, y, "Leftovers boxed", fs=8)
        b.checkbox(b.x0 + 230, y, "Would repeat", fs=8)
        y -= 20
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "What I'd do the same / different", lines=True)
        b.footer()
        b.end()
    for n in range(1, 13):
        b.begin()
        y = b.header_bar("OUT & ABOUT", f"Trip kit {n}")
        b.field("Where", b.x0, y, 160)
        b.field("Dates", b.x0 + 180, y, 150)
        y -= 20
        for p in ["Refill / pens / letter from clinic (as you already have)", "Time zone vs. injection weekday", "Protein backups in bag", "Restaurants I already know", "What I need from travel partners"]:
            b.text(p, b.x0, y, "Sans-Semi", 8, MID)
            y = b.writing_lines(y - 14, 2, gap=15) - 10
        b.footer()
        b.end()
    _clinic(b)
    for _ in range(4):
        b.notes_page()
    return b.save()


# ===================================================================== 21 archive
def build_21(path=None):
    path = path or OUTPUT / "21_GLP1_Measurements_Photos_and_Labs_Archive_6x9.pdf"
    b = Book(path, SIX_NINE, running="ARCHIVE")
    standard_front(
        b, "GLP-1 COMPANION SERIES", "Measurements, Photos & Labs",
        "A quiet archive: inches, clothing, photo log, blank lab sheets",
        "Twelve months  ·  6 × 9 in",
        extra_disclaimer=GLP_EXTRA + " Lab sheets are blank on purpose. Copy numbers from your portal. Do not interpret them here.",
        how_to=[("Numbers without a courtroom", [
            "Monthly: photos (optional), clothing, waist/hip if you use them, a range — not a daily verdict.",
            "Lab pages: copy, date, source. Leave interpretation to the clinician who ordered them.",
            "Skip any metric that makes you worse. The archive should be something you can stand to open.",
        ])],
        legend=[("Range", "A band, not a single gavel"), ("Photo", "Optional. Same light if you can.")],
        goals=["Metrics I consent to track", "Where photos live (phone album name)", "Lab portal login hint (not the password)"],
    )
    _toc(b, [("Baseline", "Once"), ("12 monthly pages", ""), ("52 optional weekly inches", ""), ("Lab copy sheets", ""), ("Clinic brief", "")])
    b.begin()
    y = b.header_bar("ARCHIVE", "Baseline")
    for p in ["Date I am starting this volume", "Clothing size I actually wear", "Waist / hip if I use them", "Photo plan (or none)", "How I want to treat a number that moves"]:
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 3, gap=16) - 10
    b.footer()
    b.end()
    for m in range(1, 13):
        b.begin()
        y = b.header_bar("ARCHIVE", f"Month {m}")
        b.field("Month / year", b.x0, y, 160)
        y -= 18
        b.field("Weight range (low / high) if I weigh", b.x0, y, b.cw)
        y -= 16
        b.field("Waist", b.x0, y, 100)
        b.field("Hip", b.x0 + 120, y, 100)
        b.field("Chest / other", b.x0 + 240, y, 90)
        y -= 18
        b.field("Clothing note", b.x0, y, b.cw)
        y -= 16
        b.field("Photo taken? album name / none", b.x0, y, b.cw)
        y -= 18
        b.box(b.x0, y - 80, b.cw, 80, "Non-scale evidence this month")
        b.writing_lines(y - 28, 3, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
        y -= 92
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "What I will not over-read", lines=True)
        b.footer()
        b.end()
        # lab sheet
        b.begin()
        y = b.header_bar("ARCHIVE", f"Month {m}  ·  lab copy sheet")
        b.field("Draw date", b.x0, y, 120)
        b.field("Lab / portal", b.x0 + 140, y, 190)
        y -= 16
        b.text("Copy values. Do not diagnose from this page.", b.x0, y, "Sans", 7.5, MUTED)
        y -= 12
        rh = 18
        headers = ["Test (as labeled)", "Value", "Units", "Note from clinician"]
        ws = [0.34, 0.16, 0.14, 0.36]
        b.c.setFillColor(PALE)
        b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
        x = b.x0
        for lab, w in zip(headers, ws):
            b.rect(x, y - rh, w * b.cw, rh, stroke=HAIR, sw=0.35)
            b.text(lab, x + 3, y - 12, "Sans-Semi", 6.5, MID)
            x += w * b.cw
        y -= rh
        for i in range(16):
            x = b.x0
            for w in ws:
                b.rect(x, y - rh, w * b.cw, rh, stroke=HAIR, sw=0.3)
                x += w * b.cw
            y -= rh
            if y < b.y0 + 36:
                break
        b.footer()
        b.end()
    for w in range(1, 53):
        b.begin()
        y = b.header_bar("ARCHIVE", f"Optional weekly inches  {w}")
        b.date_line(b.x0, y, b.cw)
        y -= 20
        b.field("Waist", b.x0, y, 100)
        b.field("Hip", b.x0 + 120, y, 100)
        b.field("Other", b.x0 + 240, y, 90)
        y -= 22
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Note (clothes, photos, skip)", lines=True)
        b.footer()
        b.end()
    _clinic(b)
    return b.save()


# ===================================================================== 22 sleep bowel hydration
def build_22(path=None):
    path = path or OUTPUT / "22_GLP1_Sleep_Bowel_and_Hydration_Companion_6x9.pdf"
    b = Book(path, SIX_NINE, running="SLEEP · BOWEL · WATER")
    standard_front(
        b, "GLP-1 COMPANION SERIES", "Sleep, Bowel & Hydration",
        "Ninety days of the unglamorous trio that decides whether a week feels human",
        "Undated  ·  6 × 9 in",
        extra_disclaimer=GLP_EXTRA + " Blood in stool, black stool, no stool for several days with pain/vomiting, or chest pain needs a clinician — not a better water chart.",
        how_to=[("Three columns, one day", [
            "Sleep: hours and quality, not a performance.",
            "Bowel: Bristol 1–7 as a tracking shorthand + ease. Not a diagnosis.",
            "Water: tick glasses. If your clinician set a target, copy it on the goals page.",
        ])],
        legend=[("Bristol 1–7", "1 hard · 4 smooth · 7 watery"), ("Ease", "1 strain · 5 easy")],
        goals=["Water target I was given, if any", "Sleep window I am aiming for", "What my clinician already said about constipation / reflux"],
    )
    _toc(b, [("90 daily pages", ""), ("Weekly recap", "every 7 days"), ("Clinic brief", "")])
    bristol = ["1 hard", "2 lumpy", "3 cracked", "4 smooth", "5 soft", "6 mushy", "7 watery"]
    for d in range(1, 91):
        b.begin()
        y = b.header_bar("SLEEP · BOWEL · WATER", f"Day {d}")
        b.date_line(b.x0, y, b.cw)
        y -= 20
        b.text("Sleep", b.x0, y, "Cormorant-Semi", 13, INK)
        y -= 16
        b.field("Bed", b.x0, y, 90)
        b.field("Rise", b.x0 + 110, y, 90)
        b.field("Hours", b.x0 + 220, y, 90)
        y -= 18
        b.scale_row("Quality", b.x0, y, b.cw, left="broken", right="restored")
        y -= 48
        b.text("Bowel  (tracking only)", b.x0, y, "Cormorant-Semi", 13, INK)
        y -= 16
        for i, lab in enumerate(bristol):
            b.checkbox(b.x0 + (i % 4) * (b.cw / 4), y - (i // 4) * 15, lab, fs=7)
        y -= 40
        b.scale_row("Ease", b.x0, y, b.cw * 0.48)
        b.field("Time(s)", b.x0 + b.cw * 0.52, y, b.cw * 0.48)
        y -= 48
        b.text("Water", b.x0, y, "Cormorant-Semi", 13, INK)
        y -= 8
        b.water_row(b.x0, y, n=8, gap=18)
        y -= 28
        b.field("What helped (fiber, walk, stool plan I already have)", b.x0, y, b.cw)
        y -= 18
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Notes for clinic if this stacks", lines=True)
        b.footer()
        b.end()
        if d % 7 == 0:
            b.begin()
            y = b.header_bar("SLEEP · BOWEL · WATER", f"Week {d // 7}")
            for p in ["Sleep pattern", "Bowel pattern", "Hydration pattern", "What I will mention"]:
                b.text(p, b.x0, y, "Sans-Semi", 8, MID)
                y = b.writing_lines(y - 14, 3, gap=16) - 10
            b.footer()
            b.end()
    _clinic(b)
    return b.save()


# ===================================================================== 23 body image
def build_23(path=None):
    path = path or OUTPUT / "23_GLP1_Body_Image_and_Mindset_90_Day_6x9.pdf"
    b = Book(path, SIX_NINE, running="BODY IMAGE & MINDSET")
    standard_front(
        b, "GLP-1 COMPANION SERIES", "Body Image & Mindset",
        "Ninety unique prompts. A truce practice, not a glow-up homework packet.",
        "Undated  ·  6 × 9 in",
        extra_disclaimer=GLP_EXTRA,
        how_to=[("How to not make this another test", [
            "One prompt a day. If it spikes you, skip it and write 'not today'.",
            "This is not exposure therapy. It is a record of how you spoke to a changing body.",
            "Weekly page: what you will wear / do that is not earned by a number.",
        ])],
        legend=[("Not today", "A complete answer"), ("Truce", "No improvement project after 8 p.m.")],
        goals=["Why I want a record that is not the scale", "A clothing item I will not exile", "Who is a safe witness"],
    )
    _toc(b, [("90 prompt pages", "none repeated"), ("Weekly truce", ""), ("Clinic / therapist brief", "")])
    for d in range(1, 91):
        b.begin()
        y = b.header_bar("BODY IMAGE & MINDSET", f"Day {d} of 90")
        b.date_line(b.x0, y, b.cw)
        y -= 18
        prompt = BODY_IMAGE_90[(d - 1) % 90]
        b.rect(b.x0, y - 78, b.cw, 78, stroke=RULE, sw=0.6, r=3)
        b.text("Prompt", b.x0 + 8, y - 14, "Sans-Semi", 7, MID)
        b.paragraph(prompt, b.x0 + 8, y - 32, b.cw - 16, "Cormorant-Italic", 12, 15, INK)
        y -= 90
        b.scale_row("Body kindness", b.x0, y, b.cw * 0.48, left="harsh", right="fair")
        b.scale_row("Mirror / check urge", b.x0 + b.cw * 0.52, y, b.cw * 0.48)
        y -= 50
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Response  (or write: not today)", lines=True)
        b.footer()
        b.end()
        if d % 7 == 0:
            b.begin()
            y = b.header_bar("BODY IMAGE & MINDSET", f"Week {d // 7}  ·  truce")
            for p in ["Meanest sentence I used — rewritten once", "A thing I did in this body that was living, not managing", "Clothing / event I will not hold hostage", "Help I need (friend, therapist, less weighing)"]:
                b.text(p, b.x0, y, "Sans-Semi", 8, MID)
                y = b.writing_lines(y - 14, 3, gap=16) - 10
            b.footer()
            b.end()
    _clinic(b, "Therapist / clinician brief")
    return b.save()


# ===================================================================== 24 weekly clinic brief
def build_24(path=None):
    path = path or OUTPUT / "24_GLP1_Weekly_Review_and_Clinic_Brief_6x9.pdf"
    b = Book(path, SIX_NINE, running="WEEKLY BRIEF")
    standard_front(
        b, "GLP-1 COMPANION SERIES", "Weekly Review & Clinic Brief",
        "Fifty-two weeks: one review spread + a one-page brief you could hand over",
        "Undated  ·  6 × 9 in",
        extra_disclaimer=GLP_EXTRA,
        how_to=[("Sunday-or-whenever", [
            "Left: the week in signals (sleep, protein, shot, mood, constipation, life).",
            "Right: a clean brief — three observations, questions, refill status. Write as if a tired clinician has ninety seconds.",
        ])],
        legend=[("Flag", "Bring this week to clinic"), ("Quiet week", "Still fill the brief. Quiet is data.")],
        goals=["Usual review weekday", "Portal / phone for refill", "What 'flag' means for me"],
    )
    _toc(b, [("52 weeks", "review + brief"), ("Quarterly letters", "4 pages")])
    for w in range(1, 53):
        b.begin()
        y = b.header_bar("WEEKLY BRIEF", f"Week {w}  ·  review")
        b.field("Week of", b.x0, y, 160)
        b.checkbox(b.x0 + 200, y, "Flag for clinic", fs=8)
        y -= 20
        rows = ["Shot as prescribed", "Protein most days", "Sleep decent", "Bowel okay", "Mood okay", "Life loud"]
        for i, r in enumerate(rows):
            b.checkbox(b.x0 + (i % 2) * (b.cw / 2), y - (i // 2) * 16, r, fs=8)
        y -= 16 * 3 + 8
        b.scale_row("How human the week felt", b.x0, y, b.cw)
        y -= 48
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "What actually happened (not the plan)", lines=True)
        b.footer()
        b.end()
        b.begin()
        y = b.header_bar("WEEKLY BRIEF", f"Week {w}  ·  clinic brief")
        b.field("Name", b.x0, y, 150)
        b.field("Week of", b.x0 + 170, y, 150)
        y -= 18
        b.text("Three observations", b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 4, gap=16) - 8
        b.text("Questions", b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 3, gap=16) - 8
        b.field("Refill / next visit", b.x0, y, b.cw)
        y -= 18
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Please see / please ignore", lines=True)
        b.footer()
        b.end()
    for q in range(1, 5):
        _clinic(b, f"Quarter {q} letter")
    return b.save()


# ===================================================================== 25 shot-day pocket
def build_25(path=None):
    path = path or OUTPUT / "25_GLP1_Shot_Day_0_48h_Pocket_Log_5x8.pdf"
    b = Book(path, FIVE_EIGHT, gutter=0.62 * inch, outer=0.42 * inch, top=0.40 * inch, bottom=0.44 * inch, running="SHOT-DAY 0–48h")
    standard_front(
        b, "GLP-1 COMPANION SERIES", "Shot-Day 0–48h Log",
        "Pocket pages for the day of and the day after — how it actually went",
        "5 × 8 in  ·  Thirty-six cycles",
        extra_disclaimer=GLP_EXTRA + " Severe symptoms after injection need clinical advice, not a better notebook.",
        how_to=[("One cycle = two pages", [
            "Page A: shot day as prescribed (time, site, hours 0–12).",
            "Page B: the next 24–48 hours. Appetite, nausea, sleep, what you ate that sat.",
            "Copy the dose. Do not invent a new one because a page looks empty.",
        ])],
        legend=[("0–12h", "Shot day"), ("+24 / +48", "The echo")],
        goals=["Usual weekday", "Site rotation I was taught", "What 'bad enough to call' means for me"],
        belongs_fields=["Name", "Prescriber", "Pharmacy", "If found, return to"],
    )
    for n in range(1, 37):
        b.begin()
        y = b.header_bar("SHOT-DAY 0–48h", f"Cycle {n}  ·  shot day")
        b.field("Date", b.x0, y, 110)
        b.field("Time", b.x0 + 130, y, 90)
        y -= 16
        b.field("Dose as Rx", b.x0, y, 110)
        b.field("Site", b.x0 + 130, y, 90)
        y -= 18
        b.text("0–12 hours  (tick what showed up)", b.x0, y, "Sans-Semi", 7.2, MID)
        y -= 14
        for i, lab in enumerate(["Fine", "Tired", "Nausea", "Headache", "Injection-site", "Low appetite", "Sulphur", "Other"]):
            b.checkbox(b.x0 + (i % 2) * (b.cw / 2), y - (i // 2) * 14, lab, fs=7.2)
        y -= 14 * 4 + 8
        b.box(b.x0, b.y0 + 14, b.cw, y - (b.y0 + 14), "What I ate that sat  /  notes", lines=True, line_gap=14)
        b.footer()
        b.end()
        b.begin()
        y = b.header_bar("SHOT-DAY 0–48h", f"Cycle {n}  ·  +24 to +48h")
        b.scale_row("Appetite", b.x0, y, b.cw)
        y -= 44
        b.scale_row("Nausea", b.x0, y, b.cw)
        y -= 44
        b.field("Sleep that night (h)", b.x0, y, b.cw)
        y -= 16
        b.field("Bowel", b.x0, y, b.cw)
        y -= 16
        b.checkbox(b.x0, y, "Call clinic? no", fs=7.5)
        b.checkbox(b.x0 + 110, y, "Maybe / did", fs=7.5)
        y -= 18
        b.box(b.x0, b.y0 + 14, b.cw, y - (b.y0 + 14), "Echo notes", lines=True, line_gap=14)
        b.footer()
        b.end()
    _clinic(b)
    return b.save()


# ===================================================================== 26 kitchen
def build_26(path=None):
    path = path or OUTPUT / "26_GLP1_Protein_Kitchen_Recipe_and_Leftover_Log_6x9.pdf"
    b = Book(path, SIX_NINE, running="PROTEIN KITCHEN")
    standard_front(
        b, "GLP-1 COMPANION SERIES", "Protein Kitchen Journal",
        "Sixty recipe cards you write yourself, plus leftover and 'sat well' notes",
        "Not a cookbook  ·  6 × 9 in",
        extra_disclaimer=GLP_EXTRA,
        how_to=[("Your recipes, not ours", [
            "Each card: name, protein source, how it sat, would-make-again.",
            "Leftover log so food you prepped actually gets eaten.",
            "No branded meal plans. If a dietitian gave you a list, copy it onto the goals page.",
        ])],
        legend=[("Sat 1–5", "1 did not sit · 5 easy"), ("Again", "Keep in rotation")],
        goals=["Protein ideas I already like", "Appliances I will actually use", "Foods that do not sit"],
    )
    _toc(b, [("60 recipe cards", ""), ("Leftover log", "30 pages"), ("Clinic brief", "")])
    for n in range(1, 61):
        b.begin()
        y = b.header_bar("PROTEIN KITCHEN", f"Recipe card {n}")
        b.field("Name", b.x0, y, b.cw)
        y -= 16
        b.field("Protein source", b.x0, y, b.cw * 0.55)
        b.field("Minutes", b.x0 + b.cw * 0.58, y, b.cw * 0.42)
        y -= 16
        b.text("Ingredients / method  (your notes)", b.x0, y, "Sans-Semi", 7.5, MID)
        y = b.writing_lines(y - 14, 10, gap=16) - 8
        b.scale_row("How it sat", b.x0, y, b.cw * 0.48)
        b.checkbox(b.x0 + b.cw * 0.55, y, "Make again", fs=8)
        b.checkbox(b.x0 + b.cw * 0.78, y, "Retire", fs=8)
        y -= 44
        b.box(b.x0, b.y0 + 16, b.cw, max(36, y - (b.y0 + 16)), "Tweaks", lines=True)
        b.footer()
        b.end()
    for n in range(1, 31):
        b.begin()
        y = b.header_bar("PROTEIN KITCHEN", f"Leftover log {n}")
        b.date_line(b.x0, y, b.cw)
        y -= 18
        rh = 18
        heads = ["Item", "Cooked", "Eat by", "Eaten?"]
        ws = [0.40, 0.20, 0.20, 0.20]
        b.c.setFillColor(PALE)
        b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
        x = b.x0
        for lab, w in zip(heads, ws):
            b.rect(x, y - rh, w * b.cw, rh, stroke=HAIR, sw=0.35)
            b.text(lab, x + 4, y - 12, "Sans-Semi", 7, MID)
            x += w * b.cw
        y -= rh
        for i in range(14):
            x = b.x0
            for w in ws:
                b.rect(x, y - rh, w * b.cw, rh, stroke=HAIR, sw=0.3)
                x += w * b.cw
            y -= rh
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "What got wasted / what saved the week", lines=True)
        b.footer()
        b.end()
    _clinic(b)
    return b.save()


# ===================================================================== 27 five minute
def build_27(path=None):
    path = path or OUTPUT / "27_GLP1_Five_Minute_Morning_Pages_6x9.pdf"
    b = Book(path, SIX_NINE, running="FIVE-MINUTE PAGES")
    standard_front(
        b, "GLP-1 COMPANION SERIES", "Five-Minute Morning Pages",
        "One hundred twenty compact days: shot, protein intention, one sentence, one body note",
        "For people who will not fill a two-page spread every morning  ·  6 × 9 in",
        extra_disclaimer=GLP_EXTRA,
        how_to=[("Five minutes, then leave", [
            "If you only keep one GLP-1 journal, let it be a thin honest one.",
            "Shot / not-shot, protein intention, body one-liner, one gratitude. Stop.",
        ])],
        legend=[("S", "Shot day"), ("—", "Not shot day")],
        goals=["Where this book will live", "The sentence I want most mornings"],
    )
    for d in range(1, 121):
        b.begin()
        y = b.header_bar("FIVE-MINUTE PAGES", f"Day {d}")
        b.date_line(b.x0, y, b.cw)
        y -= 18
        b.checkbox(b.x0, y, "Shot day (as prescribed)", fs=8)
        b.checkbox(b.x0 + 170, y, "Not today", fs=8)
        y -= 18
        b.field("Protein intention", b.x0, y, b.cw)
        y -= 16
        b.field("Water", b.x0, y, 140)
        b.field("Sleep (h)", b.x0 + 160, y, 160)
        y -= 18
        b.scale_row("Body / mood", b.x0, y, b.cw)
        y -= 48
        b.box(b.x0, y - 70, b.cw, 70, "One sentence")
        b.writing_lines(y - 28, 2, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
        y -= 80
        b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "One gratitude / one ask", lines=True)
        b.footer()
        b.end()
        if d % 30 == 0:
            b.begin()
            y = b.header_bar("FIVE-MINUTE PAGES", f"Days {d-29}–{d}  harvest")
            b.writing_lines(y, 24, gap=18)
            b.footer()
            b.end()
    return b.save()


BUILDERS_C = [build_19, build_20, build_21, build_22, build_23, build_24, build_25, build_26, build_27]
