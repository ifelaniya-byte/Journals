# Minimum-price markets: platforms whose floor is over $10

Matched-pricing editions from each platform's own minimum rules. All $0 upfront.
Main catalog stays $9.99 everywhere. Interiors unchanged.
Hardcover: journals LIST, coloring HOLD. B&N print: ≥120pp LIST, thin HOLD.

| Book | Pages | KDP-HC cost | HC floor | HC entry | HC royalty |
|---|---|---|---|---|---|
| **HOLD** Architectural Visions: Cathedral and Cityscape Coloring Book for Adults | 140 | $7.33 | $12.22 | $13.99 | $1.06 |
| The 5-Minute Dump: Micro-Journal for People Who Hate Journaling | 200 | $8.05 | $13.42 | $15.99 | $1.54 |
| **HOLD** First Strokes: Easy Coloring Book for Adult Beginners | 100 | $6.80 | $11.33 | $13.99 | $1.59 |
| **HOLD** Fractal Dreams: Advanced Mathematical Coloring Book | 140 | $7.33 | $12.22 | $13.99 | $1.06 |
| **HOLD** Easy Garden: Bold and Easy Flower Coloring Book for Adults | 100 | $6.80 | $11.33 | $13.99 | $1.59 |
| **HOLD** Mosaic Mind: Geometric Coloring Book for Adults | 120 | $7.09 | $11.82 | $13.99 | $1.30 |
| The Night Pages: An Insomnia Journal for 3 A.M.  [NO hardcover: 5x8 not a KDP HC trim] | 120 | - | - | - | - |
| Parallel Lives: A Split-Page Therapy Journal | 160 | $7.57 | $12.62 | $14.99 | $1.42 |
| **HOLD** Woodland Wonders: Forest Animals Coloring Book for Adults | 120 | $7.09 | $11.82 | $13.99 | $1.30 |
| **HOLD** Botanical Ink: Fine-Line Floral Coloring Book for Adults | 104 | $6.80 | $11.33 | $13.99 | $1.59 |
| **HOLD** Celestial Atlas: Constellation Coloring Book for Adults | 104 | $6.80 | $11.33 | $13.99 | $1.59 |
| **HOLD** Cozy Corners: Cozy Spaces Coloring Book for Adults | 104 | $6.80 | $11.33 | $13.99 | $1.59 |
| The Dopamine Menu: An ADHD Journal for Ordering Your Stimulation | 150 | $7.45 | $12.42 | $14.99 | $1.54 |
| The Middle Season: Perimenopause Symptom Tracker & Journal | 160 | $7.57 | $12.62 | $14.99 | $1.42 |
| Settle: A Somatic Journal for a Wired Nervous System | 172 | $7.71 | $12.85 | $14.99 | $1.28 |
| The Slow Page: A Slow Living Journal for Four Seasons | 144 | $7.38 | $12.30 | $13.99 | $1.01 |
| The 75 Soft Journal | 96 | $6.80 | $11.33 | $13.99 | $1.59 |
| **HOLD** Tidal Ink: Jellyfish and Deep-Sea Fine-Line Coloring Book for Adults | 104 | $6.80 | $11.33 | $13.99 | $1.59 |

**LIST 7 journal hardcovers** (dump, settle, parallel, middle, dopamine, slow, soft).
**HOLD 10 coloring hardcovers** — kits exist; do not upload (PLATFORM_DECISIONS.md).
Night Pages has NO hardcover kit: 5x8 is not among KDP's hardcover trims
(5.5x8.5, 6x9, 6.14x9.21, 6.69x9.61, 7x10, 7.44x9.69, 7.5x9.25, 8.5x11), and
interiors are locked so we do not resize. Verify the 8.5x11 hardcover option in
KDP's size picker at setup (source lists differ slightly on the largest sizes).

Blurb kits live in markets/blurb/ (one per book; entry = estimated base + $1;
confirm base cost AND trim availability in their calculator before publishing).
B&N Press print ($14.99 platform minimum): markets/bn-print/.

## Floors over $10 NOT entered at the minimum (zero royalty at floor)
| Platform | Format | Our floor | Why
|---|---|---|---|
| Lulu | hardcover | ~$21+ (mfg ~$20.22 at 160pp) | minimum = breakeven; $0 at floor |
| IngramSpark | hardcover | ~$23.56 (200pp, 55% discount) | minimum = breakeven; $0 at floor |

IngramSpark paperback floors are under $10 for all 18 books; standard $9.99 works there.

Regenerate: python3 make_min_market_kits.py (deterministic)
