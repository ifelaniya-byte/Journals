# The Ritual Library — start here

This is a Git-ready 18-SKU KDP scout catalog with two companion deluxe-hero packages. It is deliberately organized like a production repository: every paperback has interior, wrap, seven listing images, metadata, upload settings, rebuild code, and automated structural QC.

## First actions
1. Read `LEGAL_AND_CLAIMS.md` before changing or publishing health-adjacent metadata.
2. Open `CATALOG.csv` to see every KDP listing title, price, format, and file path.
3. Read `RELEASE_POLICY.md` and `PORTFOLIO.md`. For each **Wave 1** scout only, open its `release/[ID]-[slug]/metadata.txt`; copy the **AMAZON TITLE**, not merely the cover word.
4. Use `UPLOAD_CHECKLIST.md` and KDP Print Previewer. Order a proof before enabling ads.
5. Run `python validate_catalog.py` after any rebuild. A green validation result is structural QC, not legal/clinical clearance.

## Two collections
| Collection | IDs | Customer promise |
|---|---|---|
| Pace & Progress | A01–A08 | Gentle, private support for routines, reflection, and care journeys. |
| Stillwork Editions | A09, B10–B18 | Small tactile rituals for hard days, desks, relationships, rest, and outdoors. |

## Files in every KDP product folder
| File | Purpose |
|---|---|
| `interior.pdf` | KDP paperback interior |
| `cover_wrap.pdf` | Full paperback wrap, sized from page count / white-paper spine formula |
| `cover.jpg` | Listing image 1 / front-cover asset |
| `listing_02`–`05_interior.jpg` | Interior-preview images |
| `listing_06_callout.jpg` | Trim / page / paper / scout-price card |
| `listing_07_series.jpg` | Collection card |
| `metadata.txt` | Upload title, listing description, seven keywords, categories, price, claims boundary |

## Rebuild / package / QC
```bash
pip install -r requirements.txt
python build_catalog.py        # regenerates the full release package
python validate_catalog.py     # structural QC; exits non-zero on a failure
python make_zips.py            # creates only the six Wave 1 candidate bundles
python make_zips.py --all-vault # explicit internal archive only; never an upload plan
# Only after a real domain and deployment: python configure_wave1_qr.py --domain <domain> --apply --verify-live
```

Do not release a product simply because it validates or has a ZIP file. Follow `RELEASE_POLICY.md`; only six Wave 1 SKUs are potential September uploads. Stillwork Studio is the working imprint candidate, subject to clearance. Clear names/claims, complete the QR/audio gate where applicable, validate the final KDP template, and approve proof copies.
