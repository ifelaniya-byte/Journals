"""Section A — nine GLP-1 / incretin tracking interiors."""

from __future__ import annotations

from reportlab.lib.units import inch

from lib.kit import (
    FIVE_EIGHT,
    GHOST,
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
    Book,
    G,
    section_opener,
    standard_front,
)

GLP_EXTRA = (
    "If you use a GLP-1 or similar medication (including semaglutide or tirzepatide programs), "
    "treat this book as a log of your own observations. Dosing, titration, missed doses, and "
    "side-effect decisions belong only to you and your prescriber."
)

SITES = ["Abdomen", "Thigh", "Arm", "Other"]


def _site_row(b: Book, x, y, gap=72):
    for i, s in enumerate(SITES):
        b.checkbox(x + i * gap, y, s, size=8, fs=7.4)


def _mini_scale(b: Book, x, y, n=10, gap=11.2, r=3.8):
    for i in range(n):
        b.set_stroke(INK2, 0.6)
        b.c.circle(x + i * gap, y, r, stroke=1, fill=0)


# ===================================================================== 01
def _01_left(b: Book, day: int):
    b.begin()
    y = b.header_bar("GLP-1 MEAL & SATIETY", f"Day {day}")
    b.date_line(b.x0, y, b.cw)
    y -= 26

    top = y
    h = 64
    b.rect(b.x0, y - h, b.cw, h, stroke=RULE, sw=0.6, r=3)
    b.text("Injection timing  (as directed by my prescriber)", b.x0 + 8, y - 12, "Sans-Semi", 7.2, MID)
    b.field("Time", b.x0 + 8, y - 28, 150)
    b.field("Pen / lot (opt.)", b.x0 + 170, y - 28, 150)
    b.text("Site", b.x0 + 8, y - 46, "Sans", 7.5, MID)
    _site_row(b, b.x0 + 36, y - 48, gap=70)
    y -= h + 10

    b.text("Hunger on waking", b.x0, y, "Sans-Semi", 7.4, MID)
    b.text("1 = none    10 = strongest", b.x1, y, "Sans", 6.5, MUTED, "right")
    _mini_scale(b, b.x0 + 8, y - 16, n=10, gap=14, r=4.2)
    for i in range(10):
        b.text(str(i + 1), b.x0 + 8 + i * 14, y - 30, "Sans", 5.8, MUTED, "center")
    y -= 42

    meals = [
        ("Meal 1", "Usually breakfast"),
        ("Meal 2", "Usually lunch"),
        ("Meal 3", "Usually dinner"),
        ("Snacks / sips", "If any"),
    ]
    block_h = 78
    for name, hint in meals:
        b.rect(b.x0, y - block_h, b.cw, block_h, stroke=RULE, sw=0.55, r=3)
        b.c.setFillColor(WASH)
        b.c.rect(b.x0, y - 16, b.cw, 16, stroke=0, fill=1)
        b.set_stroke(RULE, 0.55)
        b.c.roundRect(b.x0, y - block_h, b.cw, block_h, 3, stroke=1, fill=0)
        b.text(name, b.x0 + 8, y - 12, "Sans-Semi", 7.6, INK)
        b.text(hint, b.x0 + 70, y - 12, "Sans-Italic", 7, MUTED)
        b.field("Time", b.x0 + 8, y - 30, 110)
        b.text("Hunger before", b.x0 + 150, y - 30, "Sans", 6.8, MID)
        _mini_scale(b, b.x0 + 218, y - 27, n=10, gap=10.2, r=3.4)
        b.writing_lines(y - 46, 2, gap=14, x0=b.x0 + 8, x1=b.x1 - 8)
        b.text("Protein g", b.x0 + 8, y - block_h + 10, "Sans", 7, MID)
        b.dotted_field(b.x0 + 58, y - block_h + 10, 40)
        b.text("Fiber g", b.x0 + 110, y - block_h + 10, "Sans", 7, MID)
        b.dotted_field(b.x0 + 150, y - block_h + 10, 40)
        b.text("Fullness after", b.x0 + 204, y - block_h + 10, "Sans", 7, MID)
        _mini_scale(b, b.x0 + 272, y - block_h + 13, n=5, gap=10, r=3.2)
        y -= block_h + 6

    b.text("Water", b.x0, y - 2, "Sans-Semi", 7.4, MID)
    b.water_row(b.x0 + 48, y, n=8, gap=17)
    b.footer()
    b.end()


def _01_right(b: Book, day: int):
    b.begin()
    y = b.header_bar("GLP-1 MEAL & SATIETY", f"Day {day}  ·  evening")
    b.text("Daily totals", b.x0, y, "Cormorant-Semi", 13, INK)
    y -= 8
    # totals table
    rows = [
        ("Protein (g)", "Target", "Actual"),
        ("Fiber (g)", "Target", "Actual"),
        ("Fluids", "Target", "Actual"),
        ("Steps / movement", "Target", "Actual"),
    ]
    rh, col1 = 22, b.cw * 0.42
    table_h = rh * (len(rows) + 1)
    b.rect(b.x0, y - table_h, b.cw, table_h, stroke=RULE, sw=0.5)
    b.c.setFillColor(PALE)
    b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
    b.text("Metric", b.x0 + 8, y - 14, "Sans-Semi", 7.4, MID)
    b.text("Target", b.x0 + col1, y - 14, "Sans-Semi", 7.4, MID)
    b.text("Actual", b.x0 + col1 + (b.cw - col1) / 2, y - 14, "Sans-Semi", 7.4, MID)
    yy = y - rh
    for i, (m, _t, _a) in enumerate(rows):
        yy -= rh
        if i % 2 == 0:
            b.c.setFillColor(WASH)
            b.c.rect(b.x0, yy, b.cw, rh, stroke=0, fill=1)
        b.hline(yy + rh, color=HAIR, width=0.3)
        b.text(m, b.x0 + 8, yy + 7, "Sans", 8, INK2)
        b.dotted_field(b.x0 + col1, yy + 7, 70)
        b.dotted_field(b.x0 + col1 + (b.cw - col1) / 2, yy + 7, 70)
    b.rect(b.x0, y - table_h, b.cw, table_h, stroke=RULE, sw=0.5)
    y -= table_h + 22

    b.scale_row("Energy", b.x0, y, b.cw * 0.48, n=10)
    b.scale_row("Mood", b.x0 + b.cw * 0.52, y, b.cw * 0.48, n=10)
    y -= 52

    h = 78
    b.box(b.x0, y - h, b.cw, h, "Non-scale victories today")
    b.text("Energy · clothing fit · labs · social · sleep · other", b.x0 + 8, y - 28, "Sans", 7, MUTED)
    b.writing_lines(y - 44, 2, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 10

    h = 86
    b.box(b.x0, y - h, b.cw, h, "Satiety notes  (early fullness, metallic taste, no interest, true hunger)")
    b.writing_lines(y - 28, 3, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 10

    h = 78
    b.box(b.x0, y - h, b.cw, h, "Evening reflection")
    b.writing_lines(y - 28, 3, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 12

    b.field("Tomorrow's protein target (g)", b.x0, y, b.cw * 0.55)
    b.field("Prep note", b.x0 + b.cw * 0.58, y, b.cw * 0.42)
    b.footer()
    b.end()


def _01_week(b: Book, week: int):
    b.begin()
    y = b.header_bar("GLP-1 MEAL & SATIETY", f"Week {week} recap")
    b.field("Week of", b.x0, y, 180)
    y -= 22
    b.text("At-a-glance  (circle a word)", b.x0, y, "Sans-Semi", 8, MID)
    y -= 16
    for lab, opts in [
        ("Appetite", "quiet  ·  uneven  ·  strong  ·  unpredictable"),
        ("Protein", "hit most days  ·  hit some days  ·  struggled"),
        ("Energy", "steady  ·  afternoon dip  ·  flat  ·  improved"),
        ("Adherence", "on schedule  ·  delayed  ·  skipped (note why)"),
    ]:
        b.text(lab, b.x0, y, "Sans-Semi", 8, INK)
        b.text(opts, b.x0 + 70, y, "Sans", 8, INK2)
        y -= 16
    y -= 6
    # 7-day mini
    days = list("MTWTFSS")
    rh, cw = 20, b.cw / 8
    b.text("Protein hit?", b.x0, y, "Sans-Semi", 7.2, MID)
    y -= 6
    for i, d in enumerate([" "] + days):
        b.rect(b.x0 + i * cw, y - rh, cw, rh, stroke=HAIR, sw=0.4, fill=PALE if i == 0 else None)
        b.text(d, b.x0 + i * cw + cw / 2, y - 13, "Sans-Semi", 7.5, MID, "center")
    y -= rh
    for row in ["Protein", "Fiber", "Walked", "Water 8"]:
        b.rect(b.x0, y - rh, cw, rh, stroke=HAIR, sw=0.4)
        b.text(row, b.x0 + 4, y - 13, "Sans", 6.8, INK2)
        for i in range(7):
            b.rect(b.x0 + (i + 1) * cw, y - rh, cw, rh, stroke=HAIR, sw=0.4)
        y -= rh
    y -= 16
    b.box(b.x0, y - 90, b.cw, 90, "What I learned about satiety this week")
    b.writing_lines(y - 28, 4, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= 102
    b.box(b.x0, b.y0 + 18, b.cw, y - (b.y0 + 18), "One change I will try next week")
    b.footer()
    b.end()


def build_01(path=None):
    path = path or OUTPUT / "01_GLP1_Meal_and_Satiety_Journal_6x9.pdf"
    b = Book(path, SIX_NINE, running="GLP-1 MEAL & SATIETY")
    standard_front(
        b,
        "GLP-1 TRACKING SERIES",
        "Meal & Satiety Journal",
        "Daily two-page spreads for protein, fiber, hunger, and non-scale victories",
        "Eight undated weeks  ·  6 × 9 in  ·  Grayscale interior",
        extra_disclaimer=GLP_EXTRA,
        how_to=[
            (
                "What this book is for",
                [
                    "Use one two-page spread per day. Left page captures meals, hunger, and injection timing. Right page captures totals, satiety notes, and a non-scale victory.",
                    "Fill in numbers your clinician already gave you (protein targets, injection day). This book does not set those numbers.",
                    "Hunger scales are 1 (none) to 10 (strongest). Fullness after eating uses a shorter 1-5 row so it stays honest and quick.",
                ],
            ),
            (
                "How to stay consistent",
                [
                    "Write during or just after the meal — memory is a poor satiety instrument.",
                    "If a day is messy, still tick water and protein. A half-filled page is more useful than a skipped one.",
                    "At the end of each week, complete the recap before starting the next seven days.",
                ],
            ),
        ],
        legend=[
            ("Hunger 1-10", "1 none · 5 moderate · 10 strongest urge to eat"),
            ("Fullness 1-5", "1 still hungry · 3 satisfied · 5 uncomfortably full"),
            ("Site boxes", "Mark the injection site you actually used, then rotate as directed"),
            ("NSV", "Non-scale victory: energy, clothing, labs, mood, social ease"),
        ],
        goals=[
            "Protein target my clinician or dietitian suggested (g / day)",
            "Fiber target I am aiming for (g / day)",
            "Injection day(s) and time window I was given",
            "What 'satisfied' feels like in my body, in my own words",
            "Non-scale victories I care about more than a single weigh-in",
        ],
    )
    section_opener(b, "BEGIN", "Daily pages", "Left: meals and timing.  Right: totals and reflection.")
    for day in range(1, 57):
        _01_left(b, day)
        _01_right(b, day)
        if day % 7 == 0:
            _01_week(b, day // 7)
    for _ in range(4):
        b.notes_page("Extra notes")
    return b.save()


# ===================================================================== 02
SYMPTOMS = [
    "Nausea",
    "Vomiting",
    "Reflux / heartburn",
    "Constipation",
    "Diarrhea",
    "Fatigue",
    "Headache",
    "Dizziness",
    "Injection-site",
    "Appetite change",
    "Muscle aches",
    "Hair changes",
    "Mood dip",
    "Sleep change",
    "Sulphur burps",
    "Other",
]


def _02_left(b: Book, week: int):
    b.begin()
    y = b.header_bar("GLP-1 SIDE-EFFECT DIARY", f"Week {week}")
    b.field("Week of", b.x0, y, 160)
    b.field("Dose recorded (as prescribed)", b.x0 + 190, y, 140)
    y -= 18
    b.text("Severity  0 none  ·  1 mild  ·  2 moderate  ·  3 strong  ·  4 severe  ·  5 worst", b.x0, y, "Sans", 6.6, MUTED)
    y -= 10
    days = ["S", "M", "T", "W", "T", "F", "S"]
    lab_w = 92
    cell = (b.cw - lab_w) / 7
    rh = 18.2
    # header
    b.c.setFillColor(PALE)
    b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
    b.rect(b.x0, y - rh, b.cw, rh, stroke=HAIR, sw=0.4)
    b.text("Observation", b.x0 + 4, y - 12, "Sans-Semi", 6.8, MID)
    for i, d in enumerate(days):
        b.text(d, b.x0 + lab_w + i * cell + cell / 2, y - 12, "Sans-Semi", 7.5, INK, "center")
    y -= rh
    for i, s in enumerate(SYMPTOMS):
        fill = WASH if i % 2 == 0 else None
        if fill:
            b.c.setFillColor(fill)
            b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
        b.rect(b.x0, y - rh, lab_w, rh, stroke=HAIR, sw=0.35)
        b.text(s, b.x0 + 4, y - 12, "Sans", 7, INK2)
        for c in range(7):
            b.rect(b.x0 + lab_w + c * cell, y - rh, cell, rh, stroke=HAIR, sw=0.35)
        y -= rh
    y -= 12
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Other observations / timing (e.g. worse 24h after injection)")
    b.footer()
    b.end()


def _02_right(b: Book, week: int):
    b.begin()
    y = b.header_bar("GLP-1 SIDE-EFFECT DIARY", f"Week {week}  ·  management log")
    h = 70
    b.box(b.x0, y - h, b.cw, h, "What seemed to help  (foods, timing, rest, clinician advice I already have)")
    b.writing_lines(y - 28, 2, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8
    h = 70
    b.box(b.x0, y - h, b.cw, h, "What seemed to aggravate")
    b.writing_lines(y - 28, 2, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8

    b.text("Hydration  (glasses)", b.x0, y, "Sans-Semi", 7.4, MID)
    b.water_row(b.x0 + 110, y + 2, n=8, gap=16)
    y -= 28
    b.text("Days I flagged for my clinician", b.x0, y, "Sans-Semi", 7.4, MID)
    b.day_pills(b.x0 + 160, y + 2)
    y -= 24

    h = 92
    b.box(b.x0, y - h, b.cw, h, "Bring-to-visit notes  (patterns, questions, photos to show)")
    b.writing_lines(y - 28, 4, gap=15, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8
    h = 64
    b.box(b.x0, y - h, b.cw, h, "Sleep this week  (hours, quality 1-5)")
    b.writing_lines(y - 28, 2, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Next appointment  ·  date / time / questions")
    b.footer()
    b.end()


def _02_visit(b: Book, n: int):
    b.begin()
    y = b.header_bar("GLP-1 SIDE-EFFECT DIARY", f"Visit prep  {n}")
    b.field("Appointment date", b.x0, y, 160)
    b.field("Clinician", b.x0 + 180, y, 150)
    y -= 24
    for p in [
        "Top three observations since last visit",
        "Questions I want answered",
        "Changes since last visit (dose as prescribed, other meds, life stress)",
        "What I need from this appointment",
    ]:
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 3, gap=16) - 12
    b.footer()
    b.end()


def build_02(path=None):
    path = path or OUTPUT / "02_GLP1_Side_Effect_and_Symptom_Diary_6x9.pdf"
    b = Book(path, SIX_NINE, running="GLP-1 SIDE-EFFECT DIARY")
    standard_front(
        b,
        "GLP-1 TRACKING SERIES",
        "Side-Effect & Symptom Diary",
        "Weekly adverse-event checklists, severity sliders, and visit-prep pages",
        "Thirty-six undated weeks  ·  6 × 9 in  ·  Grayscale interior",
        extra_disclaimer=GLP_EXTRA + " This diary does not diagnose. Worsening or severe symptoms require clinical care, not a journal entry.",
        how_to=[
            (
                "Weekly rhythm",
                [
                    "Left page: score each observation 0-5 for each day. Leave a cell blank if you did not notice it.",
                    "Right page: capture what helped, what aggravated, and anything you want on the next clinic list.",
                    "Every four weeks, fill a visit-prep page even if you do not have an appointment yet — it keeps the story linear.",
                ],
            ),
            (
                "Be specific, not dramatic",
                [
                    "Timing matters: note whether nausea clustered after injection day, after a high-fat meal, or on an empty stomach.",
                    "Do not change your dose because of a pattern you see here. Bring the pattern to your prescriber.",
                ],
            ),
        ],
        legend=[
            ("0-5 severity", "0 none · 3 interrupts the day · 5 worst I have had"),
            ("Flagged days", "Circle weekday pills for days you want to discuss"),
            ("Visit prep", "A one-page brief for your clinician, not a diagnosis form"),
        ],
        goals=[
            "Current dose I was prescribed (record only)",
            "Known sensitivities I already have",
            "My clinician's contact / portal notes",
            "The single symptom I most want to understand",
        ],
    )
    section_opener(b, "BEGIN", "Weekly diary", "Score 0-5. Blank means you did not notice it.")
    visit = 1
    for week in range(1, 37):
        _02_left(b, week)
        _02_right(b, week)
        if week % 4 == 0:
            _02_visit(b, visit)
            visit += 1
    for _ in range(4):
        b.notes_page()
    return b.save()


# ===================================================================== 03
PROMPTS_30 = [
    "What would 'enough protein' look like on a genuinely busy day?",
    "Name one thing that is working, even if the scale is quiet.",
    "Where did I feel true hunger versus habit versus boredom today?",
    "If I could keep only one habit this week, which one actually moves the needle?",
    "What story am I telling about this plateau, and is it useful?",
    "Which meal is the weakest protein moment in my day?",
    "How did I sleep, and how did that change my appetite cues?",
    "What would a kind coach tell me about the last seven days?",
    "Did I walk after a meal? What happened to evening snacking?",
    "Which non-scale victory did I skip past too quickly?",
    "What am I measuring besides weight — and what am I ignoring?",
    "Where did I under-drink water, and what replaced it?",
    "If this plateau lasted another month, what skill would I want stronger?",
    "What food still earns a place because it helps me stay on the plan?",
    "When did I last lift something heavy, even briefly?",
    "What would 'maintenance practice' look like for one evening out?",
    "Which cue makes me graze when I am not hungry?",
    "How can I make tomorrow's first meal easier than today's?",
    "What did fullness feel like in my body, in plain language?",
    "Who is a useful witness for this work, and who is not?",
    "Did I confuse 'the dose is not working' with 'life was loud this week'?",
    "What 10-minute movement is realistic on my worst day?",
    "Which clothes fit differently, even if the number did not?",
    "What am I willing to stop tracking for a week so I can rest?",
    "Where did I keep a promise to myself today?",
    "What would I tell a friend who is exactly where I am?",
    "Is my protein target still the one I was given — or a rumor I invented?",
    "What does 'enough food' mean on a low-appetite day?",
    "Which habit is identity now, not a grind?",
    "How will I mark the end of these 30 days without using the scale as a verdict?",
]


def _habit_grid(b: Book, x, y, w, habits, days=None):
    """habits: list of labels. One row of checkboxes for 'today' or weekdays."""
    if days is None:
        # today: single checkbox row
        col = w / max(len(habits), 1)
        for i, h in enumerate(habits):
            cx = x + i * col
            b.checkbox(cx, y, "", size=9)
            # wrap habit name under
            lines = h.split(" ")
            b.text(h, cx + 12, y + 1, "Sans", 6.3, INK2)
        return y
    lab_w = 88
    cell = (w - lab_w) / 7
    rh = 16
    b.c.setFillColor(PALE)
    b.c.rect(x, y - rh, w, rh, stroke=0, fill=1)
    for i, d in enumerate(list("MTWTFSS")):
        b.text(d, x + lab_w + i * cell + cell / 2, y - 11, "Sans-Semi", 7, MID, "center")
    y -= rh
    for i, h in enumerate(habits):
        if i % 2 == 0:
            b.c.setFillColor(WASH)
            b.c.rect(x, y - rh, w, rh, stroke=0, fill=1)
        b.rect(x, y - rh, lab_w, rh, stroke=HAIR, sw=0.35)
        b.text(h, x + 4, y - 11, "Sans", 6.8, INK2)
        for c in range(7):
            b.rect(x + lab_w + c * cell, y - rh, cell, rh, stroke=HAIR, sw=0.35)
        y -= rh
    return y


def _03_left(b: Book, day: int):
    b.begin()
    y = b.header_bar("PLATEAU-BREAKER 30", f"Day {day} of 30")
    b.date_line(b.x0, y, b.cw)
    y -= 24
    # big day number
    b.rect(b.x0, y - 52, 64, 52, stroke=INK, sw=0.8, fill=PALE)
    b.text(str(day), b.x0 + 32, y - 38, "Cormorant-Bold", 26, INK, "center")
    b.text("TODAY", b.x0 + 80, y - 14, "Sans-Semi", 8, MID)
    b.field("Wake time", b.x0 + 80, y - 32, 120)
    b.field("Sleep (h)", b.x0 + 220, y - 32, 90)
    y -= 64

    b.text("Habit grid  (tick if done — not if perfect)", b.x0, y, "Sans-Semi", 7.5, MID)
    y -= 16
    habits = [
        "Protein target",
        "Fiber focus",
        "Water goal",
        "Step target",
        "Strength / lift",
        "10 min outside",
        "Screen-off hour",
        "In bed on time",
    ]
    for i, h in enumerate(habits):
        col = i % 2
        row = i // 2
        x = b.x0 + col * (b.cw / 2)
        yy = y - row * 18
        b.checkbox(x, yy, h, size=9, fs=8)
    y -= 18 * 4 + 10

    b.rect(b.x0, y - 88, b.cw, 88, stroke=RULE, sw=0.6, r=3)
    b.text("Mindset prompt", b.x0 + 8, y - 14, "Sans-Semi", 7.2, MID)
    prompt = PROMPTS_30[(day - 1) % len(PROMPTS_30)]
    y2 = b.paragraph(prompt, b.x0 + 8, y - 30, b.cw - 16, "Cormorant-Italic", 11, 14, INK)
    b.writing_lines(y2 - 8, 2, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= 100

    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "What I actually did (not what I intended)", lines=True)
    b.footer()
    b.end()


def _03_right(b: Book, day: int):
    b.begin()
    y = b.header_bar("PLATEAU-BREAKER 30", f"Day {day}  ·  the needle")
    b.scale_row("True hunger (not habit)", b.x0, y, b.cw * 0.48)
    b.scale_row("Follow-through", b.x0 + b.cw * 0.52, y, b.cw * 0.48)
    y -= 46
    h = 80
    b.box(b.x0, y - h, b.cw, h, "Protein at each eating occasion  (tick + quick note)")
    for i, lab in enumerate(["Occasion 1", "Occasion 2", "Occasion 3", "Occasion 4"]):
        x = b.x0 + 8 + i * (b.cw / 4)
        b.checkbox(x, y - 36, lab, fs=6.8)
        b.dotted_field(x, y - 54, 70)
        b.dotted_field(x, y - 70, 70)
    y -= h + 8
    h = 72
    b.box(b.x0, y - h, b.cw, h, "Steps  ·  movement  ·  lifting")
    b.field("Steps", b.x0 + 8, y - 32, 100)
    b.field("Lift / carry", b.x0 + 140, y - 32, 160)
    b.writing_lines(y - 50, 1, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8
    h = 72
    b.box(b.x0, y - h, b.cw, h, "Non-scale victory")
    b.writing_lines(y - 28, 2, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8
    h = 80
    b.box(b.x0, y - h, b.cw, h, "If the scale did not move, what still counted?")
    b.writing_lines(y - 28, 3, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "One setup for tomorrow (food, shoes, calendar)")
    b.footer()
    b.end()


def _03_week(b: Book, week: int):
    b.begin()
    y = b.header_bar("PLATEAU-BREAKER 30", f"Week {week} review")
    for p in [
        "Average follow-through (1-10) and why",
        "The habit that slipped — and the real reason",
        "Evidence the plateau is not the whole story",
        "Adjustment I will test next week (not a new personality)",
    ]:
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 2, gap=16) - 10
    # Optional publisher QR (pep-talk) — blank so you can paste your own
    side = 58
    b.rect(b.x0, b.y0 + 18, side, side, stroke=HAIR, sw=0.6, r=2)
    b.set_stroke(HAIR, 0.4)
    b.c.setDash(1.5, 1.5)
    b.c.rect(b.x0 + 4, b.y0 + 22, side - 8, side - 8, stroke=1, fill=0)
    b.c.setDash()
    b.text("Optional QR", b.x0 + side + 10, b.y0 + 52, "Sans-Semi", 7.2, MID)
    b.text("Paste your own pep-talk / audio link. Leave blank if unused.", b.x0 + side + 10, b.y0 + 38, "Sans", 7, MUTED)
    b.footer()
    b.end()


def _03_encore(b: Book, day: int):
    b.begin()
    y = b.header_bar("PLATEAU-BREAKER 30", f"Encore day {day}")
    b.date_line(b.x0, y, b.cw)
    y -= 22
    habits = ["Protein", "Fiber", "Water", "Steps", "Lift", "Sleep"]
    for i, h in enumerate(habits):
        b.checkbox(b.x0 + (i % 3) * (b.cw / 3), y - (i // 3) * 18, h, fs=8)
    y -= 48
    b.scale_row("Follow-through", b.x0, y, b.cw)
    y -= 40
    b.box(b.x0, y - 90, b.cw, 90, "Notes")
    b.writing_lines(y - 28, 4, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= 102
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "NSV / setup for tomorrow")
    b.footer()
    b.end()


def build_03(path=None):
    path = path or OUTPUT / "03_GLP1_Plateau_Breaker_30_Day_Planner_6x9.pdf"
    b = Book(path, SIX_NINE, running="PLATEAU-BREAKER 30")
    standard_front(
        b,
        "GLP-1 TRACKING SERIES",
        "Plateau-Breaker 30-Day Challenge",
        "Daily habit grids, mindset prompts, and a second encore cycle",
        "Thirty challenge days + thirty encore days  ·  6 × 9 in",
        extra_disclaimer=GLP_EXTRA + " A plateau is not a diagnosis. Sudden or severe symptoms need a clinician, not a challenge calendar.",
        how_to=[
            (
                "How the 30 days work",
                [
                    "Each day is a two-page spread: habits and a prompt on the left, protein/movement/NSV on the right.",
                    "Do not add five new habits. Tick the grid honestly. The point is a clean signal, not a gold star.",
                    "A weekly review sits after every seven days. After day 30, use the encore pages if you want another cycle without buying a second copy.",
                ],
            ),
            (
                "About pep talks",
                [
                    "Prompts are printed in the book so you do not need an audio file or a QR code. Read them out loud if you like.",
                ],
            ),
        ],
        legend=[
            ("Habit tick", "Done enough. Not perfect."),
            ("Encore", "A lighter one-page day if you repeat the cycle"),
        ],
        goals=[
            "My definition of a plateau (how long, what I expected)",
            "Protein and step targets I was already given",
            "The one habit I will not drop even if everything else slips",
            "How I will celebrate day 30 without using the scale as a judge",
        ],
    )
    section_opener(b, "CYCLE ONE", "30-day challenge", "Two pages a day. Honesty over intensity.")
    for day in range(1, 31):
        _03_left(b, day)
        _03_right(b, day)
        if day % 7 == 0:
            _03_week(b, day // 7)
    _03_week(b, 5)
    section_opener(b, "CYCLE TWO", "Encore days", "Lighter pages if you run it again.")
    for day in range(1, 31):
        _03_encore(b, day)
    for _ in range(4):
        b.notes_page()
    return b.save()


# ===================================================================== 04
def _04_month_open(b: Book, month: int):
    b.begin()
    y = b.header_bar("GLP-1 MAINTENANCE", f"Month {month}  ·  check-in")
    b.field("Month / year", b.x0, y, 160)
    b.field("Refill due", b.x0 + 180, y, 140)
    y -= 22
    b.text("Weight range band  (not a daily verdict — a band you and your clinician agree on)", b.x0, y, "Sans", 7.2, MUTED)
    y -= 16
    b.rect(b.x0, y - 54, b.cw, 54, stroke=RULE, sw=0.6, r=3)
    b.field("Lower bound", b.x0 + 8, y - 18, 140)
    b.field("Upper bound", b.x0 + 170, y - 18, 140)
    b.field("Waist", b.x0 + 8, y - 38, 100)
    b.field("Hip", b.x0 + 120, y - 38, 100)
    b.field("How clothes fit", b.x0 + 230, y - 38, 100)
    y -= 68
    h = 80
    b.box(b.x0, y - h, b.cw, h, "Relapse-risk reflection  (travel, stress, missed doses, all-or-nothing thinking)")
    b.writing_lines(y - 28, 3, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 10
    h = 80
    b.box(b.x0, y - h, b.cw, h, "Labs / appointments this month")
    b.writing_lines(y - 28, 3, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 10
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Maintenance intention for the next four weeks")
    b.footer()
    b.end()


def _04_week(b: Book, month: int, week: int):
    b.begin()
    y = b.header_bar("GLP-1 MAINTENANCE", f"Month {month}  ·  week {week}")
    b.date_line(b.x0, y, b.cw)
    y -= 22
    b.rect(b.x0, y - 50, b.cw, 50, stroke=RULE, sw=0.55, r=3)
    b.field("This week's range (low)", b.x0 + 8, y - 18, 150)
    b.field("This week's range (high)", b.x0 + 180, y - 18, 140)
    b.field("Waist / clothes note", b.x0 + 8, y - 38, 300)
    y -= 62
    habits = ["Protein most days", "Walks", "Lifting", "Sleep window", "Refill check", "Social plan"]
    for i, h in enumerate(habits):
        b.checkbox(b.x0 + (i % 2) * (b.cw / 2), y - (i // 2) * 18, h, fs=8)
    y -= 18 * 3 + 8
    b.text("Relapse-risk this week", b.x0, y, "Sans-Semi", 7.4, MID)
    b.slider(b.x0 + 130, y + 3, 180, ticks=5, labels=["low", "", "", "", "high"])
    y -= 28
    h = 78
    b.box(b.x0, y - h, b.cw, h, "What protected maintenance this week")
    b.writing_lines(y - 28, 3, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= h + 8
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "What wobbled — and the smallest repair")
    b.footer()
    b.end()


def _04_review(b: Book, month: int):
    b.begin()
    y = b.header_bar("GLP-1 MAINTENANCE", f"Month {month}  ·  close")
    for p in [
        "Did I stay inside the range band? What do I notice without judging?",
        "Refill status / next pen / next visit",
        "Body composition clues (energy, lifting, clothing) — not just mass",
        "Keep / drop / tweak for next month",
    ]:
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 3, gap=16) - 12
    b.footer()
    b.end()


def build_04(path=None):
    path = path or OUTPUT / "04_GLP1_Maintenance_Phase_Tracker_6x9.pdf"
    b = Book(path, SIX_NINE, running="GLP-1 MAINTENANCE")
    standard_front(
        b,
        "GLP-1 TRACKING SERIES",
        "Maintenance-Phase Tracker",
        "Twelve undated months of range bands, refill reminders, and relapse-risk notes",
        "Weekly pages inside each month  ·  6 × 9 in",
        extra_disclaimer=GLP_EXTRA + " Maintenance ranges should be set with your clinician. This book only records them.",
        how_to=[
            (
                "Range, not a daily trial",
                [
                    "Open each month by writing the weight band you and your care team agreed on. Track the week's range, not a courtroom weigh-in every morning.",
                    "Four weekly pages, then a close-out. Use refill and lab lines so logistics do not ambush you.",
                    "Relapse-risk is about patterns (travel, skipped meals, all-or-nothing days), not moral failure.",
                ],
            )
        ],
        legend=[
            ("Range band", "Lower and upper bounds you already chose with a clinician"),
            ("Relapse-risk slider", "How wobbly the week felt, 1-5"),
        ],
        goals=[
            "Agreed maintenance range",
            "Waist / clothing baseline",
            "Refill cadence I was given",
            "Early warning signs that I am slipping into all-or-nothing",
        ],
    )
    section_opener(b, "BEGIN", "Twelve months", "A quieter kind of tracking.")
    for m in range(1, 13):
        _04_month_open(b, m)
        for w in range(1, 5):
            _04_week(b, m, w)
        _04_review(b, m)
    for _ in range(6):
        b.notes_page()
    return b.save()


# ===================================================================== 05
def _quad(b: Book, x, y, w, h, title):
    b.rect(x, y - h, w, h, stroke=RULE, sw=0.6, r=3)
    b.c.setFillColor(WASH)
    b.c.rect(x, y - 16, w, 16, stroke=0, fill=1)
    b.set_stroke(RULE, 0.6)
    b.c.roundRect(x, y - h, w, h, 3, stroke=1, fill=0)
    b.text(title, x + 7, y - 12, "Sans-Semi", 7.2, MID)
    return y - 22


def _05_day(b: Book, day: int):
    b.begin()
    y = b.header_bar("HUNGER & CRAVING LOG", f"Day {day}")
    b.date_line(b.x0, y, b.cw)
    y -= 18
    gap = 8
    qw = (b.cw - gap) / 2
    qh = 195
    # Q1 mood
    top = y
    iy = _quad(b, b.x0, y, qw, qh, "1  ·  Mood")
    for i, m in enumerate(["Calm", "Anxious", "Low", "Irritable", "Restless", "Content", "Tired", "Wired"]):
        b.checkbox(b.x0 + 10 + (i % 2) * (qw / 2), iy - 8 - (i // 2) * 16, m, fs=7.5)
    b.text("Notes", b.x0 + 10, iy - 84, "Sans", 7, MUTED)
    b.writing_lines(iy - 98, 4, gap=14, x0=b.x0 + 10, x1=b.x0 + qw - 10)
    # Q2 craving
    iy = _quad(b, b.x0 + qw + gap, y, qw, qh, "2  ·  Craving intensity")
    b.text("Peak today", b.x0 + qw + gap + 10, iy - 8, "Sans", 7.4, MID)
    _mini_scale(b, b.x0 + qw + gap + 10, iy - 28, n=10, gap=11.5, r=4)
    b.text("1 none", b.x0 + qw + gap + 10, iy - 44, "Sans", 6.2, MUTED)
    b.text("10 overwhelming", b.x0 + qw + gap + qw - 12, iy - 44, "Sans", 6.2, MUTED, "right")
    b.text("What I craved", b.x0 + qw + gap + 10, iy - 62, "Sans", 7.4, MID)
    b.writing_lines(iy - 76, 2, gap=14, x0=b.x0 + qw + gap + 10, x1=b.x0 + b.cw - 10)
    b.text("Time(s)", b.x0 + qw + gap + 10, iy - 112, "Sans", 7.4, MID)
    b.dotted_field(b.x0 + qw + gap + 52, iy - 112, 90)
    b.text("Hunger or habit?", b.x0 + qw + gap + 10, iy - 132, "Sans", 7.4, MID)
    b.checkbox(b.x0 + qw + gap + 10, iy - 150, "True hunger", fs=7.2)
    b.checkbox(b.x0 + qw + gap + 10, iy - 166, "Habit / cue", fs=7.2)
    b.checkbox(b.x0 + qw + gap + qw / 2, iy - 150, "Emotion", fs=7.2)
    b.checkbox(b.x0 + qw + gap + qw / 2, iy - 166, "Unsure", fs=7.2)

    y = top - qh - gap
    qh2 = 175
    iy = _quad(b, b.x0, y, qw, qh2, "3  ·  What I did instead")
    b.writing_lines(iy - 8, 8, gap=16, x0=b.x0 + 8, x1=b.x0 + qw - 8)
    iy = _quad(b, b.x0 + qw + gap, y, qw, qh2, "4  ·  Reward / sticker space")
    b.text("A small kindness or tick for handling it.", b.x0 + qw + gap + 8, iy - 6, "Sans", 6.8, MUTED)
    # sticker box
    b.rect(b.x0 + qw + gap + 16, y - qh2 + 16, qw - 32, qh2 - 50, stroke=HAIR, sw=0.5, r=4)
    y = y - qh2 - 10
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Evening one-liner", lines=True)
    b.footer()
    b.end()


def _05_week(b: Book, week: int):
    b.begin()
    y = b.header_bar("HUNGER & CRAVING LOG", f"Week {week} pattern")
    b.paragraph(
        "Look for clusters: time of day, mood, people, places. Cravings are data, not a character review.",
        b.x0,
        y,
        b.cw,
        "Sans",
        8.5,
        12,
        INK2,
    )
    y -= 36
    for p in [
        "Most common time window",
        "Most common mood underneath",
        "The 'instead' that actually worked",
        "What I will set up next week (not a vow — a setup)",
    ]:
        b.text(p, b.x0, y, "Sans-Semi", 8, MID)
        y = b.writing_lines(y - 14, 3, gap=16) - 12
    b.footer()
    b.end()


def build_05(path=None):
    path = path or OUTPUT / "05_GLP1_Hunger_and_Craving_Mood_Log_6x9.pdf"
    b = Book(path, SIX_NINE, running="HUNGER & CRAVING LOG")
    standard_front(
        b,
        "GLP-1 TRACKING SERIES",
        "Hunger & Craving Mood Log",
        "Four-quadrant daily pages: mood, intensity, what I did instead, reward space",
        "Ninety undated days  ·  6 × 9 in",
        extra_disclaimer=GLP_EXTRA,
        how_to=[
            (
                "The four quadrants",
                [
                    "Mood first — cravings are easier to read when you name the weather underneath.",
                    "Intensity 1-10 is the peak, not the average. Write what you craved in plain food words.",
                    "Quadrant 3 is the skill: walk, protein, delay, text, tea. Quadrant 4 is a sticker / tick box so your brain gets a close-the-loop reward.",
                ],
            )
        ],
        legend=[
            ("Intensity 1-10", "Peak craving, not all-day average"),
            ("Reward space", "Sticker, tally, or a word. Keep it small."),
        ],
        goals=[
            "Cravings I already expect (time of day / food)",
            "Two 'instead' options that are realistic in my kitchen",
            "A reward that is not food",
        ],
    )
    section_opener(b, "BEGIN", "Daily quadrants")
    for d in range(1, 91):
        _05_day(b, d)
        if d % 7 == 0:
            _05_week(b, d // 7)
    for _ in range(4):
        b.notes_page()
    return b.save()


# ===================================================================== 06
def _timer_ring(b: Book, cx, cy, r=46):
    b.set_stroke(INK2, 1.0)
    b.c.circle(cx, cy, r, stroke=1, fill=0)
    b.set_stroke(HAIR, 0.6)
    b.c.circle(cx, cy, r - 8, stroke=1, fill=0)
    for i, lab in enumerate(["0", "15", "30", "45"]):
        ang = 90 - i * 90  # 0 at top
        import math

        rad = math.radians(ang)
        x1 = cx + (r - 2) * math.cos(rad)
        y1 = cy + (r - 2) * math.sin(rad)
        x2 = cx + (r + 5) * math.cos(rad)
        y2 = cy + (r + 5) * math.sin(rad)
        b.line(x1, y1, x2, y2, INK2, 0.8)
        xt = cx + (r + 14) * math.cos(rad)
        yt = cy + (r + 14) * math.sin(rad) - 3
        b.text(lab, xt, yt, "Sans", 6.5, MID, "center")
    b.text("min", cx, cy - 3, "Sans", 6.5, MUTED, "center")


def _06_left(b: Book, week: int):
    b.begin()
    y = b.header_bar("GLP-1 FITNESS COMPANION", f"Week {week}  ·  plan")
    b.field("Week of", b.x0, y, 150)
    b.field("Injection day (recorded)", b.x0 + 180, y, 140)
    y -= 22
    # split boxes
    h = 150
    w = (b.cw - 8) / 2
    b.box(b.x0, y - h, w, h, "Strength  (known lifts)")
    b.writing_lines(y - 28, 6, gap=16, x0=b.x0 + 8, x1=b.x0 + w - 8)
    b.box(b.x0 + w + 8, y - h, w, h, "Cardio / steps")
    b.writing_lines(y - 28, 6, gap=16, x0=b.x0 + w + 16, x1=b.x1 - 8)
    y -= h + 12
    b.text("Injection-to-workout cooldown  (personal record only — not a recommendation)", b.x0, y, "Sans", 6.8, MUTED)
    y -= 8
    _timer_ring(b, b.x0 + 58, y - 58, 44)
    b.text("Circle minutes I waited", b.x0 + 120, y - 20, "Sans-Semi", 7.5, MID)
    b.writing_lines(y - 40, 4, gap=16, x0=b.x0 + 120, x1=b.x1)
    y -= 128
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Recovery plan  (sleep, rest, protein)", lines=True)
    b.footer()
    b.end()


def _06_right(b: Book, week: int):
    b.begin()
    y = b.header_bar("GLP-1 FITNESS COMPANION", f"Week {week}  ·  log")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    rh = 48
    for i, d in enumerate(days):
        if y - rh < b.y0 + 70:
            break
        b.rect(b.x0, y - rh, b.cw, rh, stroke=HAIR, sw=0.45, r=2)
        b.c.setFillColor(PALE)
        b.c.rect(b.x0, y - rh, 36, rh, stroke=0, fill=1)
        b.text(d[:2].upper(), b.x0 + 18, y - rh / 2 - 3, "Sans-Semi", 7.5, MID, "center")
        b.field("What", b.x0 + 42, y - 16, 180)
        b.field("Steps", b.x0 + 230, y - 16, 90)
        b.field("RPE 1-10", b.x0 + 42, y - 34, 80)
        b.field("Note", b.x0 + 140, y - 34, 180)
        y -= rh + 4
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Week in one sentence")
    b.footer()
    b.end()


def build_06(path=None):
    path = path or OUTPUT / "06_GLP1_Fitness_and_Step_Companion_6x9.pdf"
    b = Book(path, SIX_NINE, running="GLP-1 FITNESS COMPANION")
    standard_front(
        b,
        "GLP-1 TRACKING SERIES",
        "Fitness & Step Companion",
        "Weekly strength-cardio splits, recovery notes, and a cooldown timer graphic",
        "Thirty-two undated weeks  ·  6 × 9 in",
        extra_disclaimer=GLP_EXTRA + " Exercise timing around injections is individual. The timer is a blank record, not a protocol.",
        how_to=[
            (
                "Plan on the left, log on the right",
                [
                    "Write a strength idea and a cardio/step idea you already know how to do. This is not a workout program.",
                    "Log RPE (rate of perceived effort) 1-10. Protect recovery on low-appetite weeks.",
                    "The ring is only for circling how many minutes you happened to wait. It is not advice to train or to wait.",
                ],
            )
        ],
        legend=[
            ("RPE", "1 easy · 5 moderate · 10 all-out"),
            ("Timer ring", "Personal record of minutes, not a medical wait time"),
        ],
        goals=[
            "Movement I enjoy enough to repeat",
            "Step range that feels human",
            "Rest-day rule I can keep",
        ],
    )
    section_opener(b, "BEGIN", "Weekly training pages")
    for w in range(1, 33):
        _06_left(b, w)
        _06_right(b, w)
        if w % 4 == 0:
            b.begin()
            y = b.header_bar("GLP-1 FITNESS COMPANION", f"Weeks {w-3}-{w}  ·  review")
            for p in ["What got easier", "What needs a smaller version", "PRs / clothes / energy", "Next block focus"]:
                b.text(p, b.x0, y, "Sans-Semi", 8, MID)
                y = b.writing_lines(y - 14, 3, gap=16) - 12
            b.footer()
            b.end()
    for _ in range(6):
        b.notes_page()
    return b.save()


# ===================================================================== 07 pocket 5x8
def build_07(path=None):
    path = path or OUTPUT / "07_GLP1_Titration_Schedule_Notebook_5x8.pdf"
    b = Book(
        path,
        FIVE_EIGHT,
        gutter=0.62 * inch,
        outer=0.42 * inch,
        top=0.40 * inch,
        bottom=0.44 * inch,
        running="GLP-1 TITRATION LOG",
    )
    standard_front(
        b,
        "GLP-1 TRACKING SERIES",
        "Titration Schedule Notebook",
        "Pocket log for dose dates, next-pen reminders, and sticker space",
        "5 × 8 in  (KDP pocket trim)  ·  Fifty-two weeks",
        extra_disclaimer=GLP_EXTRA + " Never change a dose because a table in a notebook looks 'due.' Only your prescriber sets titration.",
        how_to=[
            (
                "How to log, not how to titrate",
                [
                    "Copy the dose your prescriber already gave you. Write the date you took it. That is the whole job.",
                    "Use the next-pen line when you open a new pen or vial so you are not surprised mid-week.",
                    "The margin is for a small sticker or lot number. This is a record, not a protocol.",
                ],
            )
        ],
        legend=[
            ("Dose column", "The amount you were directed to take — copied, not chosen"),
            ("Skip / delay", "If delayed, write why. No catch-up unless your prescriber said so"),
        ],
        goals=[
            "Prescribed starting dose (record only)",
            "Planned follow-up visit",
            "Pharmacy / refill phone or portal",
        ],
        belongs_fields=["Name", "Prescriber / clinic", "Pharmacy", "If found, please return to"],
    )
    section_opener(b, "BEGIN", "Weekly dose table", "Copy. Date. Do not invent.")
    for week in range(1, 53):
        b.begin()
        y = b.header_bar("GLP-1 TITRATION LOG", f"Week {week}")
        b.field("Week of", b.x0, y, 130)
        b.field("Prescribed dose", b.x0 + 150, y, 90)
        y -= 18
        # table header
        cols = [("Day", 0.18), ("Date", 0.22), ("Dose (as Rx)", 0.26), ("Time / site", 0.34)]
        rh = 16
        cw_s = [c[1] * b.cw for c in cols]
        b.c.setFillColor(PALE)
        b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
        x = b.x0
        for (lab, _), w in zip(cols, cw_s):
            b.rect(x, y - rh, w, rh, stroke=HAIR, sw=0.4)
            b.text(lab, x + 3, y - 11, "Sans-Semi", 6.3, MID)
            x += w
        y -= rh
        for i, d in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
            x = b.x0
            rowfill = WASH if i % 2 == 0 else None
            if rowfill:
                b.c.setFillColor(rowfill)
                b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
            for w in cw_s:
                b.rect(x, y - rh, w, rh, stroke=HAIR, sw=0.35)
                x += w
            b.text(d, b.x0 + 4, y - 11, "Sans", 7, INK2)
            y -= rh
        y -= 10
        b.field("Next pen / vial reminder", b.x0, y, b.cw)
        y -= 18
        b.field("Opened on", b.x0, y, b.cw * 0.48)
        b.field("Discard-after date (from label)", b.x0 + b.cw * 0.52, y, b.cw * 0.48)
        y -= 20
        h = 56
        b.box(b.x0, y - h, b.cw, h, "Notes (skipped, delayed, questions for clinic)")
        b.writing_lines(y - 26, 2, gap=14, x0=b.x0 + 6, x1=b.x1 - 6)
        y -= h + 8
        # sticker margin
        b.rect(b.x0, b.y0 + 14, b.cw, y - (b.y0 + 14), stroke=HAIR, sw=0.5, r=3)
        b.text("Sticker / lot / med-label space", b.x0 + 8, y - 12, "Sans-Semi", 6.8, MUTED)
        b.footer()
        b.end()
        if week % 4 == 0:
            b.begin()
            y = b.header_bar("GLP-1 TITRATION LOG", f"Month close  ·  after week {week}")
            b.field("Month", b.x0, y, 140)
            y -= 20
            for p in ["Doses taken as prescribed / delayed / skipped (counts only)", "Refill status", "Questions for my prescriber"]:
                b.text(p, b.x0, y, "Sans-Semi", 7.5, MID)
                y = b.writing_lines(y - 12, 3, gap=14) - 10
            b.footer()
            b.end()
    for _ in range(6):
        b.notes_page()
    return b.save()


# ===================================================================== 08
NSV_PROMPTS = [
    "Clothing that moved differently",
    "Energy I did not have to bargain for",
    "A lab, scan, or reading I can celebrate",
    "Sleep that felt like sleep",
    "A social moment that was easier",
    "Strength I could feel",
    "A craving I rode out",
    "Kindness I showed this body",
    "A walk I actually wanted",
    "Pain or reflux that was quieter",
    "Focus that lasted",
    "A photo or mirror note that was fair",
]


def _08_day(b: Book, day: int):
    b.begin()
    y = b.header_bar("NSV GRATITUDE", f"Day {day}")
    b.date_line(b.x0, y, b.cw)
    y -= 18
    h = (y - b.y0 - 24) / 2 - 6
    # gratitude
    b.rect(b.x0, y - h, b.cw, h, stroke=RULE, sw=0.6, r=3)
    b.text("Gratitude", b.x0 + 10, y - 18, "Cormorant-Semi", 14, INK)
    b.text("Three small true things.", b.x0 + 10, y - 34, "Sans", 7.5, MUTED)
    b.writing_lines(y - 52, 8, gap=18, x0=b.x0 + 10, x1=b.x1 - 10)
    y = y - h - 12
    b.rect(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), stroke=RULE, sw=0.6, r=3)
    b.text("Non-scale victory", b.x0 + 10, y - 18, "Cormorant-Semi", 14, INK)
    hint = NSV_PROMPTS[(day - 1) % len(NSV_PROMPTS)]
    b.text(hint, b.x0 + 10, y - 34, "Sans-Italic", 8, MUTED)
    b.writing_lines(y - 52, 6, gap=18, x0=b.x0 + 10, x1=b.x1 - 10)
    b.footer()
    b.end()


def build_08(path=None):
    path = path or OUTPUT / "08_GLP1_Non_Scale_Victories_Gratitude_Journal_6x9.pdf"
    b = Book(path, SIX_NINE, running="NSV GRATITUDE")
    standard_front(
        b,
        "GLP-1 TRACKING SERIES",
        "Non-Scale Victories Gratitude Journal",
        "Half-page gratitude, half-page NSV capture — energy, clothing, labs",
        "One hundred twenty undated days  ·  6 × 9 in",
        extra_disclaimer=GLP_EXTRA,
        how_to=[
            (
                "Two halves, one day",
                [
                    "Top: three true gratitudes, not a performance.",
                    "Bottom: one non-scale victory. The rotating hint is optional; ignore it if the day already named itself.",
                    "If nothing 'big' happened, write a small true thing. That is the practice.",
                ],
            )
        ],
        legend=[("NSV", "Non-scale victory — anything the scale is too crude to see")],
        goals=[
            "Why I want a record that is not weight",
            "Victories I already have and keep forgetting",
        ],
    )
    section_opener(b, "BEGIN", "Daily pages", "Quiet evidence.")
    for d in range(1, 121):
        _08_day(b, d)
        if d % 30 == 0:
            b.begin()
            y = b.header_bar("NSV GRATITUDE", f"Days {d-29}-{d}  ·  harvest")
            b.paragraph("List the victories you would miss if you only kept the scale.", b.x0, y, b.cw, "Sans", 9, 13, INK2)
            y -= 24
            b.writing_lines(y, 22, gap=18)
            b.footer()
            b.end()
    return b.save()


# ===================================================================== 09 letter calendar
def _calendar_grid(b: Book, y_top, rows=6):
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    grid_h = y_top - (b.y0 + 8)
    hdr = 18
    cell_h = (grid_h - hdr) / rows
    cell_w = b.cw / 7
    b.c.setFillColor(PALE)
    b.c.rect(b.x0, y_top - hdr, b.cw, hdr, stroke=0, fill=1)
    for i, d in enumerate(days):
        b.rect(b.x0 + i * cell_w, y_top - hdr, cell_w, hdr, stroke=INK2, sw=0.5)
        b.text(d, b.x0 + i * cell_w + cell_w / 2, y_top - 13, "Sans-Semi", 8, INK, "center")
    for r in range(rows):
        for c in range(7):
            x = b.x0 + c * cell_w
            y = y_top - hdr - (r + 1) * cell_h
            b.rect(x, y, cell_w, cell_h, stroke=HAIR, sw=0.45)
            # small sticker circle
            b.set_stroke(GHOST, 0.7)
            b.c.circle(x + 12, y + cell_h - 12, 7, stroke=1, fill=0)
            b.line(x + 8, y + 10, x + cell_w - 8, y + 10, HAIR, 0.3)
            b.line(x + 8, y + 22, x + cell_w - 8, y + 22, HAIR, 0.3)


def _09_month_cal(b: Book, month: int):
    b.begin()
    y = b.header_bar("INJECTION CALENDAR", f"Month {month}")
    b.field("Month name", b.x0, y, 150)
    b.field("Year", b.x0 + 170, y, 80)
    b.field("Prescribed day(s)", b.x0 + 270, y, 160)
    y -= 16
    b.text("Write 1 on the correct weekday. Use vinyl stickers in the circle. Matte toner pages take stickers well if you press firmly.", b.x0, y, "Sans", 7, MUTED)
    y -= 12
    _calendar_grid(b, y, rows=6)
    b.footer()
    b.end()


def _09_log(b: Book, month: int):
    b.begin()
    y = b.header_bar("INJECTION CALENDAR", f"Month {month}  ·  injection log")
    cols = [("Date", 0.14), ("Time", 0.12), ("Site", 0.16), ("Dose (as Rx)", 0.18), ("Lot / pen", 0.18), ("Notes", 0.22)]
    rh = 18
    b.c.setFillColor(PALE)
    b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
    x = b.x0
    ws = [c[1] * b.cw for c in cols]
    for (lab, _), w in zip(cols, ws):
        b.rect(x, y - rh, w, rh, stroke=HAIR, sw=0.4)
        b.text(lab, x + 4, y - 12, "Sans-Semi", 7, MID)
        x += w
    y -= rh
    for i in range(16):
        x = b.x0
        if i % 2 == 0:
            b.c.setFillColor(WASH)
            b.c.rect(b.x0, y - rh, b.cw, rh, stroke=0, fill=1)
        for w in ws:
            b.rect(x, y - rh, w, rh, stroke=HAIR, sw=0.35)
            x += w
        y -= rh
        if y < b.y0 + 90:
            break
    # site rotation
    b.text("Site rotation sketch  (abdomen quadrants — follow the map your clinic gave you)", b.x0, y - 8, "Sans-Semi", 7.2, MID)
    y -= 16
    # four abdomen boxes
    s = 36
    labels = ["RUQ", "LUQ", "LLQ", "RLQ"]
    positions = [(0, 1), (1, 1), (1, 0), (0, 0)]
    ox, oy = b.x0 + 8, b.y0 + 18
    for lab, (px, py) in zip(labels, positions):
        b.rect(ox + px * s, oy + py * s, s, s, stroke=INK2, sw=0.7)
        b.text(lab, ox + px * s + s / 2, oy + py * s + 14, "Sans", 6.5, MID, "center")
    b.text("Thigh L / R     Arm L / R     Other", ox + 100, oy + 40, "Sans", 8, INK2)
    b.writing_lines(oy + 24, 2, gap=16, x0=ox + 100, x1=b.x1)
    b.footer()
    b.end()


def _09_notes(b: Book, month: int):
    b.begin()
    y = b.header_bar("INJECTION CALENDAR", f"Month {month}  ·  refill & notes")
    b.field("Pharmacy", b.x0, y, 200)
    b.field("Refill due", b.x0 + 220, y, 160)
    y -= 20
    b.field("Coupon / savings program name (write it — programs change)", b.x0, y, b.cw * 0.72)
    side = 52
    b.rect(b.x1 - side, y - 8, side, side, stroke=HAIR, sw=0.6, r=2)
    b.text("QR", b.x1 - side / 2, y + 12, "Sans", 6, MUTED, "center")
    y -= 28
    b.box(b.x0, y - 90, b.cw, 90, "Questions for clinic")
    b.writing_lines(y - 28, 4, gap=16, x0=b.x0 + 8, x1=b.x1 - 8)
    y -= 102
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Notes")
    b.footer()
    b.end()


def _09_week(b: Book, month: int, week: int):
    b.begin()
    y = b.header_bar("INJECTION CALENDAR", f"Month {month}  ·  week {week}")
    b.date_line(b.x0, y, b.cw)
    y -= 20
    b.rect(b.x0, y - 70, b.cw, 70, stroke=RULE, sw=0.55, r=3)
    b.field("Injection this week?  date/time", b.x0 + 8, y - 18, 240)
    b.field("Site", b.x0 + 270, y - 18, 140)
    b.field("How I felt 24h later", b.x0 + 8, y - 40, 400)
    b.field("Sticker used", b.x0 + 8, y - 58, 160)
    y -= 84
    b.box(b.x0, b.y0 + 16, b.cw, y - (b.y0 + 16), "Week notes")
    b.footer()
    b.end()


def build_09(path=None):
    path = path or OUTPUT / "09_GLP1_Injection_Sticker_Calendar_85x11.pdf"
    b = Book(
        path,
        LETTER,
        gutter=0.80 * inch,
        outer=0.55 * inch,
        top=0.50 * inch,
        bottom=0.52 * inch,
        running="INJECTION CALENDAR",
    )
    standard_front(
        b,
        "GLP-1 TRACKING SERIES",
        "Pre- & Post-Injection Sticker Calendar",
        "Undated monthly calendars with sticker circles, site rotation, and refill logs",
        "8.5 × 11 in  ·  Twelve months  ·  Grayscale (white paper recommended)",
        extra_disclaimer=GLP_EXTRA,
        how_to=[
            (
                "Calendars made for stickers",
                [
                    "Each month opens with a six-row calendar. Number the days yourself so the book never expires.",
                    "The small circle in each cell is for a vinyl sticker (pre-injection / done). Press firmly; white KDP paper holds better than cream.",
                    "Facing log pages catch dose-as-prescribed, lot, and site. A weekly sheet sits after the month log.",
                    "Skip printable QR coupons — write any savings program name on the refill line. Coupons change; ink does not.",
                ],
            )
        ],
        legend=[
            ("Cell circle", "Sticker target"),
            ("RUQ/LUQ/LLQ/RLQ", "Abdomen quadrants — use the rotation your clinic taught you"),
        ],
        goals=[
            "Usual injection weekday",
            "Sticker system I will actually use",
            "Pharmacy / refill reminder method",
        ],
    )
    section_opener(b, "BEGIN", "Twelve undated months")
    # site map page
    b.begin()
    y = b.header_bar("INJECTION CALENDAR", "Site map  (copy what your clinic showed you)")
    b.paragraph(
        "This is a blank map, not instructions. Draw arrows in the order you were taught. If you were not taught a map, ask — do not invent one from a book.",
        b.x0,
        y,
        b.cw,
        "Sans",
        9,
        13,
        INK2,
    )
    y -= 50
    # large abdomen
    bw, bh = 220, 180
    bx = b.x0 + 20
    by = y - bh
    b.rect(bx, by, bw, bh, stroke=INK, sw=1)
    b.line(bx + bw / 2, by, bx + bw / 2, by + bh, INK, 0.6)
    b.line(bx, by + bh / 2, bx + bw, by + bh / 2, INK, 0.6)
    b.text("RIGHT UPPER", bx + bw * 0.25, by + bh * 0.72, "Sans", 8, MID, "center")
    b.text("LEFT UPPER", bx + bw * 0.75, by + bh * 0.72, "Sans", 8, MID, "center")
    b.text("RIGHT LOWER", bx + bw * 0.25, by + bh * 0.22, "Sans", 8, MID, "center")
    b.text("LEFT LOWER", bx + bw * 0.75, by + bh * 0.22, "Sans", 8, MID, "center")
    b.text("Center cross = navel. Do not inject there unless directed.", bx + bw / 2, by - 14, "Sans", 7, MUTED, "center")
    b.rect(bx + bw + 40, by + 90, 120, 80, stroke=INK, sw=0.8)
    b.text("Thigh window", bx + bw + 100, by + 125, "Sans", 8, MID, "center")
    b.rect(bx + bw + 40, by, 120, 70, stroke=INK, sw=0.8)
    b.text("Arm window", bx + bw + 100, by + 30, "Sans", 8, MID, "center")
    b.footer()
    b.end()
    for m in range(1, 13):
        _09_month_cal(b, m)
        _09_log(b, m)
        for w in range(1, 5):
            _09_week(b, m, w)
        _09_notes(b, m)
    for _ in range(6):
        b.notes_page()
    return b.save()


BUILDERS_A = [
    build_01,
    build_02,
    build_03,
    build_04,
    build_05,
    build_06,
    build_07,
    build_08,
    build_09,
]
