# Upload runbook — 54 SKUs to KDP paperback ($9.99)

Prepared 2026-08-31 · read-only · **no upload performed** · sources: frozen `ADHD-Journals` @ `3feca69` + `Range-Band` @ `8562469`

## Who does what

| Step | Who |
|---|---|
| Prepare fields/files | ✅ done (this package) |
| Create 6 series pages | human (KDP) |
| Upload each KDP product | **human** — logged-in Amazon/KDP account, browser + TOS; no agent path exists and policy blocks `kdp_upload` |
| Verify live listing, price, ED | human (then feed back data to agent) |
| Run ads | human; agent drafts only; no ads on RB-14 |

## Sequence (per SELL_HUB — do not skip, do not all-at-once for ads)

**Wave 1 (10, upload now):** QM dopamine, soft, middle, cozy → RB 01, 09, 05, 30, 10, 12.
**Wave 2+ cadence:** QM ≈5 titles/week after clean Wave-1 data; RB Wave 2 (7: 02,19,08,25,07,24,22) → Wave 3 (8) → Wave 4 (15).
**Channels order:** KDP paperback (all 54) → Wave 2 digital (QM 17 + RB 36) → QM hardcovers (7) + Blurb (6) → B&N (QM 11 thick; RB 36) → Lulu → Ingram (after ISBNs).
**Never:** ads-blast all 54; mix series; $14.99 on KDP; ED ON; digital-PDF Middle Season; list RB-14 with ads.

## Global KDP settings (every product)

| Setting | Value |
|---|---|
| Price | $9.99 |
| Bleed | OFF | Interior: black & white | Language: English |
| Expanded Distribution | OFF | Author: imprint name | ISBN: KDP free fine |
| Cover | **WRAP** PDF (never COVER_FRONT / merged) |
| QM title | paste AMAZON TITLE from metadata.txt | RB title | KDP title from listing.txt |
| Series | one of the 6 pages | |

## Series pages (create first)

- Quiet Mind Journals (8) · Quiet Mind Color (10) · GLP-1 Tracking (9) · Wellness Tracking (9) · GLP-1 Companion (9) · Wellness Companion (9)

## Per-title fields

Full paste-ready fields for all 54: `UPLOAD_ENTRY_SHEET_ALL54.md` (human-readable) and `UPLOAD_FIELDS_ALL54.csv` (machine).

## Per-product notes

- **RB interior filenames:** listing.txt/METADATA reference stale names; upload the actual `*_interior.pdf` listed in the sheet. Verified page counts match.
- **RB listing images:** none built (36). Conversion will be cover-only on Amazon. Recommend generating interior spread JPGs before ads on Wave 1 (offer available).
- **QM Middle Season:** print-only — do not upload a digital PDF.
- **QM B&N:** list 11 ≥120pp only; hold thin 7 (firststroke, garden, soft, cozy, botanical, celestial, tidal).
- **QM hardcovers:** 7 journals LIST; 10 coloring HOLD; Night none (5×8 trim).
- **Empty QR:** RB 03, 09, 17 — no URL invented. **Spine OFF:** RB 07.
- **RB-14:** KDP listing allowed but ADS HOLD (vs Middle Season).
- **Proof before ads (RB):** 01 (6×9), 07 (5×8), 09 (8.5×11).

## Human gate checklist
- [ ] Create 6 series pages
- [ ] Upload Wave 1 (10) in order $9.99 / bleed OFF / ED OFF / WRAP
- [ ] Confirm live listings + prices
- [ ] Wave 2+ per cadence; ads only Wave 1 until ~10 reviews
- [ ] Never mix imprints or series; never $14.99 on KDP
