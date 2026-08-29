# Quiet Mind Press — start here

SELLING: read PLATFORM_DECISIONS.md (what lists where) then PLATFORM_PLAYBOOK.md (how) — every sales platform, zero-upfront-fee verified 2026-08-28, exact file packages per site.

18 paperbacks on branch `ADHD-Journals`. Two Amazon series. Built 2026.

**Paste the AMAZON TITLE from each `metadata.txt`, not the short word on the cover.**

## Two series (create both on KDP)

| Series | Titles |
|---|---|
| Quiet Mind Journals | 5-Minute Dump, Parallel Lives, Night Pages, Settle, Middle Season, Dopamine Menu, Slow Page, 75 Soft |
| Quiet Mind Color | First Strokes → Easy Garden → Cozy Corners → Woodland → Mosaic → Botanical Ink → Tidal Ink → Celestial Atlas → Fractal Dreams → Architectural Visions |

## Format inventory (per title)

| File | Purpose |
|---|---|
| `*_interior.pdf` | KDP interior |
| `*_cover_wrap.pdf` | KDP cover (full wrap) |
| `*_cover.jpg` | listing image 1 |
| `listing_02`–`05_interior.jpg` | listing images 2–5 (interiors first for coloring) |
| `listing_06_callout.jpg` | trim / paper / difficulty / price |
| `listing_07_series.jpg` | series card (journals stack or color ladder) |
| `metadata.txt` | title, HTML description, 7 keywords, BISAC, price |
| `CATALOG.csv` / `LOOKBOOK.pdf` / `MARKETING.md` | catalog + ads plan |

## Upload settings

Paperback · B&W · **bleed OFF** · matte · expanded distribution OFF  
Paper: cream (journals) / white (coloring + Middle Season grids)

## Staging (account health)

1. **Ads launch (week 1):** Dopamine Menu, 75 Soft, Middle Season, Cozy Corners
2. Week 2: Dump, Night Pages, Settle
3. Week 3: remaining journals
4. Week 4+: color ladder in order, interiors on the listing before the cover

## Pricing

**Every KDP title is $9.99 US** (catalog-wide cap, 60% royalty floor). Other stores: `MARKETS/PLAYBOOK.md`. Do not put B&N prices on KDP.

## Rebuild

```
python build_nine_products.py
python build_batch4.py
python gen_catalog.py          # ALWAYS last
python make_zips.py all        # optional
```

Do not merge this branch with `Range-Band` (Range Band Press, the GLP-1 36).
