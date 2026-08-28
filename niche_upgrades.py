#!/usr/bin/env python3
"""Niche-identification upgrades for our 18 titles (batch 3 + batch 4).

These override the PRODUCT dicts at metadata-generation time (gen_catalog.py)
so the build scripts remain untouched. Interiors/covers are unaffected —
keywords, categories, prices and descriptions are listing-side only.

Rules enforced by gen_catalog:
  - keywords: EXACTLY 7 per title, no duplicates across the catalog
  - price: only where a strategic change is justified (see comments)
"""

KEYWORDS = {
    # ── batch 3 ──────────────────────────────────────────────────────
    "dump": "5 minute journal, adhd brain dump, brain dump notebook, quick journal for anxiety, "
            "low effort journaling, micro journal prompts, journal for people who hate journaling",
    "parallel": "side by side journal, dual perspective journal, therapy journal for adults, cbt journal prompts, "
                "self awareness workbook, journaling for overthinkers, reflective writing journal",
    "night": "insomnia journal, journal for when you cant sleep, 3am journal, sleep anxiety notebook, "
             "racing thoughts journal, bedside journal prompts, worry dump before bed",
    "firststroke": "easy coloring book for adults, large print coloring book, simple coloring book for seniors, "
                   "thick lines coloring book, beginner coloring book, dementia coloring book, stroke recovery coloring",
    "garden": "flower coloring book for adults, easy botanical coloring book, garden coloring book, "
              "large print flower coloring, spring coloring book for adults, plant coloring book, relaxing floral coloring",
    "mosaic": "geometric coloring book for adults, tessellation coloring book, mosaic coloring book, "
              "islamic pattern coloring book, celtic knot coloring book, op art coloring book, intermediate mandala coloring",
    "woodland": "woodland coloring book, forest animals coloring book for adults, cottagecore forest coloring book, "
                "mushroom coloring book, fox coloring book, woodland creatures coloring, owl coloring book for adults",
    "fractal": "fractal coloring book, math coloring book for adults, sacred geometry coloring book, "
               "intricate coloring book for adults, complex coloring book, advanced detailed coloring book, geometric pattern coloring",
    "architect": "architecture coloring book, cityscape coloring book, cathedral coloring book, "
                 "stained glass coloring book for adults, building coloring book, fine line coloring book, detailed city coloring book",
    # ── batch 4 ──────────────────────────────────────────────────────
    "settle": "somatic journal, nervous system regulation workbook, polyvagal journal, grounding techniques journal, "
              "body scan journal, somatic exercises workbook, vagus nerve journal",
    "middle": "perimenopause journal, perimenopause symptom tracker, hot flash tracker journal, "
              "night sweats log book, menopause transition journal, perimenopause brain fog, hormone journal for women",
    "dopamine": "dopamine menu journal, adhd journal for adults, dopamine menu template, adhd motivation journal, "
                "executive function planner, neurodivergent journal prompts, adhd regulation journal",
    "slow": "slow living journal, seasonal living journal, hygge journal, intentional living workbook, "
            "quiet morning journal, slow living workbook, cozy lifestyle journal",
    "soft": "75 soft journal, 75 soft challenge tracker, 75 day challenge journal, 75 soft book for women, "
            "gentle fitness journal, 75 medium tracker, wellness challenge workbook",
    "cozy": "cozy coloring book, cozy spaces coloring book, cottagecore coloring book, hygge coloring book, "
            "aesthetic coloring book for adults, reading nook coloring book, fall coloring book for adults",
    "botanical": "botanical coloring book, fine line floral coloring book, botanical line art coloring, "
                 "detailed flower coloring book, herbarium coloring book, vintage botanical coloring, garden coloring book for adults",
    "celestial": "celestial coloring book, constellation coloring book, astronomy coloring book, "
                 "moon phase coloring book, space coloring book for adults, galaxy coloring book, star coloring book fine line",
    "tidal": "ocean coloring book for adults, jellyfish coloring book, sea life coloring book, "
             "nautilus coloring book, underwater coloring book, marine life coloring book, coastal coloring book",
}

# Strategic price moves (listing-side only; nothing printed in the books):
#   middle  $16.99 -> $13.99 : direct niche collision is priced at $9.99 on the other
#                              line; premium is defensible (160pp vs 107pp, richer
#                              weekly/monthly architecture) but not +70%.
#   night   $10.99 ->  $9.99 : pocket-format impulse price point; matches the floor.
PRICES = {"middle": "$13.99", "night": "$9.99"}

# Description extensions — appended niche identifiers (listing-side only).
DESC_APPEND = {
    "firststroke": " Occupational therapists and caregivers: the 3–5 shape pages double as fine-motor "
                   "practice for stroke recovery, dementia care, and tremor-friendly coloring.",
    "woodland": " Drawn in the cottagecore spirit — toadstools, ferns and quiet forest friends for "
                "anyone whose aesthetic lives somewhere between a cabin and a storybook.",
    "settle": " Language is trauma-informed and polyvagal-friendly: no diagnosis required, no protocol "
              "to fail — just state, body, tool, repeat.",
}
