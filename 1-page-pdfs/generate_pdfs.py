#!/usr/bin/env python3
"""
One-page PDF product generator.

Renders 16 polished, print-ready one-page PDFs (US Letter) — improved, cleaner,
and more detailed versions of the proven best-selling one-pagers found on
Etsy/Gumroad (sales trackers, cheat sheets, clinical references, etc.).

Usage:
    python3 1-page-pdfs/generate_pdfs.py

Requires: fpdf2   (pip install fpdf2)
Outputs:  1-page-pdfs/*.pdf
"""

from __future__ import annotations

import platform
from datetime import datetime
from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    from fpdf2 import FPDF

OUT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Design system
# ---------------------------------------------------------------------------

PAGE_W = 215.9  # US Letter width (mm)
PAGE_H = 279.4
MARGIN = 12.0
CONTENT_W = PAGE_W - 2 * MARGIN

# Accent palettes per category
INK = (30, 34, 40)          # near-black text
MUTED = (110, 118, 128)     # secondary text
LIGHT = (238, 240, 243)     # light fill
RULE = (200, 205, 212)      # hairline

FONT = "DejaVu"
# Cross-platform font paths
if platform.system() == "Windows":
    FONT_PATH = "C:\\Windows\\Fonts\\arial.ttf"
    FONT_PATH_B = "C:\\Windows\\Fonts\\arialbd.ttf"
else:
    FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    FONT_PATH_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


class OnePager(FPDF):
    def __init__(self, title: str, subtitle: str, accent):
        super().__init__(orientation="P", unit="mm", format="Letter")
        self.set_creation_date(datetime(2026, 1, 1, 0, 0, 0))  # deterministic output
        self.title = title
        self.subtitle = subtitle
        self.accent = accent
        self.add_font(FONT, "", FONT_PATH)
        self.add_font(FONT, "B", FONT_PATH_B)
        self.add_font(FONT, "I", FONT_PATH)  # no oblique available; use regular
        self.set_auto_page_break(auto=False)
        self.set_margins(MARGIN, MARGIN, MARGIN)
        self.add_page()

    # ---- primitives -------------------------------------------------------
    def _accent(self):
        self.set_text_color(*self.accent)

    def _ink(self):
        self.set_text_color(*INK)

    def _muted(self):
        self.set_text_color(*MUTED)

    def header(self):
        self.set_fill_color(*self.accent)
        self.rect(MARGIN, MARGIN, CONTENT_W, 20, style="F")
        self.set_xy(MARGIN + 4, MARGIN + 3)
        self.set_font(FONT, "B", 17)
        self.set_text_color(255, 255, 255)
        self.cell(CONTENT_W - 8, 8, self.title, ln=1)
        self.set_x(MARGIN + 4)
        self.set_font(FONT, "", 9.5)
        self.cell(CONTENT_W - 8, 6, self.subtitle, ln=1)
        self.set_y(MARGIN + 22)

    def section(self, text: str, fill=None):
        """A filled section band."""
        if self.get_y() > PAGE_H - 26:
            return
        fill = fill or self.accent
        self.set_fill_color(*fill)
        self.rect(MARGIN, self.get_y(), CONTENT_W, 6.2, style="F")
        self.set_xy(MARGIN + 2, self.get_y() + 0.6)
        self.set_font(FONT, "B", 8.6)
        self.set_text_color(255, 255, 255)
        self.cell(CONTENT_W - 4, 5, text.upper(), ln=1)
        self.ln(1.6)

    def label(self, text: str):
        self.set_font(FONT, "B", 8.2)
        self._ink()
        self.cell(0, 4.4, text, ln=1)

    def body(self, text: str, size=8.4, h=4.2):
        self.set_font(FONT, "", size)
        self._ink()
        self.multi_cell(CONTENT_W, h, text, align="L")
        self.set_x(MARGIN)

    def muted(self, text: str, size=7.2):
        self.set_font(FONT, "I", size)
        self._muted()
        self.multi_cell(CONTENT_W, 3.8, text, align="L")
        self.set_x(MARGIN)

    def rule(self):
        y = self.get_y()
        self.set_draw_color(*RULE)
        self.set_line_width(0.25)
        self.line(MARGIN, y, PAGE_W - MARGIN, y)
        self.ln(2)

    def _row(self, widths, data, header=False, row_h=6.0):
        """Draw a table row with wrapping; returns new y."""
        x0 = MARGIN
        y0 = self.get_y()
        # compute wrapped heights
        lines = []
        for i, (w, txt) in enumerate(zip(widths, data)):
            t = str(txt)
            if header:
                self.set_font(FONT, "B", 8.0)
            else:
                self.set_font(FONT, "", 7.8)
            n = max(1, int(self.get_string_width(t) / (w - 2.2)) + 1)
            lines.append(n)
        h = max(row_h, max(lines) * 4.4)
        if y0 + h > PAGE_H - 26:
            return y0  # no room; caller handles
        for i, (w, txt) in enumerate(zip(widths, data)):
            x = x0 + sum(widths[:i])
            if header:
                self.set_fill_color(*self.accent)
                self.set_text_color(255, 255, 255)
                self.set_font(FONT, "B", 8.0)
            else:
                self.set_fill_color(*LIGHT) if i % 2 == 0 else self.set_fill_color(255, 255, 255)
                self.set_text_color(*INK)
                self.set_font(FONT, "", 7.8)
            self.set_xy(x, y0)
            self.rect(x, y0, w, h, style="F")
            self.set_xy(x + 1.1, y0 + 0.7)
            self.multi_cell(w - 2.2, 4.4, str(txt), align="L")
        self.set_y(y0 + h)
        self.set_x(MARGIN)
        return self.get_y()

    def table(self, headers, rows, widths):
        self._row(widths, headers, header=True)
        for r in rows:
            self._row(widths, r)

    def field_row(self, label_text, lines=1, width=None, hint=""):
        """A fill-in field: bold label, then ruled blank line(s)."""
        w = width or CONTENT_W
        self.set_x(MARGIN)
        self.set_font(FONT, "B", 8.2)
        self._ink()
        self.cell(w, 4.4, label_text, ln=1)
        for _ in range(lines):
            y = self.get_y()
            self.set_draw_color(*RULE)
            self.set_line_width(0.3)
            self.line(MARGIN, y + 3.2, MARGIN + w, y + 3.2)
            if hint:
                self.set_font(FONT, "I", 6.8)
                self._muted()
                self.set_xy(MARGIN, y + 0.4)
                self.cell(w, 3, hint, align="R")
            self.ln(4.4)

    def checklist(self, items, cols=2, box_h=4.6):
        cw = (CONTENT_W - (cols - 1) * 4) / cols
        x0 = MARGIN
        y0 = self.get_y()
        per_col = (len(items) + cols - 1) // cols
        for c in range(cols):
            for i in range(per_col):
                idx = c * per_col + i
                if idx >= len(items):
                    break
                y = y0 + i * box_h
                self.set_draw_color(*RULE)
                self.set_line_width(0.3)
                self.rect(x0 + c * (cw + 4), y, 2.8, 2.8)
                self.set_font(FONT, "", 7.8)
                self._ink()
                self.set_xy(x0 + c * (cw + 4) + 4, y - 0.6)
                self.multi_cell(cw - 4, 3.8, items[idx], align="L")
        self.set_y(y0 + per_col * box_h)
        self.set_x(MARGIN)

    def footer(self):
        self.set_y(PAGE_H - 13)
        self.set_x(MARGIN)
        self.rule()
        self.set_font(FONT, "I", 7)
        self._muted()
        self.cell(CONTENT_W, 4, "Printable one-page reference · US Letter · ", align="L")
        self.set_font(FONT, "B", 7)
        self._accent()
        self.set_x(MARGIN)
        self.cell(0, 4, self.title, align="R", ln=1)


# ---------------------------------------------------------------------------
# 1. Sales Tracker (improved)
# ---------------------------------------------------------------------------
def sales_tracker():
    p = OnePager("Sales Tracker", "Daily order log — track every sale, fee, and profit at a glance", (16, 92, 120))
    p.header()

    p.field_row("Business / seller name: ____________________________", lines=1, hint="date range: ___/___/___  →  ___/___/___")

    p.section("Order log")
    p.table(
        ["Date", "Order #", "Item / SKU", "Qty", "Price", "Fees", "Ship", "Profit", "Pay"],
        [["", "", "", "", "", "", "", "", ""] for _ in range(9)],
        [20, 20, 44, 12, 19, 17, 17, 19, 23.9],
    )

    p.ln(1)
    p.section("Run summary", fill=(16, 92, 120))
    p.body("Total revenue  $________      Total fees  $________      Total profit  $________\n"
           "Orders  ____      Avg. order value  $________      Profit margin  ______%", size=8.6)

    p.ln(1)
    p.section("Notes")
    p.body("", size=7)
    p.field_row("Best seller this period:", lines=1, hint="repeat your #1 product here")

    p.footer()
    return p


# ---------------------------------------------------------------------------
# 2. Sales Log (A4/A5/Letter) — cleaner grid + status + tax
# ---------------------------------------------------------------------------
def sales_log():
    p = OnePager("Sales Log", "Clean one-page order register with status and tax tracking", (20, 84, 132))
    p.header()
    p.field_row("Seller: ______________________    Log period: ___/___/___  →  ___/___/___", lines=1)
    p.section("Orders")
    p.table(
        ["Date", "Item", "Qty", "Gross", "Tax", "Discount", "Fees", "Net", "Status"],
        [["", "", "", "", "", "", "", "", ""] for _ in range(10)],
        [19, 42, 10, 17, 15, 18, 15, 17, 32.9],
    )
    p.ln(1)
    p.section("Totals")
    p.body("Gross $_______   Tax $_______   Discounts $_______   Fees $_______   Net $_______", size=8.4)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 3. Editable Sales Tracker — monthly summary + payment methods
# ---------------------------------------------------------------------------
def editable_sales_tracker():
    p = OnePager("Editable Sales Tracker", "Type-anywhere sales register with monthly roll-up", (18, 76, 120))
    p.header()
    p.section("Daily sales")
    p.table(
        ["Date", "Order #", "Customer", "Item", "Amount", "Method"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [20, 20, 42, 44, 20, 45.9],
    )
    p.ln(1)
    p.section("Payment method totals")
    p.body("Cash $______     Card $______     Online $______     Other $______     TOTAL $______", size=8.4)
    p.ln(1)
    p.section("Monthly summary")
    p.body("Best day: ______      Best item: ______      Repeat customers: ____      Refunds: ____", size=8.2)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 4. Brand Vision Planner (one page)
# ---------------------------------------------------------------------------
def brand_vision():
    p = OnePager("Brand Vision Planner", "Answer these and you'll know exactly what to build — and why", (150, 78, 40))
    p.header()

    p.section("Purpose", fill=(150, 78, 40))
    p.field_row("1. What problem do we solve, for whom?", lines=1)
    p.field_row("2. Why does our brand exist beyond profit?", lines=1)

    p.section("Identity", fill=(150, 78, 40))
    p.field_row("3. Mission (what we do daily):", lines=1)
    p.field_row("4. Vision — 'where could we be?' (3 yrs):", lines=2)
    p.field_row("5. Core values (top 3):", lines=1)

    p.section("Audience", fill=(150, 78, 40))
    p.field_row("6. Ideal customer (one sentence):", lines=1)
    p.field_row("7. Their #1 pain point:", lines=1)

    p.section("Voice", fill=(150, 78, 40))
    p.checklist(["Friendly", "Authoritative", "Playful", "Minimal", "Bold", "Warm", "Technical", "Luxury"], cols=4)
    p.field_row("8. Tagline (6 words or fewer):", lines=1)

    p.footer()
    return p


# ---------------------------------------------------------------------------
# 5. Mahjong Hand Tracker (one page)
# ---------------------------------------------------------------------------
def mahjong_tracker():
    p = OnePager("Mahjong Hand Tracker", "Track every hand, score, and win across game night", (26, 96, 66))
    p.header()
    p.field_row("Player: ______________________    Date: __________", lines=1)
    p.section("Hands played")
    p.table(
        ["Round", "Hand category", "Points", "Won?", "Notes"],
        [["", "", "", "", ""] for _ in range(12)],
        [22, 66, 20, 18, 65.9],
    )
    p.ln(1)
    p.section("Game total")
    p.body("Total points  ______      Hands won  ____ / ____      Win rate  ______%", size=8.4)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 6. American Mahjong Cheat Sheet
# ---------------------------------------------------------------------------
def mahjong_cheat():
    p = OnePager("American Mahjong Cheat Sheet", "Every rule you need, one clean page", (26, 96, 66))
    p.header()

    p.section("Setup")
    p.body("4 players · 152 tiles · National Mah Jongg League card required · 13 tiles in hand, draw to 14 and discard.", size=8.2)

    p.section("Reading the card")
    p.body("Each line = one winning hand. Category (e.g. 2026, 2468, Consecutive Run) → hand pattern → points.\n"
           "A hand must match a line on the CURRENT year's card to be valid.", size=8.2)

    p.section("The Charleston")
    p.body("First pass: pass 3 tiles right · Second pass: 3 left · Third (optional): 3 across. Then pass 1-2-3 (courtesy).", size=8.2)

    p.section("Jokers & claiming")
    p.body("Jokers substitute for any tile in a hand (never in a pair unless a pair is part of the hand).\n"
           "Call 'Pung'/'Kong'/'Quint' for discards that complete a set; claim with the exact matching set.", size=8.2)

    p.section("Quick rules")
    p.checklist(["Pick & discard", "Expose on claim", "Win by self-draw or discard", "One pair required", "Mah Jongg = highest win"], cols=2)

    p.muted("Reference only — always verify against the current NMJL card and local table rules.")
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 7. American Mahjong Quick Reference
# ---------------------------------------------------------------------------
def mahjong_quick():
    p = OnePager("American Mahjong Quick Reference", "Start-to-finish turn order in 30 seconds", (26, 96, 66))
    p.header()
    p.section("Turn order")
    steps = [
        "1. Draw a tile",
        "2. Check for a winning hand (Mah Jongg)",
        "3. Discard a tile",
        "4. Others may claim (Pung / Kong / Quint)",
        "5. Pass the turn",
    ]
    p.body("\n".join(steps), size=9)

    p.section("Key terms")
    p.table(
        ["Term", "Meaning"],
        [["Mah Jongg", "A complete winning hand"],
         ["Pung", "Three of a kind"],
         ["Kong", "Four of a kind"],
         ["Quint", "Five of a kind (with jokers)"],
         ["Charleston", "Opening tile exchange"],
         ["Joker", "Wildcard for any tile"]],
        [40, 151.9],
    )
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 8. OASIS-E2 Cheat Sheet (home health)
# ---------------------------------------------------------------------------
def oasis_e2():
    p = OnePager("OASIS-E2 Start of Care Cheat Sheet", "Section-by-section SOC documentation checklist", (24, 68, 118))
    p.header()
    p.muted("Clinical quick reference — not a substitute for CMS OASIS-E2 guidance.")
    p.section("Patient / admission")
    p.field_row("Patient: ________________    MRN: ________    SOC date: __________    Clinician: __________", lines=1)

    p.section("SOC documentation checklist")
    p.checklist([
        "Demographics & payer",
        "Admission source & diagnosis",
        "Medications & allergies reconciled",
        "Functional status (M1800s)",
        "Cognitive / sensory status",
        "Skin & integumentary assessment",
        "Falls risk & safety",
        "Care plan & goals",
        "Emergency plan",
        "Clinician & visit schedule",
    ], cols=2)

    p.section("Key timestamps")
    p.body("Assessment window, medication reconciliation, and care-plan signatures documented same visit.", size=8.2)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 9. SBAR Nurse Report Sheet
# ---------------------------------------------------------------------------
def sbar():
    p = OnePager("SBAR Report Sheet", "Hand off cleanly — Situation, Background, Assessment, Recommendation", (30, 72, 122))
    p.header()
    p.field_row("Patient: ______________    Room: ______    Date: __________    Shift: ________", lines=1)

    p.section("S — Situation")
    p.field_row("What is happening right now?", lines=2)

    p.section("B — Background")
    p.field_row("Relevant history / context:", lines=2)

    p.section("A — Assessment")
    p.field_row("What you think is going on:", lines=2)

    p.section("R — Recommendation")
    p.field_row("What you need / suggest next:", lines=2)

    p.section("Vitals / labs")
    p.field_row("HR ____  BP ____  RR ____  SpO2 ____  Temp ____  |  Notable labs:", lines=1)

    p.footer()
    return p


# ---------------------------------------------------------------------------
# 10. Nursing Cheat Sheet (labs + meds + vitals)
# ---------------------------------------------------------------------------
def nursing_cheat():
    p = OnePager("Nursing Quick Reference", "Normal labs, vital signs, and common med classes", (30, 72, 122))
    p.header()
    p.muted("Quick reference only — follow institutional policy and current guidelines.")

    p.section("Adult vital signs")
    p.table(
        ["Sign", "Normal range"],
        [["Heart rate", "60–100 bpm"],
         ["BP", "90/60 – 120/80 mmHg"],
         ["Respirations", "12–20 /min"],
         ["Temperature", "36.1–37.2 °C"],
         ["SpO2", "95–100%"]],
        [80, 111.9],
    )

    p.section("Common lab ranges")
    p.table(
        ["Lab", "Normal"],
        [["Sodium", "135–145 mEq/L"],
         ["Potassium", "3.5–5.0 mEq/L"],
         ["Glucose (fasting)", "70–100 mg/dL"],
         ["Hgb", "12–16 (F) / 14–18 (M) g/dL"],
         ["Creatinine", "0.6–1.2 mg/dL"],
         ["INR (not on AC)", "0.8–1.1"]],
        [70, 121.9],
    )

    p.section("Med classes (key watch points)")
    p.body("Anticoagulants → bleeding · Beta blockers → HR/BP · Insulin → hypoglycemia · "
           "Opioids → respiratory depression · Diuretics → electrolytes.", size=8.0)

    p.footer()
    return p


# ---------------------------------------------------------------------------
# 11. Psychopharmacology Cheat Sheet
# ---------------------------------------------------------------------------
def psychopharm():
    p = OnePager("Psychopharmacology Cheat Sheet", "Major drug classes, examples, and monitoring", (70, 52, 120))
    p.header()
    p.muted("Educational reference — not a prescribing or diagnostic tool.")

    p.section("Antidepressants")
    p.body("SSRI — fluoxetine, sertraline, escitalopram · SNRI — venlafaxine, duloxetine.\nWatch: activation, GI upset, sexual side effects, discontinuation syndrome.", size=8.0)
    p.section("Antipsychotics")
    p.body("Typical — haloperidol · Atypical — risperidone, olanzapine, quetiapine, aripiprazole.\nWatch: EPS, metabolic syndrome, sedation; monitor weight, glucose, lipids.", size=8.0)
    p.section("Mood stabilizers")
    p.body("Lithium (monitor levels + renal/thyroid) · Valproate (LFTs, levels) · Lamotrigine (rash/SJS).", size=8.0)
    p.section("Anxiolytics & stimulants")
    p.body("Benzodiazepines — lorazepam, clonazepam (dependence) · Stimulants — methylphenidate, amphetamines (BP, appetite, misuse).", size=8.0)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 12. Gottman Method Cheat Sheet
# ---------------------------------------------------------------------------
def gottman():
    p = OnePager("Gottman Method Cheat Sheet", "The four horsemen, their antidotes, and the 7 principles", (176, 92, 56))
    p.header()
    p.muted("Therapist / couple reference — adapted from the Gottman Method.")

    p.section("The four horsemen → antidotes")
    p.table(
        ["Horseman", "Antidote"],
        [["Criticism", "Gentle start-up: 'I feel… about…'"],
         ["Contempt", "Build appreciation & respect"],
         ["Defensiveness", "Take responsibility"],
         ["Stonewalling", "Physiological self-soothing + re-engage"]],
        [46, 145.9],
    )

    p.section("The 7 principles (key)")
    p.body("1. Enhance love maps · 2. Nurture fondness & admiration · 3. Turn toward, not away · "
           "4. Accept influence · 5. Solve solvable problems · 6. Manage conflict · 7. Create shared meaning.", size=8.0)

    p.section("Rituals & repair")
    p.checklist(["Daily stress-reducing conversation", "Weekly date", "Repair attempts", "Emotional bank account", "Rituals of connection"], cols=2)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 13. IFS Cheat Sheet
# ---------------------------------------------------------------------------
def ifs_cheat():
    p = OnePager("IFS Cheat Sheet", "The 6 F's, 8 C's, 5 P's, and the unblending path", (120, 88, 66))
    p.header()
    p.muted("Reference for Internal Family Systems work.")

    p.section("The 6 F's (working with a part)")
    p.body("Find → Focus → Flesh out → Feel toward → beFriend → Fears (what would it fear without its role).", size=8.4)

    p.section("The 8 C's of Self")
    p.body("Curiosity · Compassion · Calm · Clarity · Confidence · Courage · Creativity · Connectedness", size=8.4)

    p.section("The 5 P's of Self")
    p.body("Presence · Patience · Perspective · Persistence · Playfulness", size=8.4)

    p.section("Unblending steps")
    p.checklist(["Ask the part to step back", "Ask it to 'separate'", "Notice what shifts", "Check Self-energy", "Return with curiosity"], cols=2)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 14. Piano Chord Chart
# ---------------------------------------------------------------------------
def piano_chords():
    p = OnePager("Piano Chord Chart", "Build any chord from its formula — major, minor, 7th, and more", (96, 60, 140))
    p.header()

    p.section("Chord formulas (semitones from root)")
    p.table(
        ["Chord", "Formula", "Example (C)"],
        [["Major", "0-4-7", "C-E-G"],
         ["Minor", "0-3-7", "C-Eb-G"],
         ["Dominant 7th", "0-4-7-10", "C-E-G-Bb"],
         ["Major 7th", "0-4-7-11", "C-E-G-B"],
         ["Minor 7th", "0-3-7-10", "C-Eb-G-Bb"],
         ["Diminished", "0-3-6", "C-Eb-Gb"],
         ["Augmented", "0-4-8", "C-E-G#"]],
        [44, 42, 105.9],
    )

    p.section("Key signatures")
    p.body("Sharps: G D A E B F# C# · Flats: F Bb Eb Ab Db Gb Cb · Circle of fifths = add one sharp/flat per step.", size=8.0)

    p.section("Inversions")
    p.body("Root (1-3-5) · 1st (3-5-1) · 2nd (5-1-3). Practice each inversion in all 12 keys.", size=8.0)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 15. Customer Order Log
# ---------------------------------------------------------------------------
def customer_order_log():
    p = OnePager("Customer Order Log", "Track orders, customers, and fulfillment status", (18, 84, 110))
    p.header()
    p.field_row("Business: ______________________    Period: ___/___/___  →  ___/___/___", lines=1)
    p.section("Orders")
    p.table(
        ["Order #", "Date", "Customer", "Contact", "Item(s)", "Amount", "Status"],
        [["", "", "", "", "", "", ""] for _ in range(10)],
        [18, 17, 34, 34, 44, 18, 26.9],
    )
    p.ln(1)
    p.section("Status key")
    p.body("P = pending · F = fulfilled · S = shipped · D = delivered · R = refunded", size=7.8)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 16. Egg Production & Sales Tracker
# ---------------------------------------------------------------------------
def egg_tracker():
    p = OnePager("Egg Production & Sales Tracker", "Daily egg counts, sales, and expenses", (168, 106, 32))
    p.header()
    p.field_row("Flock: ______________    Hens: ______    Month: __________", lines=1)

    p.section("Daily production & sales")
    p.table(
        ["Date", "Eggs collected", "Eggs sold", "Income", "Expenses", "Notes"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [22, 30, 24, 24, 24, 67.9],
    )

    p.ln(1)
    p.section("Monthly summary")
    p.body("Total eggs  ______      Dozens  ______      Income $______      Expenses $______      Net $______", size=8.2)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 17. AI Prompt Cheat Sheet (trending +180% YoY)
# ---------------------------------------------------------------------------
def ai_prompt_cheat():
    p = OnePager("AI Prompt Cheat Sheet", "Write prompts that actually work — the formula, patterns, and examples", (90, 50, 140))
    p.header()

    p.section("The 5-part formula")
    p.body("Role + Task + Context + Format + Tone", size=9)
    p.body("\u201cAct as [ROLE]. Do [TASK]. Context: [BACKGROUND]. Format: [STYLE]. Tone: [VOICE].\u201d", size=8.2)
    p.muted("Example: \u201cAct as a senior copywriter. Rewrite this product description. Format: 3 short bullets. Tone: friendly, confident.\u201d")

    p.section("Prompt patterns")
    p.table(
        ["Pattern", "When to use it"],
        [["Act as…", "Give the model a specific role/expertise"],
         ["Chain-of-thought", "\u201cThink step by step\u201d for logic & math"],
         ["Few-shot", "Show 2–3 examples first, then the task"],
         ["Step-by-step", "Force an ordered, repeatable output"],
         ["Refine & iterate", "\u201cImprove this…\u201d / \u201cMake it shorter\u201d"],
         ["Constraints", "Set length, audience, format, do/don't"]],
        [44, 147.9],
    )

    p.section("Power verbs")
    p.checklist(["Summarize", "Explain", "Compare", "Draft", "Rewrite", "Brainstorm",
                 "Translate", "Analyze", "Outline", "Prioritize", "Debug", "Simplify"], cols=4)

    p.section("Quick wins")
    p.body("\u2022 Add \u201cask me questions before you answer\u201d \u00b7 \u2022 \u201cGive 3 options\u201d \u00b7 \u2022 \u201cNo jargon\u201d \u00b7 \u2022 \u201cOutput as a table\u201d", size=8.2)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 18. ADHD Productivity Planner (trending +140% YoY)
# ---------------------------------------------------------------------------
def adhd_daily_planner():
    p = OnePager("ADHD Daily Planner", "One page, low-friction: priorities, time blocks, and a dopamine menu", (220, 90, 60))
    p.header()
    p.field_row("Date: __________    Today's focus word: ____________________", lines=1)

    p.section("Top 3 priorities (do these first)")
    p.field_row("\u2610  1.", lines=1, hint="")
    p.field_row("\u2610  2.", lines=1)
    p.field_row("\u2610  3.", lines=1)

    p.section("Time blocks")
    p.table(
        ["Time", "Plan", "Done"],
        [["", "", ""] for _ in range(8)],
        [24, 128, 39.9],
    )

    p.section("Brain dump")
    p.field_row("Get it out of your head:", lines=2)

    p.section("Distraction parking lot")
    p.field_row("Park it, come back later:", lines=1)

    p.section("Dopamine menu (5-min resets)")
    p.checklist(["Walk", "Water", "Stretch", "Music", "Sunlight", "Deep breaths"], cols=3)

    p.section("End of day")
    p.field_row("What got done: ________________________________    Wins to celebrate: ____________________", lines=1)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 19. Budget Tracker (trending, financial anxiety)
# ---------------------------------------------------------------------------
def budget_tracker():
    p = OnePager("Budget Tracker", "Income, expenses, and the 50/30/20 rule in one pass", (20, 100, 80))
    p.header()
    p.field_row("Month: __________    Take-home pay: $____________", lines=1)

    p.section("Income")
    p.field_row("Paycheck $______    Side income $______    Other $______    TOTAL $______", lines=1)

    p.section("Expenses")
    p.table(
        ["Category", "Budget", "Actual", "Difference"],
        [["Housing", "", "", ""],
         ["Groceries", "", "", ""],
         ["Transport", "", "", ""],
         ["Utilities", "", "", ""],
         ["Insurance", "", "", ""],
         ["Debt payments", "", "", ""],
         ["Subscriptions", "", "", ""],
         ["Fun / dining", "", "", ""],
         ["Savings", "", "", ""],
         ["Other", "", "", ""]],
        [70, 40.6, 40.6, 40.6],
    )

    p.section("The 50/30/20 rule")
    p.body("50% needs · 30% wants · 20% savings/debt. My split: ___% / ___% / ___%", size=8.4)
    p.section("Savings goal")
    p.field_row("This month I'm saving $______ toward: ________________________", lines=1)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 20. Habit Tracker (steady high demand)
# ---------------------------------------------------------------------------
def habit_tracker():
    p = OnePager("Habit Tracker", "Five-week grid with streaks — build habits that stick", (40, 120, 140))
    p.header()
    p.field_row("Month: __________    Focus habit: ________________________", lines=1)

    p.section("Weekly grid (mark X or \u2713 per day)")
    p.table(
        ["Habit", "Wk 1", "Wk 2", "Wk 3", "Wk 4", "Wk 5", "Streak"],
        [["", "", "", "", "", "", ""] for _ in range(14)],
        [66, 18, 18, 18, 18, 18, 35.9],
    )

    p.section("Why & reward")
    p.field_row("Why this matters: ____________________________________________________", lines=1)
    p.field_row("Reward at 7 days: ________________    Reward at 30 days: ________________", lines=1)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 21. Daily Affirmations (trending wellness)
# ---------------------------------------------------------------------------
def affirmations():
    p = OnePager("Daily Affirmations", "Morning and evening statements — plus space for your own", (200, 90, 150))
    p.header()
    p.muted("Say them out loud, in the mirror, once a day. Repetition rewires the habit.")

    p.section("Morning affirmations")
    p.checklist(["I am capable of handling today", "I choose progress over perfection",
                 "I am worthy of good things", "I release what I can't control",
                 "I start with one small step", "My best is enough today"], cols=2)

    p.section("Evening affirmations")
    p.checklist(["I did something good today", "I forgive myself for what's undone",
                 "Rest is productive", "I am learning, not failing"], cols=2)

    p.section("Write your own")
    p.field_row("1. I am ______________________________________________________", lines=1)
    p.field_row("2. I am ______________________________________________________", lines=1)
    p.field_row("3. I am ______________________________________________________", lines=1)

    p.section("Today's intention")
    p.field_row("Today I will feel good by: ______________________________", lines=1)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 22. Grief Journaling Prompts (trending +90% YoY)
# ---------------------------------------------------------------------------
def grief_prompts():
    p = OnePager("Grief Journaling Prompts", "Gentle prompts to help you feel, remember, and heal", (90, 90, 120))
    p.header()
    p.muted("There is no right way to grieve. Write what you can, skip what you can't.")

    p.section("Feel it")
    p.field_row("1. Right now, I feel\u2026", lines=1)
    p.field_row("2. The hardest part of today was\u2026", lines=1)
    p.field_row("3. Something I'm carrying that I can set down\u2026", lines=1)

    p.section("Remember")
    p.field_row("4. A memory that makes me smile\u2026", lines=1)
    p.field_row("5. Something they taught me\u2026", lines=1)
    p.field_row("6. What I wish I could tell them today\u2026", lines=1)

    p.section("Heal")
    p.field_row("7. One kind thing I can do for myself today\u2026", lines=1)
    p.field_row("8. What I need from others right now\u2026", lines=1)

    p.section("Self-care check-in")
    p.checklist(["Ate a meal", "Drank water", "Slept", "Talked to someone", "Went outside", "Asked for help"], cols=3)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 23. DBT Skills Cheat Sheet (therapy worksheets +75%)
# ---------------------------------------------------------------------------
def dbt_skills():
    p = OnePager("DBT Skills Cheat Sheet", "Distress tolerance, emotion regulation, and interpersonal skills", (140, 60, 120))
    p.header()
    p.muted("Reference only — work with a qualified therapist for personalized care.")

    p.section("Distress tolerance — TIPP")
    p.body("Temperature (cold water) \u00b7 Intense exercise \u00b7 Paced breathing \u00b7 Paired muscle relaxation.", size=8.2)

    p.section("STOP (before reacting)")
    p.body("Stop \u00b7 Take a step back \u00b7 Observe \u00b7 Proceed mindfully.", size=8.2)

    p.section("Emotion regulation — ABC PLEASE")
    p.body("Accumulate positives \u00b7 Build mastery \u00b7 Cope ahead \u00b7 treat PhysicaL illness \u00b7 Eat balanced \u00b7 Avoid mood-altering drugs \u00b7 Sleep \u00b7 Exercise.", size=8.0)

    p.section("Interpersonal — DEAR MAN")
    p.body("Describe \u00b7 Express \u00b7 Assert \u00b7 Reinforce \u00b7 stay Mindful \u00b7 Appear confident \u00b7 Negotiate.", size=8.2)

    p.section("Mindfulness — WHAT & HOW")
    p.body("WHAT: Observe \u00b7 Describe \u00b7 Participate.   HOW: Non-judgmentally \u00b7 One-mindfully \u00b7 Effectively.", size=8.2)

    p.section("Grounding (5-4-3-2-1)")
    p.body("5 things you see \u00b7 4 you feel \u00b7 3 you hear \u00b7 2 you smell \u00b7 1 you taste.", size=8.2)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 24. Blood Pressure & Glucose Log (high-volume medical)
# ---------------------------------------------------------------------------
def blood_pressure_log():
    p = OnePager("Blood Pressure & Glucose Log", "Daily readings with target ranges", (180, 60, 60))
    p.header()
    p.field_row("Name: ______________________    Date range: ___/___/___  \u2192  ___/___/___", lines=1)

    p.section("Daily readings")
    p.table(
        ["Date", "Time", "Sys/Dia", "Pulse", "Glucose", "Notes"],
        [["", "", "", "", "", ""] for _ in range(14)],
        [24, 20, 34, 20, 26, 67.9],
    )

    p.section("Targets (per your provider)")
    p.body("BP target: ______/______ mmHg      Fasting glucose: ______ mg/dL      Post-meal: ______ mg/dL", size=8.2)
    p.muted("Share this log at your next appointment.")
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 25. Medication Log (high-volume medical)
# ---------------------------------------------------------------------------
def medication_log():
    p = OnePager("Medication Log", "Track every med, dose, and refill", (40, 90, 160))
    p.header()
    p.field_row("Name: ______________________    Allergies: ______________________________", lines=1)

    p.section("Medications")
    p.table(
        ["Medication", "Dose", "Frequency", "Time(s)", "Refill due", "Notes"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [46, 24, 34, 26, 28, 33.9],
    )

    p.section("Pharmacy & reminders")
    p.field_row("Pharmacy: ____________________    Phone: ________________    Next pickup: __________", lines=1)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 26. Password & Account Log (evergreen)
# ---------------------------------------------------------------------------
def password_log():
    p = OnePager("Password & Account Log", "Keep every login in one secure place", (60, 70, 90))
    p.header()
    p.muted("Keep this page private. Consider a password manager for better security.")

    p.section("Accounts")
    p.table(
        ["Site / App", "Username", "Email", "Password", "Security Q", "Notes"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [42, 34, 42, 34, 30, 9.9],
    )

    p.section("Updates")
    p.body("Password changed: ________    Last review: ________    Two-factor on: \u2610", size=8.0)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 27. Travel Packing List (evergreen)
# ---------------------------------------------------------------------------
def packing_list():
    p = OnePager("Travel Packing List", "Pack by category and never forget the essentials", (30, 130, 120))
    p.header()
    p.field_row("Trip: ______________________    Dates: ___/___/___  \u2192  ___/___/___", lines=1)

    p.section("Clothing")
    p.checklist(["Underwear", "Socks", "Shirts", "Pants", "Sweater/jacket", "Sleepwear", "Shoes", "Swimwear"], cols=2)
    p.section("Toiletries")
    p.checklist(["Toothbrush/paste", "Deodorant", "Shampoo/soap", "Skincare", "Medications", "Razor"], cols=2)
    p.section("Tech & documents")
    p.checklist(["Phone + charger", "Power bank", "Adapter", "ID/passport", "Tickets", "Wallet/cards", "Keys"], cols=2)
    p.section("Last-minute check")
    p.checklist(["Snacks", "Water bottle", "Headphones", "Book", "Umbrella", "Reusable bag"], cols=3)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 28. Weekly Chore Chart (evergreen / back-to-school)
# ---------------------------------------------------------------------------
def chore_chart():
    p = OnePager("Weekly Chore Chart", "Assign chores and check them off, day by day", (200, 120, 40))
    p.header()
    p.field_row("Week of: __________    People: ______________________________", lines=1)

    p.section("Chores")
    p.table(
        ["Chore", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        [["", "", "", "", "", "", "", ""] for _ in range(10)],
        [68, 15.1, 15.1, 15.1, 15.1, 15.1, 15.1, 15.1],
    )

    p.section("Rewards")
    p.body("Weekly reward: ______________________    Bonus: ______________________", size=8.2)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 29. Reading Log (evergreen)
# ---------------------------------------------------------------------------
def reading_log():
    p = OnePager("Reading Log", "Every book you finish — title, rating, and a one-line takeaway", (120, 80, 160))
    p.header()
    p.field_row("Year: __________    Goal: ______ books", lines=1)

    p.section("Books")
    p.table(
        ["Book", "Author", "Started", "Finished", "Rating", "One-line note"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [44, 38, 20, 20, 18, 51.9],
    )

    p.section("This month's favorite")
    p.field_row("____________________________________ because ____________________________________", lines=1)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 30. Appointment Tracker (evergreen)
# ---------------------------------------------------------------------------
def appointment_tracker():
    p = OnePager("Appointment Tracker", "Every appointment in one place, with reminders", (30, 110, 180))
    p.header()
    p.field_row("Name: ______________________    Reminders: 1 day before \u2610   1 hour before \u2610", lines=1)

    p.section("Appointments")
    p.table(
        ["Date", "Time", "Who / What", "Location", "Purpose", "Notes"],
        [["", "", "", "", "", ""] for _ in range(13)],
        [22, 18, 46, 40, 40, 25.9],
    )

    p.footer()
    return p


# ---------------------------------------------------------------------------
# 31. Meal Planner + Grocery List (evergreen)
# ---------------------------------------------------------------------------
def meal_planner():
    p = OnePager("Meal Planner & Grocery List", "Plan the week, then shop once", (160, 90, 40))
    p.header()
    p.field_row("Week of: __________", lines=1)

    p.section("Meals")
    p.table(
        ["Day", "Breakfast", "Lunch", "Dinner", "Snacks"],
        [["Mon", "", "", "", ""],
         ["Tue", "", "", "", ""],
         ["Wed", "", "", "", ""],
         ["Thu", "", "", "", ""],
         ["Fri", "", "", "", ""],
         ["Sat", "", "", "", ""],
         ["Sun", "", "", "", ""]],
        [20, 43, 43, 43, 42.9],
    )

    p.section("Grocery list")
    p.checklist(["", "", "", "", "", "", "", ""], cols=2)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# 32. SMART Goal Planner (evergreen)
# ---------------------------------------------------------------------------
def goal_planner():
    p = OnePager("SMART Goal Planner", "Turn one goal into a plan you'll actually follow", (20, 130, 90))
    p.header()
    p.field_row("Goal: ________________________________________________________________", lines=1)

    p.section("Make it SMART")
    p.field_row("S — Specific (what exactly?):", lines=1)
    p.field_row("M — Measurable (how will you know?):", lines=1)
    p.field_row("A — Achievable (is it realistic?):", lines=1)
    p.field_row("R — Relevant (why now?):", lines=1)
    p.field_row("T — Time-bound (by when?):", lines=1)

    p.section("Action steps")
    p.field_row("1. First step (next 24 hrs):", lines=1)
    p.field_row("2. This week:", lines=1)
    p.field_row("3. This month:", lines=1)

    p.section("Milestones & review")
    p.field_row("Milestone 1 (by ______): ______________    Milestone 2 (by ______): ______________", lines=1)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# Batch 3 — trending on TikTok / Reddit / Pinterest / X / YouTube (2026)
# ---------------------------------------------------------------------------

# 33. Social Media Content Calendar
def content_calendar():
    p = OnePager("Content Calendar", "Plan a week of posts across every platform", (200, 60, 100))
    p.header()
    p.field_row("Week of: __________    Focus / campaign: ______________________________", lines=1)

    p.section("Posts")
    p.table(
        ["Day", "Platform", "Topic / hook", "Format", "Status"],
        [["Mon", "", "", "", ""],
         ["Tue", "", "", "", ""],
         ["Wed", "", "", "", ""],
         ["Thu", "", "", "", ""],
         ["Fri", "", "", "", ""],
         ["Sat", "", "", "", ""],
         ["Sun", "", "", "", ""]],
        [18, 34, 60, 40, 39.9],
    )

    p.section("Posting checklist")
    p.checklist(["Hook in first 2s", "Caption + hashtags", "CTA (call to action)", "Reply to comments", "Trending audio/format"], cols=2)
    p.footer()
    return p


# 34. Faceless Reel / Video Idea Planner
def reel_ideas():
    p = OnePager("Faceless Reel Ideas", "Hook → script → b-roll, planned out before you film", (220, 50, 90))
    p.header()
    p.muted("Faceless = no face on camera. Use b-roll, text, and voiceover.")

    p.section("Reel plan")
    p.table(
        ["#", "Hook (first 2s)", "Script / beats", "B-roll / text", "Audio"],
        [["", "", "", "", ""] for _ in range(8)],
        [10, 46, 52, 46, 37.9],
    )

    p.section("Viral formats to try")
    p.checklist(["Listicle (3 tips)", "Before / after", "POV", "Myth vs fact", "Day in the life", "Reaction", "Storytime", "How-to"], cols=4)
    p.footer()
    return p


# 35. Hashtag & Caption Planner
def hashtag_caption_planner():
    p = OnePager("Hashtag & Caption Planner", "Captions and hashtags ready for every post", (180, 60, 130))
    p.header()
    p.field_row("Niche: ______________________    Best posting times: ____________________", lines=1)

    p.section("Caption bank")
    p.field_row("Caption 1:", lines=1)
    p.field_row("Caption 2:", lines=1)
    p.field_row("Caption 3:", lines=1)
    p.field_row("Caption 4:", lines=1)

    p.section("Hashtag sets (mix 3 sizes: big / mid / niche)")
    p.field_row("Set A — 30 total:", lines=2)
    p.field_row("Set B — 30 total:", lines=2)
    p.field_row("Set C — 30 total:", lines=2)
    p.footer()
    return p


# 36. Batch Content Planner
def content_batch_planner():
    p = OnePager("Batch Content Planner", "Film / write once, publish all month", (150, 60, 140))
    p.header()
    p.field_row("Batch session date: __________    Goal: ______ posts this month", lines=1)

    p.section("Ideas backlog")
    p.field_row("1.", lines=1)
    p.field_row("2.", lines=1)
    p.field_row("3.", lines=1)
    p.field_row("4.", lines=1)

    p.section("This batch (write → record → edit → schedule)")
    p.table(
        ["Idea", "Outline", "Record", "Edit", "Schedule"],
        [["", "", "", "", ""] for _ in range(6)],
        [44, 52, 28, 28, 39.9],
    )

    p.section("Batch workflow")
    p.checklist(["Outline all first", "Record in one sitting", "Edit in one block", "Schedule + captions", "Analyze top performer"], cols=2)
    p.footer()
    return p


# 37. Pinterest Pin Planner
def pinterest_pin_planner():
    p = OnePager("Pinterest Pin Planner", "Keywords, boards, and pin ideas that get saved", (190, 40, 60))
    p.header()
    p.field_row("Profile focus: ______________________    Keyword pillars: ____________________", lines=1)

    p.section("Pin ideas")
    p.table(
        ["Pin idea", "Keywords", "Board", "Link to", "Done"],
        [["", "", "", "", ""] for _ in range(9)],
        [56, 40, 40, 40, 15.9],
    )

    p.section("Pin checklist")
    p.checklist(["Vertical 2:3 image", "Clear text overlay", "Keyword-rich title", "Description + 3 keywords", "Pin to 2+ boards", "Fresh pin weekly"], cols=2)
    p.footer()
    return p


# 38. Job Application Tracker
def job_tracker():
    p = OnePager("Job Application Tracker", "Every application, status, and follow-up in one place", (20, 90, 140))
    p.header()
    p.field_row("Target role: ______________________    Salary range: $______ – $______", lines=1)

    p.section("Applications")
    p.table(
        ["Company", "Role", "Date", "Status", "Contact", "Next step"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [38, 36, 18, 26, 38, 35.9],
    )

    p.section("Status key")
    p.body("Applied · Interview · Offer · Rejected · Ghosted → follow up after 5–7 days", size=7.8)
    p.footer()
    return p


# 39. Resume Cheat Sheet
def resume_cheat():
    p = OnePager("Resume Cheat Sheet", "Structure, action verbs, and ATS keywords", (20, 100, 150))
    p.header()
    p.muted("One page. Impact first. Tailor keywords to each job posting.")

    p.section("Resume skeleton")
    p.body("Name + title · Contact (phone, email, LinkedIn) · Summary (2 lines) · Skills · Experience (reverse-chronological) · Education · Certifications.", size=8.2)

    p.section("Power action verbs")
    p.checklist(["Led", "Built", "Launched", "Grew", "Reduced", "Automated", "Negotiated", "Designed", "Analyzed", "Delivered", "Mentored", "Optimized"], cols=4)

    p.section("Quantify impact")
    p.body("Use numbers: \u201cincreased X by Y%\u201d, \u201csaved $Z\u201d, \u201cmanaged N people\u201d. Match the job's keywords for ATS filters.", size=8.2)

    p.section("Common mistakes")
    p.checklist(["Over 1 page", "Vague (no numbers)", "Typos", "Photo (US)", "Generic objective", "One resume for all jobs"], cols=2)
    p.footer()
    return p


# 40. Interview Prep (STAR)
def interview_prep():
    p = OnePager("Interview Prep Sheet", "Research, STAR stories, and questions to ask", (25, 110, 160))
    p.header()
    p.field_row("Company: ______________________    Role: ______________________    Date: __________", lines=1)

    p.section("Research (know these)")
    p.field_row("What they do / who they serve:", lines=1)
    p.field_row("Recent news / product:", lines=1)
    p.field_row("Why I want this role:", lines=1)

    p.section("STAR stories (Situation · Task · Action · Result)")
    p.field_row("Story 1 — Leadership:", lines=2)
    p.field_row("Story 2 — Problem solved:", lines=2)
    p.field_row("Story 3 — Failure & lesson:", lines=2)

    p.section("Questions to ask them")
    p.field_row("1. ____________________   2. ____________________   3. ____________________", lines=1)
    p.footer()
    return p


# 41. Kids Bedtime Routine
def bedtime_routine():
    p = OnePager("Bedtime Routine Chart", "A calm, consistent wind-down your kids can follow", (120, 90, 160))
    p.header()
    p.field_row("Child: ______________________    Bedtime: ______", lines=1)

    p.section("Evening routine")
    p.checklist(["Bath / wash up", "Pajamas", "Brush teeth", "Pick tomorrow's clothes",
                 "One last drink of water", "Story or quiet reading", "Lights out", "Sleep"], cols=2)

    p.section("Weekly star chart")
    p.table(
        ["Day", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        [["Stars", "", "", "", "", "", "", ""]],
        [22, 24.3, 24.3, 24.3, 24.3, 24.3, 24.3, 24.3],
    )

    p.section("Reward")
    p.body("Reward at ___ stars: ______________________", size=8.4)
    p.footer()
    return p


# 42. Screen Time Tracker
def screen_time_tracker():
    p = OnePager("Screen Time Tracker", "Balance screen time with other activities", (90, 90, 170))
    p.header()
    p.field_row("Child: ______________________    Daily limit: ______ hrs", lines=1)

    p.section("Daily log")
    p.table(
        ["Day", "Time on", "App / activity", "Earned how?", "Notes"],
        [["", "", "", "", ""] for _ in range(12)],
        [22, 22, 46, 46, 55.9],
    )

    p.section("Earn screen time")
    p.checklist(["Homework done", "Chores done", "Outside time", "Reading time", "Kind to siblings"], cols=2)
    p.footer()
    return p


# 43. Behavior / Reward Chart
def behavior_chart():
    p = OnePager("Behavior Chart", "Track good choices and celebrate wins", (200, 110, 50))
    p.header()
    p.field_row("Child: ______________________    Week of: __________    Goal: ________________", lines=1)

    p.section("Daily goals")
    p.table(
        ["Goal / behavior", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        [["", "", "", "", "", "", "", ""] for _ in range(7)],
        [68, 15.1, 15.1, 15.1, 15.1, 15.1, 15.1, 15.1],
    )

    p.section("Rewards menu")
    p.checklist(["Pick a treat", "Extra playtime", "Choose dinner", "Family movie", "Small toy", "Special outing"], cols=3)
    p.footer()
    return p


# 44. School Lunchbox Planner
def lunchbox_planner():
    p = OnePager("Lunchbox Planner", "Pack balanced lunches without the daily scramble", (210, 130, 40))
    p.header()
    p.field_row("Week of: __________    Food allergies: ______________________________", lines=1)

    p.section("Lunch plan")
    p.table(
        ["Day", "Main", "Fruit/Veg", "Snack", "Drink"],
        [["Mon", "", "", "", ""],
         ["Tue", "", "", "", ""],
         ["Wed", "", "", "", ""],
         ["Thu", "", "", "", ""],
         ["Fri", "", "", "", ""]],
        [18, 48, 42, 42, 41.9],
    )

    p.section("Quick ideas")
    p.checklist(["Wrap / sandwich", "Pasta salad", "Quesadilla", "Soup + crackers", "Leftovers", "Veggies + dip", "Fruit cup", "Yogurt"], cols=2)
    p.footer()
    return p


# 45. Kids Morning Routine
def morning_routine_kids():
    p = OnePager("Morning Routine Chart", "A no-nag morning checklist kids can own", (220, 120, 60))
    p.header()
    p.field_row("Child: ______________________    Leave by: ______", lines=1)

    p.section("Morning checklist")
    p.checklist(["Wake up", "Make bed", "Get dressed", "Brush teeth", "Brush hair",
                 "Breakfast", "Pack backpack", "Shoes on", "Lunch/water", "Out the door"], cols=2)

    p.section("Backpack checklist")
    p.checklist(["Homework", "Lunch", "Water bottle", "Library book", "PE clothes", "Signed forms"], cols=2)

    p.section("Morning wins")
    p.field_row("Stickers earned this week: ________    Reward: ____________________", lines=1)
    p.footer()
    return p


# 46. Daily Prayer Journal
def prayer_journal():
    p = OnePager("Prayer Journal", "One page to pray, give thanks, and listen", (120, 80, 50))
    p.header()
    p.field_row("Date: __________    Verse of the day: ______________________________", lines=1)

    p.section("Gratitude")
    p.field_row("Today I'm thankful for:", lines=2)

    p.section("Prayer requests")
    p.field_row("For myself:", lines=2)
    p.field_row("For others:", lines=2)

    p.section("Listen / reflect")
    p.field_row("What I sense God is saying:", lines=2)

    p.section("Answer log")
    p.field_row("Answered prayers to remember:", lines=2)
    p.footer()
    return p


# 47. Bible Study Page
def scripture_study():
    p = OnePager("Bible Study Page", "Read, observe, and apply any passage", (130, 90, 60))
    p.header()
    p.field_row("Passage: ______________________    Date: __________", lines=1)

    p.section("Observe")
    p.field_row("Key words / repeated ideas:", lines=2)
    p.field_row("Who, what, when, where:", lines=2)

    p.section("Understand")
    p.field_row("What does this say about God / people?", lines=2)

    p.section("Apply")
    p.field_row("One thing I'll do this week:", lines=2)

    p.section("Pray")
    p.field_row("My prayer from this passage:", lines=2)
    p.footer()
    return p


# 48. Daily Devotional Planner
def devotional_planner():
    p = OnePager("Daily Devotional Planner", "A week of quiet time, planned", (110, 80, 70))
    p.header()
    p.field_row("Week of: __________    Focus: ______________________________", lines=1)

    p.section("Quiet time plan")
    p.table(
        ["Day", "Scripture", "Devotional", "Prayer", "Takeaway"],
        [["Mon", "", "", "", ""],
         ["Tue", "", "", "", ""],
         ["Wed", "", "", "", ""],
         ["Thu", "", "", "", ""],
         ["Fri", "", "", "", ""],
         ["Sat", "", "", "", ""],
         ["Sun", "", "", "", ""]],
        [18, 42, 46, 40, 45.9],
    )

    p.footer()
    return p


# 49. Workout Log
def workout_log():
    p = OnePager("Workout Log", "Exercises, sets, reps, and progress", (30, 120, 110))
    p.header()
    p.field_row("Goal: ______________________    Week of: __________", lines=1)

    p.section("Workouts")
    p.table(
        ["Day", "Exercise", "Sets × Reps", "Weight", "Notes"],
        [["", "", "", "", ""] for _ in range(12)],
        [22, 56, 34, 28, 51.9],
    )

    p.section("Progress")
    p.field_row("This week: Weight ______    Cardio ______ min    PRs: ____________________", lines=1)
    p.footer()
    return p


# 50. Macro / Calorie Tracker
def macro_tracker():
    p = OnePager("Macro Tracker", "Hit your protein, carbs, and fat targets daily", (20, 130, 100))
    p.header()
    p.field_row("Daily targets: ______ kcal    Protein ______g    Carbs ______g    Fat ______g", lines=1)

    p.section("Daily food log")
    p.table(
        ["Meal", "Food", "Cal", "Protein", "Carbs", "Fat"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [20, 60, 20, 24, 20, 47.9],
    )

    p.section("Daily totals")
    p.body("Calories ______ / ______    Protein ______g    Carbs ______g    Fat ______g    Water ______ cups", size=8.2)
    p.footer()
    return p


# 51. Symptom Tracker (chronic illness)
def symptom_tracker():
    p = OnePager("Symptom Tracker", "Track symptoms, triggers, and patterns for your doctor", (170, 60, 60))
    p.header()
    p.field_row("Name: ______________________    Date range: ___/___/___  →  ___/___/___", lines=1)

    p.section("Daily log")
    p.table(
        ["Date", "Symptom", "Severity (1-10)", "Trigger", "Med / relief", "Notes"],
        [["", "", "", "", "", ""] for _ in range(13)],
        [22, 42, 24, 32, 34, 37.9],
    )

    p.section("To share with your doctor")
    p.field_row("Pattern I've noticed: ______________________________    Questions: ____________________", lines=1)
    p.footer()
    return p


# 52. Sleep Log
def sleep_log():
    p = OnePager("Sleep Log", "Bedtime, wake time, and what affected your rest", (50, 60, 130))
    p.header()
    p.field_row("Week of: __________    Sleep goal: ______ hrs/night", lines=1)

    p.section("Nightly log")
    p.table(
        ["Day", "Bed time", "Wake time", "Hours", "Quality", "Caffeine/notes"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [22, 28, 28, 20, 24, 69.9],
    )

    p.section("Weekly summary")
    p.body("Avg hours: ______    Best night: ______    Pattern to fix: ____________________", size=8.2)
    p.footer()
    return p


# 53. Period Tracker
def period_tracker():
    p = OnePager("Period & Cycle Tracker", "Track your cycle, symptoms, and moods", (200, 70, 130))
    p.header()
    p.field_row("Month: __________    Cycle length: ______ days    Period length: ______ days", lines=1)

    p.section("Daily log")
    p.table(
        ["Day", "Flow", "Symptoms", "Mood", "Notes"],
        [["", "", "", "", ""] for _ in range(14)],
        [18, 26, 60, 40, 47.9],
    )

    p.section("Cycle notes")
    p.field_row("Ovulation (approx): __________    Next period due: __________    Symptoms to mention: ____________", lines=1)
    p.footer()
    return p


# 54. Cleaning Checklist
def cleaning_checklist():
    p = OnePager("Cleaning Checklist", "Daily, weekly, and monthly cleaning in one pass", (40, 130, 150))
    p.header()

    p.section("Daily")
    p.checklist(["Make beds", "Wipe kitchen counters", "Do dishes", "Quick sweep", "10-min tidy"], cols=2)
    p.section("Weekly")
    p.checklist(["Vacuum floors", "Mop", "Bathrooms", "Dust", "Laundry", "Change sheets", "Take out trash"], cols=2)
    p.section("Monthly")
    p.checklist(["Fridge purge", "Windows", "Baseboards", "Fans/vents", "Oven/microwave", "Declutter one area"], cols=2)
    p.section("Rotation")
    p.field_row("This week's deep-clean zone: ______________________________", lines=1)
    p.footer()
    return p


# 55. 30-Day Declutter Challenge
def declutter_challenge():
    p = OnePager("30-Day Declutter Challenge", "One small area a day — a calmer home in a month", (20, 120, 130))
    p.header()
    p.muted("Rule: if it's not used, loved, or needed — donate, sell, or toss it.")

    p.section("Day-by-day")
    p.table(
        ["Day", "Area", "Done", "Day", "Area", "Done"],
        [["1", "Junk drawer", "", "16", "Shoes", ""],
         ["2", "Nightstand", "", "17", "Coats", ""],
         ["3", "Bathroom cabinet", "", "18", "Under bed", ""],
         ["4", "Makeup / toiletries", "", "19", "Books", ""],
         ["5", "Fridge + pantry", "", "20", "Desk drawer", ""],
         ["6", "Kitchen counters", "", "21", "Cords / chargers", ""],
         ["7", "Tupperware", "", "22", "Craft supplies", ""],
         ["8", "Closet — tops", "", "23", "Garage / entry", ""],
         ["9", "Closet — bottoms", "", "24", "Car", ""],
         ["10", "Sock drawer", "", "25", "Photos (digital)", ""],
         ["11", "Living room", "", "26", "Email inbox", ""],
         ["12", "Papers / mail", "", "27", "Phone apps", ""],
         ["13", "Kids' toys", "", "28", "Linens", ""],
         ["14", "Kitchen gadgets", "", "29", "Seasonal decor", ""],
         ["15", "Accessories", "", "30", "Celebrate! ★", ""]],
        [10, 56, 16, 10, 56, 43.9],
    )
    p.footer()
    return p


# 56. Pantry & Freezer Inventory
def pantry_inventory():
    p = OnePager("Pantry & Freezer Inventory", "Know what you have so you stop overbuying", (150, 100, 40))
    p.header()
    p.field_row("Last updated: __________", lines=1)

    p.section("Pantry")
    p.table(
        ["Item", "Qty", "Use by", "Item", "Qty", "Use by"],
        [["", "", "", "", "", ""] for _ in range(10)],
        [44, 16, 34, 44, 16, 37.9],
    )

    p.section("Freezer")
    p.table(
        ["Item", "Qty", "Use by", "Item", "Qty", "Use by"],
        [["", "", "", "", "", ""] for _ in range(6)],
        [44, 16, 34, 44, 16, 37.9],
    )
    p.footer()
    return p


# 57. Subscription Tracker
def subscription_tracker():
    p = OnePager("Subscription Tracker", "Cancel the ones you forgot — keep what's worth it", (120, 90, 40))
    p.header()
    p.field_row("Monthly subscription budget: $______", lines=1)

    p.section("Subscriptions")
    p.table(
        ["Service", "Cost", "Billing date", "Worth it?", "Cancel?"],
        [["", "", "", "", ""] for _ in range(12)],
        [46, 24, 34, 26, 61.9],
    )

    p.section("Monthly total")
    p.body("Total $______ / budget $______    To cancel: ______________________    To keep: ______________________", size=8.0)
    p.footer()
    return p


# 58. Wedding Budget Tracker
def wedding_budget():
    p = OnePager("Wedding Budget Tracker", "Every vendor and cost, tracked against your total", (150, 60, 110))
    p.header()
    p.field_row("Total budget: $__________    Date: __________    Guests: ______", lines=1)

    p.section("Spending")
    p.table(
        ["Category", "Budget", "Actual", "Deposit", "Paid?"],
        [["Venue", "", "", "", ""],
         ["Catering", "", "", "", ""],
         ["Photography", "", "", "", ""],
         ["Attire", "", "", "", ""],
         ["Flowers", "", "", "", ""],
         ["Music / DJ", "", "", "", ""],
         ["Cake", "", "", "", ""],
         ["Rings", "", "", "", ""],
         ["Invitations", "", "", "", ""],
         ["Other", "", "", "", ""]],
        [64, 30, 30, 30, 37.9],
    )

    p.section("Totals")
    p.body("Spent $______    Remaining $______    Over/under $______", size=8.4)
    p.footer()
    return p


# 59. Wedding Planning Checklist
def wedding_checklist():
    p = OnePager("Wedding Planning Checklist", "From engagement to honeymoon, in order", (160, 70, 120))
    p.header()

    p.section("First steps")
    p.checklist(["Set budget", "Pick date", "Guest list", "Book venue", "Choose wedding party"], cols=2)
    p.section("Big vendors")
    p.checklist(["Photographer", "Caterer", "DJ / band", "Florist", "Officiant", "Cake baker"], cols=2)
    p.section("Details")
    p.checklist(["Dress / attire", "Invitations", "Registry", "Rings", "Hair & makeup", "Decor", "Seating chart", "Transport"], cols=2)
    p.section("Final weeks")
    p.checklist(["Marriage license", "Final vendor confirmations", "Timeline to vendors", "Pack for honeymoon", "Tip envelopes"], cols=2)
    p.footer()
    return p


# 60. Guest List Tracker
def guest_list():
    p = OnePager("Guest List Tracker", "Names, RSVPs, meals, and gifts in one place", (140, 60, 100))
    p.header()
    p.field_row("Event: ______________________    Date: __________    Target count: ______", lines=1)

    p.section("Guests")
    p.table(
        ["Name", "Invited", "RSVP", "Meal", "Gift", "Thank-you sent"],
        [["", "", "", "", "", ""] for _ in range(13)],
        [44, 22, 22, 34, 34, 35.9],
    )

    p.footer()
    return p


# 61. Pet Care & Health Log
def pet_care_log():
    p = OnePager("Pet Care & Health Log", "Feed, meds, weight, and vet visits", (90, 110, 40))
    p.header()
    p.field_row("Pet: ______________    Breed: ____________    Weight: ______    Vet: ____________", lines=1)

    p.section("Daily care")
    p.table(
        ["Date", "Food", "Meds", "Walk / play", "Notes"],
        [["", "", "", "", ""] for _ in range(10)],
        [22, 44, 40, 40, 45.9],
    )

    p.section("Vet visits & vaccines")
    p.table(
        ["Date", "Visit", "Vaccine / treatment", "Next due"],
        [["", "", "", ""] for _ in range(4)],
        [24, 52, 62, 53.9],
    )
    p.footer()
    return p


# 62. Pet Sitter Info Sheet
def pet_sitter_info():
    p = OnePager("Pet Sitter Info Sheet", "Everything your sitter needs, one clear page", (100, 120, 50))
    p.header()
    p.field_row("Pet(s): ______________________    Emergency contact: ____________________", lines=1)

    p.section("Feeding")
    p.field_row("Food + amount + time:", lines=2)

    p.section("Meds")
    p.field_row("Medication + dose + time:", lines=2)

    p.section("Routine & rules")
    p.checklist(["Walks: ______ times/day", "Crate at night", "Allowed on furniture", "Doorbell behavior", "Special treats ok"], cols=2)

    p.section("Vet & backup")
    p.field_row("Vet: ______________________    Phone: ________________    Backup sitter: ________________", lines=1)
    p.footer()
    return p


# 63. Mood Tracker
def mood_tracker():
    p = OnePager("Mood Tracker", "A month of moods at a glance", (140, 100, 160))
    p.header()
    p.field_row("Month: __________    Mood key: 5 great · 4 good · 3 okay · 2 low · 1 rough", lines=1)

    p.section("Daily mood grid (color or number 1–5)")
    days = [str(i) for i in range(1, 32)] + ["", "", "", ""]
    rows = [days[i:i + 7] for i in range(0, 35, 7)]
    p.table(
        ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        rows,
        [27.4] * 7,
    )

    p.section("Reflect")
    p.field_row("Best day + why: ________________________________    Pattern I notice: ____________________", lines=1)
    p.footer()
    return p


# 64. Self-Care Menu
def self_care_menu():
    p = OnePager("Self-Care Menu", "Pick one from each list, based on how much time you have", (60, 130, 110))
    p.header()
    p.muted("Self-care isn't selfish — it's maintenance.")

    p.section("5 minutes")
    p.checklist(["Drink water", "Stretch", "Deep breaths", "Step outside", "Text a friend", "Listen to a song"], cols=2)
    p.section("15 minutes")
    p.checklist(["Walk", "Journal", "Read a chapter", "Tidy one spot", "Make tea", "Stretch / yoga"], cols=2)
    p.section("1 hour")
    p.checklist(["Bath", "Hobby time", "Call a loved one", "Nap", "Cook a nice meal", "Workout"], cols=2)
    p.section("Half day")
    p.checklist(["Nature trip", "Massage", "Movie + blanket", "No-phone afternoon", "Catch up with a friend"], cols=2)

    p.section("This week I'll do")
    p.field_row("1. ______________   2. ______________   3. ______________", lines=1)
    p.footer()
    return p


# ---------------------------------------------------------------------------
# ===========================================================================
# Batch 4 — Premium & geo-localized (higher-income buyers + specific locales)
# ===========================================================================

# ---- A. Wealth & investing ------------------------------------------------
def net_worth_tracker():
    p = OnePager("Net Worth Tracker", "Assets minus liabilities — your true wealth at a glance", (20, 45, 85))
    p.header()
    p.field_row("As of date: __________", lines=1)
    p.section("Assets")
    p.table(
        ["Category", "Institution / account", "Value"],
        [["Cash & checking", "", ""],
         ["Savings / emergency", "", ""],
         ["Investments (stocks/ETFs)", "", ""],
         ["Retirement (401k/IRA)", "", ""],
         ["Real estate", "", ""],
         ["Business value", "", ""],
         ["Crypto", "", ""],
         ["Vehicles / other", "", ""]],
        [70, 82, 39.9],
    )
    p.section("Liabilities")
    p.table(
        ["Debt", "Balance", "Rate"],
        [["Mortgage", "", ""],
         ["Auto loan", "", ""],
         ["Student loans", "", ""],
         ["Credit cards", "", ""],
         ["Other", "", ""]],
        [70, 82, 39.9],
    )
    p.section("Summary")
    p.body("Total assets $______    Total liabilities $______    NET WORTH $______", size=8.6)
    p.footer()
    return p


def investment_portfolio():
    p = OnePager("Investment Portfolio Tracker", "Holdings, cost basis, and allocation", (8, 90, 70))
    p.header()
    p.field_row("Brokerage: ______________________    Account type: ______________________", lines=1)
    p.section("Holdings")
    p.table(
        ["Symbol", "Name", "Shares", "Cost basis", "Price", "Value", "Allocation"],
        [["", "", "", "", "", "", ""] for _ in range(12)],
        [20, 42, 20, 28, 22, 26, 33.9],
    )
    p.section("Totals")
    p.body("Portfolio value $______    Cost $______    Gain/loss $______ (______%)    Target allocation: ______ / ______", size=8.0)
    p.footer()
    return p


def dividend_tracker():
    p = OnePager("Dividend Tracker", "Ticker, yield, and income by payout", (140, 100, 30))
    p.header()
    p.field_row("Year: __________    Goal: $______ / year passive income", lines=1)
    p.section("Dividends")
    p.table(
        ["Ticker", "Company", "Shares", "Yield", "Payout freq", "Annual income"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [20, 48, 18, 18, 30, 57.9],
    )
    p.section("Income summary")
    p.body("Q1 $______    Q2 $______    Q3 $______    Q4 $______    TOTAL $______", size=8.4)
    p.footer()
    return p


def crypto_portfolio():
    p = OnePager("Crypto Portfolio Tracker", "Coins, cost basis, and realized gains", (140, 60, 20))
    p.header()
    p.field_row("Exchange / wallet: ______________________    Tax method: FIFO / HIFO / other", lines=1)
    p.section("Holdings")
    p.table(
        ["Coin", "Amount", "Avg buy price", "Current", "Value", "Gain/loss"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [30, 30, 32, 30, 34, 35.9],
    )
    p.section("Activity log")
    p.table(
        ["Date", "Buy/Sell", "Coin", "Amount", "Price", "Fee"],
        [["", "", "", "", "", ""] for _ in range(4)],
        [22, 24, 30, 28, 24, 63.9],
    )
    p.footer()
    return p


def trading_journal():
    p = OnePager("Trading Journal", "Every trade, with setup, outcome, and lessons", (30, 60, 110))
    p.header()
    p.field_row("Market: ______________________    Strategy: ______________________    Week: __________", lines=1)
    p.section("Trades")
    p.table(
        ["Date", "Symbol", "Long/Short", "Entry", "Exit", "P/L", "Setup / lesson"],
        [["", "", "", "", "", "", ""] for _ in range(12)],
        [18, 22, 22, 22, 22, 20, 65.9],
    )
    p.section("Weekly review")
    p.body("Win rate ______%    Net P/L $______    Biggest lesson: ______________________________", size=8.2)
    p.footer()
    return p


def real_estate_deal_analyzer():
    p = OnePager("Rental Deal Analyzer", "Run the numbers before you buy", (20, 90, 110))
    p.header()
    p.field_row("Property: ______________________    List price: $__________", lines=1)
    p.section("Income & expenses")
    p.table(
        ["Line item", "Monthly", "Annual"],
        [["Gross rent", "", ""],
         ["Vacancy (5-10%)", "", ""],
         ["Property tax", "", ""],
         ["Insurance", "", ""],
         ["Management", "", ""],
         ["Maintenance", "", ""],
         ["Mortgage (P&I)", "", ""],
         ["Utilities / HOA", "", ""]],
        [80, 55.9, 55.9],
    )
    p.section("Key metrics")
    p.body("Net cash flow $______/mo    Cap rate ______%    Cash-on-cash return ______%    Price-to-rent ______", size=8.2)
    p.footer()
    return p


def landlord_income():
    p = OnePager("Landlord Income & Expense Log", "Track rent, repairs, and net per property", (10, 80, 95))
    p.header()
    p.field_row("Property: ______________________    Year: __________", lines=1)
    p.section("Monthly ledger")
    p.table(
        ["Month", "Rent collected", "Repairs", "Taxes/ins", "Other", "Net"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [30, 34, 34, 34, 30, 29.9],
    )
    p.section("Year total")
    p.body("Gross rent $______    Expenses $______    Net income $______", size=8.4)
    p.footer()
    return p


def retirement_planner():
    p = OnePager("Retirement Planner", "Project savings, income, and withdrawal", (40, 70, 100))
    p.header()
    p.field_row("Target retirement date: __________    Target annual income: $__________", lines=1)
    p.section("Sources of retirement income")
    p.table(
        ["Source", "Account", "Balance", "Monthly income"],
        [["401(k) / 403(b)", "", "", ""],
         ["IRA / Roth IRA", "", "", ""],
         ["Pension", "", "", ""],
         ["Social Security", "", "", ""],
         ["Brokerage", "", "", ""],
         ["Real estate", "", "", ""]],
        [50, 46, 30, 65.9],
    )
    p.section("Plan")
    p.body("Gap to close: $______/yr    Withdrawal rate ______%    Years to retirement: ______", size=8.2)
    p.footer()
    return p


def sinking_fund():
    p = OnePager("Sinking Funds Tracker", "Save for every goal at once, without stress", (90, 60, 110))
    p.header()
    p.field_row("Month: __________", lines=1)
    p.section("Funds")
    p.table(
        ["Goal", "Target", "By when", "Saved", "This month", "Remaining"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [46, 26, 26, 26, 30, 37.9],
    )
    p.section("Rules")
    p.body("Fund each goal monthly = target ÷ months left. Treat it like a bill.", size=8.2)
    p.footer()
    return p


def debt_payoff():
    p = OnePager("Debt Payoff Tracker", "Snowball or avalanche — watch every balance fall", (150, 40, 50))
    p.header()
    p.field_row("Strategy: Snowball (smallest first) / Avalanche (highest rate first)", lines=1)
    p.section("Debts")
    p.table(
        ["Debt", "Balance", "Rate", "Min payment", "Extra", "Paid off"],
        [["", "", "", "", "", ""] for _ in range(10)],
        [46, 28, 18, 30, 26, 43.9],
    )
    p.section("Progress")
    p.body("Total owed $______    Paid this month $______    Debt-free date: __________", size=8.4)
    p.footer()
    return p


def estate_planning_checklist():
    p = OnePager("Estate Planning Checklist", "Documents and decisions, organized", (30, 60, 90))
    p.header()
    p.muted("Reference only — work with an estate attorney in your jurisdiction.")
    p.section("Core documents")
    p.checklist(["Will", "Living trust", "Power of attorney (financial)", "Healthcare directive / proxy",
                 "Beneficiary designations", "Guardianship for minors", "Letter of instruction", "Digital asset plan"], cols=2)
    p.section("Inventory")
    p.field_row("Assets & accounts: ______________________________    Location of documents: ____________________", lines=2)
    p.section("Review")
    p.body("Last reviewed: __________    Next review: __________    Attorney: ______________________", size=8.2)
    p.footer()
    return p


def insurance_inventory():
    p = OnePager("Insurance Policy Inventory", "Every policy, coverage, and contact", (20, 70, 100))
    p.header()
    p.field_row("Family / household: ______________________", lines=1)
    p.section("Policies")
    p.table(
        ["Type", "Company", "Policy #", "Coverage", "Premium", "Renewal"],
        [["", "", "", "", "", ""] for _ in range(10)],
        [40, 40, 30, 34, 24, 23.9],
    )
    p.section("Emergency contacts")
    p.field_row("Agent: ______________________    Phone: ____________________", lines=1)
    p.footer()
    return p


# ---- B. Geo-localized tax & bookkeeping ----------------------------------
def uk_self_assessment():
    p = OnePager("UK Self Assessment Tracker", "Income, expenses, and tax due — HMRC ready", (20, 60, 110))
    p.header()
    p.muted("UK tax year 6 April – 5 April. Deadline 31 Jan. Reference only — verify with HMRC.")
    p.field_row("Tax year: ______ / ______    UTR: ______________    Sole trader / landlord", lines=1)
    p.section("Income")
    p.table(
        ["Source", "Gross", "Notes"],
        [["Self-employment", "", ""],
         ["Employment (P60)", "", ""],
         ["Property (rental)", "", ""],
         ["Interest / dividends", "", ""],
         ["Other", "", ""]],
        [60, 40, 91.9],
    )
    p.section("Allowable expenses")
    p.table(
        ["Category", "Amount", "Category", "Amount"],
        [["Cost of goods", "", "Travel", ""],
         ["Office / rent", "", "Marketing", ""],
         ["Equipment", "", "Subscriptions", ""],
         ["Phone / internet", "", "Professional fees", ""]],
        [50, 46, 50, 45.9],
    )
    p.section("Summary")
    p.body("Total income £______    Expenses £______    Profit £______    Est. tax £______", size=8.4)
    p.footer()
    return p


def uk_vat_tracker():
    p = OnePager("UK VAT Tracker", "Quarterly VAT records, ready for MTD", (10, 70, 120))
    p.header()
    p.muted("Making Tax Digital quarterly reporting. Reference only — confirm rates & thresholds.")
    p.field_row("VAT period: __________    VAT reg no: ______________    Scheme: Standard / Flat rate", lines=1)
    p.section("VAT ledger")
    p.table(
        ["Date", "Sale (output)", "VAT on sales", "Purchase (input)", "VAT on purchases"],
        [["", "", "", "", ""] for _ in range(10)],
        [22, 36, 32, 36, 65.9],
    )
    p.section("Return")
    p.body("Output VAT £______    Input VAT £______    Net due to HMRC £______    Box 5 = £______", size=8.4)
    p.footer()
    return p


def uk_mileage_log():
    p = OnePager("UK Business Mileage Log", "Claim every business mile (45p / 25p)", (120, 70, 30))
    p.header()
    p.muted("Simplified expenses: 45p/mi first 10,000 miles, 25p/mi after. Reference only.")
    p.field_row("Vehicle: ______________    Reg: ______________    Month: __________", lines=1)
    p.section("Journeys")
    p.table(
        ["Date", "From", "To", "Purpose", "Miles"],
        [["", "", "", "", ""] for _ in range(13)],
        [20, 44, 44, 50, 33.9],
    )
    p.section("Total")
    p.body("Business miles ______    Claim £______ (______ mi × rate)", size=8.4)
    p.footer()
    return p


def canada_tax_checklist():
    p = OnePager("Canada Tax Return Checklist", "CRA documents and deductions, one page", (180, 30, 40))
    p.header()
    p.muted("CRA reference only — verify current year forms and limits.")
    p.section("Documents to gather")
    p.checklist(["T4 (employment)", "T5 (investment income)", "RRSP contribution receipts", "Charitable donation receipts",
                 "Medical expenses", "Childcare receipts", "Tuition (T2202)", "Student loan interest", "Moving expenses", "Self-employment income (T2125)"], cols=2)
    p.section("Deductions & credits")
    p.field_row("RRSP: $______    TFSA (non-taxable): $______    Other: ____________________", lines=1)
    p.section("Deadlines")
    p.body("Filing: 30 April (self-employed 15 June) · RRSP deadline: ~1 March · Instalments: quarterly", size=8.0)
    p.footer()
    return p


def canada_rrsp_tfsa():
    p = OnePager("RRSP & TFSA Tracker", "Contribution room and balances, tracked", (150, 30, 60))
    p.header()
    p.muted("Reference only — confirm CRA contribution room each year.")
    p.field_row("Year: __________    RRSP room: $__________    TFSA room: $__________", lines=1)
    p.section("Contributions")
    p.table(
        ["Account", "Contribution", "Room used", "Remaining"],
        [["RRSP", "", "", ""],
         ["TFSA", "", "", ""],
         ["Spousal RRSP", "", "", ""],
         ["", "", "", ""]],
        [60, 44, 44, 43.9],
    )
    p.section("Balances")
    p.body("RRSP balance $______    TFSA balance $______    Total $______", size=8.4)
    p.footer()
    return p


def canada_gst_hst():
    p = OnePager("Canada GST/HST Tracker", "Sales tax collected vs paid", (20, 80, 120))
    p.header()
    p.muted("GST 5% + provincial portion. Reference only — confirm rates for your province.")
    p.field_row("Reporting period: __________    GST/HST #: ______________", lines=1)
    p.section("Ledger")
    p.table(
        ["Date", "Revenue", "GST/HST collected", "GST/HST paid", "Net"],
        [["", "", "", "", ""] for _ in range(11)],
        [22, 38, 38, 38, 55.9],
    )
    p.section("Filing")
    p.body("Collected $______    Paid (ITCs) $______    Remit $______    Due date: __________", size=8.4)
    p.footer()
    return p


def australia_bas():
    p = OnePager("Australia BAS Tracker", "Business Activity Statement, ready to lodge", (10, 90, 110))
    p.header()
    p.muted("ATO reference only — confirm GST and rates with your accountant.")
    p.field_row("BAS period: __________    ABN: ______________    GST registered: Yes / No", lines=1)
    p.section("GST & PAYG")
    p.table(
        ["Label", "Item", "Amount"],
        [["G1", "Total sales", ""],
         ["1A", "GST on sales", ""],
         ["G11", "Total purchases", ""],
         ["1B", "GST on purchases", ""],
         ["W1", "Wages (PAYG)", ""],
         ["W2", "PAYG withheld", ""]],
        [30, 100, 61.9],
    )
    p.section("Summary")
    p.body("GST payable $______    GST credits $______    Net GST $______    Lodge by: __________", size=8.4)
    p.footer()
    return p


def australia_deductions():
    p = OnePager("Australia Tax Deductions Log", "Claim every work expense at EOFY", (200, 90, 30))
    p.header()
    p.muted("ATO reference only — keep receipts; verify what's deductible.")
    p.field_row("Financial year: 1 July ______ – 30 June ______", lines=1)
    p.section("Deductions")
    p.table(
        ["Date", "Expense", "Amount", "Category", "Receipt kept"],
        [["", "", "", "", ""] for _ in range(12)],
        [22, 58, 26, 46, 39.9],
    )
    p.section("Categories")
    p.body("Work vehicle/travel · Home office · Tools & equipment · Self-education · Uniform/protective · Professional fees · Phone/internet", size=7.6)
    p.footer()
    return p


def us_1099_tracker():
    p = OnePager("1099 Income & Expense Tracker", "Freelancer and contractor income, IRS ready", (15, 55, 100))
    p.header()
    p.muted("US reference only — confirm current forms (1099-NEC) and rates.")
    p.field_row("Tax year: __________    SSN/EIN: ______________", lines=1)
    p.section("Income")
    p.table(
        ["Client", "Date", "Amount", "1099 issued?"],
        [["", "", "", ""] for _ in range(8)],
        [62, 26, 30, 73.9],
    )
    p.section("Expenses")
    p.table(
        ["Date", "Expense", "Category", "Amount"],
        [["", "", "", ""] for _ in range(7)],
        [26, 70, 52, 43.9],
    )
    p.section("Summary")
    p.body("Gross income $______    Expenses $______    Net $______    Est. self-employment tax $______", size=8.2)
    p.footer()
    return p


def us_business_deductions():
    p = OnePager("Business Deduction Log", "Don't leave money on the table", (20, 80, 90))
    p.header()
    p.muted("US reference only — verify current IRS rules.")
    p.section("Track these")
    p.checklist(["Home office", "Business mileage", "Equipment", "Software / subscriptions",
                 "Marketing & ads", "Professional fees", "Insurance", "Travel & meals",
                 "Education & training", "Phone / internet"], cols=2)
    p.section("Log")
    p.table(
        ["Date", "Item", "Category", "Amount", "Receipt?"],
        [["", "", "", "", ""] for _ in range(8)],
        [22, 60, 44, 26, 39.9],
    )
    p.section("Total")
    p.body("Deductions this year: $______", size=8.4)
    p.footer()
    return p


def us_mileage_log():
    p = OnePager("IRS Mileage Log", "Standard mileage rate, every trip logged", (90, 50, 20))
    p.header()
    p.muted("US reference only — confirm the current IRS standard mileage rate.")
    p.field_row("Vehicle: ______________    Year: __________    Rate: $______ / mile", lines=1)
    p.section("Trips")
    p.table(
        ["Date", "From", "To", "Purpose", "Miles"],
        [["", "", "", "", ""] for _ in range(13)],
        [20, 46, 46, 46, 33.9],
    )
    p.section("Total")
    p.body("Business miles ______    Deduction $______", size=8.4)
    p.footer()
    return p


def us_home_office():
    p = OnePager("Home Office Deduction", "Simplified or actual — track it right", (10, 90, 80))
    p.header()
    p.muted("US reference only — simplified $5/sq ft up to 300 sq ft. Verify current rules.")
    p.field_row("Method: Simplified / Actual    Office sq ft: ______    Home sq ft: ______", lines=1)
    p.section("Actual method expenses")
    p.table(
        ["Expense", "Total", "Business %", "Deductible"],
        [["Rent / mortgage interest", "", "", ""],
         ["Utilities", "", "", ""],
         ["Home insurance", "", "", ""],
         ["Repairs", "", "", ""],
         ["Property tax", "", "", ""]],
        [60, 40, 40, 51.9],
    )
    p.section("Result")
    p.body("Deduction $______    Business use % = ______%", size=8.4)
    p.footer()
    return p


# ---- C. Executive & business owner ---------------------------------------
def kpi_scorecard():
    p = OnePager("KPI Scorecard", "The 6-10 numbers that run your business", (55, 60, 75))
    p.header()
    p.field_row("Company: ______________________    Period: __________", lines=1)
    p.section("Key metrics")
    p.table(
        ["KPI", "Target", "This period", "Trend", "Owner"],
        [["", "", "", "", ""] for _ in range(9)],
        [52, 26, 34, 24, 55.9],
    )
    p.section("Red / yellow / green")
    p.body("RED needs attention: ________________    YELLOW watch: ________________    GREEN on track: ________________", size=8.0)
    p.footer()
    return p


def meeting_notes():
    p = OnePager("Meeting Notes", "Decisions and actions, never lost", (60, 55, 70))
    p.header()
    p.field_row("Meeting: ______________________    Date: __________    Attendees: ____________________", lines=1)
    p.section("Agenda")
    p.field_row("1. ____________________________________", lines=1)
    p.field_row("2. ____________________________________", lines=1)
    p.field_row("3. ____________________________________", lines=1)
    p.section("Notes")
    p.field_row("", lines=4)
    p.section("Decisions made")
    p.field_row("1. ____________________________________", lines=1)
    p.field_row("2. ____________________________________", lines=1)
    p.section("Action items")
    p.table(
        ["Action", "Owner", "Due"],
        [["", "", ""] for _ in range(5)],
        [110, 50, 31.9],
    )
    p.footer()
    return p


def one_on_one_agenda():
    p = OnePager("1:1 Meeting Agenda", "Manager ↔ report, every week", (70, 50, 100))
    p.header()
    p.field_row("Manager: ______________    Report: ______________    Date: __________", lines=1)
    p.section("Report: what's going well")
    p.field_row("", lines=2)
    p.section("Report: blockers / challenges")
    p.field_row("", lines=2)
    p.section("Career & growth")
    p.field_row("", lines=2)
    p.section("Manager: feedback & support")
    p.field_row("", lines=2)
    p.section("Actions")
    p.field_row("1. ________________   2. ________________   3. ________________", lines=1)
    p.footer()
    return p


def eos_level10():
    p = OnePager("Level 10 Meeting (EOS)", "Weekly leadership meeting agenda", (120, 60, 40))
    p.header()
    p.muted("90-minute weekly leadership meeting — EOS® style.")
    p.section("Agenda (timed)")
    p.table(
        ["Segment", "Minutes", "Notes"],
        [["1. Good news (share wins)", "5", ""],
         ["2. Scorecard review", "5", ""],
         ["3. Rocks (90-day goals)", "5", ""],
         ["4. Headlines / customer issues", "5", ""],
         ["5. To-do list review", "5", ""],
         ["6. IDS — Identify, Discuss, Solve", "60", ""],
         ["7. Wrap up + cascade", "5", ""]],
        [110, 24, 57.9],
    )
    p.section("IDS")
    p.body("Identify the real issue → Discuss → Solve: decide an action with an owner + due date.", size=8.2)
    p.footer()
    return p


def business_plan_one_pager():
    p = OnePager("One-Page Business Plan", "Your whole business on a single sheet", (20, 80, 60))
    p.header()
    p.section("What we do")
    p.field_row("", lines=2)
    p.section("Who we serve")
    p.field_row("", lines=1)
    p.section("Problem & solution")
    p.field_row("Problem: ____________________________________", lines=1)
    p.field_row("Solution: ____________________________________", lines=1)
    p.section("Business model")
    p.field_row("Revenue: ______________    Pricing: ______________    Margin: ______%", lines=1)
    p.section("Marketing & channels")
    p.field_row("", lines=1)
    p.section("Milestones (next 90 days)")
    p.field_row("1. ____________   2. ____________   3. ____________", lines=1)
    p.section("Key numbers")
    p.field_row("Revenue goal: $______    Burn: $______/mo    Runway: ______ months", lines=1)
    p.footer()
    return p


def profit_loss():
    p = OnePager("Monthly Profit & Loss", "Revenue, expenses, and profit snapshot", (15, 70, 95))
    p.header()
    p.field_row("Business: ______________________    Month: __________", lines=1)
    p.section("Revenue")
    p.table(
        ["Stream", "Amount"],
        [["Product sales", ""],
         ["Services", ""],
         ["Subscriptions", ""],
         ["Other", ""]],
        [120, 71.9],
    )
    p.section("Expenses")
    p.table(
        ["Category", "Amount", "Category", "Amount"],
        [["COGS", "", "Payroll", ""],
         ["Marketing", "", "Software", ""],
         ["Rent", "", "Other", ""]],
        [50, 46, 50, 45.9],
    )
    p.section("Result")
    p.body("Revenue $______    Expenses $______    NET PROFIT $______    Margin ______%", size=8.6)
    p.footer()
    return p


def client_roster():
    p = OnePager("Client & Account Roster", "Every client, value, and next touch", (60, 45, 90))
    p.header()
    p.field_row("Business: ______________________    Quarter: __________", lines=1)
    p.section("Clients")
    p.table(
        ["Client", "Contact", "Value", "Status", "Last touch", "Next step"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [40, 34, 22, 24, 26, 45.9],
    )
    p.footer()
    return p


def hiring_scorecard():
    p = OnePager("Interview Scorecard", "Compare candidates fairly", (90, 40, 60))
    p.header()
    p.field_row("Role: ______________________    Interviewer: ______________________    Date: __________", lines=1)
    p.section("Candidate & scores (1-5)")
    p.table(
        ["Criteria", "Candidate 1", "Candidate 2", "Candidate 3"],
        [["Skills / competence", "", "", ""],
         ["Experience", "", "", ""],
         ["Problem solving", "", "", ""],
         ["Communication", "", "", ""],
         ["Culture fit", "", "", ""],
         ["Growth potential", "", "", ""],
         ["TOTAL", "", "", ""]],
        [70, 40.6, 40.6, 40.6],
    )
    p.section("Decision")
    p.field_row("Hire / No / Next round: ____________________    Notes: ____________________", lines=1)
    p.footer()
    return p


def project_status():
    p = OnePager("Project Status Report", "Scope, progress, and risks", (25, 80, 110))
    p.header()
    p.field_row("Project: ______________________    Owner: ____________    Date: __________", lines=1)
    p.section("Status")
    p.body("Status: GREEN on track / YELLOW at risk / RED blocked    % complete: ______    Due: __________", size=8.4)
    p.section("Milestones")
    p.table(
        ["Milestone", "Due", "Status"],
        [["", "", ""] for _ in range(6)],
        [110, 40, 41.9],
    )
    p.section("Risks & blockers")
    p.field_row("1. ____________________   2. ____________________", lines=1)
    p.section("Next steps")
    p.field_row("", lines=1)
    p.footer()
    return p


def vendor_contract_log():
    p = OnePager("Vendor & Contract Log", "Who you pay, what you owe, when it renews", (30, 60, 90))
    p.header()
    p.field_row("Company: ______________________", lines=1)
    p.section("Vendors & contracts")
    p.table(
        ["Vendor", "Service", "Cost", "Start", "End / renewal", "Notes"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [40, 46, 22, 24, 30, 29.9],
    )
    p.section("Renewal watch")
    p.body("Up for renewal this quarter: ______________________________", size=8.2)
    p.footer()
    return p


def okr_goals():
    p = OnePager("OKR & Annual Goals", "Objectives and key results, quarterly", (70, 50, 120))
    p.header()
    p.field_row("Company / team: ______________________    Quarter: __________", lines=1)
    p.section("Objective 1")
    p.field_row("O: ____________________________________", lines=1)
    p.field_row("KR1: ______________    KR2: ______________    KR3: ______________", lines=1)
    p.section("Objective 2")
    p.field_row("O: ____________________________________", lines=1)
    p.field_row("KR1: ______________    KR2: ______________    KR3: ______________", lines=1)
    p.section("Objective 3")
    p.field_row("O: ____________________________________", lines=1)
    p.field_row("KR1: ______________    KR2: ______________    KR3: ______________", lines=1)
    p.section("Scoring")
    p.body("0.0–1.0 per KR · ~0.7 = stretch achieved · Review: __________", size=8.2)
    p.footer()
    return p


def delegation_log():
    p = OnePager("Delegation Log", "Hand it off, then track it to done", (20, 90, 70))
    p.header()
    p.field_row("Manager: ______________________    Week: __________", lines=1)
    p.section("Delegated tasks")
    p.table(
        ["Task", "Assigned to", "Due", "Status", "Follow-up"],
        [["", "", "", "", ""] for _ in range(11)],
        [52, 40, 24, 24, 51.9],
    )
    p.section("Handoff checklist")
    p.checklist(["Clear outcome", "Deadline set", "Context shared", "Authority given", "Check-in scheduled"], cols=2)
    p.footer()
    return p


# ---- D. Affluent lifestyle -------------------------------------------------
def luxury_travel_itinerary():
    p = OnePager("Luxury Travel Itinerary", "Flights, stays, and reservations, in order", (110, 30, 45))
    p.header()
    p.field_row("Destination: ______________________    Dates: ___/___/___  →  ___/___/___", lines=1)
    p.section("Itinerary")
    p.table(
        ["Day", "Time", "Activity", "Location", "Confirmation #"],
        [["", "", "", "", ""] for _ in range(10)],
        [16, 20, 56, 52, 47.9],
    )
    p.section("Reservations")
    p.body("Hotel: ______________    Flights: ______________    Dining: ______________    Concierge: ______________", size=7.8)
    p.footer()
    return p


def wine_cellar_log():
    p = OnePager("Wine Cellar Log", "Every bottle, vintage, and when to drink", (120, 40, 30))
    p.header()
    p.field_row("Cellar: ______________________    Total bottles: ______", lines=1)
    p.section("Collection")
    p.table(
        ["Wine", "Vintage", "Region", "Qty", "Drink by", "Notes"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [44, 22, 40, 14, 26, 45.9],
    )
    p.footer()
    return p


def wine_tasting_notes():
    p = OnePager("Wine Tasting Notes", "Taste, score, and remember", (140, 50, 40))
    p.header()
    p.field_row("Wine: ______________________    Vintage: ______    Region: ______________________", lines=1)
    p.section("Appearance")
    p.body("Clarity: ______    Color: ____________________    Viscosity: ______", size=8.2)
    p.section("Nose")
    p.field_row("Aromas: ____________________________________", lines=1)
    p.section("Palate")
    p.field_row("Flavors: ____________________________________    Body: ______    Acidity: ______    Tannin: ______", lines=1)
    p.section("Finish & verdict")
    p.field_row("Finish: __________    Score: ______ / 100    Pair with: ____________________", lines=1)
    p.footer()
    return p


def art_collection():
    p = OnePager("Art Collection Inventory", "Artist, provenance, and insured value", (50, 40, 60))
    p.header()
    p.field_row("Collection: ______________________    Location: ______________________", lines=1)
    p.section("Pieces")
    p.table(
        ["Title", "Artist", "Year", "Medium", "Value", "Location"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [38, 34, 18, 32, 30, 39.9],
    )
    p.section("Insurance")
    p.body("Total insured value: $______    Policy: ______________________    Appraisal date: __________", size=8.0)
    p.footer()
    return p


def home_maintenance_log():
    p = OnePager("Home Maintenance Log", "Keep a big investment in top shape", (30, 80, 70))
    p.header()
    p.field_row("Property: ______________________    Year: __________", lines=1)
    p.section("Seasonal tasks")
    p.checklist(["Change HVAC filters", "Clean gutters", "Smoke/CO detectors", "Water heater flush", "Roof inspection", "Pest check", "Seal windows/doors", "Irrigation check"], cols=2)
    p.section("Repairs & service log")
    p.table(
        ["Date", "Item", "Vendor", "Cost", "Notes"],
        [["", "", "", "", ""] for _ in range(8)],
        [22, 50, 48, 26, 45.9],
    )
    p.footer()
    return p


def renovation_budget():
    p = OnePager("Renovation Budget & Timeline", "Every line item, before you demo", (140, 70, 20))
    p.header()
    p.field_row("Project: ______________________    Total budget: $__________", lines=1)
    p.section("Budget")
    p.table(
        ["Category", "Budget", "Actual", "Over/under"],
        [["Demolition", "", "", ""],
         ["Materials", "", "", ""],
         ["Labor", "", "", ""],
         ["Permits", "", "", ""],
         ["Fixtures / finishes", "", "", ""],
         ["Contingency (10-20%)", "", "", ""]],
        [70, 40.6, 40.6, 40.6],
    )
    p.section("Timeline")
    p.body("Start: __________    End: __________    Milestone 1: ________    Milestone 2: ________", size=8.2)
    p.footer()
    return p


def holiday_gift_planner():
    p = OnePager("Holiday Gift Planner", "Everyone on your list, on budget", (150, 40, 50))
    p.header()
    p.field_row("Season: __________    Total budget: $__________", lines=1)
    p.section("Gift list")
    p.table(
        ["Recipient", "Idea", "Budget", "Spent", "Purchased", "Wrapped"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [36, 48, 24, 24, 30, 29.9],
    )
    p.section("Totals")
    p.body("Spent $______    Remaining $______    Cards sent: ______", size=8.4)
    p.footer()
    return p


def vacation_rental_income():
    p = OnePager("Vacation Rental Income Log", "Bookings, cleaning, and net per stay", (20, 100, 110))
    p.header()
    p.field_row("Property: ______________________    Platform: ______________________", lines=1)
    p.section("Bookings")
    p.table(
        ["Dates", "Guest", "Rate", "Cleaning", "Fees", "Net"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [34, 40, 26, 26, 26, 39.9],
    )
    p.section("Monthly summary")
    p.body("Revenue $______    Expenses $______    Net $______    Occupancy ______%", size=8.4)
    p.footer()
    return p


def vehicle_maintenance():
    p = OnePager("Vehicle Maintenance Log", "Service history for every car", (20, 70, 100))
    p.header()
    p.field_row("Vehicle: ______________    VIN: ______________    Odometer: ______", lines=1)
    p.section("Service log")
    p.table(
        ["Date", "Odometer", "Service", "Cost", "Shop", "Next due"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [20, 24, 50, 22, 42, 33.9],
    )
    p.footer()
    return p


def golf_score_log():
    p = OnePager("Golf Score & Handicap Log", "Track rounds, stats, and improvement", (20, 100, 60))
    p.header()
    p.field_row("Player: ______________________    Handicap index: ______", lines=1)
    p.section("Rounds")
    p.table(
        ["Date", "Course", "Score", "Par", "Fairways", "Putts", "Notes"],
        [["", "", "", "", "", "", ""] for _ in range(11)],
        [20, 46, 18, 16, 24, 18, 49.9],
    )
    p.section("Trends")
    p.body("Avg score ______    Best round ______    Birdies ______    GIR ______%", size=8.2)
    p.footer()
    return p


def home_inventory():
    p = OnePager("Home Inventory", "Document valuables for insurance", (30, 70, 90))
    p.header()
    p.muted("For insurance claims — attach photos and receipts where possible.")
    p.section("Inventory by room")
    p.table(
        ["Room", "Item", "Make/model", "Value", "Receipt?"],
        [["", "", "", "", ""] for _ in range(12)],
        [32, 50, 46, 24, 39.9],
    )
    p.section("High-value items")
    p.body("Jewelry: ______________    Art: ______________    Electronics: ______________    Total: $______", size=7.8)
    p.footer()
    return p


def dinner_party_planner():
    p = OnePager("Dinner Party Planner", "Menu, guests, and timeline", (90, 45, 60))
    p.header()
    p.field_row("Event: ______________________    Date: __________    Guests: ______", lines=1)
    p.section("Menu")
    p.table(
        ["Course", "Dish", "Diet notes"],
        [["Starter", "", ""],
         ["Main", "", ""],
         ["Side", "", ""],
         ["Dessert", "", ""],
         ["Drinks", "", ""]],
        [40, 80, 71.9],
    )
    p.section("Guests & dietary")
    p.field_row("", lines=2)
    p.section("Timeline")
    p.body("2 days before: shop · 1 day: prep · morning: set table · 1 hr before: cook · 30 min: light candles", size=7.8)
    p.footer()
    return p


# ---- E. Affluent parents & education -------------------------------------
def college_application_tracker():
    p = OnePager("College Application Tracker", "Every school, deadline, and requirement", (40, 50, 100))
    p.header()
    p.field_row("Student: ______________________    Graduation year: ______", lines=1)
    p.section("Applications")
    p.table(
        ["College", "Deadline", "Essay", "Recs", "Fees", "Status"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [46, 24, 28, 22, 22, 49.9],
    )
    p.section("Checklist")
    p.checklist(["Transcripts sent", "Test scores sent", "FAFSA/FAFSA submitted", "Interviews scheduled", "Thank-you notes"], cols=2)
    p.footer()
    return p


def scholarship_tracker():
    p = OnePager("Scholarship Tracker", "Free money, organized", (120, 80, 30))
    p.header()
    p.field_row("Student: ______________________    Total goal: $__________", lines=1)
    p.section("Scholarships")
    p.table(
        ["Scholarship", "Amount", "Deadline", "Essay?", "Submitted", "Won"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [50, 24, 24, 22, 26, 45.9],
    )
    p.section("Total")
    p.body("Applied $______    Won $______    Remaining to apply: ______________________", size=8.4)
    p.footer()
    return p


def college_budget():
    p = OnePager("College Cost & Budget", "Compare schools on real cost", (30, 80, 110))
    p.header()
    p.field_row("Student: ______________________    Year: ______", lines=1)
    p.section("Cost comparison")
    p.table(
        ["School", "Tuition", "Room/board", "Aid", "Net cost"],
        [["", "", "", "", ""] for _ in range(8)],
        [44, 28, 34, 34, 51.9],
    )
    p.section("Monthly budget")
    p.body("Books $______    Food $______    Transport $______    Fun $______    Total $______/mo", size=8.2)
    p.footer()
    return p


def college_visit_checklist():
    p = OnePager("College Visit Comparison", "Score each campus fairly", (60, 50, 110))
    p.header()
    p.field_row("School: ______________________    Date: __________", lines=1)
    p.section("What to check (1-5)")
    p.table(
        ["Factor", "Score", "Notes"],
        [["Academics / major", "", ""],
         ["Campus feel", "", ""],
         ["Dorms & food", "", ""],
         ["Location & safety", "", ""],
         ["Clubs / social life", "", ""],
         ["Career support", "", ""],
         ["Financial aid", "", ""]],
        [80, 20, 91.9],
    )
    p.section("Verdict")
    p.field_row("Gut feeling: ______________    Pros: ____________    Cons: ____________", lines=1)
    p.footer()
    return p


def tutor_session_log():
    p = OnePager("Tutoring Session Log", "Progress per session, per subject", (20, 90, 100))
    p.header()
    p.field_row("Student: ______________________    Tutor: ______________________", lines=1)
    p.section("Sessions")
    p.table(
        ["Date", "Subject", "Topics", "Homework", "Progress"],
        [["", "", "", "", ""] for _ in range(12)],
        [20, 34, 52, 44, 41.9],
    )
    p.section("Next session")
    p.field_row("Focus: ______________________________    Prep: ______________________________", lines=1)
    p.footer()
    return p


def kids_activity_schedule():
    p = OnePager("Kids Activity Schedule", "Lessons, practices, and carpool, sorted", (150, 60, 40))
    p.header()
    p.field_row("Child(ren): ______________________    Week of: __________", lines=1)
    p.section("Weekly schedule")
    p.table(
        ["Day", "Time", "Activity", "Location", "Who drives"],
        [["Mon", "", "", "", ""],
         ["Tue", "", "", "", ""],
         ["Wed", "", "", "", ""],
         ["Thu", "", "", "", ""],
         ["Fri", "", "", "", ""],
         ["Sat", "", "", "", ""],
         ["Sun", "", "", "", ""]],
        [18, 24, 52, 48, 49.9],
    )
    p.footer()
    return p


def summer_camp_planner():
    p = OnePager("Summer Camp Planner", "Plan the whole summer, week by week", (20, 110, 90))
    p.header()
    p.field_row("Child(ren): ______________________    Summer: ______", lines=1)
    p.section("Weeks")
    p.table(
        ["Week", "Camp / activity", "Cost", "Registered", "Packed"],
        [["", "", "", "", ""] for _ in range(11)],
        [26, 60, 30, 40, 35.9],
    )
    p.section("Totals")
    p.body("Total camp cost $______    Deposit due dates: ______________________", size=8.4)
    p.footer()
    return p


def family_travel_itinerary():
    p = OnePager("Family Travel Itinerary", "One plan everyone can follow", (30, 90, 110))
    p.header()
    p.field_row("Trip: ______________________    Dates: ___/___/___  →  ___/___/___", lines=1)
    p.section("Day-by-day")
    p.table(
        ["Day", "Morning", "Afternoon", "Evening", "Notes"],
        [["", "", "", "", ""] for _ in range(9)],
        [16, 44, 44, 44, 43.9],
    )
    p.section("Essentials")
    p.field_row("Hotel: ______________    Confirmation: ______________    Docs: passports / IDs / tickets", lines=1)
    p.footer()
    return p


def babysitter_info():
    p = OnePager("Babysitter Info Sheet", "Everything your sitter needs to know", (90, 50, 100))
    p.header()
    p.field_row("Child(ren) + ages: ______________________    Parents' phones: ____________________", lines=1)
    p.section("Schedule & routine")
    p.field_row("Bedtime ______    Dinner ______    Screen rules: ____________________", lines=1)
    p.section("Food & allergies")
    p.field_row("", lines=2)
    p.section("House rules & safety")
    p.checklist(["Doors locked", "No visitors", "Medication instructions", "Emergency plan", "Pets routine"], cols=2)
    p.section("Emergency contacts")
    p.field_row("Doctor: ______________    Neighbor: ______________    Poison control: 1-800-222-1222", lines=1)
    p.footer()
    return p


def allowance_ledger():
    p = OnePager("Kids Money Ledger", "Chores, allowance, and saving habits", (140, 90, 30))
    p.header()
    p.field_row("Child: ______________________    Week: __________", lines=1)
    p.section("Earnings")
    p.table(
        ["Chore / task", "Amount", "Done", "Date"],
        [["", "", "", ""] for _ in range(8)],
        [90, 30, 24, 47.9],
    )
    p.section("Money rules")
    p.body("Save ______%    Spend ______%    Give ______%    Balance: $______    Goal: ____________________", size=8.2)
    p.footer()
    return p


def extracurricular_expenses():
    p = OnePager("Activities & Lessons Budget", "What each activity really costs", (60, 50, 100))
    p.header()
    p.field_row("Child: ______________________    Year: __________", lines=1)
    p.section("Activities")
    p.table(
        ["Activity", "Tuition", "Equipment", "Travel", "Total"],
        [["", "", "", "", ""] for _ in range(9)],
        [60, 34, 34, 30, 33.9],
    )
    p.section("Summary")
    p.body("Total investment $______    Per month $______    Worth it? Prioritize: ____________________", size=8.2)
    p.footer()
    return p


def college_savings_529():
    p = OnePager("529 College Savings Tracker", "Contribute, grow, and project", (10, 80, 90))
    p.header()
    p.muted("US reference only — confirm plan rules and tax benefits.")
    p.field_row("Beneficiary: ______________________    Plan: ______________________", lines=1)
    p.section("Contributions")
    p.table(
        ["Date", "Contribution", "Balance", "Growth"],
        [["", "", "", ""] for _ in range(8)],
        [30, 46, 46, 69.9],
    )
    p.section("Projection")
    p.body("Current $______    Goal $______    Years until college: ______    Monthly needed: $______", size=8.2)
    p.footer()
    return p


# ---- F. Health & longevity (premium wellness) -----------------------------
def supplement_tracker():
    p = OnePager("Supplement Tracker", "What you take, when, and why", (15, 90, 80))
    p.header()
    p.field_row("Name: ______________________    Health goal: ______________________________", lines=1)
    p.section("Daily stack")
    p.table(
        ["Supplement", "Dose", "AM", "PM", "Notes / purpose"],
        [["", "", "", "", ""] for _ in range(11)],
        [60, 26, 20, 20, 65.9],
    )
    p.section("Review")
    p.body("Started: __________    Next review with doctor: __________    Changes: ____________________", size=8.2)
    p.footer()
    return p


def blood_panel_log():
    p = OnePager("Blood Panel Log", "Track labs over time, spot trends", (150, 30, 50))
    p.header()
    p.muted("Reference only — discuss results with your physician.")
    p.field_row("Name: ______________________    Lab: ______________________", lines=1)
    p.section("Results over time")
    p.table(
        ["Marker", "Date", "Result", "Range", "Trend"],
        [["", "", "", "", ""] for _ in range(12)],
        [52, 26, 34, 44, 35.9],
    )
    p.section("Markers to watch")
    p.body("Lipids · HbA1c · Vitamin D · B12 · Ferritin · Thyroid (TSH) · CRP · Hormones", size=7.8)
    p.footer()
    return p


def fasting_log():
    p = OnePager("Intermittent Fasting Log", "Fasting windows, meals, and how you feel", (120, 50, 70))
    p.header()
    p.muted("Consult a doctor before fasting, especially with medical conditions.")
    p.field_row("Protocol (e.g. 16:8): __________    Week: __________", lines=1)
    p.section("Daily log")
    p.table(
        ["Day", "Fast started", "Fast ended", "Hours", "Energy", "Notes"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [22, 30, 30, 20, 22, 67.9],
    )
    p.section("Reflection")
    p.body("Best fasting window: ______    Weight/measure: ______    Hunger pattern: ____________________", size=8.2)
    p.footer()
    return p


def medical_history():
    p = OnePager("Personal Medical History", "Everything a new doctor should know", (20, 60, 90))
    p.header()
    p.field_row("Name: ______________________    DOB: __________    Blood type: ______    Allergies: ____________", lines=1)
    p.section("Conditions & diagnoses")
    p.field_row("", lines=3)
    p.section("Surgeries & hospitalizations")
    p.field_row("", lines=2)
    p.section("Medications & supplements")
    p.field_row("", lines=2)
    p.section("Family history")
    p.field_row("", lines=2)
    p.section("Vaccinations & screenings")
    p.field_row("Last physical: __________    Vaccines: ____________________    Screenings: ____________________", lines=1)
    p.footer()
    return p


# ===========================================================================
# Batch 5 — Niche-profession one-pagers (high-income professionals)
# ===========================================================================

# ---- Real estate ----------------------------------------------------------
def realtor_cma():
    p = OnePager("CMA — Comparative Market Analysis", "Price a listing with comps and adjustments", (0, 100, 120))
    p.header()
    p.field_row("Subject property: ______________________    List price target: $__________", lines=1)
    p.section("Comparable sales")
    p.table(
        ["Address", "Sold price", "Sq ft", "$/sq ft", "Beds/Baths", "Sold date"],
        [["", "", "", "", "", ""] for _ in range(8)],
        [40, 26, 20, 24, 28, 53.9],
    )
    p.section("Adjustments")
    p.body("Condition: ______    Upgrades: ______    Location: ______    Suggested list: $__________", size=8.2)
    p.section("Active & pending competition")
    p.field_row("Active listings: ______    Avg days on market: ______    Notes: ____________________", lines=1)
    p.footer()
    return p


def realtor_showings():
    p = OnePager("Showing & Buyer Follow-Up Log", "Track every tour and never drop a lead", (0, 90, 110))
    p.header()
    p.field_row("Agent: ______________________    Month: __________", lines=1)
    p.section("Showings")
    p.table(
        ["Date", "Buyer", "Property", "Feedback", "Follow-up"],
        [["", "", "", "", ""] for _ in range(11)],
        [22, 40, 44, 48, 37.9],
    )
    p.section("Pipeline")
    p.body("Hot buyers: ______    Pre-approved: ______    Under contract: ______    Need nudge: ____________________", size=8.0)
    p.footer()
    return p


def realtor_transaction():
    p = OnePager("Transaction Timeline", "Listing to close, every step checked", (0, 110, 100))
    p.header()
    p.field_row("Property: ______________________    Close date: __________    Price: $__________", lines=1)
    p.section("Milestones")
    p.table(
        ["Step", "Due", "Done", "Notes"],
        [["Listing agreement signed", "", "", ""],
         ["Photos + staging", "", "", ""],
         ["MLS listing live", "", "", ""],
         ["Open house", "", "", ""],
         ["Offer accepted", "", "", ""],
         ["Inspection", "", "", ""],
         ["Appraisal", "", "", ""],
         ["Title + escrow", "", "", ""],
         ["Final walkthrough", "", "", ""],
         ["Closing!", "", "", ""]],
        [70, 26, 20, 75.9],
    )
    p.footer()
    return p


def realtor_open_house():
    p = OnePager("Open House Sign-In & Feedback", "Capture every visitor and their reaction", (10, 95, 115))
    p.header()
    p.field_row("Property: ______________________    Date: __________    Agent: ______________________", lines=1)
    p.section("Visitor sign-in")
    p.table(
        ["Name", "Phone / email", "Realtor?", "Pre-approved?", "Feedback"],
        [["", "", "", "", ""] for _ in range(11)],
        [34, 42, 20, 26, 69.9],
    )
    p.section("Follow-up")
    p.body("Call within 24h: ______    Send comps: ______    Book private tour: ______    Note: ____________________", size=8.0)
    p.footer()
    return p


# ---- Legal ----------------------------------------------------------------
def lawyer_case_log():
    p = OnePager("Case & Matter Log", "Every matter, deadline, and next step", (60, 40, 100))
    p.header()
    p.field_row("Attorney: ______________________    Practice area: ______________________", lines=1)
    p.section("Matters")
    p.table(
        ["Matter / client", "Type", "Opened", "Deadline", "Status", "Next step"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [44, 30, 20, 22, 26, 49.9],
    )
    p.section("Deadline watch")
    p.body("Due this week: ______________________________    Statute of limitations: ____________________", size=8.0)
    p.footer()
    return p


def lawyer_billable_hours():
    p = OnePager("Billable Hours Log", "Time entries, ready to invoice", (55, 35, 95))
    p.header()
    p.field_row("Attorney: ______________________    Week: __________    Rate: $______ / hr", lines=1)
    p.section("Time entries")
    p.table(
        ["Date", "Client / matter", "Description", "Hours", "Amount"],
        [["", "", "", "", ""] for _ in range(13)],
        [20, 46, 70, 20, 35.9],
    )
    p.section("Weekly total")
    p.body("Total hours: ______    Billable: $______    Non-billable: ______ hrs", size=8.4)
    p.footer()
    return p


def lawyer_intake():
    p = OnePager("Client Intake Sheet", "Capture the facts on the first call", (65, 45, 105))
    p.header()
    p.field_row("Client: ______________________    Date: __________    Referred by: ____________________", lines=1)
    p.section("Matter")
    p.field_row("Legal issue (summary):", lines=2)
    p.field_row("Key dates / deadlines:", lines=1)
    p.field_row("Opposing party:", lines=1)
    p.section("Facts & documents")
    p.field_row("Documents to request: ____________________    Witnesses: ____________________", lines=1)
    p.section("Fees & engagement")
    p.field_row("Retainer: $______    Rate: $______    Engagement letter sent: ______", lines=1)
    p.footer()
    return p


# ---- Accounting / finance -------------------------------------------------
def cpa_tax_client_tracker():
    p = OnePager("Tax Season Client Tracker", "Every client, every document, every status", (20, 70, 110))
    p.header()
    p.field_row("Firm: ______________________    Tax year: __________", lines=1)
    p.section("Clients")
    p.table(
        ["Client", "Docs received", "Prep", "Review", "Filed", "Notes"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [42, 34, 24, 24, 20, 47.9],
    )
    p.section("Deadlines")
    p.body("Filing deadline: __________    Extensions needed: ____________________    E-file / paper: __________", size=8.0)
    p.footer()
    return p


def cpa_monthly_close():
    p = OnePager("Month-End Close Checklist", "Close the books without missing a step", (15, 65, 105))
    p.header()
    p.field_row("Company: ______________________    Month: __________", lines=1)
    p.section("Close checklist")
    p.checklist(["Reconcile all bank accounts", "Reconcile credit cards", "Review A/R aging", "Review A/P", "Accrue payroll", "Depreciation entry", "Prepaids & accruals", "Review P&L vs budget", "Close subledgers", "Lock the period"], cols=2)
    p.section("Sign-off")
    p.field_row("Prepared by: __________    Reviewed by: __________    Date closed: __________", lines=1)
    p.footer()
    return p


def bookkeeper_reconciliation():
    p = OnePager("Bank Reconciliation Log", "Match the books to the bank, every month", (25, 75, 115))
    p.header()
    p.field_row("Account: ______________________    Statement date: __________", lines=1)
    p.section("Reconciliation")
    p.table(
        ["Item", "Books", "Bank", "Diff", "Cleared"],
        [["Beginning balance", "", "", "", ""],
         ["Deposits", "", "", "", ""],
         ["Checks / payments", "", "", "", ""],
         ["Interest & fees", "", "", "", ""],
         ["Ending balance", "", "", "", ""]],
        [50, 30, 30, 30, 51.9],
    )
    p.section("Items to clear")
    p.field_row("Outstanding checks / deposits: ______________________________", lines=1)
    p.footer()
    return p


def cpa_tax_checklist():
    p = OnePager("Tax Return Document Checklist", "Collect everything from every client", (18, 68, 108))
    p.header()
    p.field_row("Client: ______________________    Tax year: __________", lines=1)
    p.section("Income documents")
    p.checklist(["W-2 / 1099", "K-1", "Interest (1099-INT)", "Dividends (1099-DIV)", "Rental income", "Business income", "Crypto / capital gains", "Other income"], cols=2)
    p.section("Deductions & credits")
    p.checklist(["Mortgage interest (1098)", "Property tax", "Charitable donations", "Medical expenses", "Student loan interest", "Retirement contributions", "Childcare", "Education credits"], cols=2)
    p.section("Status")
    p.field_row("Missing: ______________________________    E-file ready: ______", lines=1)
    p.footer()
    return p


# ---- Consulting -----------------------------------------------------------
def consultant_project_scoping():
    p = OnePager("Project Scoping Sheet", "Define the work before you quote it", (70, 60, 120))
    p.header()
    p.field_row("Client: ______________________    Project: ______________________", lines=1)
    p.section("Scope")
    p.field_row("Objective (what success looks like):", lines=2)
    p.field_row("Deliverables:", lines=2)
    p.field_row("Out of scope:", lines=1)
    p.section("Constraints & assumptions")
    p.field_row("Budget: $______    Timeline: __________    Resources: ____________________", lines=1)
    p.section("Proposal")
    p.field_row("Fee: $______    Payment terms: ____________________    Signature: __________", lines=1)
    p.footer()
    return p


def consultant_stakeholder_map():
    p = OnePager("Stakeholder Map", "Who matters, their interests, and influence", (75, 55, 115))
    p.header()
    p.field_row("Project: ______________________    Date: __________", lines=1)
    p.section("Stakeholders")
    p.table(
        ["Stakeholder", "Role", "Interest", "Influence (H/M/L)", "Engagement plan"],
        [["", "", "", "", ""] for _ in range(10)],
        [38, 30, 44, 32, 47.9],
    )
    p.section("Notes")
    p.body("Key decision-maker: ____________________    Keep informed: ____________________    Manage closely: ____________________", size=7.8)
    p.footer()
    return p


def consultant_discovery():
    p = OnePager("Discovery Call Notes", "Understand before you propose", (80, 65, 125))
    p.header()
    p.field_row("Client: ______________________    Date: __________    Contact: ____________________", lines=1)
    p.section("Situation")
    p.field_row("Current state / pain:", lines=2)
    p.section("Desired outcome")
    p.field_row("What would a win look like?", lines=2)
    p.section("Decision & budget")
    p.field_row("Decision-maker: ____________    Budget: $______    Timeline: ____________", lines=1)
    p.section("Next steps")
    p.field_row("I'll send: ____________________    Follow-up call: __________", lines=1)
    p.footer()
    return p


# ---- Financial advising ---------------------------------------------------
def advisor_client_snapshot():
    p = OnePager("Client Financial Snapshot", "The whole picture in one page", (30, 90, 90))
    p.header()
    p.field_row("Client: ______________________    Date: __________    Risk tolerance: __________", lines=1)
    p.section("Assets & liabilities")
    p.table(
        ["Category", "Value", "Category", "Value"],
        [["Cash", "", "Mortgage", ""],
         ["Investments", "", "Other debt", ""],
         ["Retirement", "", "Net worth", ""],
         ["Real estate", "", "", ""],
         ["Other", "", "", ""]],
        [60, 36, 60, 35.9],
    )
    p.section("Goals")
    p.field_row("Retire by: ______    College: $______    Other: ____________________", lines=1)
    p.section("Review")
    p.body("Next meeting: __________    Action items: ______________________________", size=8.0)
    p.footer()
    return p


def advisor_discovery():
    p = OnePager("Financial Discovery Questionnaire", "Know the client before the plan", (25, 85, 85))
    p.header()
    p.field_row("Client: ______________________    Date: __________", lines=1)
    p.section("Today")
    p.field_row("Income: $______/yr    Expenses: $______/mo    Savings rate: ______%", lines=1)
    p.section("Goals (rank 1-5)")
    p.field_row("Retirement: ____    Home: ____    College: ____    Debt-free: ____    Legacy/estate: ____", lines=1)
    p.section("Comfort & experience")
    p.checklist(["I've invested before", "I'm comfortable with volatility", "I want income now", "I'm investing long-term", "I have dependents", "I have an emergency fund"], cols=2)
    p.section("Concerns")
    p.field_row("Biggest money worry: ____________________________________", lines=1)
    p.footer()
    return p


# ---- Medical / clinical ---------------------------------------------------
def soap_note():
    p = OnePager("SOAP Note", "Subjective · Objective · Assessment · Plan", (30, 80, 130))
    p.header()
    p.field_row("Patient: ______________    Date: __________    Clinician: ____________________", lines=1)
    p.section("S — Subjective")
    p.field_row("Chief complaint + history:", lines=2)
    p.section("O — Objective")
    p.field_row("Vitals: HR ____  BP ____  RR ____  Temp ____  |  Exam findings:", lines=2)
    p.section("A — Assessment")
    p.field_row("Diagnosis / differential:", lines=2)
    p.section("P — Plan")
    p.field_row("Orders, meds, follow-up:", lines=2)
    p.footer()
    return p


def dentist_treatment_plan():
    p = OnePager("Dental Treatment Plan", "Phases, costs, and next visits", (20, 100, 120))
    p.header()
    p.field_row("Patient: ______________________    Chart #: __________    Date: __________", lines=1)
    p.section("Treatment plan")
    p.table(
        ["Tooth / quadrant", "Procedure", "Cost", "Insurance", "Patient", "Scheduled"],
        [["", "", "", "", "", ""] for _ in range(10)],
        [30, 52, 22, 24, 22, 41.9],
    )
    p.section("Recall")
    p.body("Next hygiene: __________    Next exam: __________    Treatment complete: ______", size=8.2)
    p.footer()
    return p


def pt_treatment_plan():
    p = OnePager("Physical Therapy Treatment Plan", "Goals, exercises, and progress", (35, 85, 135))
    p.header()
    p.field_row("Patient: ______________________    Dx: ______________________    Visit: ______", lines=1)
    p.section("Plan of care")
    p.table(
        ["Goal", "Exercise / intervention", "Sets × reps", "Resistance", "Notes"],
        [["", "", "", "", ""] for _ in range(9)],
        [40, 56, 26, 26, 43.9],
    )
    p.section("Progress")
    p.body("Pain (0-10): ______    ROM: ______    Strength: ______    Home program: ____________________", size=8.0)
    p.footer()
    return p


# ---- Therapy --------------------------------------------------------------
def therapist_intake():
    p = OnePager("Therapy Intake Form", "History and presenting concerns, structured", (120, 70, 90))
    p.header()
    p.muted("For clinical use — follow your practice's confidentiality & consent policies.")
    p.field_row("Client: ______________________    Date: __________    Referral: ____________________", lines=1)
    p.section("Presenting concern")
    p.field_row("", lines=2)
    p.section("History")
    p.field_row("Symptoms / duration:", lines=1)
    p.field_row("Past treatment:", lines=1)
    p.field_row("Medical / medications:", lines=1)
    p.section("Safety & support")
    p.field_row("Support system: ____________________    Risk assessment: ____________________", lines=1)
    p.section("Goals")
    p.field_row("Client's goals for therapy:", lines=1)
    p.footer()
    return p


def therapist_session_notes():
    p = OnePager("Therapy Session Notes (DAP)", "Data · Assessment · Plan", (115, 65, 85))
    p.header()
    p.field_row("Client: ______________________    Session #: ______    Date: __________", lines=1)
    p.section("D — Data")
    p.field_row("What was discussed / observed:", lines=3)
    p.section("A — Assessment")
    p.field_row("Clinical impressions / progress:", lines=2)
    p.section("P — Plan")
    p.field_row("Homework + next session focus:", lines=2)
    p.section("Admin")
    p.field_row("Billing code: __________    Next session: __________", lines=1)
    p.footer()
    return p


# ---- Trades / construction ------------------------------------------------
def contractor_estimate():
    p = OnePager("Job Estimate Sheet", "Line-item the work before you quote", (140, 90, 30))
    p.header()
    p.field_row("Client: ______________________    Job: ______________________    Date: __________", lines=1)
    p.section("Estimate")
    p.table(
        ["Line item", "Description", "Qty", "Unit price", "Total"],
        [["", "", "", "", ""] for _ in range(9)],
        [26, 66, 18, 30, 51.9],
    )
    p.section("Totals")
    p.body("Labor $______    Materials $______    Subtotal $______    Markup ______%    TOTAL $______", size=8.2)
    p.section("Terms")
    p.field_row("Valid until: __________    Payment schedule: ____________________", lines=1)
    p.footer()
    return p


def contractor_punch_list():
    p = OnePager("Punch List", "The final fixes before sign-off", (135, 85, 25))
    p.header()
    p.field_row("Project: ______________________    Date: __________    Walkthrough with: ______________", lines=1)
    p.section("Items")
    p.table(
        ["Area", "Issue", "Assigned to", "Due", "Done"],
        [["", "", "", "", ""] for _ in range(13)],
        [40, 66, 34, 24, 27.9],
    )
    p.footer()
    return p


def contractor_job_cost():
    p = OnePager("Job Costing Log", "Labor, materials, and profit per job", (145, 95, 35))
    p.header()
    p.field_row("Job: ______________________    Contract amount: $__________", lines=1)
    p.section("Costs")
    p.table(
        ["Date", "Category", "Description", "Amount"],
        [["", "Labor / Material / Sub / Other", "", ""] for _ in range(11)],
        [22, 46, 76, 47.9],
    )
    p.section("Result")
    p.body("Total costs $______    Gross profit $______ (______%)    Over/under budget $______", size=8.2)
    p.footer()
    return p


# ---- Design / creative ----------------------------------------------------
def architect_project_brief():
    p = OnePager("Project Brief", "Client, program, and constraints, defined", (80, 60, 40))
    p.header()
    p.field_row("Project: ______________________    Client: ______________________    Date: __________", lines=1)
    p.section("Program")
    p.field_row("Function / use: ____________________    Size (sq ft): ______    Floors: ______", lines=1)
    p.section("Requirements")
    p.field_row("Must-haves:", lines=2)
    p.field_row("Nice-to-haves:", lines=1)
    p.section("Site & constraints")
    p.field_row("Site: ____________________    Budget: $______    Zoning: ____________________", lines=1)
    p.section("Deliverables & schedule")
    p.field_row("Concept: __________    Schematic: __________    Final: __________", lines=1)
    p.footer()
    return p


def photographer_session():
    p = OnePager("Photo Shoot Planner", "Shot list, gear, and deliverables", (150, 70, 110))
    p.header()
    p.field_row("Client: ______________________    Shoot date: __________    Location: ____________________", lines=1)
    p.section("Shot list")
    p.table(
        ["Shot", "Location / setup", "Lens / settings", "Done"],
        [["", "", "", ""] for _ in range(9)],
        [44, 68, 48, 31.9],
    )
    p.section("Gear checklist")
    p.checklist(["Body + backup", "Lenses", "Batteries", "Memory cards", "Flash / modifiers", "Tripod", "Charger"], cols=2)
    p.section("Deliverables")
    p.field_row("Images due: __________    Format: ____________    Licensing: ____________________", lines=1)
    p.footer()
    return p


# ---- Property management --------------------------------------------------
def property_manager_tenant_ledger():
    p = OnePager("Tenant Ledger", "Rent, deposits, and balance per unit", (40, 95, 90))
    p.header()
    p.field_row("Property: ______________________    Unit: ______    Tenant: ______________________", lines=1)
    p.section("Ledger")
    p.table(
        ["Date", "Charge", "Payment", "Balance", "Notes"],
        [["", "", "", "", ""] for _ in range(12)],
        [22, 46, 46, 34, 43.9],
    )
    p.section("Summary")
    p.body("Security deposit: $______    Balance due: $______    Lease end: __________", size=8.2)
    p.footer()
    return p


def property_manager_maint_request():
    p = OnePager("Maintenance Request Log", "Every request, tracked to completion", (45, 90, 95))
    p.header()
    p.field_row("Property: ______________________    Month: __________", lines=1)
    p.section("Requests")
    p.table(
        ["Date", "Unit", "Issue", "Priority", "Vendor", "Status"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [22, 18, 56, 20, 40, 35.9],
    )
    p.section("Escalations")
    p.field_row("Emergency calls: ______________________________    Overdue: ____________________", lines=1)
    p.footer()
    return p


# ---- Other high-income professions ----------------------------------------
def loan_officer_pipeline():
    p = OnePager("Mortgage Pipeline Tracker", "Every loan from lead to closing", (25, 75, 120))
    p.header()
    p.field_row("Loan officer: ______________________    Month: __________    Goal: $__________", lines=1)
    p.section("Pipeline")
    p.table(
        ["Borrower", "Loan amount", "Type", "Rate lock", "Stage", "Close date"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [40, 28, 28, 24, 34, 37.9],
    )
    p.section("Summary")
    p.body("Funded $______    In pipeline $______    Applications ______    Conversion ______%", size=8.2)
    p.footer()
    return p


def insurance_lead_tracker():
    p = OnePager("Insurance Lead Tracker", "Quotes, follow-ups, and closes", (20, 85, 100))
    p.header()
    p.field_row("Agent: ______________________    Product: Auto / Home / Life / Health    Month: __________", lines=1)
    p.section("Leads")
    p.table(
        ["Lead", "Product", "Quote sent", "Premium", "Status", "Follow-up"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [40, 30, 26, 26, 30, 39.9],
    )
    p.section("Pipeline")
    p.body("Quotes out: ______    Closing: ______    Won: ______    Win rate ______%", size=8.2)
    p.footer()
    return p


def event_planner_timeline():
    p = OnePager("Event Planning Timeline", "Every task, owner, and deadline", (160, 60, 90))
    p.header()
    p.field_row("Event: ______________________    Date: __________    Budget: $__________", lines=1)
    p.section("Timeline")
    p.table(
        ["When", "Task", "Owner", "Done"],
        [["12+ weeks out", "", "", ""],
         ["8 weeks out", "", "", ""],
         ["4 weeks out", "", "", ""],
         ["2 weeks out", "", "", ""],
         ["1 week out", "", "", ""],
         ["Day before", "", "", ""],
         ["Day of", "", "", ""],
         ["After", "", "", ""]],
        [36, 80, 40, 35.9],
    )
    p.section("Vendors")
    p.field_row("Venue: ____________    Catering: ____________    AV: ____________    Other: ____________", lines=1)
    p.footer()
    return p


def hr_onboarding_checklist():
    p = OnePager("Employee Onboarding Checklist", "Nothing falls through the cracks", (50, 70, 120))
    p.header()
    p.field_row("New hire: ______________________    Start date: __________    Role: ____________________", lines=1)
    p.section("Before day 1")
    p.checklist(["Offer signed", "Background check", "Equipment ordered", "Accounts created", "Desk / access", "Welcome email"], cols=2)
    p.section("Day 1")
    p.checklist(["Office tour", "Team intro", "HR paperwork", "Benefits enrollment", "Tools setup", "Buddy assigned"], cols=2)
    p.section("First month")
    p.checklist(["30-60-90 plan set", "Training schedule", "Week 1 check-in", "Week 4 check-in", "Manager 1:1s"], cols=2)
    p.footer()
    return p


# ===========================================================================
# Batch 6 — "All professions" (comprehensive coverage)
# ===========================================================================

def teacher_lesson_plan():
    p = OnePager("Lesson Plan", "Objective, materials, and flow for one class", (20, 90, 110))
    p.header()
    p.field_row("Teacher: ______________    Subject: ______________    Date: __________    Grade: ______", lines=1)
    p.section("Objective")
    p.field_row("Students will be able to:", lines=2)
    p.section("Materials")
    p.field_row("", lines=1)
    p.section("Lesson flow")
    p.table(
        ["Time", "Activity", "Notes"],
        [["Warm-up", "", ""], ["Instruction", "", ""], ["Guided practice", "", ""],
         ["Independent work", "", ""], ["Wrap-up / exit ticket", "", ""]],
        [40, 76, 75.9],
    )
    p.section("Assessment")
    p.field_row("How I'll know they got it:", lines=1)
    p.footer()
    return p


def teacher_grade_tracker():
    p = OnePager("Grade Tracker", "Assignments and scores per student", (15, 85, 105))
    p.header()
    p.field_row("Class: ______________________    Term: __________", lines=1)
    p.section("Grades")
    p.table(
        ["Student", "A1", "A2", "A3", "A4", "A5", "Avg"],
        [["", "", "", "", "", "", ""] for _ in range(12)],
        [72, 20, 20, 20, 20, 20, 19.9],
    )
    p.footer()
    return p


def substitute_teacher_info():
    p = OnePager("Substitute Teacher Info", "Everything a sub needs, one sheet", (20, 95, 115))
    p.header()
    p.field_row("Teacher: ______________    Room: ______    Date: __________", lines=1)
    p.section("Class schedule")
    p.table(
        ["Period", "Class", "Notes"],
        [["", "", ""] for _ in range(7)],
        [24, 70, 97.9],
    )
    p.section("Procedures")
    p.field_row("Attendance: ____________    Bathroom policy: ____________    Helpers: ____________", lines=1)
    p.section("Important")
    p.field_row("Office ext: ________    Students with needs: ______________________________", lines=1)
    p.footer()
    return p


def homeschool_planner():
    p = OnePager("Homeschool Weekly Planner", "Subjects, lessons, and field trips", (25, 100, 120))
    p.header()
    p.field_row("Week of: __________    Student(s): ______________________", lines=1)
    p.section("Weekly plan")
    p.table(
        ["Day", "Math", "Reading", "Science", "History", "Other"],
        [["Mon", "", "", "", "", ""], ["Tue", "", "", "", "", ""], ["Wed", "", "", "", "", ""],
         ["Thu", "", "", "", "", ""], ["Fri", "", "", "", "", ""]],
        [20, 34.4, 34.4, 34.4, 34.4, 34.4],
    )
    p.section("Extras")
    p.field_row("Field trips: ______________    Co-op: ______________    Library: ______________", lines=1)
    p.footer()
    return p


def electrician_job_log():
    p = OnePager("Electrician Job & Service Log", "Jobs, parts, and hours", (120, 80, 30))
    p.header()
    p.field_row("Electrician: ______________________    License #: ______________________", lines=1)
    p.section("Jobs")
    p.table(
        ["Date", "Customer", "Work performed", "Hours", "Parts", "Total"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [20, 40, 60, 18, 24, 29.9],
    )
    p.footer()
    return p


def plumber_invoice():
    p = OnePager("Plumbing Job & Invoice", "Work done, parts, and total due", (110, 90, 40))
    p.header()
    p.field_row("Plumber: ______________________    Invoice #: ______    Date: __________", lines=1)
    p.section("Customer")
    p.field_row("Name: ______________________    Address: ______________________________    Phone: ____________", lines=1)
    p.section("Work & parts")
    p.table(
        ["Description", "Qty", "Rate", "Amount"],
        [["", "", "", ""] for _ in range(9)],
        [84, 24, 34, 49.9],
    )
    p.section("Total")
    p.body("Labor $______    Parts $______    Tax $______    TOTAL DUE $______", size=8.4)
    p.footer()
    return p


def hvac_service_log():
    p = OnePager("HVAC Service Log", "Maintenance visits and repairs", (30, 90, 130))
    p.header()
    p.field_row("Technician: ______________________    Company: ______________________", lines=1)
    p.section("Service calls")
    p.table(
        ["Date", "Customer", "System", "Work done", "Parts", "Next service"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [20, 38, 28, 52, 26, 27.9],
    )
    p.footer()
    return p


def landscaper_schedule():
    p = OnePager("Lawn & Landscape Schedule", "Properties, services, and billing", (20, 120, 70))
    p.header()
    p.field_row("Company: ______________________    Week: __________", lines=1)
    p.section("Schedule")
    p.table(
        ["Day", "Property", "Service", "Crew", "Done", "Billed"],
        [["Mon", "", "", "", "", ""], ["Tue", "", "", "", "", ""], ["Wed", "", "", "", "", ""],
         ["Thu", "", "", "", "", ""], ["Fri", "", "", "", "", ""], ["Sat", "", "", "", "", ""]],
        [20, 46, 52, 24, 22, 27.9],
    )
    p.footer()
    return p


def restaurant_food_cost():
    p = OnePager("Food Cost & Inventory", "Track ingredients and margins", (150, 60, 30))
    p.header()
    p.field_row("Restaurant: ______________________    Week: __________", lines=1)
    p.section("Inventory & cost")
    p.table(
        ["Item", "On hand", "Ordered", "Cost", "Par level"],
        [["", "", "", "", ""] for _ in range(12)],
        [52, 30, 30, 30, 49.9],
    )
    p.section("Food cost")
    p.body("Sales this week $______    Food cost $______    Food cost % ______%    Waste $______", size=8.2)
    p.footer()
    return p


def kitchen_prep_list():
    p = OnePager("Kitchen Prep List", "What to prep, by station, for service", (140, 50, 25))
    p.header()
    p.field_row("Date: __________    Shift: Lunch / Dinner    Head count: ______", lines=1)
    p.section("Prep tasks")
    p.table(
        ["Station", "Task", "Qty", "Done"],
        [["", "", "", ""] for _ in range(13)],
        [44, 78, 34, 35.9],
    )
    p.section("Line-up")
    p.field_row("86'd items: ______________________________    Specials: ____________________", lines=1)
    p.footer()
    return p


def catering_order():
    p = OnePager("Catering Order Form", "Menu, count, and logistics", (160, 70, 35))
    p.header()
    p.field_row("Client: ______________________    Event date: __________    Guests: ______", lines=1)
    p.section("Order")
    p.table(
        ["Item", "Serves", "Qty", "Price", "Total"],
        [["", "", "", "", ""] for _ in range(9)],
        [62, 22, 22, 28, 57.9],
    )
    p.section("Details")
    p.field_row("Delivery time: ______    Address: ______________________    Dietary: ____________________", lines=1)
    p.section("Total")
    p.body("Subtotal $______    Delivery $______    Deposit $______    Balance due $______", size=8.2)
    p.footer()
    return p


def bakery_order():
    p = OnePager("Custom Cake & Bakery Order", "Design, flavors, and pickup", (170, 60, 90))
    p.header()
    p.field_row("Customer: ______________________    Pickup date: __________    Phone: ____________", lines=1)
    p.section("Order details")
    p.field_row("Item (cake / cookies / etc.): ____________________    Size / servings: ____________", lines=1)
    p.field_row("Flavor: ______________    Filling: ______________    Frosting: ______________", lines=1)
    p.field_row("Design / theme / colors:", lines=2)
    p.field_row("Writing on cake:", lines=1)
    p.section("Payment")
    p.field_row("Deposit $______    Balance $______    Paid: ______    Notes: ____________________", lines=1)
    p.footer()
    return p


def bar_inventory():
    p = OnePager("Bar Inventory Log", "Stock, par, and weekly usage", (120, 40, 60))
    p.header()
    p.field_row("Bar: ______________________    Date: __________    Taken by: ____________________", lines=1)
    p.section("Inventory")
    p.table(
        ["Item", "Opening", "Received", "Closing", "Used"],
        [["", "", "", "", ""] for _ in range(13)],
        [60, 32, 32, 32, 35.9],
    )
    p.footer()
    return p


def massage_therapy_intake():
    p = OnePager("Massage Therapy Intake", "History, goals, and session notes", (20, 100, 110))
    p.header()
    p.field_row("Client: ______________________    Date: __________    Therapist: ____________________", lines=1)
    p.section("Health & history")
    p.field_row("Conditions / injuries:", lines=1)
    p.field_row("Medications / contraindications:", lines=1)
    p.section("Goals & focus")
    p.field_row("Areas of focus:", lines=1)
    p.field_row("Pressure preference: ____________________    Goals: ____________________", lines=1)
    p.section("Session notes")
    p.field_row("Work done / response:", lines=2)
    p.field_row("Recommendations + next session: ______________________________", lines=1)
    p.footer()
    return p


def esthetician_client_log():
    p = OnePager("Esthetician Client Log", "Skin history and treatments", (150, 50, 90))
    p.header()
    p.field_row("Client: ______________________    Skin type: ______________________", lines=1)
    p.section("Skin history")
    p.field_row("Concerns: ____________________    Allergies / sensitivities: ____________________", lines=1)
    p.section("Treatment log")
    p.table(
        ["Date", "Treatment", "Products used", "Result", "Next visit"],
        [["", "", "", "", ""] for _ in range(10)],
        [20, 44, 50, 40, 37.9],
    )
    p.footer()
    return p


def nutrition_coach_plan():
    p = OnePager("Nutrition Coaching Plan", "Goals, targets, and check-ins", (20, 120, 80))
    p.header()
    p.field_row("Client: ______________________    Coach: ______________________    Start: __________", lines=1)
    p.section("Plan")
    p.field_row("Goal: ____________________    Calories: ______    Protein: ______g    Carbs: ______g    Fat: ______g", lines=1)
    p.section("Weekly tracking")
    p.table(
        ["Week", "Weight", "Adherence", "Notes"],
        [["", "", "", ""] for _ in range(8)],
        [24, 30, 30, 107.9],
    )
    p.section("Habits to build")
    p.field_row("1. ____________   2. ____________   3. ____________", lines=1)
    p.footer()
    return p


def chiropractic_note():
    p = OnePager("Chiropractic Visit Note", "Complaint, findings, and adjustment", (25, 90, 115))
    p.header()
    p.field_row("Patient: ______________________    Visit: ______    Date: __________", lines=1)
    p.section("Subjective")
    p.field_row("Complaint / progress since last visit:", lines=2)
    p.section("Objective")
    p.field_row("Findings / palpation / ROM:", lines=2)
    p.section("Treatment & plan")
    p.field_row("Adjustment / therapy performed:", lines=2)
    p.field_row("Home care + next visit: ______________________________", lines=1)
    p.footer()
    return p


def salon_client_log():
    p = OnePager("Salon Client Card", "Color formula, cuts, and preferences", (130, 40, 80))
    p.header()
    p.field_row("Client: ______________________    Stylist: ______________________", lines=1)
    p.section("Hair record")
    p.field_row("Natural: ____________    History: ____________    Allergies: ____________", lines=1)
    p.section("Color formula")
    p.table(
        ["Date", "Color / formula", "Developer", "Processing", "Result"],
        [["", "", "", "", ""] for _ in range(9)],
        [20, 56, 30, 30, 55.9],
    )
    p.section("Notes & next visit")
    p.field_row("Preferences: ______________________________    Next: __________", lines=1)
    p.footer()
    return p


def musician_gig_log():
    p = OnePager("Musician Gig & Setlist Log", "Bookings, pay, and setlists", (130, 60, 130))
    p.header()
    p.field_row("Artist / band: ______________________    Contact: ______________________", lines=1)
    p.section("Gigs")
    p.table(
        ["Date", "Venue", "Pay", "Load-in", "Setlist / notes"],
        [["", "", "", "", ""] for _ in range(11)],
        [20, 46, 22, 22, 81.9],
    )
    p.footer()
    return p


def writer_article_tracker():
    p = OnePager("Writer Pitch & Article Tracker", "Pitches, deadlines, and pay", (40, 70, 140))
    p.header()
    p.field_row("Writer: ______________________    Rate: $______ / word    Month: __________", lines=1)
    p.section("Pitches & articles")
    p.table(
        ["Outlet", "Piece", "Pitched", "Due", "Status", "Pay"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [40, 44, 20, 20, 30, 37.9],
    )
    p.section("Totals")
    p.body("Earned $______    In progress $______    Pitches out: ______", size=8.2)
    p.footer()
    return p


def editor_style_sheet():
    p = OnePager("Editorial Style Sheet", "Keep a publication consistent", (60, 60, 120))
    p.header()
    p.field_row("Publication: ______________________    Updated: __________", lines=1)
    p.section("Style decisions")
    p.table(
        ["Category", "Rule", "Example"],
        [["Numbers", "", ""], ["Dates", "", ""], ["Capitalization", "", ""], ["Oxford comma", "", ""],
         ["Quotes", "", ""], ["Headings", "", ""], ["Preferred terms", "", ""]],
        [46, 72, 73.9],
    )
    p.footer()
    return p


def tattoo_aftercare():
    p = OnePager("Tattoo Consent & Aftercare", "Consent, design, and healing instructions", (20, 70, 90))
    p.header()
    p.field_row("Artist: ______________________    Client: ______________________    Date: __________", lines=1)
    p.section("Tattoo details")
    p.field_row("Design / placement: ____________________    Size: ______    Price: $______    Deposit: $______", lines=1)
    p.section("Aftercare (client keeps)")
    p.checklist(["Leave bandage on 2-4 hrs", "Wash gently, pat dry", "Thin layer of ointment", "No sun / swimming 2-3 wks", "Don't pick or scratch", "Wear loose clothing"], cols=2)
    p.section("Consent")
    p.field_row("Client initials: ______    Artist initials: ______    Aftercare explained: ______", lines=1)
    p.footer()
    return p


def dj_gig_log():
    p = OnePager("DJ Gig & Playlist Log", "Bookings, requests, and crowd notes", (90, 50, 140))
    p.header()
    p.field_row("DJ: ______________________    Contact: ______________________", lines=1)
    p.section("Gigs")
    p.table(
        ["Date", "Event", "Venue", "Pay", "Crowd / requests"],
        [["", "", "", "", ""] for _ in range(11)],
        [20, 42, 46, 22, 61.9],
    )
    p.footer()
    return p


def freelance_dev_log():
    p = OnePager("Freelance Dev Project Log", "Hours, tasks, and per-client billing", (40, 70, 140))
    p.header()
    p.field_row("Developer: ______________________    Rate: $______ / hr    Week: __________", lines=1)
    p.section("Time & tasks")
    p.table(
        ["Date", "Client", "Task", "Hours", "Amount"],
        [["", "", "", "", ""] for _ in range(12)],
        [20, 42, 74, 22, 33.9],
    )
    p.section("Weekly total")
    p.body("Hours: ______    Billable: $______", size=8.4)
    p.footer()
    return p


def qa_test_log():
    p = OnePager("QA Test Case Log", "Tests run, results, and bugs", (20, 80, 130))
    p.header()
    p.field_row("Project: ______________________    Build: ______    Tester: ____________________", lines=1)
    p.section("Test cases")
    p.table(
        ["ID", "Test case", "Expected", "Result", "Bug #"],
        [["", "", "", "", ""] for _ in range(11)],
        [12, 66, 48, 34, 31.9],
    )
    p.section("Summary")
    p.body("Passed: ______    Failed: ______    Blocked: ______    Bugs filed: ______", size=8.2)
    p.footer()
    return p


def product_roadmap():
    p = OnePager("Product Roadmap", "Now · Next · Later, on one page", (60, 50, 120))
    p.header()
    p.field_row("Product: ______________________    Owner: ______________________    Quarter: __________", lines=1)
    p.section("Now (this quarter)")
    p.field_row("1. ____________________   2. ____________________   3. ____________________", lines=2)
    p.section("Next (next quarter)")
    p.field_row("1. ____________________   2. ____________________   3. ____________________", lines=2)
    p.section("Later (future)")
    p.field_row("1. ____________________   2. ____________________", lines=1)
    p.section("Metrics")
    p.field_row("North star metric: ____________________    Release date: __________", lines=1)
    p.footer()
    return p


def it_asset_inventory():
    p = OnePager("IT Asset Inventory", "Hardware, software, and assignments", (30, 60, 120))
    p.header()
    p.field_row("Company: ______________________    Updated: __________", lines=1)
    p.section("Assets")
    p.table(
        ["Asset", "Type", "Serial #", "Assigned to", "Status"],
        [["", "", "", "", ""] for _ in range(12)],
        [44, 30, 44, 40, 33.9],
    )
    p.section("Software / licenses")
    p.field_row("License keys & renewals: ______________________________", lines=1)
    p.footer()
    return p


def sales_call_log():
    p = OnePager("Sales Call & Prospecting Log", "Calls, outcomes, and follow-ups", (20, 80, 120))
    p.header()
    p.field_row("Rep: ______________________    Week: __________    Calls goal: ______", lines=1)
    p.section("Calls")
    p.table(
        ["Date", "Lead", "Outcome", "Next step", "Notes"],
        [["", "", "", "", ""] for _ in range(12)],
        [20, 42, 40, 40, 49.9],
    )
    p.section("Stats")
    p.body("Calls: ______    Conversations: ______    Meetings booked: ______    Conversion ______%", size=8.2)
    p.footer()
    return p


def recruiter_pipeline():
    p = OnePager("Recruiter Pipeline", "Candidates from sourcing to hire", (25, 75, 120))
    p.header()
    p.field_row("Role: ______________________    Recruiter: ______________________", lines=1)
    p.section("Pipeline")
    p.table(
        ["Candidate", "Source", "Stage", "Interview", "Offer", "Notes"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [44, 30, 28, 24, 20, 45.9],
    )
    p.footer()
    return p


def helpdesk_ticket_log():
    p = OnePager("Helpdesk Ticket Log", "Tickets, priority, and resolution", (30, 70, 130))
    p.header()
    p.field_row("Technician: ______________________    Week: __________", lines=1)
    p.section("Tickets")
    p.table(
        ["#", "User", "Issue", "Priority", "Status", "Resolution"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [10, 36, 50, 22, 26, 47.9],
    )
    p.footer()
    return p


def virtual_assistant_tasks():
    p = OnePager("VA Task & Client Log", "Tasks per client, tracked to done", (60, 55, 110))
    p.header()
    p.field_row("VA: ______________________    Week: __________    Rate: $______ / hr", lines=1)
    p.section("Tasks")
    p.table(
        ["Client", "Task", "Hours", "Due", "Done"],
        [["", "", "", "", ""] for _ in range(12)],
        [40, 70, 18, 24, 39.9],
    )
    p.section("Invoicing")
    p.body("Total hours: ______    Total billable: $______", size=8.2)
    p.footer()
    return p


def trucker_log():
    p = OnePager("Trucking Trip & Expense Log", "Miles, fuel, and per-trip cost", (60, 60, 100))
    p.header()
    p.field_row("Driver: ______________________    Truck #: ______    Week: __________", lines=1)
    p.section("Trips")
    p.table(
        ["Date", "From → To", "Miles", "Fuel $", "Tolls", "Notes"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [20, 48, 20, 22, 22, 59.9],
    )
    p.section("Totals")
    p.body("Miles: ______    Fuel: $______    Tolls: $______    Other: $______", size=8.2)
    p.footer()
    return p


def rideshare_income():
    p = OnePager("Rideshare & Delivery Income", "Trips, earnings, and expenses", (40, 90, 110))
    p.header()
    p.field_row("Driver: ______________________    App: Uber / Lyft / DoorDash / Other    Week: __________", lines=1)
    p.section("Daily earnings")
    p.table(
        ["Day", "Trips", "Fares", "Tips", "Miles", "Fuel"],
        [["", "", "", "", "", ""] for _ in range(7)],
        [24, 20, 30, 24, 20, 73.9],
    )
    p.section("Net")
    p.body("Gross $______    Expenses $______    Net $______    $/mile ______", size=8.2)
    p.footer()
    return p


def pilot_flight_log():
    p = OnePager("Pilot Flight Log", "Flights, hours, and currency", (20, 70, 100))
    p.header()
    p.field_row("Pilot: ______________________    Certificate: ______________________", lines=1)
    p.section("Flights")
    p.table(
        ["Date", "From → To", "Aircraft", "Hrs", "Landings", "Notes"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [20, 46, 40, 18, 22, 45.9],
    )
    p.section("Totals")
    p.body("Total time: ______    PIC: ______    Night: ______    Instrument: ______    Landings: ______", size=8.0)
    p.footer()
    return p


def delivery_route_log():
    p = OnePager("Delivery Route & Stop Log", "Stops, packages, and signatures", (20, 90, 90))
    p.header()
    p.field_row("Driver: ______________________    Route: ______    Date: __________", lines=1)
    p.section("Stops")
    p.table(
        ["Stop", "Address", "Packages", "Time", "Signed"],
        [["", "", "", "", ""] for _ in range(14)],
        [14, 70, 24, 20, 63.9],
    )
    p.footer()
    return p


def warehouse_inventory():
    p = OnePager("Warehouse Inventory", "Stock counts and locations", (50, 60, 100))
    p.header()
    p.field_row("Warehouse: ______________________    Count date: __________", lines=1)
    p.section("Inventory")
    p.table(
        ["SKU", "Item", "Location", "On hand", "Counted", "Diff"],
        [["", "", "", "", "", ""] for _ in range(13)],
        [30, 50, 34, 26, 26, 25.9],
    )
    p.footer()
    return p


def nanny_daily_log():
    p = OnePager("Nanny Daily Log", "Feedings, naps, and activities for parents", (90, 60, 120))
    p.header()
    p.field_row("Child: ______________________    Date: __________    Nanny: ____________________", lines=1)
    p.section("Daily log")
    p.field_row("Meals / bottles:", lines=2)
    p.field_row("Naps:", lines=1)
    p.field_row("Diapers / potty:", lines=1)
    p.section("Activities & mood")
    p.field_row("Activities: ____________________    Mood: ____________________", lines=1)
    p.section("Notes for parents")
    p.field_row("", lines=2)
    p.footer()
    return p


def elderly_care_log():
    p = OnePager("Elderly Care Daily Log", "Medications, meals, and wellbeing", (20, 90, 80))
    p.header()
    p.field_row("Name: ______________________    Date: __________    Caregiver: ____________________", lines=1)
    p.section("Daily log")
    p.field_row("Medications (time + dose):", lines=2)
    p.field_row("Meals & fluids:", lines=1)
    p.section("Wellbeing")
    p.field_row("Mood: ____________    Mobility: ____________    Appetite: ____________", lines=1)
    p.field_row("Appointments / visitors / notes:", lines=2)
    p.footer()
    return p


def pet_groomer_log():
    p = OnePager("Pet Groomer Client Card", "Breed, notes, and grooming history", (140, 80, 30))
    p.header()
    p.field_row("Pet: ______________________    Breed: ____________    Owner: ______________________", lines=1)
    p.section("Grooming record")
    p.table(
        ["Date", "Services", "Notes / behavior", "Next visit"],
        [["", "", "", ""] for _ in range(9)],
        [20, 52, 80, 39.9],
    )
    p.section("Preferences")
    p.field_row("Cut style: ____________________    Allergies / sensitivities: ____________________", lines=1)
    p.footer()
    return p


def housekeeping_checklist():
    p = OnePager("Housekeeping Service Checklist", "Room-by-room cleaning, signed off", (20, 110, 90))
    p.header()
    p.field_row("Client: ______________________    Cleaner: ______________________    Date: __________", lines=1)
    p.section("Checklist")
    p.checklist(["Kitchen — counters, sink, floors", "Bathrooms — full clean", "Bedrooms — beds, dust, vacuum", "Living areas — dust, vacuum", "Trash removed", "Mirrors & glass", "Laundry", "Restock supplies"], cols=2)
    p.section("Notes & sign-off")
    p.field_row("Notes: ______________________________    Time: ______    Signature: __________", lines=1)
    p.footer()
    return p


# ===========================================================================
# Batch 7 — Affluent & high-net-worth (collectors, owners, family office)
# ===========================================================================

# ---- A. Collectors & connoisseurs -----------------------------------------
def watch_collection_log():
    p = OnePager("Luxury Watch Collection", "Every reference, its cost basis, and current value", (30, 40, 60))
    p.header()
    p.field_row("Collector: ______________________    Insured under: ____________________    Policy #: ________", lines=1)
    p.section("Collection")
    p.table(
        ["Brand", "Reference", "Movement", "Purchased", "Cost", "Value", "Notes"],
        [["", "", "", "", "", "", ""] for _ in range(11)],
        [34, 34, 26, 22, 20, 22, 33.9],
    )
    p.section("Portfolio summary")
    p.body("Total cost $______    Current value $______    Gain/loss $______    Best performer: ____________________", size=8.2)
    p.section("Service & insurance")
    p.field_row("Next service due: __________    Next insurance renewal: __________    Appraisal date: __________", lines=1)
    p.footer()
    return p


def watch_service_log():
    p = OnePager("Watch Service & Insurance Log", "Service history, polish, and insured value per piece", (60, 45, 80))
    p.header()
    p.field_row("Collector: ______________________    Watchmaker: ______________________", lines=1)
    p.section("Service history")
    p.table(
        ["Watch", "Service", "Date", "Cost", "Watchmaker", "Next due"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [30, 44, 20, 20, 40, 37.9],
    )
    p.section("Insurance & valuation")
    p.field_row("Insured value $______    Policy #: ____________    Renewal: __________    Appraisal on file: ______", lines=1)
    p.footer()
    return p


def whiskey_collection_log():
    p = OnePager("Whiskey & Spirits Collection", "Distillery, cask, and what each bottle is worth", (120, 70, 30))
    p.header()
    p.field_row("Collector: ______________________    Cabinet / storage: ______________________", lines=1)
    p.section("Collection")
    p.table(
        ["Bottle", "Distillery", "Region", "Cask / ABV", "Opened", "Rating", "Value"],
        [["", "", "", "", "", "", ""] for _ in range(10)],
        [36, 30, 24, 24, 18, 20, 39.9],
    )
    p.section("Tasting highlight")
    p.field_row("Favorite pour this quarter: ______________________    Reason: ______________________________", lines=1)
    p.section("Collection value")
    p.body("Bottles ______    Total cost $______    Estimated value $______    To restock: ____________________", size=8.2)
    p.footer()
    return p


def wine_auction_log():
    p = OnePager("Wine Auction & Bid Log", "Track lots, estimates, and hammer prices", (120, 30, 45))
    p.header()
    p.field_row("Auction house: ______________________    Sale date: __________    Buyer #: ________", lines=1)
    p.section("Bids & results")
    p.table(
        ["Lot", "Wine", "Estimate", "Hammer", "Premium", "Total", "Notes"],
        [["", "", "", "", "", "", ""] for _ in range(11)],
        [16, 44, 24, 22, 24, 22, 39.9],
    )
    p.section("Budget & wishlist")
    p.field_row("Auction budget $______    Spent $______    Wishlist lots: ______________________________", lines=1)
    p.footer()
    return p


def coin_collection_log():
    p = OnePager("Coin Collection Inventory", "Grade, mintage, and value for every coin", (140, 90, 30))
    p.header()
    p.field_row("Collector: ______________________    Collection focus: ______________________", lines=1)
    p.section("Holdings")
    p.table(
        ["Coin", "Year", "Mint", "Grade", "Qty", "Cost", "Value"],
        [["", "", "", "", "", "", ""] for _ in range(12)],
        [40, 18, 22, 20, 14, 22, 55.9],
    )
    p.section("Summary")
    p.body("Pieces ______    Total cost $______    Catalog value $______    Insured: ______", size=8.2)
    p.footer()
    return p


def stamp_collection_log():
    p = OnePager("Stamp Collection Inventory", "Catalog every stamp, condition, and value", (20, 70, 90))
    p.header()
    p.field_row("Collector: ______________________    Album / country focus: ______________________", lines=1)
    p.section("Collection")
    p.table(
        ["Country", "Issue", "Scott #", "Condition", "Qty", "Value"],
        [["", "", "", "", "", ""] for _ in range(13)],
        [38, 40, 22, 24, 14, 53.9],
    )
    p.section("Notes")
    p.body("Total value $______    Mounted in album: ______    Needs cataloging: ______", size=8.2)
    p.footer()
    return p


def rare_book_log():
    p = OnePager("Rare & First Edition Library", "Edition, condition, and provenance", (60, 30, 90))
    p.header()
    p.field_row("Library: ______________________    Location: ______________________    Insured: ______", lines=1)
    p.section("Collection")
    p.table(
        ["Title", "Author", "Edition / Year", "Condition", "Signed?", "Value"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [50, 34, 30, 22, 20, 35.9],
    )
    p.section("Care")
    p.checklist(["Acid-free sleeves", "Climate control", "Shelf away from sun", "Handled with gloves", "Appraisal on file"], cols=2)
    p.footer()
    return p


def antiques_inventory():
    p = OnePager("Antiques & Heirloom Inventory", "Provenance and appraised value for insurance", (90, 60, 30))
    p.header()
    p.muted("For insurance claims — attach photos and appraisals where possible.")
    p.field_row("Household: ______________________    Appraiser: ______________________", lines=1)
    p.section("Inventory")
    p.table(
        ["Item", "Origin", "Age", "Appraisal", "Insured", "Location"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [40, 34, 20, 24, 20, 53.9],
    )
    p.section("Summary")
    p.body("Total appraised value $______    Policy #: ____________    Renewal: __________", size=8.2)
    p.footer()
    return p


def jewelry_inventory():
    p = OnePager("Fine Jewelry & Gemstone Log", "Appraisals, stones, and insurance", (120, 60, 80))
    p.header()
    p.field_row("Owner: ______________________    Jeweler / appraiser: ______________________", lines=1)
    p.section("Pieces")
    p.table(
        ["Piece", "Metal", "Stone(s)", "Appraised", "Policy", "Notes"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [32, 24, 40, 24, 30, 41.9],
    )
    p.section("Coverage")
    p.body("Total value $______    Scheduled on policy: ______    Vault / safe: ______    Photos: ______", size=8.2)
    p.footer()
    return p


def sneaker_collection_log():
    p = OnePager("Sneaker Collection & Resale Log", "Deadstock pairs, cost, and resale value", (200, 70, 30))
    p.header()
    p.field_row("Collector: ______________________    Size: ______    Storage: ______________________", lines=1)
    p.section("Collection")
    p.table(
        ["Sneaker", "Size", "Paid", "Market", "Sold", "Profit"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [52, 16, 24, 24, 20, 55.9],
    )
    p.section("Summary")
    p.body("Pairs ______    Cost $______    Market value $______    Realized profit $______", size=8.2)
    p.footer()
    return p


def luxury_goods_log():
    p = OnePager("Designer Handbag & Luxury Goods Log", "Authentication, retail, and resale value", (140, 40, 60))
    p.header()
    p.field_row("Owner: ______________________    Authenticator / source: ______________________", lines=1)
    p.section("Collection")
    p.table(
        ["Item", "Brand", "Retail", "Resale", "Auth", "Notes"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [42, 30, 24, 24, 20, 51.9],
    )
    p.section("Care & resale")
    p.field_row("Dust bags / boxes: ______    Next consignment: __________    Photos: ______", lines=1)
    p.footer()
    return p


def collector_car_log():
    p = OnePager("Collector Car Log", "Restoration, shows, and value", (120, 50, 20))
    p.header()
    p.field_row("Vehicle: ______________________    Year / make / model: ______________________    VIN: ______________", lines=1)
    p.section("Service & restoration")
    p.table(
        ["Date", "Service / restoration", "Cost", "Vendor", "Notes"],
        [["", "", "", "", ""] for _ in range(12)],
        [20, 60, 24, 40, 47.9],
    )
    p.section("Shows & valuation")
    p.field_row("Last show: __________    Awards: ______________________    Insured value $______    Mileage: ______", lines=1)
    p.footer()
    return p


def art_acquisition_log():
    p = OnePager("Art Acquisition & Advisory Log", "Budget, galleries, and every acquisition", (70, 40, 60))
    p.header()
    p.field_row("Collector: ______________________    Advisor: ______________________    Budget $__________", lines=1)
    p.section("Acquisitions")
    p.table(
        ["Piece", "Artist", "Gallery / auction", "Cost", "Insured value"],
        [["", "", "", "", ""] for _ in range(11)],
        [40, 30, 40, 26, 55.9],
    )
    p.section("Wishlist & relationships")
    p.field_row("Galleries to watch: ______________________    Pieces on wishlist: ______________________", lines=1)
    p.footer()
    return p


# ---- B. Equine & kennel ---------------------------------------------------
def horse_health_log():
    p = OnePager("Horse Health & Vet Log", "Vet, farrier, vaccines, and deworming", (20, 100, 60))
    p.header()
    p.field_row("Horse: ______________________    Breed: ____________    Age: ______    Owner: ____________________", lines=1)
    p.section("Health record")
    p.table(
        ["Date", "Type (vet / farrier / dent)", "Detail", "Cost", "Next due"],
        [["", "", "", "", ""] for _ in range(11)],
        [20, 40, 56, 22, 53.9],
    )
    p.section("Routine care")
    p.checklist(["Vaccines current", "Deworming scheduled", "Teeth floated", "Farrier every 6-8 wks", "Coggins on file", "Emergency kit stocked"], cols=2)
    p.footer()
    return p


def horse_training_log():
    p = OnePager("Horse Training & Ride Log", "Rides, lessons, and progress", (30, 90, 70))
    p.header()
    p.field_row("Horse: ______________________    Rider: ______________________    Discipline: ____________________", lines=1)
    p.section("Rides & lessons")
    p.table(
        ["Date", "Horse", "Discipline", "Duration", "Notes / progress"],
        [["", "", "", "", ""] for _ in range(13)],
        [20, 34, 40, 24, 73.9],
    )
    p.section("Goals")
    p.field_row("Current focus: ______________________    Next competition: __________    Trainer notes: ____________", lines=1)
    p.footer()
    return p


def horse_show_log():
    p = OnePager("Horse Show & Competition Log", "Classes, results, and points", (40, 80, 60))
    p.header()
    p.field_row("Horse: ______________________    Rider: ______________________    Division: ____________________", lines=1)
    p.section("Results")
    p.table(
        ["Date", "Show", "Class", "Horse", "Result", "Points"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [20, 44, 36, 34, 26, 31.9],
    )
    p.section("Season summary")
    p.body("Shows ______    Classes ______    Placings ______    Points ______    Qualifying for: ____________________", size=8.2)
    p.footer()
    return p


def horse_breeding_log():
    p = OnePager("Broodmare & Breeding Record", "Cycles, covers, and foaling", (120, 40, 60))
    p.header()
    p.field_row("Mare: ______________________    Stallion: ______________________    Breeding year: __________", lines=1)
    p.section("Breeding record")
    p.table(
        ["Date", "Event (cycle / cover / check)", "Detail", "Vet", "Notes"],
        [["", "", "", "", ""] for _ in range(11)],
        [20, 44, 52, 30, 45.9],
    )
    p.section("Foaling")
    p.field_row("Due date: __________    Foaling kit ready: ______    Vet on call: ______________________", lines=1)
    p.footer()
    return p


def stable_management_log():
    p = OnePager("Boarding & Stable Management", "Stalls, feed, turnout, and billing", (90, 60, 30))
    p.header()
    p.field_row("Stable: ______________________    Barn manager: ______________________    Month: __________", lines=1)
    p.section("Boarders")
    p.table(
        ["Horse", "Owner", "Stall", "Feed", "Turnout", "Board"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [40, 40, 18, 36, 30, 27.9],
    )
    p.section("Notes")
    p.body("Feed schedule: ______________________    Turnout groups: ______________________    Farrier / vet days: __________", size=8.0)
    p.footer()
    return p


def kennel_club_log():
    p = OnePager("Show Dog & Kennel Log", "Pedigree, health testing, and show results", (60, 50, 100))
    p.header()
    p.field_row("Kennel: ______________________    Breed: ______________________    Registry: ____________________", lines=1)
    p.section("Dogs")
    p.table(
        ["Dog", "Breed", "Reg #", "Health tests", "Shows", "Titles"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [36, 28, 26, 36, 26, 39.9],
    )
    p.section("Health testing")
    p.checklist(["OFA hips/elbows", "Eye cert (CERF/CAER)", "Cardiac", "DNA / breed panel", "Vaccines", "Microchip"], cols=2)
    p.footer()
    return p


# ---- C. Yachting & aviation ------------------------------------------------
def boat_maintenance_log():
    p = OnePager("Boat & Yacht Maintenance Log", "Engine hours, systems, and winterization", (20, 70, 110))
    p.header()
    p.field_row("Vessel: ______________________    Hull #: ______________    Engine hours: ______    Marina: ____________", lines=1)
    p.section("Maintenance")
    p.table(
        ["Date", "System", "Service", "Hours", "Cost", "Next due"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [20, 36, 50, 20, 22, 43.9],
    )
    p.section("Seasonal")
    p.checklist(["Bottom paint", "Winterize / de-winterize", "Anodes", "Bilge pumps", "Safety gear", "Registration / docs"], cols=2)
    p.footer()
    return p


def yacht_crew_log():
    p = OnePager("Yacht Crew & Staff Schedule", "Rotations, certifications, and charters", (30, 80, 120))
    p.header()
    p.field_row("Vessel: ______________________    Captain: ______________________    Season: __________", lines=1)
    p.section("Crew")
    p.table(
        ["Crew", "Role", "Rotation", "Cert expires", "Notes"],
        [["", "", "", "", ""] for _ in range(11)],
        [40, 40, 30, 30, 51.9],
    )
    p.section("Standards")
    p.checklist(["STCW current", "Medical / first aid", "Man overboard drill", "Fire drill", "Provisions stocked", "Guest preference sheet"], cols=2)
    p.footer()
    return p


def yacht_charter_log():
    p = OnePager("Yacht Charter Log", "Guests, provisions, fuel, and itinerary", (10, 80, 100))
    p.header()
    p.field_row("Vessel: ______________________    Charter season: __________    Charter rate: $__________", lines=1)
    p.section("Charters")
    p.table(
        ["Date", "Guest", "Ports", "Fuel", "Provisions", "Notes"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [20, 36, 36, 22, 30, 47.9],
    )
    p.section("Season summary")
    p.body("Charters ______    Revenue $______    Fuel $______    Provisions $______    Crew payroll $______", size=8.2)
    p.footer()
    return p


def aircraft_logbook():
    p = OnePager("Private Aircraft Logbook", "Flights, hours, and squawks", (15, 60, 100))
    p.header()
    p.field_row("Aircraft: ______________________    N-number / reg: ____________    Base: ____________________", lines=1)
    p.section("Flights")
    p.table(
        ["Date", "Route", "Hobbs", "Landings", "Fuel", "Squawks"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [20, 40, 20, 24, 22, 65.9],
    )
    p.section("Totals")
    p.body("Total time ______    Landings ______    Fuel burned ______    Next inspection (tach): ______", size=8.2)
    p.footer()
    return p


def charter_flight_log():
    p = OnePager("Charter Flight & Booking Log", "Every charter, crew, and invoice", (20, 80, 110))
    p.header()
    p.field_row("Operator: ______________________    Aircraft: ______________________    Month: __________", lines=1)
    p.section("Bookings")
    p.table(
        ["Date", "Client", "Route", "Aircraft", "Crew", "Invoice"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [20, 36, 40, 30, 26, 39.9],
    )
    p.section("Summary")
    p.body("Legs ______    Hours ______    Revenue $______    Fuel $______    Landing / fees $______", size=8.2)
    p.footer()
    return p


# ---- D. Wealth & family office --------------------------------------------
def family_office_dashboard():
    p = OnePager("Family Office Dashboard", "Entities, accounts, and advisors at a glance", (20, 50, 90))
    p.header()
    p.field_row("Family / principal: ______________________    Quarter: __________    Total AUM $__________", lines=1)
    p.section("Holdings")
    p.table(
        ["Entity", "Type", "Account(s)", "Custodian", "Advisor", "Value"],
        [["", "", "", "", "", ""] for _ in range(10)],
        [36, 28, 30, 34, 30, 33.9],
    )
    p.section("Cash & commitments")
    p.body("Operating cash $______    Pending capital calls $______    Tax estimate $______    Next review: __________", size=8.2)
    p.footer()
    return p


def trust_administration_log():
    p = OnePager("Trust Administration Checklist", "Funding, distributions, and filings", (60, 40, 90))
    p.header()
    p.muted("Reference only — work with trust counsel and a CPA in your jurisdiction.")
    p.field_row("Trust: ______________________    Grantor: ______________________    Trustee: ____________________", lines=1)
    p.section("Administration checklist")
    p.checklist(["Trust funded (assets retitled)", "EIN obtained", "Beneficiaries notified", "Distributions made", "Accounting prepared", "Tax return (1041) filed", "Crummey / ILIT notices", "Annual review"], cols=2)
    p.section("Key dates")
    p.field_row("Fiscal year end: __________    Tax deadline: __________    Next distribution: __________", lines=1)
    p.footer()
    return p


def philanthropy_log():
    p = OnePager("Philanthropy & Giving Log", "Donations, impact, and tax receipts", (100, 50, 60))
    p.header()
    p.field_row("Donor: ______________________    Giving year: __________    Budget $__________", lines=1)
    p.section("Donations")
    p.table(
        ["Date", "Organization", "Amount", "Receipt", "Impact / notes"],
        [["", "", "", "", ""] for _ in range(11)],
        [20, 40, 24, 20, 87.9],
    )
    p.section("Summary")
    p.body("Total given $______    Receipts on file: ______    Matching eligible: ______    Focus areas: ____________________", size=8.0)
    p.footer()
    return p


def private_banking_overview():
    p = OnePager("Private Banking & Accounts Overview", "Every account, balance, and contact", (25, 55, 85))
    p.header()
    p.field_row("Client: ______________________    Relationship manager: ______________________", lines=1)
    p.section("Accounts")
    p.table(
        ["Bank", "Account type", "Acct #", "Balance", "Advisor", "Contact"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [30, 30, 30, 26, 36, 39.9],
    )
    p.section("Consolidation")
    p.body("Total deposits $______    Total credit / loans $______    Rates to renegotiate: ____________________", size=8.2)
    p.footer()
    return p


def donor_advised_fund_log():
    p = OnePager("Donor-Advised Fund & Grant Log", "Contributions, grants, and balances", (90, 50, 60))
    p.header()
    p.field_row("DAF sponsor: ______________________    Account #: ____________    Advisors: ____________________", lines=1)
    p.section("Activity")
    p.table(
        ["Date", "Contribution / grant", "Organization", "Amount", "Balance"],
        [["", "", "", "", ""] for _ in range(12)],
        [20, 46, 46, 26, 53.9],
    )
    p.section("Summary")
    p.body("Contributions $______    Grants $______    Current balance $______    Successor advisors: ____________________", size=8.2)
    p.footer()
    return p


def syndication_tracker():
    p = OnePager("Real Estate Syndication Tracker", "Capital calls, distributions, and K-1s", (30, 60, 80))
    p.header()
    p.field_row("Investor: ______________________    Portfolio of deals: ______    Year: __________", lines=1)
    p.section("Deals")
    p.table(
        ["Deal", "Sponsor", "Capital", "Distributions", "K-1", "Notes"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [36, 32, 24, 28, 20, 51.9],
    )
    p.section("Performance")
    p.body("Committed $______    Called $______    Distributed $______    IRR ______%    Sponsors to review: ____________", size=8.0)
    p.footer()
    return p


def angel_investment_log():
    p = OnePager("Angel & VC Investment Log", "Deals, check size, and exits", (20, 90, 100))
    p.header()
    p.field_row("Investor / syndicate: ______________________    Annual budget $__________", lines=1)
    p.section("Portfolio")
    p.table(
        ["Company", "Date", "Check", "Stage", "Follow-on", "Exit"],
        [["", "", "", "", "", ""] for _ in range(11)],
        [44, 20, 22, 30, 26, 49.9],
    )
    p.section("Pipeline & exits")
    p.body("Deals reviewed ______    Invested ______    Exits $______    Multiple on invested ______x    Losses $______", size=8.0)
    p.footer()
    return p


def exchange_1031_log():
    p = OnePager("1031 Exchange Tracker", "45/180-day deadlines, every step", (20, 70, 90))
    p.header()
    p.muted("US reference only — verify current IRS rules with a qualified intermediary.")
    p.field_row("Relinquished property: ______________________    QI: ______________________    Sale date: __________", lines=1)
    p.section("Timeline checklist")
    p.checklist(["QI engaged before sale", "Funds to QI (never seller)", "45-day ID list filed", "180-day close", "Replacement identified", "Replacement closed", "Reinvest full net proceeds", "Reporting (Form 8824)"], cols=2)
    p.section("Replacement properties")
    p.table(
        ["Property", "Offer", "Close", "Status", "Notes"],
        [["", "", "", "", ""] for _ in range(6)],
        [40, 22, 22, 30, 77.9],
    )
    p.section("Deadlines")
    p.body("45-day ID by: __________    180-day close by: __________    Days remaining: ______", size=8.4)
    p.footer()
    return p


# ---- E. Concierge health & appearance -------------------------------------
def concierge_medicine_plan():
    p = OnePager("Concierge Medicine Plan", "Physician, care plan, and visits", (30, 80, 120))
    p.header()
    p.field_row("Patient: ______________________    Physician: ______________________    Membership: $______ / yr", lines=1)
    p.section("Care plan")
    p.table(
        ["Date", "Visit / test", "Result", "Follow-up"],
        [["", "", "", ""] for _ in range(12)],
        [20, 50, 50, 71.9],
    )
    p.section("Goals & notes")
    p.field_row("Health goals: ______________________    Next visit: __________    Referrals: ____________________", lines=1)
    p.footer()
    return p


def med_spa_plan():
    p = OnePager("Med Spa Treatment Plan", "Services, injectables, and intervals", (160, 60, 100))
    p.header()
    p.field_row("Client: ______________________    Provider: ______________________    Consent on file: ______", lines=1)
    p.section("Treatment log")
    p.table(
        ["Treatment", "Area", "Date", "Units", "Cost", "Next"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [40, 26, 20, 18, 22, 65.9],
    )
    p.section("Plan")
    p.body("Next appointment: __________    Package balance: $______    Contraindications: ____________________", size=8.2)
    p.footer()
    return p


def cosmetic_consult_log():
    p = OnePager("Cosmetic & Plastic Surgery Consult", "Procedures, quotes, and recovery", (140, 60, 60))
    p.header()
    p.field_row("Patient: ______________________    Surgeon: ______________________    Consult date: __________", lines=1)
    p.section("Procedures")
    p.table(
        ["Procedure", "Quote", "Date", "Recovery", "Notes"],
        [["", "", "", "", ""] for _ in range(10)],
        [44, 24, 20, 30, 73.9],
    )
    p.section("Decision")
    p.field_row("Scheduled: ______________________    Financing: ______________________    Pre-op done: ______", lines=1)
    p.footer()
    return p


def longevity_protocol():
    p = OnePager("Longevity & Anti-Aging Protocol", "Biomarkers, interventions, and milestones", (60, 90, 40))
    p.header()
    p.muted("Work with a physician before starting any intervention or supplement.")
    p.field_row("Name: ______________________    Coach / physician: ______________________    Baseline date: __________", lines=1)
    p.section("Biomarkers")
    p.table(
        ["Biomarker", "Baseline", "Target", "Latest", "Trend"],
        [["", "", "", "", ""] for _ in range(11)],
        [44, 30, 30, 30, 57.9],
    )
    p.section("Interventions")
    p.checklist(["Sleep 7-9h", "Strength training 2-3x", "Zone 2 cardio", "Protein target", "Fast / window", "HRV tracking", "Labs quarterly", "DEXA / body comp"], cols=2)
    p.footer()
    return p


def executive_physical_log():
    p = OnePager("Executive Physical & Screening Log", "Every screening, result, and follow-up", (20, 80, 110))
    p.header()
    p.field_row("Patient: ______________________    Clinic: ______________________    Program date: __________", lines=1)
    p.section("Screenings")
    p.table(
        ["Screening", "Date", "Result", "Range", "Next due"],
        [["", "", "", "", ""] for _ in range(13)],
        [52, 20, 36, 30, 53.9],
    )
    p.section("Follow-up")
    p.field_row("Recommendations: ______________________    Referrals: ______________________    Next: __________", lines=1)
    p.footer()
    return p


def premium_pt_plan():
    p = OnePager("Premium Personal Training Plan", "Program, sessions, and results", (40, 110, 90))
    p.header()
    p.field_row("Client: ______________________    Coach: ______________________    Package: ______ sessions", lines=1)
    p.section("Program")
    p.table(
        ["Week", "Focus", "Sessions", "Progress", "Notes"],
        [["", "", "", "", ""] for _ in range(12)],
        [20, 40, 26, 40, 65.9],
    )
    p.section("Metrics")
    p.body("Start weight ______    Goal ______    Body fat ______%    Strength PRs: ____________________", size=8.2)
    p.footer()
    return p


def wellness_retreat_planner():
    p = OnePager("Wellness Retreat Planner", "Destination, program, and logistics", (150, 90, 40))
    p.header()
    p.field_row("Destination: ______________________    Dates: ___/___/___  →  ___/___/___    Budget $__________", lines=1)
    p.section("Program")
    p.table(
        ["Day", "Session / activity", "Time", "Location", "Notes"],
        [["", "", "", "", ""] for _ in range(9)],
        [16, 56, 20, 46, 53.9],
    )
    p.section("Logistics")
    p.field_row("Lodging: ______________________    Meals / dietary: ______________________    Transfers: ____________________", lines=1)
    p.footer()
    return p


# ---- F. Luxury lifestyle & services ---------------------------------------
def private_chef_intake():
    p = OnePager("Private Chef Client Intake", "Preferences, dietary needs, and service plan", (120, 60, 30))
    p.header()
    p.field_row("Client: ______________________    Household size: ______    Service: Weekly / Event    Chef: ____________", lines=1)
    p.section("Preferences & dietary")
    p.checklist(["No allergies", "Dairy-free", "Gluten-free", "Vegetarian", "Pescatarian", "Keto / low-carb", "No pork", "No seafood"], cols=4)
    p.field_row("Favorite cuisines: ______________________    Dislikes: ______________________", lines=1)
    p.section("Service plan")
    p.table(
        ["Day", "Meal", "Menu / request", "Servings", "Notes"],
        [["", "", "", "", ""] for _ in range(8)],
        [20, 26, 66, 24, 55.9],
    )
    p.section("Logistics")
    p.field_row("Kitchen access: __________    Budget per week $______    Shopping: Chef / client    Storage: ______________", lines=1)
    p.footer()
    return p


def estate_staff_roster():
    p = OnePager("Estate & Household Staff Roster", "Every staff member, role, and schedule", (60, 60, 40))
    p.header()
    p.field_row("Estate: ______________________    Estate manager: ______________________", lines=1)
    p.section("Staff")
    p.table(
        ["Staff", "Role", "Schedule", "Pay", "Contact", "Notes"],
        [["", "", "", "", "", ""] for _ in range(12)],
        [36, 36, 30, 22, 34, 33.9],
    )
    p.section("Household")
    p.field_row("Payroll date: __________    Backup coverage: ______________________    Staff handbook signed: ______", lines=1)
    p.footer()
    return p


def concierge_service_log():
    p = OnePager("Concierge Request Log", "Bookings, reservations, and errands", (80, 50, 60))
    p.header()
    p.field_row("Client: ______________________    Concierge: ______________________    Week: __________", lines=1)
    p.section("Requests")
    p.table(
        ["Date", "Request", "Status", "Confirmation #", "Notes"],
        [["", "", "", "", ""] for _ in range(13)],
        [20, 52, 30, 40, 49.9],
    )
    p.section("Priorities")
    p.field_row("Top 3 today: 1. ____________   2. ____________   3. ____________", lines=1)
    p.footer()
    return p


def vacation_home_management():
    p = OnePager("Second Home Management", "Vendors, maintenance, and rentals", (20, 90, 60))
    p.header()
    p.field_row("Property: ______________________    Location: ______________________    Managed by: ____________________", lines=1)
    p.section("Vendors & maintenance")
    p.table(
        ["Vendor", "Service", "Schedule", "Cost", "Contact"],
        [["", "", "", "", ""] for _ in range(12)],
        [40, 40, 30, 26, 55.9],
    )
    p.section("Rentals & use")
    p.field_row("Rental platform: ______________________    Rate $______ / night    Owner stays: ____________________", lines=1)
    p.footer()
    return p


def private_club_log():
    p = OnePager("Private Club & Membership Log", "Dues, reservations, and guest passes", (30, 60, 70))
    p.header()
    p.field_row("Member: ______________________    Family memberships: ______________________", lines=1)
    p.section("Clubs")
    p.table(
        ["Club", "Dues", "Renewal", "Benefits", "Notes"],
        [["", "", "", "", ""] for _ in range(10)],
        [36, 22, 24, 60, 49.9],
    )
    p.section("Reservations")
    p.field_row("Tee times: ______________________    Dining: ______________________    Guest passes used: ______ / ______", lines=1)
    p.footer()
    return p


def bespoke_tailor_log():
    p = OnePager("Bespoke Tailoring & Wardrobe Log", "Measurements, commissions, and fittings", (80, 50, 30))
    p.header()
    p.field_row("Client: ______________________    Tailor: ______________________    Last fitting: __________", lines=1)
    p.section("Measurements")
    p.field_row("Chest ______    Waist ______    Hips ______    Inseam ______    Sleeve ______    Shoulder ______", lines=1)
    p.section("Commissions")
    p.table(
        ["Commission", "Fabric", "Fittings", "Cost", "Status"],
        [["", "", "", "", ""] for _ in range(9)],
        [46, 36, 26, 24, 59.9],
    )
    p.section("Wardrobe")
    p.field_row("Pieces in rotation: ______    To alter: ______________________    To commission: ____________________", lines=1)
    p.footer()
    return p


def interior_design_brief():
    p = OnePager("Interior Design Client Brief", "Rooms, budget, and style direction", (90, 60, 60))
    p.header()
    p.field_row("Client: ______________________    Property: ______________________    Designer: ____________________", lines=1)
    p.section("Style direction")
    p.checklist(["Modern / minimal", "Transitional", "Traditional", "Coastal", "Industrial", "Japandi", "Maximalist", "Organic"], cols=4)
    p.section("Rooms & scope")
    p.table(
        ["Room", "Scope", "Budget", "Status"],
        [["", "", "", ""] for _ in range(9)],
        [40, 66, 30, 55.9],
    )
    p.section("Project")
    p.field_row("Total budget $______    Timeline: __________    Key pieces to source: ____________________", lines=1)
    p.footer()
    return p


def estate_landscape_plan():
    p = OnePager("Estate Landscape & Garden Plan", "Zones, plantings, and seasonal care", (30, 100, 40))
    p.header()
    p.field_row("Property: ______________________    Landscape architect: ______________________    Zone: ______", lines=1)
    p.section("Plan")
    p.table(
        ["Zone", "Planting / feature", "Season", "Task", "Done"],
        [["", "", "", "", ""] for _ in range(11)],
        [40, 52, 24, 46, 29.9],
    )
    p.section("Care")
    p.checklist(["Irrigation check", "Pruning", "Fertilization", "Pest / disease scout", "Seasonal color", "Lighting"], cols=2)
    p.footer()
    return p


def ski_trip_planner():
    p = OnePager("Ski & Alpine Trip Planner", "Lift tickets, lessons, and gear", (20, 80, 120))
    p.header()
    p.field_row("Resort: ______________________    Dates: ___/___/___  →  ___/___/___    Pass type: ________________", lines=1)
    p.section("Daily plan")
    p.table(
        ["Day", "Mountain / area", "Tickets", "Lessons", "Gear"],
        [["", "", "", "", ""] for _ in range(9)],
        [16, 48, 40, 40, 47.9],
    )
    p.section("Logistics")
    p.field_row("Lodging: ______________________    Rentals: ______________________    Après / dining: ____________________", lines=1)
    p.footer()
    return p


def safari_planner():
    p = OnePager("Luxury Safari Planner", "Camps, wildlife, and logistics", (140, 90, 30))
    p.header()
    p.field_row("Destination: ______________________    Dates: ___/___/___  →  ___/___/___    Operator: ________________", lines=1)
    p.section("Itinerary")
    p.table(
        ["Day", "Camp / lodge", "Game drives", "Notes"],
        [["", "", "", ""] for _ in range(9)],
        [16, 50, 50, 75.9],
    )
    p.section("Prep & logistics")
    p.checklist(["Visas", "Vaccinations / prophylaxis", "Camera + lenses", "Neutral clothing", "Travel insurance", "Binoculars"], cols=2)
    p.field_row("Packing list: ______________________    Emergency contact: ______________________", lines=1)
    p.footer()
    return p


def smart_home_inventory():
    p = OnePager("Smart Home & AV System Inventory", "Devices, accounts, and integrator contacts", (40, 60, 100))
    p.header()
    p.field_row("Property: ______________________    Integrator: ______________________    Network SSID: ____________", lines=1)
    p.section("Devices")
    p.table(
        ["Device", "Room", "Hub / app", "Credentials", "Integrator"],
        [["", "", "", "", ""] for _ in range(12)],
        [40, 30, 36, 40, 45.9],
    )
    p.section("Maintenance")
    p.field_row("Firmware last updated: __________    Warranty expirations: ______________________    Backup contact: ____________", lines=1)
    p.footer()
    return p


def main():
    products = [
        sales_tracker, sales_log, editable_sales_tracker, brand_vision,
        mahjong_tracker, mahjong_cheat, mahjong_quick, oasis_e2, sbar,
        nursing_cheat, psychopharm, gottman, ifs_cheat, piano_chords,
        customer_order_log, egg_tracker,
        ai_prompt_cheat, adhd_daily_planner, budget_tracker, habit_tracker,
        affirmations, grief_prompts, dbt_skills, blood_pressure_log,
        medication_log, password_log, packing_list, chore_chart,
        reading_log, appointment_tracker, meal_planner, goal_planner,
        content_calendar, reel_ideas, hashtag_caption_planner, content_batch_planner,
        pinterest_pin_planner, job_tracker, resume_cheat, interview_prep,
        bedtime_routine, screen_time_tracker, behavior_chart, lunchbox_planner,
        morning_routine_kids, prayer_journal, scripture_study, devotional_planner,
        workout_log, macro_tracker, symptom_tracker, sleep_log, period_tracker,
        cleaning_checklist, declutter_challenge, pantry_inventory, subscription_tracker,
        wedding_budget, wedding_checklist, guest_list, pet_care_log, pet_sitter_info,
        mood_tracker, self_care_menu,
        net_worth_tracker, investment_portfolio, dividend_tracker, crypto_portfolio,
        trading_journal, real_estate_deal_analyzer, landlord_income, retirement_planner,
        sinking_fund, debt_payoff, estate_planning_checklist, insurance_inventory,
        uk_self_assessment, uk_vat_tracker, uk_mileage_log, canada_tax_checklist,
        canada_rrsp_tfsa, canada_gst_hst, australia_bas, australia_deductions,
        us_1099_tracker, us_business_deductions, us_mileage_log, us_home_office,
        kpi_scorecard, meeting_notes, one_on_one_agenda, eos_level10,
        business_plan_one_pager, profit_loss, client_roster, hiring_scorecard,
        project_status, vendor_contract_log, okr_goals, delegation_log,
        luxury_travel_itinerary, wine_cellar_log, wine_tasting_notes, art_collection,
        home_maintenance_log, renovation_budget, holiday_gift_planner, vacation_rental_income,
        vehicle_maintenance, golf_score_log, home_inventory, dinner_party_planner,
        college_application_tracker, scholarship_tracker, college_budget, college_visit_checklist,
        tutor_session_log, kids_activity_schedule, summer_camp_planner, family_travel_itinerary,
        babysitter_info, allowance_ledger, extracurricular_expenses, college_savings_529,
        supplement_tracker, blood_panel_log, fasting_log, medical_history,
        realtor_cma, realtor_showings, realtor_transaction, realtor_open_house,
        lawyer_case_log, lawyer_billable_hours, lawyer_intake,
        cpa_tax_client_tracker, cpa_monthly_close, bookkeeper_reconciliation, cpa_tax_checklist,
        consultant_project_scoping, consultant_stakeholder_map, consultant_discovery,
        advisor_client_snapshot, advisor_discovery,
        soap_note, dentist_treatment_plan, pt_treatment_plan,
        therapist_intake, therapist_session_notes,
        contractor_estimate, contractor_punch_list, contractor_job_cost,
        architect_project_brief, photographer_session,
        property_manager_tenant_ledger, property_manager_maint_request,
        loan_officer_pipeline, insurance_lead_tracker, event_planner_timeline, hr_onboarding_checklist,
        teacher_lesson_plan, teacher_grade_tracker, substitute_teacher_info, homeschool_planner,
        electrician_job_log, plumber_invoice, hvac_service_log, landscaper_schedule,
        restaurant_food_cost, kitchen_prep_list, catering_order, bakery_order, bar_inventory,
        massage_therapy_intake, esthetician_client_log, nutrition_coach_plan, chiropractic_note, salon_client_log,
        musician_gig_log, writer_article_tracker, editor_style_sheet, tattoo_aftercare, dj_gig_log,
        freelance_dev_log, qa_test_log, product_roadmap, it_asset_inventory,
        sales_call_log, recruiter_pipeline, helpdesk_ticket_log, virtual_assistant_tasks,
        trucker_log, rideshare_income, pilot_flight_log, delivery_route_log, warehouse_inventory,
        nanny_daily_log, elderly_care_log, pet_groomer_log, housekeeping_checklist,
        watch_collection_log, watch_service_log, whiskey_collection_log, wine_auction_log,
        coin_collection_log, stamp_collection_log, rare_book_log, antiques_inventory,
        jewelry_inventory, sneaker_collection_log, luxury_goods_log, collector_car_log,
        art_acquisition_log,
        horse_health_log, horse_training_log, horse_show_log, horse_breeding_log,
        stable_management_log, kennel_club_log,
        boat_maintenance_log, yacht_crew_log, yacht_charter_log, aircraft_logbook,
        charter_flight_log,
        family_office_dashboard, trust_administration_log, philanthropy_log,
        private_banking_overview, donor_advised_fund_log, syndication_tracker,
        angel_investment_log, exchange_1031_log,
        concierge_medicine_plan, med_spa_plan, cosmetic_consult_log, longevity_protocol,
        executive_physical_log, premium_pt_plan, wellness_retreat_planner,
        private_chef_intake, estate_staff_roster, concierge_service_log,
        vacation_home_management, private_club_log, bespoke_tailor_log,
        interior_design_brief, estate_landscape_plan, ski_trip_planner, safari_planner,
        smart_home_inventory,
    ]
    OUT.mkdir(exist_ok=True)
    for fn in products:
        p = fn()
        name = fn.__name__ + ".pdf"
        p.output(str(OUT / name))
        print(f"{name:38s} pages={p.page}")
    print(f"\nDone — {len(products)} PDFs in {OUT}/")


if __name__ == "__main__":
    main()
