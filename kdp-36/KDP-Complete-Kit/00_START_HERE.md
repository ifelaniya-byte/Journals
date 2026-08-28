# KDP Complete Kit — 36 tracking journals

Vol 1 (01–18) + Vol 2 (19–36). Everything for all 36 titles, in one place.

**List price for every title: $9.99 US** (KDP 60% paperback royalty floor).

Read `SELLING_AND_VALUATION.md` for royalties, marketplaces, and the exact files to upload.
Read `PROOF_REPORT.md` for the verification that every listing is $9.99.

## Folder map

```
KDP-Complete-Kit/
  00_START_HERE.md          ← you are here
  SELLING_AND_VALUATION.md  ← prices, royalties, where to sell, upload files
  PROOF_REPORT.md           ← verification of files, trims, pages, $9.99
  METADATA.csv              ← titles, trims, spines, keywords, prices
  LOOKBOOK.pdf              ← all 36 covers + upload specs
  _covers/                  ← every wrap + front PDF
  _interiors/               ← every interior PDF
  01_…/ through 36_…/       ← per-title pack (interior + wrap + listing)
```

Each numbered folder contains:

| File | Upload where |
|---|---|
| `*_interior.pdf` | KDP interior |
| `*_COVER_WRAP.pdf` | KDP cover (full wrap with spine + barcode box) |
| `*_COVER_FRONT.pdf` | Mockups / ads only — do **not** upload as the cover |
| `listing.txt` | Title, subtitle, HTML description, 7 keywords, BISAC, spine math |

## Upload recipe (every title)

1. Paperback · **Bleed OFF** · Interior **black & white** · Paper **white**
2. Trim = the listing sheet (almost all **6 × 9**; **07 and 25 are 5 × 8**; **09 is 8.5 × 11**)
3. Interior PDF, then wrap cover PDF
4. Paste listing copy. Set **$9.99**. Order a proof.

## What was deliberately not invented

- No fake publisher name on the cover (put yours in KDP's author field)
- No live QR URLs — dashed QR boxes are on titles 03, 09, 17 so you can paste your own
- No Ozempic-as-brand in titles (GLP-1 is the stem)
- No exercise videos, dosing schedules, or treatment claims
- 4 × 6 pocket is not a KDP trim; 07 and 25 ship as **5 × 8**

## Spine math

White B&W: `spine_in = pages × 0.002252`  
Wrap width = `0.125 + trim_w + spine + trim_w + 0.125`  
Wrap height = `0.125 + trim_h + 0.125`  
Spine text only if **≥ 79 pages** (07 is 78 — no spine type)

Re-generate from source: `python3 /home/user/kdp-journals/assemble_kit.py`
