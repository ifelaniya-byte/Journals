# Digital PDF editions: the $4.99 / $6.99 print-at-home line

Built 2026-08-28 by owner decision. 17 of our 18 books as print-at-home PDFs.

## Pricing architecture (owner-set)

| Tier | Books | Why |
|---|---|---|
| NO PDF (print-only lane) | The Middle Season | Our highest lane stays print-only to keep the sub-$5 space unsaturated and protect the flagship paperback |
| $4.99 attractors (5) | The 5-Minute Dump, The Dopamine Menu, Cozy Corners, The 75 Soft Journal, Settle | The biggest audience pools; low price pulls new buyers in |
| $6.99 (12) | Parallel Lives, The Night Pages, The Slow Page, First Strokes, Easy Garden, Mosaic Mind, Woodland Wonders, Fractal Dreams, Architectural Visions, Botanical Ink, Celestial Atlas, Tidal Ink | As many as possible at the higher tier |

Each product file = 1 license/title page + the complete validated interior (page counts
verified: interior + 1). Print editions stay $9.99 and separate. Interiors untouched.

## Where to list: every free PDF store, ranked LEAST to MOST popular

Traffic scale is approximate (public estimates, 2026). Price minimums: none of these
stores enforces any minimum price - our $4.99 / $6.99 clears every floor.

| Rank (least first) | Store | Fee when we sell | Price minimum | Our price | Notes |
|---|---|---|---|---|---|
| 1 | Lemon Squeezy | 5% + $0.50 | none | $4.99 / $6.99 | Merchant of record (handles global tax) |
| 2 | Whop | ~3% (sources vary) | none | - | Skipped for books: community marketplace, wrong buyers |
| 3 | Payhip | 5% + processor | none | $4.99 / $6.99 | Best free tier; also our Gumroad redundancy; primary direct store |
| 4 | Ko-fi Shop | 5% | none | $4.99 / $6.99 | Tips + shop in one place |
| 5 | Gumroad | 10% | none | $4.99 / $6.99 | Leads with bundles + samplers; best checkout/email capture |
| 6 | Etsy (digital) | $0.20/listing + 6.5% + ~3% + $0.25 | none | both tiers | FLAGGED for owner OK (~$3.60 one-time): journals-first, its #1 digital category is planners/trackers |
| 7 | Google Play Books | 30% (we keep 70%) | none | $4.99 / $6.99 | Accepts the PDF natively; biggest reach of all |

Multilingual listing copy (zh hi es fr ha yo) for these stores lives in MARKETS/i18n/.

## Bundles (raise average order value)

| Bundle | Contents | Bought singly | Bundle price | Buyer saves |
|---|---|---|---|---|
| The Starter Shelf | 5-Minute Dump + Dopamine Menu + 75 Soft Journal | $14.97 | $11.99 | $2.98 |
| Quiet Mind Color Complete | all 10 coloring PDFs | $69.90 | $39.99 | $29.91 |

## Free samplers (lead magnets, markets/digital/samplers/)

Two free 9-page PDFs - one per series - sample pages plus a price-labeled CTA page.
List at $0 on Gumroad/Payhip/Ko-fi/Google Play to capture emails and funnel buyers.

## Listing images (important)

Use cover.jpg + listing_02-05 + listing_07. NEVER listing_06_callout.jpg on digital
listings - it shows the $9.99 print price (noted in every metadata-digital.txt).

## Where the actual binary files live

All store binaries (17 digital PDFs, 36 B&N cover panels, 2 samplers) are pushed to
the repo branch **Market-Files** (root folders: digital/, bn-panels/, samplers/).
Materialize locally any time: make_bn_kits.py + make_digital_kits.py (+ samplers step).

## Files

- markets/digital/<book>/metadata-digital.txt - paste-ready listing text at the tier price
- No folder exists for The Middle Season. That is intentional.
