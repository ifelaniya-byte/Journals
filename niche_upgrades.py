#!/usr/bin/env python3
"""Listing-side upgrades for the Quiet Mind Press 18.

Interiors and wrap PDFs are NOT regenerated. Covers keep their short brand
titles; Amazon titles below carry the search phrase.

Rules enforced by gen_catalog.py:
  - keywords: EXACTLY 7 per title, unique across the whole catalog
  - no medical-protocol keywords (vagus stimulation, polyvagal exercises,
    sleep-disorder / ADHD-as-disease browse nodes)
"""

# Amazon TITLE (≤200). Cover PDF still uses the short brand name.
TITLES = {
    "dump": "The 5-Minute Dump: Micro-Journal for People Who Hate Journaling",
    "parallel": "Parallel Lives: A Split-Page Therapy Journal",
    "night": "The Night Pages: An Insomnia Journal for 3 A.M.",
    "firststroke": "First Strokes: Easy Coloring Book for Adult Beginners",
    "garden": "Easy Garden: Bold and Easy Flower Coloring Book for Adults",
    "mosaic": "Mosaic Mind: Geometric Coloring Book for Adults",
    "woodland": "Woodland Wonders: Forest Animals Coloring Book for Adults",
    "fractal": "Fractal Dreams: Advanced Mathematical Coloring Book",
    "architect": "Architectural Visions: Cathedral and Cityscape Coloring Book for Adults",
    "settle": "Settle: A Somatic Journal for a Wired Nervous System",
    "middle": "The Middle Season: Perimenopause Symptom Tracker & Journal",
    "dopamine": "The Dopamine Menu: An ADHD Journal for Ordering Your Stimulation",
    "slow": "The Slow Page: A Slow Living Journal for Four Seasons",
    "soft": "The 75 Soft Journal",
    "cozy": "Cozy Corners: Cozy Spaces Coloring Book for Adults",
    "botanical": "Botanical Ink: Fine-Line Floral Coloring Book for Adults",
    "celestial": "Celestial Atlas: Constellation Coloring Book for Adults",
    "tidal": "Tidal Ink: Jellyfish and Deep-Sea Fine-Line Coloring Book for Adults",
}

SUBTITLES = {
    "dump": "200 Pages of Rotating Five-Minute Prompts, Undated",
    "parallel": "160 Pages of Side-by-Side Prompts: What Happened and How It Felt",
    "night": "A 5 by 8 Pocket Nightstand Journal for Racing Thoughts",
    "firststroke": "37 Super Simple Designs with 3 to 5 Large Shapes per Page",
    "garden": "47 Big and Simple Designs with Thick Lines",
    "mosaic": "57 Stained-Glass Mosaics, Tessellations and Islamic Stars",
    "woodland": "57 Cottagecore Designs: Owls, Foxes, Mushrooms and Ferns",
    "fractal": "67 Real Fractals: Sierpinski, Julia Sets and Golden Spirals",
    "architect": "67 Intricate Cathedrals, Cityscapes and Rose Windows",
    "settle": "Daily Body Tracking with No Protocol and No Streaks, Undated",
    "middle": "Hot Flashes, Sleep, Brain Fog and Clinic Notes, Undated",
    "dopamine": "Five Courses and a Daily Order Ticket, 150 Pages",
    "slow": "One Unhurried Page a Day for Four Seasons",
    "soft": "A Gentler 75-Day Challenge Tracker with a Day 76 Page",
    "cozy": "49 Cozy Spaces: Reading Nooks, Rainy Windows and Hygge Rooms",
    "botanical": "49 Herbarium Plates with Real Phyllotaxis Spirals",
    "celestial": "49 Constellation Plates from Real Star Positions",
    "tidal": "49 Fine-Line Deep-Sea Plates from Real Logarithmic Spirals",
}

# Two Amazon series — do not mix journals and coloring in one series.
SERIES = {
    "dump": "Quiet Mind Journals",
    "parallel": "Quiet Mind Journals",
    "night": "Quiet Mind Journals",
    "settle": "Quiet Mind Journals",
    "middle": "Quiet Mind Journals",
    "dopamine": "Quiet Mind Journals",
    "slow": "Quiet Mind Journals",
    "soft": "Quiet Mind Journals",
    "firststroke": "Quiet Mind Color",
    "garden": "Quiet Mind Color",
    "mosaic": "Quiet Mind Color",
    "woodland": "Quiet Mind Color",
    "fractal": "Quiet Mind Color",
    "architect": "Quiet Mind Color",
    "cozy": "Quiet Mind Color",
    "botanical": "Quiet Mind Color",
    "celestial": "Quiet Mind Color",
    "tidal": "Quiet Mind Color",
}

DIFFICULTY = {
    "firststroke": "Beginner",
    "garden": "Beginner",
    "cozy": "Beginner–Easy",
    "woodland": "Intermediate",
    "mosaic": "Intermediate",
    "botanical": "Fine line",
    "tidal": "Fine line",
    "celestial": "Fine line",
    "fractal": "Advanced",
    "architect": "Advanced",
}

# Printed on every coloring listing. Too-easy / too-hard next title.
LADDER = [
    ("firststroke", "First Strokes"),
    ("garden", "Easy Garden"),
    ("cozy", "Cozy Corners"),
    ("woodland", "Woodland Wonders"),
    ("mosaic", "Mosaic Mind"),
    ("botanical", "Botanical Ink"),
    ("tidal", "Tidal Ink"),
    ("celestial", "Celestial Atlas"),
    ("fractal", "Fractal Dreams"),
    ("architect", "Architectural Visions"),
]

JOURNAL_STACKS = {
    "dump": "Pairs with The Dopamine Menu (ADHD stack).",
    "dopamine": "Pairs with The 5-Minute Dump (ADHD stack).",
    "night": "Pairs with Settle (night anxiety + body).",
    "settle": "Pairs with The Night Pages (3 a.m.) or The Middle Season (peri).",
    "middle": "Pairs with Settle (body) when symptoms are loud.",
    "slow": "Gift with Cozy Corners (Quiet Mind Color).",
    "soft": "Standalone 75-day track. After day 76, try The Slow Page.",
    "parallel": "Standalone therapy journal. Pairs with Settle if the body is loud.",
}

KEYWORDS = {
    "dump": "5 minute journal, adhd brain dump notebook, micro journal for beginners, low effort journaling, brain dump journal undated, journal for people who hate journaling, tiny prompts journal",
    "parallel": "side by side journal, dual column therapy journal, cbt journal for adults, split page journal, overthinking journal prompts, two perspective notebook, self awareness journal",
    "night": "insomnia journal undated, 3am journal, can't sleep notebook, racing thoughts journal, bedside pocket journal, night anxiety writing, worry dump journal",
    "firststroke": "easy coloring book for adults, large print coloring book for seniors, thick lines coloring book, simple coloring book for seniors, beginner coloring book adults, large shapes coloring, marker friendly coloring book",
    "garden": "bold and easy coloring book for adults, flower coloring book large print, thick line coloring book for adults, simple garden coloring book, flower coloring book for adults, beginner flower coloring book, garden coloring book for adults",
    "mosaic": "mosaic coloring book for adults, stained glass coloring book, geometric coloring book adults, tessellation coloring book, islamic star coloring book, celtic knot coloring, geometric coloring book for men",
    "woodland": "woodland animals coloring book, forest coloring book adults, cottagecore coloring forest, mushroom coloring book adults, cottagecore coloring book, nature scenes coloring book, wildlife coloring book adults",
    "fractal": "fractal coloring book adults, real mathematics coloring, sacred geometry coloring book, advanced intricate coloring, sierpinski coloring pages, complex pattern coloring book, math coloring book for adults",
    "architect": "architecture coloring book for adults, cathedral coloring book, gothic coloring book for adults, cityscape coloring book for adults, travel coloring book for adults, stained glass windows coloring, building coloring book for adults",
    "settle": "somatic journal undated, grounding journal for anxiety, nervous system journal, body scan notebook, settle journal, trauma informed journal, regulation tracking journal",
    "middle": "perimenopause journal, perimenopause symptom tracker, hot flash log book, night sweats tracker, midlife hormone journal, brain fog journal women, menopause transition notebook",
    "dopamine": "dopamine menu journal, adhd journal for adults, dopamine menu template book, executive function journal, neurodivergent daily journal, adhd stimulation tracker, adhd motivation notebook",
    "slow": "slow living journal, seasonal living notebook, hygge daily journal, intentional living journal, four seasons journal, unhurried morning pages, quiet life journal",
    "soft": "75 soft journal, 75 day gentle challenge, 75 soft tracker undated, gentle habit challenge book, kind fitness journal, 75 day wellness tracker, soft challenge workbook",
    "cozy": "cozy coloring book adults, cozy spaces coloring, hygge coloring book, reading nook coloring pages, cottagecore interiors coloring, fireplace coloring book, aesthetic cozy coloring",
    "botanical": "botanical coloring book adults, fine line floral coloring, herbarium coloring book, vintage botanical line art, detailed flower coloring adults, botanical garden coloring book, plant lover coloring book",
    "celestial": "constellation coloring book, celestial coloring book adults, real star map coloring, moon phases coloring book, astronomy coloring adults, galaxy fine line coloring, night sky coloring book",
    "tidal": "jellyfish coloring book adults, ocean coloring book adults, nautilus spiral coloring, deep sea coloring book, marine life fine line coloring, coastal coloring book adults, underwater coloring pages",
}

# Safer than Health > Sleep Disorders / Nervous System / ADHD-as-disease / Science > Math.
CATEGORIES = {
    "dump": "Self-Help / Journaling | Self-Help / Anxieties & Phobias",
    "parallel": "Self-Help / Journaling | Self-Help / Personal Growth",
    "night": "Self-Help / Journaling | Self-Help / Anxieties & Phobias",
    "firststroke": "Crafts / Coloring Books | Self-Help / Stress Management",
    "garden": "Crafts / Coloring Books | Crafts / Nature",
    "mosaic": "Crafts / Coloring Books | Crafts / Mandalas & Patterns",
    "woodland": "Crafts / Coloring Books | Crafts / Animals",
    "fractal": "Crafts / Coloring Books | Crafts / Mandalas & Patterns",
    "architect": "Crafts / Coloring Books | Crafts / Architecture",
    "settle": "Self-Help / Journaling | Self-Help / Stress Management",
    "middle": "Health / Women's Health | Self-Help / Journaling",
    "dopamine": "Self-Help / Journaling | Self-Help / Personal Growth",
    "slow": "Self-Help / Journaling | Self-Help / Motivational",
    "soft": "Health / Fitness | Self-Help / Journaling",
    "cozy": "Crafts / Coloring Books | Self-Help / Stress Management",
    "botanical": "Crafts / Coloring Books | Arts / Drawing",
    "celestial": "Crafts / Coloring Books | Arts / Drawing",
    "tidal": "Crafts / Coloring Books | Crafts / Animals",
}

# Listing-side only. Night to $9.99 (pocket impulse). Middle $16.99 → $13.99
# (peri will pay, but not +70% over a $9.99 competitor).
# PRICE POLICY (listing-side only): catalog-wide $9.99 cap — owner decision 2026-08-28.
# Matches the kit line's price point; one clean impulse price across all 18.
PRICE_CAP = 9.99
PRICES = {}  # per-title overrides (none — cap applies uniformly)


def cap_price(price_str):
    try:
        v = float(str(price_str).replace("$", ""))
    except ValueError:
        return price_str
    return f"${min(v, PRICE_CAP):.2f}"

# Extra sentences appended to the original interior-faithful description.
DESC_APPEND = {
    "dump": " Mechanism: five minutes, rotating micro-prompts, no essays.",
    "parallel": " Mechanism: every spread is split — what happened / how it felt.",
    "night": " Mechanism: 5×8 nightstand size, prompts written for the dark.",
    "firststroke": " Difficulty: Beginner. Single-sided. Thick marker-friendly lines. 37 designs of 3 to 5 large shapes, nothing tiny.",
    "garden": " Difficulty: Beginner. Single-sided pages. Thick marker-friendly lines.",
    "mosaic": " Difficulty: Intermediate.",
    "woodland": " Difficulty: Intermediate. Single-sided. 57 cottagecore forest designs.",
    "fractal": " Difficulty: Advanced. Single-sided. Every plate generated from real mathematics, not clip-art.",
    "architect": " Difficulty: Advanced.",
    "settle": " Language is tracking-only: state, where in the body, what helped, state after. No diagnosis, no protocol to fail, no streaks.",
    "middle": " Pairs with Settle when the body is loud.",
    "dopamine": " Mechanism: five courses (starters, mains, sides, specials, desserts) plus a daily order ticket.",
    "slow": " Gift with Cozy Corners from Quiet Mind Color.",
    "soft": " 96 pages on purpose: 75 daily trackers, weekly recaps with no score, and a Day 76 page. Not a punishment-reset challenge — the sixth rule is be kind to yourself.",
    "cozy": " Difficulty: Beginner to Easy. Single-sided, frame-able. 49 cozy spaces.",
    "botanical": " Difficulty: Fine line. Real phyllotaxis spirals. Single-sided. 49 herbarium plates.",
    "celestial": " Difficulty: Fine line. Constellation plates from real star positions, magnitude-scaled. Single-sided. 49 plates.",
    "tidal": " Difficulty: Fine line. Nautilus from the real logarithmic spiral. Single-sided. 49 deep-sea plates.",
}

HOOKS = {
    "dump": "Each page takes five minutes or less. No long prompts. No essays.",
    "parallel": "Every spread splits the page in two. The gap between the two sides is where the insight lives.",
    "night": "This journal lives on your nightstand. When your brain won't shut up at 3am, open it.",
    "firststroke": "The simplest coloring book you'll find. 3–5 shapes per page. Lines so thick a marker can't miss.",
    "garden": "A garden that never needs watering. Thick, forgiving lines, one big subject per page. Bold and easy.",
    "mosaic": "The coloring sweet spot between too easy and too hard: mosaic tiles that build like stained glass.",
    "woodland": "Owls, foxes, deer, mushroom villages — cottagecore forest, flattened.",
    "fractal": "Generated from real mathematics. Not for beginners. For the colorist who has done everything else.",
    "architect": "Gothic cathedrals, dense cityscapes, rose windows. Every page rewards a whole afternoon.",
    "settle": "A somatic journal for anyone whose body holds what the mind can't talk down. No streaks. No fixing.",
    "middle": "A calm, private tracker for perimenopause — the years everyone talks around.",
    "dopamine": "Your brain runs on stimulation. The Dopamine Menu turns regulating it into a restaurant you run.",
    "slow": "One page a day, done slowly. Less than any journal you've abandoned.",
    "soft": "75 days of structure without the punishment. The sixth rule is be kind to yourself. Day 76 is in the book.",
    "cozy": "Reading nooks, rainy windows, string lights. Small scenes you can finish in one sitting.",
    "botanical": "Fine-line botanicals drawn the old way — ferns, monstera, herbarium plates. A garden that never wilts.",
    "celestial": "A night sky you color yourself. Real star positions, true moon terminators, quiet skies.",
    "tidal": "Jellyfish, nautilus, kelp. Every spiral is real mathematics. Color it blue. Or don't.",
}

ADS_LAUNCH = ["dopamine", "soft", "middle", "cozy"]

BANNED_FRAGMENTS = (
    "vagus nerve stimulation",
    "polyvagal exercises",
    "sleep disorders",
    "elderly coloring",
    "75 hard",
    "75 medium",
)
