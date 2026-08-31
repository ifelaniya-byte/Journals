# The Ritual Library — start here

This is a Git-ready 18-concept product catalog with 15 conditional KDP book options, two private book-form references, and one non-KDP calendar with two companion deluxe-hero packages. It is deliberately organized like a production repository: every paperback has interior, wrap, seven listing images, metadata, upload settings, rebuild code, and automated structural QC.

## First actions
1. Read `LEGAL_AND_CLAIMS.md` before changing or publishing health-adjacent metadata.
2. Open `CATALOG.csv` to see every product’s format/status and only the conditional KDP listing rows.
3. Read `RELEASE_POLICY.md` and `PORTFOLIO.md`. For each **Wave 1** scout only, open its `release/[ID]-[slug]/metadata.txt`; copy the **AMAZON TITLE**, not merely the cover word.
4. Use `UPLOAD_CHECKLIST.md` and KDP Print Previewer. Order a proof before enabling ads.
5. Read `SALE_READINESS_COMPLETION_MATRIX.md` for each SKU's structural state and outstanding human gates. It records 0 `Clear for upload` products and is not release authorization.
6. For the six Wave 1 candidates, use `WAVE1_COUNSEL_AND_FINALIZATION_PACKET.md` to obtain product-specific human/counsel decisions; it creates no clearance itself.
7. Read `EXPANSION_36_RESEARCH_AND_STAGE_GATE.md` before choosing any expansion candidate. The 36 concepts remain outside the governed portfolio and are not a production queue.
8. Read `TRANSLATION_HANDOFF_PACKAGE.md` and its source manifest before any localization. It locks English sources; it does not create translations or bilingual editions.
9. Read `MULTILINGUAL_MULTICHANNEL_MODEL.md` before creating any edition, store price, translation, or distribution plan. Its `MULTICHANNEL_PRICING_MODEL.csv` is planning-only; it is not a price or publishing authorization.
10. Run `python validate_catalog.py` after any rebuild. A green validation result is structural QC, not legal/clinical clearance.
11. For the two-read Oct 31 / Nov 28 Gate 1 calculations, use `/home/user/ritual-library-launch-kit/gate-1-validation-scorecard.xlsx` and its adjacent `SCORECARD_READ1_READ2_SPEC.md`.

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
python verify_canonical.py   # PORTFOLIO.md decision baseline vs source/artifacts
python verify_pricing.py     # Wave 1 price source/artifact agreement
python build_multichannel_pricing.py  # writes planning-only channel/edition grid
python verify_multichannel_pricing.py # confirms it retains canonical Wave 1 anchors
python build_translation_manifest.py  # locks current English sources for future qualified handoff
python verify_translation_manifest.py # confirms source digests and non-live language state
python validate_catalog.py     # structural QC + canonical/price-model/source-lock guards; exits non-zero on a failure
python make_zips.py            # creates only the six Wave 1 candidate bundles
python make_zips.py --all-vault # explicit internal archive only; never an upload plan
# Only after a real domain and deployment: python configure_wave1_qr.py --domain <domain> --apply --verify-live
```

Do not release a product simply because it validates or has a ZIP file. Follow `RELEASE_POLICY.md`; only six Wave 1 SKUs are potential September uploads. Stillwork Studio is the working imprint candidate, subject to clearance. Clear names/claims, complete the QR/audio gate where applicable, validate the final KDP template, and approve proof copies.
