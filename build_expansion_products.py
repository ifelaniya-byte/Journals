"""Build the owner-directed local prototype packages for E01-E36.

These are original, controlled production prototypes. They are neither listings nor
release files: every package is marked as held until title/rights, print/vendor,
claims-boundary, proof, and named-human release gates are complete.

Requires: reportlab, Pillow, PyMuPDF. Install in an isolated environment with:
  pip install -r requirements.txt
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import shutil
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "EXPANSION_36_CONCEPT_REGISTER.csv"
OUT = ROOT / "expansion-release"
BRAND = json.loads((ROOT / "brand_config.json").read_text(encoding="utf-8"))
AUTHOR = BRAND["author"]
STATUS = "LOCAL PROTOTYPE PACKAGE - HOLD - NOT FOR SALE, UPLOAD, OR MANUFACTURE"
COPYRIGHT_NOTE = (
    "Copyright 2026 " + AUTHOR + ". Local prototype material only. "
    "No public identity, title, claims, platform, price, or release approval is implied."
)
BLEED = 0.125
PPI = 0.002252
INK = colors.HexColor("#252727")
MID = colors.HexColor("#5E6460")
LIGHT = colors.HexColor("#C9CFCA")
PALE = colors.HexColor("#F7F5F0")

# E03, E14, E19, E21, E25, E27, E32, and E34 deliberately do not receive a
# paperback wrap: their registered route is direct-object/printable/B2B first.
DIRECT_FIRST = {"E03", "E14", "E19", "E21", "E25", "E27", "E32", "E34"}

PALETTES = [
    ("20313D", "B9D5CA"), ("4B6070", "D3E3E8"), ("7A5246", "EAC9A6"),
    ("44524A", "C5D7C4"), ("6D5268", "E8C7DE"), ("6A4D3C", "E5C29B"),
    ("405A56", "BFD9D0"), ("665B3F", "E2D0A2"), ("3E6650", "C5DEAF"),
    ("4C5363", "C8D2E7"), ("735D45", "E8C79B"), ("744B54", "E7C4BF"),
    ("44565B", "BBD5D6"), ("4D6B59", "CDE0B7"), ("805B3F", "F0CA9C"),
    ("5C5272", "D9D0EE"), ("5F485C", "E9C9DD"), ("556B5E", "D0E3C9"),
    ("354B59", "B8D3DD"), ("5A4B3C", "E4C79D"), ("395A64", "B7D9DE"),
    ("4D5364", "CBD3E8"), ("594B46", "E7CBBB"), ("3B5967", "BBD8E4"),
    ("754F42", "E9C4A8"), ("3D5960", "B9D6D3"), ("6C5A4C", "E2CAA6"),
    ("79515A", "E9C2CB"), ("454A67", "C8CDE8"), ("6A4D3C", "E8D0A7"),
    ("4B5851", "C3D9C8"), ("293D55", "BFD2E8"), ("725746", "E5C6AB"),
    ("3D5560", "B5D4D8"), ("4E6270", "C9DCE0"), ("564D68", "D7CEE8"),
]

# Every profile has its own customer job, entry fields, work-surface type, and
# cycle language. The shared rendering system prevents production drift; it does
# not reuse one generic journal interior.
PROFILES = {
    "E01": dict(kind="ledger", pages=96, cycle="Reading encounter", verb="Keep the thread", starter=["A book or text I want to enter", "A question I am carrying", "A reading rhythm that feels realistic"], fields=["TEXT / AUTHOR", "PASSAGE OR IDEA IN MY OWN WORDS", "WHAT IT CONNECTS TO", "A QUESTION FOR THE ROOM"], review=["A thought worth returning to", "A book-club question", "Where this belongs in my commonplace index"], prompts=["What did this text make newly visible?", "Where did an idea change shape for me?", "What would I like to discuss instead of summarize?"], surface="quote_map"),
    "E02": dict(kind="field", pages=80, cycle="Small trip", verb="Notice the route", starter=["A nearby or faraway place I want to remember", "A pace that leaves room for surprise", "One thing I do not want to rush past"], fields=["DATE / PLACE", "HOW I ARRIVED", "A DETAIL I WOULD MISS IN A PHOTO", "A TICKET, SKETCH, OR SMALL MAP NOTE"], review=["A scene I want to send to later", "A return-later idea", "A sentence to my future self"], prompts=["What did this place ask me to notice?", "What ordinary detail became the souvenir?", "Where would I pause longer next time?"], surface="route_map"),
    "E03": dict(kind="recipe", pages=112, cycle="Recipe story", verb="Gather the story", starter=["A dish people ask about", "A person or place connected to it", "How I want future cooks to feel using this book"], fields=["RECIPE NAME / CONTRIBUTOR", "THE STORY BEHIND IT", "INGREDIENTS AS THEY ARE REMEMBERED", "METHOD IN THE CONTRIBUTOR'S WORDS"], review=["When we make this", "A variation we love", "Who should receive this story next"], prompts=["What makes this recipe belong to your people?", "Which detail never appears on a recipe card?", "What do I want a future cook to know about the table around it?"], surface="recipe_card"),
    "E04": dict(kind="collect", pages=88, cycle="Collection entry", verb="Curate what matters", starter=["The collection I am building or rediscovering", "What makes an object worth keeping to me", "One display corner I want to make more intentional"], fields=["OBJECT / SET", "WHERE IT CAME FROM (AS TOLD)", "WHAT I NOTICE ABOUT IT", "DISPLAY OR ROTATION IDEA"], review=["A companion object", "A label in my own words", "What I want to photograph or remember"], prompts=["What story appears when the objects sit together?", "What does this piece ask for: light, space, company, or rest?", "What makes the collection personal rather than complete?"], surface="catalog_grid"),
    "E05": dict(kind="photo", pages=96, cycle="Photo story", verb="Tell the moment", starter=["A month or season I want to rescue from the camera roll", "A simple way I will choose images", "A person, place, or detail I hope to remember"], fields=["PHOTO / DATE", "WHY I CHOSE THIS IMAGE", "CAPTION IN MY OWN WORDS", "A DETAIL OUTSIDE THE FRAME"], review=["A photo to print", "A person to share it with", "The story this month was really about"], prompts=["What does this photograph hold that I did not notice then?", "Which image deserves words rather than another scroll?", "What would the caption say if it were only for me?"], surface="photo_frame"),
    "E06": dict(kind="letter", pages=88, cycle="Correspondence moment", verb="Send something real", starter=["People I want to write to", "Occasions I want to remember", "The kinds of notes I want to keep making time for"], fields=["TO / OCCASION", "WHAT I WANT TO SAY", "A DETAIL THAT MAKES IT SPECIFIC", "DATE SENT / HOW IT FELT"], review=["A note I want to write next", "A phrase worth keeping", "What I learned about this person"], prompts=["What gratitude becomes clearer when it is specific?", "What ordinary moment deserves a written note?", "What would I say without trying to make it perfect?"], surface="letter_sheet"),
    "E07": dict(kind="home", pages=96, cycle="One-shelf reset", verb="Make one decision", starter=["A room that needs less pressure", "One surface I can begin with", "A realistic amount of time I have today"], fields=["ZONE / STARTING POINT", "WHAT IS HERE NOW", "KEEP / RELEASE / REHOME THOUGHTS", "ONE SMALL FINISHING TOUCH"], review=["What became easier to use", "A donation or handoff note", "The next one-shelf choice"], prompts=["What is the smallest visible win here?", "What already works in this room?", "What can leave without turning this into an all-house project?"], surface="decision_tree"),
    "E08": dict(kind="kitchen", pages=88, cycle="Small-kitchen repeat", verb="Use the space well", starter=["The kitchen corner I know best", "Meals or moments I want to make easier", "A storage frustration worth observing"], fields=["MEAL / ROUTINE", "WHAT THE SPACE MADE EASY", "WHAT FELT CROWDED", "A REPEAT I WANT TO KEEP"], review=["Pantry or fridge cue", "A guest-with-little-space note", "One layout experiment"], prompts=["What repeat makes this kitchen feel like mine?", "What can live where I actually reach for it?", "What small ritual makes a compact space generous?"], surface="kitchen_map"),
    "E09": dict(kind="garden", pages=104, cycle="Growing-space note", verb="Observe the season", starter=["A windowsill, balcony, or small plot", "Light and weather patterns I want to notice", "A gentle experiment I want to track"], fields=["DATE / SPACE", "LIGHT / WEATHER AS I NOTICE IT", "WHAT I SEE CHANGING", "WHAT I WANT TO TRY OR ASK"], review=["A small success", "A next-season note", "A harvest or flowering memory"], prompts=["What is this small space teaching me to notice?", "What changed slowly enough that I almost missed it?", "What will I try next without treating it as a test?"], surface="season_grid"),
    "E10": dict(kind="home", pages=104, cycle="Home rhythm", verb="Keep it lived-in", starter=["A season I am entering", "Ordinary tasks that make home work", "A definition of done that is kind enough"], fields=["SEASON / ZONE", "A ROUTINE TO NOTICE", "WHAT WAS COMPLETED - NOT PERFECT", "WHO OR WHAT NEEDS A HANDOFF"], review=["A seasonal ritual to repeat", "A task worth simplifying", "What made the home feel lived in"], prompts=["What does this season ask of the house, not of perfection?", "What belongs on a list and what belongs in a rhythm?", "What can be good enough this week?"], surface="season_wheel"),
    "E11": dict(kind="move", pages=96, cycle="Arrival step", verb="Make the place yours", starter=["The place I am leaving or arriving", "A room I want to make functional first", "One memory I want to carry with me"], fields=["ROOM / ADDRESS-CHANGE TASK", "WHAT NEEDS TO HAPPEN", "WHAT MAKES THIS FEEL LIKE MINE", "A FIRST-MONTH MEMORY"], review=["A helpful contact or question", "What is already working", "A small arrival ritual"], prompts=["What makes a new place begin to feel inhabited?", "What can be unpacked emotionally, not only physically?", "Which first deserves to be recorded?"], surface="arrival_map"),
    "E12": dict(kind="host", pages=88, cycle="Gathering note", verb="Welcome simply", starter=["The kinds of gatherings I enjoy", "How I want guests to feel", "What I can realistically host"], fields=["GATHERING / DATE", "WHO MAY BE THERE", "A FLEXIBLE MENU OR PLAN", "A COMFORT DETAIL"], review=["What felt warm and easy", "What I would skip next time", "A keeper note for future hosting"], prompts=["What makes an invitation feel low-pressure?", "What can be prepared without overproducing?", "What detail made people linger?"], surface="table_plan"),
    "E13": dict(kind="mend", pages=88, cycle="Mend or make note", verb="Keep things in use", starter=["Something I would like to keep using", "Materials I already have", "A repair question I need to document rather than solve here"], fields=["ITEM / PROJECT", "WHAT I NOTICE", "MATERIAL OR SWATCH NOTE", "WHAT I TRIED OR WANT TO ASK"], review=["Before-and-after story", "A repair referral or next question", "What keeping this taught me"], prompts=["What is worth keeping in use?", "Where does the repair become part of the object's story?", "What do I need to document before I decide?"], surface="mending_board"),
    "E14": dict(kind="nature", pages=96, cycle="Pressed-things page", verb="Keep the season", starter=["A season I want to notice", "A place I want to return to", "A non-specimen way to remember what I find"], fields=["DATE / PLACE", "COLOR / SHAPE / TEXTURE", "WHAT I NOTICED", "MOUNTING OR DISPLAY IDEA"], review=["A seasonal pairing", "A page title", "A memory this finding carries"], prompts=["What can I observe without needing to name it?", "What shape or color keeps returning?", "Where will this page take me later?"], surface="specimen_frame"),
    "E15": dict(kind="baking", pages=96, cycle="Bake note", verb="Remember the repeat", starter=["A bake I want to learn from", "People I enjoy feeding", "A note-taking style I will actually use"], fields=["BAKE / DATE", "WHAT I CHANGED", "TEXTURE / LOOK / TIMING AS I NOTICED IT", "WHO I SHARED IT WITH"], review=["Would I repeat it?", "A future variation", "The occasion it belongs to"], prompts=["What detail will make this easier to repeat?", "What did the people at the table say or do?", "What am I curious to change next time?"], surface="bake_matrix"),
    "E16": dict(kind="zine", pages=88, cycle="Tiny issue", verb="Make a page", starter=["A small subject worth an issue", "A reader or future self I imagine", "A project boundary that makes this finishable"], fields=["ISSUE / PAGE IDEA", "WORDS / IMAGES I WILL MAKE", "LAYOUT OR FOLD NOTE", "WHAT THIS PAGE NEEDS NEXT"], review=["What the issue is becoming", "A page to cut or simplify", "A non-distribution reason to finish"], prompts=["What can fit on one small page?", "Which idea is mine to shape without borrowing someone else's work?", "What would make this issue feel complete enough?"], surface="zine_fold"),
    "E17": dict(kind="color", pages=80, cycle="Color study", verb="Build a palette", starter=["Colors I keep returning to", "Materials I want to observe", "A project where I could use a color reference"], fields=["PALETTE / MATERIAL", "COLORS I SEE", "A MIX OR SWATCH NOTE", "WHAT THE COMBINATION SUGGESTS"], review=["A palette name in my own words", "Where I might use it", "What I learned by looking longer"], prompts=["What changes when I name the color more specifically?", "Which pairing surprises me?", "What is the mood without calling it a result?"], surface="palette_grid"),
    "E18": dict(kind="project", pages=88, cycle="First-project session", verb="Return to the work", starter=["One beginner project I choose", "Words I want to learn in my own way", "A restart cue for the day I lose my place"], fields=["PROJECT / SESSION", "WHAT I WORKED ON", "MATERIALS OR TOOLS I USED", "WHERE I AM WHEN I RETURN"], review=["A win I can name", "A question to take to a teacher or source", "The next tiny session"], prompts=["What is clear enough for the next session?", "What did I learn in my own words?", "What makes it easier to come back after a pause?"], surface="project_path"),
    "E19": dict(kind="meeting", pages=96, cycle="Meeting map", verb="Make the handoff visible", starter=["The kind of meeting I want to leave with clarity", "A note-taking boundary that keeps this useful", "A way I will distinguish decisions from discussion"], fields=["DATE / TOPIC", "DECISION OR QUESTION", "WHO OWNS THE NEXT STEP", "CONTEXT / DISAGREEMENT / FOLLOW-UP"], review=["What actually moved", "What needs a clearer handoff", "A review date"], prompts=["What needs a decision rather than more notes?", "What belongs to an owner, a date, or a later conversation?", "What context will make this useful tomorrow?"], surface="meeting_map"),
    "E20": dict(kind="weekly", pages=88, cycle="Friday closeout", verb="Close the week", starter=["What I want a weekly closeout to protect", "A Friday ritual that fits my actual schedule", "A way to carry work forward without carrying everything"], fields=["WEEK OF", "WHAT MOVED", "WHAT WAITED", "WHAT I WANT TO START CLEAN NEXT WEEK"], review=["Evidence of effort", "A calendar boundary", "One thing I am done holding"], prompts=["What moved even if it did not finish?", "What can wait without becoming a failure?", "What will make Monday easier?"], surface="weekly_strip"),
    "E21": dict(kind="client", pages=96, cycle="Client-project record", verb="Keep the project legible", starter=["A project I want to document", "The scope in my own notes", "How I will separate requests from commitments"], fields=["PROJECT / STAGE", "DELIVERABLE OR NOTE", "REVISION / FEEDBACK MAP", "WHAT NEEDS A HANDOFF"], review=["What was delivered", "What I learned for next time", "A closeout record"], prompts=["What belongs in the project record now?", "What changed and why?", "What would make the next handoff clearer?"], surface="handoff_board"),
    "E22": dict(kind="season", pages=96, cycle="Studio week", verb="Stay with one project", starter=["A project for this season", "Why it matters to me", "A finish line that does not require perfection"], fields=["WEEK / MILESTONE", "WHAT I MADE OR MOVED", "FRICTION I NOTICED", "ONE SMALL STUDIO DATE"], review=["What I am learning", "What I will change", "A record of the season so far"], prompts=["What would count as a meaningful next move?", "What friction is information rather than failure?", "What needs less scope to remain alive?"], surface="milestone_arc"),
    "E23": dict(kind="decision", pages=88, cycle="Decision record", verb="Leave a trace", starter=["A choice I want to understand", "How long I want decisions to remain open", "A reminder that a later outcome cannot erase present context"], fields=["CHOICE / DATE", "CONTEXT AND ASSUMPTIONS", "ALTERNATIVES I SAW", "A REVIEW DATE"], review=["What I decided", "What later information changed", "What I would carry into the next choice"], prompts=["What did I know at the time?", "Which tradeoff is worth naming plainly?", "What question would future me ask?"], surface="decision_canvas"),
    "E24": dict(kind="hybrid", pages=104, cycle="Hybrid week", verb="Plan the location", starter=["The places where I work and reset", "A transition that helps a day change shape", "Home tasks that deserve an honest place in the plan"], fields=["WEEK / LOCATION MIX", "WORK BLOCKS", "HOME OR COMMUTE TRANSITION", "A SETUP OR HANDOFF NOTE"], review=["What location supported the work", "What needs adjustment", "A next-week cue"], prompts=["What changes when I plan the location, not only the task?", "What helps the shift between work and home feel intentional?", "What needs to travel with me?"], surface="hybrid_grid"),
    "E25": dict(kind="supper", pages=96, cycle="Supper club gathering", verb="Make a tradition", starter=["The kind of table I want to gather", "People I want to invite over time", "A scale of hosting that feels generous and possible"], fields=["DATE / THEME", "GUEST CIRCLE", "MENU OR TABLE IDEA", "A MOMENT I WANT TO REMEMBER"], review=["A dish or story to repeat", "What guests added", "The next table"], prompts=["What turns a meal into a tradition?", "What belongs at this table besides food?", "What could become easier next time?"], surface="supper_table"),
    "E26": dict(kind="picnic", pages=80, cycle="Outdoor day", verb="Remember the day outside", starter=["A local outdoor place I want to use", "What pack-light means to me", "People or solo moments I want to make room for"], fields=["DATE / PLACE", "WHAT I BROUGHT", "WEATHER AS I EXPERIENCED IT", "A SMALL SHARED MEMORY"], review=["A spot to return to", "What stayed in the bag", "A next low-key outing"], prompts=["What makes a small outing feel complete?", "What did we notice once we settled?", "What would I bring or leave next time?"], surface="picnic_map"),
    "E27": dict(kind="home", pages=96, cycle="First-year home memory", verb="Mark the firsts", starter=["The home I am making", "Firsts I want to notice", "A way to welcome people without making this a generic guest book"], fields=["DATE / ROOM", "A FIRST OR VISIT", "WHAT HAPPENED HERE", "A DETAIL OF HOME-MADE-HERE"], review=["A person who showed up", "A room story", "What I want the next year to hold"], prompts=["What makes a place become our place?", "Which ordinary first deserves a page?", "What did someone bring into this home besides an object?"], surface="home_story"),
    "E28": dict(kind="celebrate", pages=88, cycle="Milestone capsule", verb="Keep the moment", starter=["Milestones I want to notice beyond the obvious", "People I hope to include", "A way to celebrate without needing a perfect event"], fields=["OCCASION / DATE", "WHAT HAPPENED", "WHO SHOWED UP", "A LETTER OR IMAGE PROMPT"], review=["What I want to remember later", "A small detail worth keeping", "The next ordinary win"], prompts=["What makes this worth marking?", "Who helped make the moment possible?", "What would a future version of me be glad to find?"], surface="time_capsule"),
    "E29": dict(kind="music", pages=88, cycle="Listening memory", verb="Trace the sound", starter=["Music moments I want to remember", "A listening ritual I enjoy", "A way to write about songs without copying protected lyrics or artwork"], fields=["ALBUM / SHOW / PLAYLIST", "WHERE AND WHEN I LISTENED", "THE STORY IT CARRIES", "A NON-LYRIC DETAIL"], review=["A person to share it with", "A sound or performance memory", "What I want to hear again"], prompts=["What does this music bring back without needing to quote it?", "Where was I when the song became mine?", "What is the story around the listening?"], surface="listening_map"),
    "E30": dict(kind="gift", pages=80, cycle="Little-treat note", verb="Make delight visible", starter=["What a little treat means to me", "People I like to surprise", "Ways to celebrate that do not need a major occasion"], fields=["PERSON OR MOMENT", "A SMALL DELIGHT", "WHY IT FITS", "WHEN I GAVE OR ENJOYED IT"], review=["A joy worth repeating", "A future idea", "What I noticed about care"], prompts=["What makes a gesture feel seen rather than expensive?", "Which ordinary day could use a small marker?", "What detail turns a gift into a memory?"], surface="gift_menu"),
    "E31": dict(kind="cafe", pages=88, cycle="Home-cafe ritual", verb="Notice the corner", starter=["A drink ritual I enjoy", "A home corner I want to make more mine", "A way to keep notes without turning taste into expertise"], fields=["DRINK / DATE", "WHAT I MADE OR NOTICED", "SPACE / CUP / COMPANY DETAIL", "A REPEAT I WANT TO KEEP"], review=["A guest drink idea", "A corner adjustment", "The ritual in one sentence"], prompts=["What makes this a ritual instead of a routine?", "What small detail changes the corner?", "What do I want to remember about sharing it?"], surface="cafe_counter"),
    "E32": dict(kind="movie", pages=88, cycle="Movie-night plan", verb="Set a scene", starter=["The kind of outdoor evening I want", "People I might invite", "A simple plan that leaves room for weather and change"], fields=["DATE / THEME", "SEATING OR BLANKET MAP", "SNACK OR AMBIENCE IDEA", "A MEMORY OF THE NIGHT"], review=["What made it easy", "A non-copyrighted conversation prompt", "What I would repeat"], prompts=["What makes an outdoor evening feel welcoming?", "What can remain simple?", "What will people remember besides the screen?"], surface="screening_map"),
    "E33": dict(kind="secondhand", pages=88, cycle="Secondhand story", verb="Follow the object's life", starter=["A kind of find I want to remember", "What provenance-as-told means to me", "A display corner I want to change slowly"], fields=["OBJECT / FIND", "WHERE IT CAME FROM (AS TOLD)", "CONDITION AS I NOTICE IT", "DISPLAY OR CARE QUESTION"], review=["A story to keep with it", "A repair referral note", "What the object changes in the room"], prompts=["What makes this find more than a purchase?", "What story can I keep without claiming certainty?", "Where does the object want to live?"], surface="object_tag"),
    "E34": dict(kind="repair", pages=88, cycle="Repair-before-replace decision", verb="Document the choice", starter=["An item with a history", "A repair question I need to keep visible", "A boundary: this book does not replace professional or manufacturer guidance"], fields=["ITEM / HISTORY", "WHAT IS HAPPENING", "SERVICE OR SUPPORT CONTACT", "REPAIR / REPLACE THOUGHTS"], review=["What information I still need", "A date to revisit", "What I decided and why"], prompts=["What would help me choose without rushing?", "What do I know and what needs a qualified answer?", "What does the item's history tell me?"], surface="repair_record"),
    "E35": dict(kind="field", pages=80, cycle="Weekend discovery", verb="Go nearby", starter=["A neighborhood or nearby place I want to explore", "A three-hour window I can protect", "A discovery habit that does not require a big trip"], fields=["DATE / AREA", "WHERE I WENT", "A ROUTE OR PLACE SKETCH", "ONE SMALL DISCOVERY"], review=["A return-later list", "A local detail to tell someone", "The next short outing"], prompts=["What did I find by looking close to home?", "Where would I wander next without making an itinerary?", "What deserves a second visit?"], surface="route_map"),
    "E36": dict(kind="season", pages=104, cycle="Seasonal swap", verb="Transition with care", starter=["A season I am entering", "Storage or routines I want to make easier", "Traditions worth carrying forward"], fields=["SEASON / ZONE", "KEEP / DONATE / STORE THOUGHTS", "A HOUSEHOLD RITUAL", "WHAT I WANT TO MAKE EASIER"], review=["A storage note", "A transition that worked", "What I want to remember next season"], prompts=["What changes when the season changes?", "What can move slowly and still get done?", "Which ritual belongs to this time of year?"], surface="season_wheel"),
}


def slugify(value: str) -> str:
    text = value.lower().replace("&", "and")
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text


def parse_trim(format_text: str) -> tuple[float, float]:
    match = re.search(r"(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)", format_text, re.I)
    if not match:
        raise ValueError(f"No trim size found in {format_text!r}")
    return float(match.group(1)), float(match.group(2))


def wrap_lines(text: str, font_name: str, size: float, width: float) -> list[str]:
    words = text.replace("\n", " \n ").split()
    lines, current = [], ""
    for word in words:
        if word == "\\n":
            if current:
                lines.append(current)
            current = ""
            continue
        candidate = (current + " " + word).strip()
        if not current or stringWidth(candidate, font_name, size) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, width: float, size: float = 9, leading: float = 12, color=INK, font_name: str = "Helvetica") -> float:
    c.setFont(font_name, size)
    c.setFillColor(color)
    for line in wrap_lines(text, font_name, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def centered(c: canvas.Canvas, text: str, x: float, y: float, width: float, size: float, leading: float, color, font_name: str = "Helvetica") -> None:
    rows = wrap_lines(text, font_name, size, width)
    y += (len(rows) - 1) * leading / 2
    c.setFont(font_name, size)
    c.setFillColor(color)
    for row in rows:
        c.drawCentredString(x, y, row)
        y -= leading


def style_for(index: int) -> tuple[str, str]:
    return PALETTES[index % len(PALETTES)]


class PrototypeBook:
    def __init__(self, path: Path, trim: tuple[float, float], candidate: dict[str, str], profile: dict, palette: tuple[str, str]):
        self.path = path
        self.w = trim[0] * inch
        self.h = trim[1] * inch
        self.trim = trim
        self.candidate = candidate
        self.profile = profile
        self.bg = colors.HexColor("#" + palette[0])
        self.accent = colors.HexColor("#" + palette[1])
        self.c = canvas.Canvas(str(path), pagesize=(self.w, self.h), pageCompression=1)
        self.n = 0
        self.mx = 0.52 * inch

    def end(self) -> None:
        self.c.showPage()
        self.n += 1

    def frame(self, label: str = "EXPANSION LOCAL PROTOTYPE", number: bool = True) -> None:
        c = self.c
        c.setFillColor(colors.white)
        c.rect(0, 0, self.w, self.h, fill=1, stroke=0)
        c.setStrokeColor(LIGHT)
        c.setLineWidth(0.4)
        c.line(self.mx, self.h - 0.48 * inch, self.w - self.mx, self.h - 0.48 * inch)
        c.line(self.mx, 0.45 * inch, self.w - self.mx, 0.45 * inch)
        c.setFillColor(MID)
        c.setFont("Helvetica-Bold", 6.2)
        c.drawString(self.mx, self.h - 0.39 * inch, label.upper())
        c.setFont("Helvetica", 6.2)
        c.drawRightString(self.w - self.mx, self.h - 0.39 * inch, STATUS[:40])
        if number and self.n > 0:
            c.drawRightString(self.w - self.mx, 0.31 * inch, str(self.n + 1))

    def title_page(self) -> None:
        c = self.c
        c.setFillColor(self.bg)
        c.rect(0, 0, self.w, self.h, fill=1, stroke=0)
        c.setStrokeColor(self.accent)
        c.setLineWidth(1)
        for radius in (0.82, 1.15, 1.48):
            c.circle(self.w * 0.76, self.h * 0.78, radius * inch, fill=0, stroke=1)
        centered(c, self.candidate["working_title"], self.w / 2, self.h * 0.58, self.w - 1.1 * inch, 21, 25, colors.white, "Helvetica-Bold")
        centered(c, self.candidate["subtitle_concept"], self.w / 2, self.h * 0.45, self.w - 1.2 * inch, 9.4, 12, self.accent)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(self.accent)
        c.drawCentredString(self.w / 2, self.h * 0.25, "LOCAL PRODUCT PROTOTYPE")
        c.setFont("Helvetica", 8.2)
        c.setFillColor(colors.white)
        c.drawCentredString(self.w / 2, self.h * 0.18, AUTHOR)
        c.setFont("Helvetica", 5.8)
        c.setFillColor(self.accent)
        c.drawCentredString(self.w / 2, 0.38 * inch, "NOT FOR SALE, UPLOAD, OR MANUFACTURE")
        self.end()

    def rights_page(self) -> None:
        self.frame("Prototype use boundary", False)
        c = self.c
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(self.mx, self.h - 0.86 * inch, "Before this becomes anything public")
        y = self.h - 1.18 * inch
        copy = (
            "This is an owner-directed local prototype for a distinct product concept. "
            "It is not a public listing, an upload file, a price decision, a manufacturing order, "
            "or proof of rights/name/platform clearance."
        )
        y = draw_wrapped(c, copy, self.mx, y, self.w - 2 * self.mx, 9.4, 12.5, INK)
        y -= 0.18 * inch
        c.setFillColor(self.bg)
        c.setFont("Helvetica-Bold", 8.2)
        c.drawString(self.mx, y, "PRODUCT-SPECIFIC BOUNDARY")
        y -= 0.22 * inch
        y = draw_wrapped(c, self.candidate["claims_boundary"], self.mx, y, self.w - 2 * self.mx, 8.8, 11.5, MID)
        y -= 0.18 * inch
        c.setFillColor(self.bg)
        c.setFont("Helvetica-Bold", 8.2)
        c.drawString(self.mx, y, "REQUIRED BEFORE ANY RELEASE")
        y -= 0.22 * inch
        release = (
            "Human title/rights review; original-asset provenance; product-specific claims and accessibility review; "
            "current printer/platform requirements; final proof; and named-human approval."
        )
        draw_wrapped(c, release, self.mx, y, self.w - 2 * self.mx, 8.8, 11.5, MID)
        c.setFillColor(MID)
        c.setFont("Helvetica-Oblique", 7)
        c.drawString(self.mx, 0.73 * inch, COPYRIGHT_NOTE)
        self.end()

    def how_to_page(self) -> None:
        self.frame("How this prototype works", False)
        c = self.c
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(self.mx, self.h - 0.86 * inch, self.profile["verb"])
        intro = (
            f"This {self.candidate['primary_format'].lower()} is organized around repeated "
            f"{self.profile['cycle'].lower()} pages. Use one cycle at a time, skip freely, and make the book yours."
        )
        y = draw_wrapped(c, intro, self.mx, self.h - 1.16 * inch, self.w - 2 * self.mx, 9.5, 12.5, INK)
        y -= 0.18 * inch
        for number, label in enumerate(("Begin", "Work the page", "Return"), 1):
            c.setFillColor(self.bg)
            c.circle(self.mx + 0.14 * inch, y - 0.04 * inch, 0.12 * inch, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 7)
            c.drawCentredString(self.mx + 0.14 * inch, y - 0.065 * inch, str(number))
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(self.mx + 0.36 * inch, y - 0.07 * inch, label)
            explanation = [
                "Choose one page or one part of the product experience.",
                "Record what is useful in your own words, sketches, photographs, or materials.",
                "Leave a small note that makes the next return easier.",
            ][number - 1]
            y = draw_wrapped(c, explanation, self.mx + 0.36 * inch, y - 0.23 * inch, self.w - 2 * self.mx - 0.36 * inch, 8.5, 11, MID)
            y -= 0.12 * inch
        self.end()

    def starter_page(self) -> None:
        self.frame("Make it yours")
        c = self.c
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(self.mx, self.h - 0.86 * inch, "Start where the product meets your life")
        y = self.h - 1.23 * inch
        for label in self.profile["starter"]:
            y = self.field(label.upper(), y, 3)
            y -= 0.05 * inch
        self.end()

    def field(self, label: str, y: float, rows: int = 2, x: float | None = None, width: float | None = None) -> float:
        c = self.c
        x = self.mx if x is None else x
        width = self.w - 2 * self.mx if width is None else width
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 7.2)
        c.drawString(x, y, label)
        y -= 0.18 * inch
        c.setStrokeColor(LIGHT)
        c.setLineWidth(0.42)
        for _ in range(rows):
            c.line(x, y, x + width, y)
            y -= 0.25 * inch
        return y - 0.06 * inch

    def entry_page(self, cycle: int) -> None:
        self.frame(self.profile["cycle"])
        c = self.c
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(self.mx, self.h - 0.86 * inch, f"{self.profile['cycle']} {cycle + 1}")
        c.setFillColor(MID)
        c.setFont("Helvetica-Oblique", 8.4)
        prompt = self.profile["prompts"][cycle % len(self.profile["prompts"])]
        y = draw_wrapped(c, '"' + prompt + '"', self.mx, self.h - 1.10 * inch, self.w - 2 * self.mx, 8.4, 10.5, MID, "Helvetica-Oblique")
        y -= 0.17 * inch
        for ix, label in enumerate(self.profile["fields"]):
            y = self.field(label, y, 2 if ix != 1 else 3)
            if y < 1.0 * inch:
                break
        self.end()

    def work_surface(self, cycle: int) -> None:
        self.frame(self.profile["kind"] + " work surface")
        c = self.c
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(self.mx, self.h - 0.86 * inch, self.surface_title())
        c.setFillColor(MID)
        c.setFont("Helvetica-Oblique", 7.8)
        c.drawString(self.mx, self.h - 1.08 * inch, "Use words, a sketch, a clipping, a photo placeholder, or leave it open.")
        y_top = self.h - 1.35 * inch
        x = self.mx
        width = self.w - 2 * self.mx
        height = self.h - 2.2 * inch
        surface = self.profile["surface"]
        c.setStrokeColor(LIGHT)
        c.setLineWidth(0.8)
        if surface in {"quote_map", "route_map", "meeting_map", "decision_canvas", "project_path", "milestone_arc", "hybrid_grid"}:
            c.roundRect(x, 1.0 * inch, width, height, 8, fill=0, stroke=1)
            for i in range(1, 5):
                xx = x + width * i / 5
                c.setStrokeColor(colors.HexColor("#E7EAE5"))
                c.line(xx, 1.0 * inch, xx, 1.0 * inch + height)
            for i in range(1, 5):
                yy = 1.0 * inch + height * i / 5
                c.line(x, yy, x + width, yy)
            c.setStrokeColor(self.accent)
            c.setLineWidth(1.2)
            c.circle(x + width * 0.5, 1.0 * inch + height * 0.52, 0.45 * inch, fill=0, stroke=1)
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                c.line(x + width * .5 + math.cos(rad) * .45 * inch, 1.0 * inch + height * .52 + math.sin(rad) * .45 * inch, x + width * .5 + math.cos(rad) * 1.2 * inch, 1.0 * inch + height * .52 + math.sin(rad) * 1.2 * inch)
        elif surface in {"recipe_card", "photo_frame", "specimen_frame", "letter_sheet", "time_capsule", "home_story"}:
            c.roundRect(x, 1.0 * inch, width, height, 8, fill=0, stroke=1)
            c.setStrokeColor(self.accent)
            c.rect(x + .25 * inch, 2.1 * inch, width * .54, height - 1.35 * inch, fill=0, stroke=1)
            c.setStrokeColor(LIGHT)
            for i in range(5):
                yy = 1.65 * inch + i * .26 * inch
                c.line(x + width * .62, yy, x + width - .22 * inch, yy)
            c.setFillColor(MID)
            c.setFont("Helvetica", 7)
            c.drawCentredString(x + width * .52, 1.65 * inch, "PLACEHOLDER FOR A SKETCH, PHOTO, RECIPE CARD, OR KEEPSAKE")
        elif surface in {"catalog_grid", "palette_grid", "object_tag", "gift_menu", "cafe_counter"}:
            cols, rows = 3, 4
            cell_w, cell_h = width / cols, height / rows
            for row in range(rows):
                for col in range(cols):
                    xx, yy = x + col * cell_w, 1.0 * inch + row * cell_h
                    c.rect(xx, yy, cell_w, cell_h, fill=0, stroke=1)
                    c.setStrokeColor(self.accent if (row + col + cycle) % 2 == 0 else LIGHT)
                    c.line(xx + .15 * inch, yy + cell_h - .25 * inch, xx + cell_w - .15 * inch, yy + cell_h - .25 * inch)
                    c.setStrokeColor(LIGHT)
        elif surface in {"decision_tree", "kitchen_map", "arrival_map", "table_plan", "supper_table", "picnic_map", "screening_map", "kitchen_map"}:
            c.roundRect(x, 1.0 * inch, width, height, 8, fill=0, stroke=1)
            c.setStrokeColor(self.accent)
            c.setLineWidth(1.0)
            c.circle(x + width * .5, 1.0 * inch + height * .52, .48 * inch, fill=0, stroke=1)
            for ix, label in enumerate(["NOTICE", "CHOOSE", "ARRANGE", "RETURN"]):
                angle = math.radians(45 + ix * 90)
                cx = x + width * .5 + math.cos(angle) * 1.45 * inch
                cy = 1.0 * inch + height * .52 + math.sin(angle) * 1.2 * inch
                c.roundRect(cx - .55 * inch, cy - .25 * inch, 1.1 * inch, .5 * inch, 5, fill=0, stroke=1)
                c.setFillColor(MID)
                c.setFont("Helvetica-Bold", 6.5)
                c.drawCentredString(cx, cy - .03 * inch, label)
                c.setStrokeColor(LIGHT)
                c.line(x + width * .5 + math.cos(angle) * .48 * inch, 1.0 * inch + height * .52 + math.sin(angle) * .48 * inch, cx - math.cos(angle) * .55 * inch, cy - math.sin(angle) * .25 * inch)
        else:
            c.roundRect(x, 1.0 * inch, width, height, 8, fill=0, stroke=1)
            c.setStrokeColor(self.accent)
            c.line(x + width * .5, 1.0 * inch, x + width * .5, 1.0 * inch + height)
            for row in range(1, 6):
                c.setStrokeColor(LIGHT)
                c.line(x, 1.0 * inch + row * height / 6, x + width, 1.0 * inch + row * height / 6)
        self.end()

    def surface_title(self) -> str:
        labels = {
            "quote_map": "Connections and questions", "route_map": "Route and return map", "recipe_card": "Recipe and story card", "catalog_grid": "Collection display board", "photo_frame": "Photo story spread", "letter_sheet": "Letter and archive sheet", "decision_tree": "One-surface decision map", "kitchen_map": "Small-kitchen map", "season_grid": "Seasonal observation grid", "season_wheel": "Seasonal rhythm wheel", "arrival_map": "Arrival map", "table_plan": "Gathering table plan", "mending_board": "Mend and make board", "specimen_frame": "Pressed-things layout", "bake_matrix": "Bake notes matrix", "zine_fold": "Tiny issue fold plan", "palette_grid": "Palette swatch grid", "project_path": "Project restart path", "meeting_map": "Decision and handoff map", "weekly_strip": "Week-at-a-glance strip", "handoff_board": "Project handoff board", "milestone_arc": "Twelve-week project arc", "decision_canvas": "Context and tradeoff canvas", "hybrid_grid": "Location-aware week", "supper_table": "Supper-club table map", "picnic_map": "Outdoor-day map", "home_story": "First-year home story", "time_capsule": "Milestone capsule", "listening_map": "Listening-memory map", "gift_menu": "Little-treat menu", "cafe_counter": "Home-cafe counter", "screening_map": "Movie-night scene map", "object_tag": "Object-story tag sheet", "repair_record": "Repair decision record",
        }
        return labels.get(self.profile["surface"], "Working surface")

    def reflection_page(self, cycle: int) -> None:
        self.frame("Return note")
        c = self.c
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(self.mx, self.h - 0.86 * inch, f"Return after {self.profile['cycle'].lower()} {cycle + 1}")
        c.setFillColor(MID)
        c.setFont("Helvetica-Oblique", 8.4)
        c.drawString(self.mx, self.h - 1.10 * inch, "A small note is enough to make the next use easier.")
        y = self.h - 1.42 * inch
        for label in self.profile["review"]:
            y = self.field(label.upper(), y, 3)
            y -= 0.08 * inch
        self.end()

    def notes_page(self) -> None:
        self.frame("Open notes")
        c = self.c
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(self.mx, self.h - 0.86 * inch, "Open notes")
        c.setFillColor(MID)
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(self.mx, self.h - 1.08 * inch, "Keep what helps. Leave the rest open.")
        c.setStrokeColor(LIGHT)
        y = self.h - 1.38 * inch
        while y > .72 * inch:
            c.line(self.mx, y, self.w - self.mx, y)
            y -= .28 * inch
        self.end()

    def build(self) -> int:
        self.title_page()
        self.rights_page()
        self.how_to_page()
        self.starter_page()
        # One entry, one task-shaped work surface, and one return page form an
        # intentionally different three-page loop for every product profile.
        cycles = max(12, (self.profile["pages"] - self.n - 6) // 3)
        for cycle in range(cycles):
            self.entry_page(cycle)
            self.work_surface(cycle)
            self.reflection_page(cycle)
        while self.n < self.profile["pages"]:
            self.notes_page()
        if self.n % 2:
            self.notes_page()
        self.c.save()
        return self.n


def motif_group(profile: dict) -> str:
    surface = profile["surface"]
    if surface in {"route_map", "meeting_map", "decision_canvas", "project_path", "milestone_arc", "hybrid_grid", "handoff_board"}:
        return "route"
    if surface in {"recipe_card", "photo_frame", "specimen_frame", "letter_sheet", "time_capsule", "home_story", "catalog_grid", "object_tag"}:
        return "cards"
    if surface in {"palette_grid", "bake_matrix", "mending_board", "zine_fold"}:
        return "making"
    if surface in {"season_grid", "season_wheel"}:
        return "season"
    if surface in {"table_plan", "supper_table", "picnic_map", "screening_map", "gift_menu", "cafe_counter"}:
        return "gather"
    if surface in {"decision_tree", "kitchen_map", "arrival_map", "repair_record", "weekly_strip"}:
        return "blocks"
    return "rings"


def draw_pdf_motif(c: canvas.Canvas, w: float, h: float, accent, group: str) -> None:
    c.setStrokeColor(accent)
    c.setLineWidth(1)
    cx, cy = w * .76, h * .79
    if group == "route":
        pts = [(w*.53,h*.93),(w*.64,h*.80),(w*.72,h*.86),(w*.82,h*.70),(w*.91,h*.76)]
        path = c.beginPath(); path.moveTo(*pts[0])
        for point in pts[1:]: path.lineTo(*point)
        c.drawPath(path, stroke=1, fill=0)
        for x, y in pts: c.circle(x, y, .065*inch, stroke=1, fill=0)
    elif group == "cards":
        for i, (dx, dy) in enumerate(((.52,.70),(.67,.80),(.78,.65))):
            c.saveState(); c.translate(w*dx,h*dy); c.rotate((-12,4,14)[i]); c.roundRect(-.43*inch,-.58*inch,.86*inch,1.16*inch,4,stroke=1,fill=0); c.restoreState()
    elif group == "making":
        for i in range(7):
            x = w*.54 + i*.065*inch; y = h*.70 + (i%2)*.12*inch
            c.circle(x,y,.115*inch,stroke=1,fill=0)
        c.line(w*.55,h*.86,w*.92,h*.64)
    elif group == "season":
        for radius in (.34,.64,.94): c.circle(cx,cy,radius*inch,stroke=1,fill=0)
        for angle in range(0,360,45):
            a=math.radians(angle); c.line(cx+math.cos(a)*.34*inch,cy+math.sin(a)*.34*inch,cx+math.cos(a)*.94*inch,cy+math.sin(a)*.94*inch)
    elif group == "gather":
        for dx, dy in ((.62,.84),(.78,.84),(.70,.67)):
            c.circle(w*dx,h*dy,.18*inch,stroke=1,fill=0)
            c.line(w*dx-.1*inch,h*dy-.27*inch,w*dx+.1*inch,h*dy-.27*inch)
    elif group == "blocks":
        for i in range(3):
            x=w*(.56+i*.12); y=h*(.69+(i%2)*.12)
            c.roundRect(x,y,.58*inch,.38*inch,5,stroke=1,fill=0)
            if i: c.line(x-.12*inch,y+.19*inch,x,y+.19*inch)
    else:
        for radius in (.82,1.18,1.54): c.circle(cx,cy,radius*inch,fill=0,stroke=1)


def make_front_cover(candidate: dict[str, str], profile: dict, trim: tuple[float, float], palette: tuple[str, str], path: Path) -> None:
    bg, accent = (colors.HexColor("#" + value) for value in palette)
    w, h = trim[0] * inch, trim[1] * inch
    c = canvas.Canvas(str(path), pagesize=(w, h), pageCompression=1)
    c.setFillColor(bg)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    draw_pdf_motif(c, w, h, accent, motif_group(profile))
    centered(c, candidate["working_title"], w / 2, h * .58, w - 1.1 * inch, 22, 26, colors.white, "Helvetica-Bold")
    centered(c, candidate["subtitle_concept"], w / 2, h * .45, w - 1.2 * inch, 9.2, 12, accent)
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 8)
    c.drawCentredString(w / 2, h * .19, AUTHOR)
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(w / 2, .38 * inch, "LOCAL PROTOTYPE - NOT FOR MANUFACTURE")
    c.save()


def make_paperback_wrap(candidate: dict[str, str], profile: dict, trim: tuple[float, float], pages: int, palette: tuple[str, str], path: Path) -> tuple[float, float, float]:
    bg, accent = (colors.HexColor("#" + value) for value in palette)
    tw, th = trim
    spine = pages * PPI
    wrap_w = 2 * BLEED + 2 * tw + spine
    wrap_h = 2 * BLEED + th
    w, h = wrap_w * inch, wrap_h * inch
    c = canvas.Canvas(str(path), pagesize=(w, h), pageCompression=1)
    c.setFillColor(bg)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    draw_pdf_motif(c, w, h, accent, motif_group(profile))
    spine_x = (BLEED + tw) * inch
    c.setStrokeColor(colors.Color(1, 1, 1, alpha=.25))
    c.line(spine_x, 0, spine_x, h)
    c.line(spine_x + spine * inch, 0, spine_x + spine * inch, h)
    front_x = (BLEED + tw + spine) * inch
    centered(c, candidate["working_title"], front_x + tw * inch / 2, h * .59, tw * inch - .8 * inch, 21, 25, colors.white, "Helvetica-Bold")
    centered(c, candidate["subtitle_concept"], front_x + tw * inch / 2, h * .46, tw * inch - .9 * inch, 8.9, 11.5, accent)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.white)
    c.drawCentredString(front_x + tw * inch / 2, h * .17, AUTHOR)
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 5.7)
    c.drawCentredString(front_x + tw * inch / 2, .38 * inch, "LOCAL PROTOTYPE - NOT FOR UPLOAD")
    back_x = BLEED * inch + .36 * inch
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(back_x, h * .67, "PRODUCT PROTOTYPE")
    back_copy = (
        f"A local prototype for {candidate['core_job'].lower()}. "
        "No public release, price, platform decision, or product claim is authorized."
    )
    draw_wrapped(c, back_copy, back_x, h * .62, tw * inch - .75 * inch, 8, 10.5, colors.white)
    c.setFillColor(colors.white)
    c.roundRect(.33 * inch, .35 * inch, 1.95 * inch, 1.18 * inch, 3, fill=1, stroke=0)
    c.setFillColor(bg)
    c.setFont("Helvetica-Bold", 5.4)
    c.drawCentredString(1.305 * inch, .88 * inch, "NO BARCODE")
    c.setFont("Helvetica", 4.7)
    c.drawCentredString(1.305 * inch, .68 * inch, "LOCAL PROTOTYPE ONLY")
    if spine >= .18:
        c.saveState()
        c.translate(spine_x + spine * inch / 2, .36 * inch)
        c.rotate(90)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", max(4, min(7, spine * 28)))
        c.drawCentredString(th * inch / 2, 0, candidate["working_title"].upper())
        c.restoreState()
    c.save()
    return spine, wrap_w, wrap_h


def image_font(size: int, bold: bool = False):
    choices = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for choice in choices:
        if Path(choice).exists():
            return ImageFont.truetype(choice, size)
    return ImageFont.load_default()


def img_lines(draw: ImageDraw.ImageDraw, text: str, font, width: int) -> list[str]:
    words, rows, current = text.split(), [], ""
    for word in words:
        candidate = (current + " " + word).strip()
        if not current or draw.textbbox((0, 0), candidate, font=font)[2] <= width:
            current = candidate
        else:
            rows.append(current)
            current = word
    if current:
        rows.append(current)
    return rows


def image_center(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, font, color: str, width: int, leading: int) -> None:
    rows = img_lines(draw, text, font, width)
    y -= leading * (len(rows) - 1) // 2
    for row in rows:
        draw.text((x, y), row, font=font, fill=color, anchor="mm")
        y += leading


def draw_image_motif(draw: ImageDraw.ImageDraw, w: int, h: int, accent: str, group: str) -> None:
    if group == "route":
        points = [(640,150),(760,275),(885,190),(1010,380),(1120,285)]
        draw.line(points, fill=accent, width=5)
        for x, y in points: draw.ellipse((x-16,y-16,x+16,y+16), outline=accent, width=4)
    elif group == "cards":
        for i, (x, y, angle) in enumerate(((690,145,-12),(845,225,4),(970,135,14))):
            card=Image.new("RGBA",(150,210),(0,0,0,0)); card_draw=ImageDraw.Draw(card); card_draw.rounded_rectangle((5,5,145,205),radius=10,outline=accent,width=4)
            card=card.rotate(angle,expand=True); draw.bitmap((x-card.width//2,y-card.height//2),card,fill=None)
    elif group == "making":
        for i in range(7):
            x=650+i*65; y=260+(i%2)*88; draw.ellipse((x-42,y-42,x+42,y+42),outline=accent,width=4)
        draw.line((630,130,1120,400),fill=accent,width=4)
    elif group == "season":
        cx,cy=930,230
        for radius in (80,150,220): draw.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline=accent,width=4)
        for angle in range(0,360,45):
            a=math.radians(angle); draw.line((cx+math.cos(a)*80,cy+math.sin(a)*80,cx+math.cos(a)*220,cy+math.sin(a)*220),fill=accent,width=3)
    elif group == "gather":
        for x,y in ((770,175),(1000,175),(885,370)):
            draw.ellipse((x-62,y-62,x+62,y+62),outline=accent,width=4); draw.line((x-38,y+92,x+38,y+92),fill=accent,width=4)
    elif group == "blocks":
        for i,(x,y) in enumerate(((700,225),(865,150),(1015,315))):
            draw.rounded_rectangle((x,y,x+150,y+95),radius=12,outline=accent,width=4)
            if i: draw.line((x-55,y+47,x,y+47),fill=accent,width=4)
    else:
        for radius in (230,340,450): draw.ellipse((w-190-radius,210-radius,w-190+radius,210+radius),outline=accent,width=3)


def make_preview(candidate: dict[str, str], profile: dict, palette: tuple[str, str], path: Path) -> None:
    bg, accent = "#" + palette[0], "#" + palette[1]
    w, h = 1200, 1800
    image = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(image)
    draw_image_motif(draw, w, h, accent, motif_group(profile))
    image_center(draw, candidate["working_title"], w // 2, int(h * .45), image_font(72, True), "#FFFFFF", w - 150, 88)
    image_center(draw, candidate["subtitle_concept"], w // 2, int(h * .60), image_font(30), accent, w - 175, 42)
    draw.text((w // 2, h - 245), AUTHOR, font=image_font(25), fill="#FFFFFF", anchor="mm")
    draw.text((w // 2, h - 105), "LOCAL PROTOTYPE - HOLD", font=image_font(18, True), fill=accent, anchor="mm")
    image.save(path, quality=92)


def render_sample(interior: Path, path: Path) -> None:
    doc = fitz.open(interior)
    page = doc[min(3, doc.page_count - 1)]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    pix.save(path)
    doc.close()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def product_brief(candidate: dict[str, str], profile: dict, page_count: int, trim: tuple[float, float], route_kind: str) -> str:
    first_test = candidate["first_test"]
    return f"""# {candidate['candidate_id']} - {candidate['working_title']}

## Local prototype status

**{STATUS}**

This package is a controlled original-content prototype built at the owner’s direction. It is not a public listing, manufacturing file, price decision, upload package, or approval to release.

## Product definition

| Field | Current prototype definition |
|---|---|
| Primary niche | {candidate['primary_niche']} |
| Core customer job | {candidate['core_job']} |
| Product form under test | {candidate['primary_format']} |
| Route in this package | {route_kind} |
| Prototype trim | {trim[0]:g} x {trim[1]:g} in. |
| Prototype pages | {page_count} |
| Differentiation hypothesis | {candidate['differentiation']} |
| First validation test | {first_test} |

## Original page architecture

- Opening pages: prototype boundary, customer-use orientation, and a product-specific starting map.
- Repeating sequence: **{profile['cycle']}** entry -> **{profile['surface'].replace('_', ' ')}** work surface -> return note.
- Closing pages: open notes for the user’s own material.

## Boundary

{candidate['claims_boundary']}

## Required next decision

Before this can move beyond local prototype status: record original-asset provenance; complete a title/rights screen; validate the chosen product route with a current printer, vendor, or platform; complete any product-specific accessibility/claims review; inspect a physical proof or appropriate usability sample; then obtain named-human release approval.

## Local author attribution

**Author shown in prototype:** {AUTHOR}

This is owner-directed provisional local attribution only. It does not establish name, trademark, publicity, or public-use clearance. The separate working-imprint decision remains unresolved.
"""


def route_notes(candidate: dict[str, str], page_count: int, trim: tuple[float, float], direct: bool) -> str:
    if direct:
        return f"""# Production route note - {candidate['candidate_id']}

**Status:** local prototype route note only. This is not an RFQ, purchase order, vendor instruction, or manufacturing authorization.

## Why this package is front-cover plus interior prototype

The registered route is **{candidate['route_recommendation']}**. A generic paperback wrap would misrepresent that decision. The included `{candidate['candidate_id']}` interior is a usability and editorial prototype at {trim[0]:g} x {trim[1]:g} in. / {page_count} pages, and the front cover is a visual concept only.

## Required production work before any physical run

1. Human confirmation of the customer-job evidence and final product form.
2. Original-art, contributor, and component provenance record.
3. Selected-vendor dielines, materials, tolerances, packaging, assembly, and accessibility review.
4. Product-specific claims/title review and a signed physical proof.
5. Named-human commercial, price, channel, and release decision.
"""
    return f"""# Paperback route note - {candidate['candidate_id']}

**Status:** local prototype route note only. The wrap is a dimensional draft and is not an upload file.

## Prototype geometry

- Trim: {trim[0]:g} x {trim[1]:g} in.
- Pages: {page_count}
- Interior: black-and-white prototype pages; final paper/ink/bleed choice is unapproved.
- Spine calculation: {page_count} x {PPI:.6f} in. = {page_count * PPI:.4f} in. white-paper working estimate.

## Required before a platform upload or print run

Use current platform/vendor specifications, rebuild the exact wrap after final page/material settings, complete title/rights and product-specific boundary review, inspect the platform preview and physical proof, then obtain a named-human release decision.
"""


def package_manifest(candidate: dict[str, str], profile: dict, page_count: int, trim: tuple[float, float], direct: bool, files: list[Path]) -> dict:
    return {
        "candidate_id": candidate["candidate_id"],
        "working_title": candidate["working_title"],
        "status": STATUS,
        "author": AUTHOR,
        "author_status": "owner-directed provisional local attribution only",
        "primary_niche": candidate["primary_niche"],
        "core_job": candidate["core_job"],
        "route_recommendation": candidate["route_recommendation"],
        "route_asset": "front_cover_concept.pdf" if direct else "paperback_cover_wrap.pdf",
        "prototype_trim_inches": list(trim),
        "prototype_page_count": page_count,
        "cycle": profile["cycle"],
        "claims_boundary": candidate["claims_boundary"],
        "first_test": candidate["first_test"],
        "files": {file.name: sha256(file) for file in files if file.exists()},
    }


def write_root_docs(candidates: list[dict[str, str]], records: list[dict]) -> None:
    rows = [
        "# Expansion 36 local prototype packages",
        "",
        f"**Status:** {STATUS}.",
        "",
        "The owner directed construction of all 36 candidate packages as original local prototypes. This changes their artifact state from research-only candidates to controlled prototype packages; it does **not** add them to the 18-SKU canonical portfolio or authorize public identity use, prices, listings, uploads, manufacturer contact, manufacture, sale, advertising, translation, or release.",
        "",
        "## Package rule",
        "",
        "Each folder has an original, product-specific interior prototype, a cover concept, a preview image, a product brief, a route note, and a checksum manifest. Paperback-route concepts contain a dimensional working wrap marked not for upload. Direct-first concepts contain a front-cover concept instead of a misleading paperback wrap.",
        "",
        "## Decision gate",
        "",
        "Each package must independently receive evidence, title/rights/provenance review, product-specific claims/accessibility review where applicable, current printer/platform validation, appropriate proof/usability review, commercial channel/price decisions, and named-human release approval. Structural completion is not release approval.",
        "",
        "## Inventory",
        "",
        "| ID | Title | Route asset | Prototype pages | Status |",
        "|---|---|---|---:|---|",
    ]
    for record in records:
        rows.append(f"| {record['candidate_id']} | {record['working_title']} | `{record['route_asset']}` | {record['prototype_page_count']} | HOLD |")
    (ROOT / "EXPANSION_36_LOCAL_PROTOTYPES.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    fields = ["candidate_id", "working_title", "primary_niche", "core_job", "route_recommendation", "route_asset", "prototype_trim_inches", "prototype_page_count", "status", "author", "author_status", "claims_boundary", "first_test"]
    with (ROOT / "EXPANSION_36_LOCAL_PRODUCTION_REGISTER.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for record in records:
            row = {key: record.get(key, "") for key in fields}
            row["prototype_trim_inches"] = "x".join(str(x) for x in record["prototype_trim_inches"])
            writer.writerow(row)


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    candidates = list(csv.DictReader(SOURCE.open(encoding="utf-8", newline="")))
    ids = [row["candidate_id"] for row in candidates]
    if ids != [f"E{i:02d}" for i in range(1, 37)]:
        raise ValueError("Expected exactly sequential candidate IDs E01 through E36")
    if set(PROFILES) != set(ids):
        raise ValueError("Profile map must contain exactly one profile for each candidate")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / "README.md").write_text(
        "# Expansion 36 - controlled local prototype packages\n\n"
        f"**Status:** {STATUS}.\n\n"
        "Each E01-E36 folder contains an original interior prototype, route-appropriate cover concept, "
        "two visual previews, product brief, production-route note, and checksum manifest. These are "
        "not customer files or release candidates. See `../EXPANSION_36_LOCAL_PROTOTYPES.md` for the "
        "catalog-wide inventory and release boundary.\n",
        encoding="utf-8",
    )
    records = []
    for index, candidate in enumerate(candidates):
        ident = candidate["candidate_id"]
        profile = PROFILES[ident]
        trim = parse_trim(candidate["primary_format"])
        palette = style_for(index)
        folder = OUT / f"{ident}-{slugify(candidate['working_title'])}"
        folder.mkdir()
        interior = folder / "interior_prototype.pdf"
        pages = PrototypeBook(interior, trim, candidate, profile, palette).build()
        direct = ident in DIRECT_FIRST
        cover = folder / ("front_cover_concept.pdf" if direct else "paperback_cover_wrap.pdf")
        if direct:
            make_front_cover(candidate, profile, trim, palette, cover)
        else:
            make_paperback_wrap(candidate, profile, trim, pages, palette, cover)
        preview = folder / "cover_preview.jpg"
        make_preview(candidate, profile, palette, preview)
        sample = folder / "interior_sample.jpg"
        render_sample(interior, sample)
        brief = folder / "PRODUCT_BRIEF.md"
        brief.write_text(product_brief(candidate, profile, pages, trim, "direct-first prototype" if direct else "paperback prototype"), encoding="utf-8")
        route = folder / "PRODUCTION_ROUTE.md"
        route.write_text(route_notes(candidate, pages, trim, direct), encoding="utf-8")
        files = [interior, cover, preview, sample, brief, route]
        manifest = package_manifest(candidate, profile, pages, trim, direct, files)
        manifest_path = folder / "package_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        manifest["folder"] = str(folder.relative_to(ROOT))
        records.append(manifest)
    write_root_docs(candidates, records)
    print(f"Built {len(records)} controlled local prototype packages in {OUT}")


if __name__ == "__main__":
    main()
