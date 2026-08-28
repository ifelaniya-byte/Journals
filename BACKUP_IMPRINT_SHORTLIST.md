# Backup imprint + Collection B decoupling shortlist

**Prepared:** August 28, 2026
**Purpose:** Give counsel a small, reversible fork to screen alongside **Stillwork Studio**.
**Status:** None of these are clear, registered, available, or approved. Limited general-web searching is not trademark clearance.

## Screening frame

The relevant commercial picture includes: **Class 16** printed journals, planners, books, cards, and stationery; **Class 35** online/wholesale retail; and **Class 41** optional non-downloadable audio/content. A formal search must include spelling, phonetic, foreign-equivalent, common-law, domain, social, marketplace, and related-goods variants. It must also screen **The Ritual Library** and the product/series names—not just an imprint label.

## Shortlist for counsel

| Candidate | Brand fit / collection fork | Limited-web screen observation | Class 16 / 35 / 41 counsel question | Preliminary status |
|---|---|---|---|---|
| **Calyven Studio** | Initially a clean, studio-led umbrella; Collection B could use **The Ritual Library — Quiet Practice** independently. | **New red flag:** `calyven.com` is an active Spanish building-renovation business, registered since 2024. The exact root is unavailable; earlier limited search was incomplete. | If useful, ask counsel for a documented no-go/qualification opinion on CALYVEN/CALVIN/CALY- phonetics; do not treat it as an available primary candidate. | **Red — do not register or deploy.** See `DOMAIN_DUE_DILIGENCE.md`. |
| **Linden Quiet Press** | More editorial/paper-led. Decouple B as **The Ritual Library — Quiet Practice** rather than sharing an imprint root. | Limited screen surfaced a UK **Linden Print Studio** and a separate registered **QUIET** software mark; neither is an exact U.S. paper-goods conclusion. | Assess LINDEN / QUIET marks, printing/publishing adjacency, U.S. common-law use, and whether combined mark offers sufficient distinction in classes 16/35/41. | Yellow — submit for full search. |
| **Norvale Paper Co.** | Wholesale/stationery-forward option. Decouple B as **Small Rituals** or a descriptive non-marked collection label until counsel approves a series name. | Limited exact-name screen did not surface a clear direct hit; nearby “Norway Press”/“Norvell” results mean phonetic and print-industry variants still need review. | Screen NORVALE/NORVELL/NORWAY and PAPER CO. variants, especially stationery/retail/publishing and web/domain use. | Yellow — submit for full search. |

## Explicitly *not* recommended as backups

- **Hearthfold Studio**: multiple consumer/physical-game and home-goods uses surfaced.
- **Morrow & Margin**: “MORROW” search results included a pending mark identifying paper notebooks/stickers, making it a poor low-friction contingency.
- **Fallowline Press**: nearby `Fallow Press LLC` and book/press results surfaced.

These observations simply narrow the counsel queue; they are not legal determinations.

## Collection B blast-radius controls

1. **Do not use the imprint root in the Collection B series unless counsel clears both.** The current `Stillwork Editions` root makes a negative imprint opinion a collection rename too.
2. **Preferred contingency:** retain the independently cleared parent brand **The Ritual Library** (if cleared) and use the descriptive KDP series **The Ritual Library — Quiet Practice**. This is less distinctive but limits a forced rename.
3. **Alternative:** use `Everyday Reflection` or `Small Rituals` internally/descriptively until a separately cleared series name is selected. Do not market a descriptive placeholder as a proprietary mark.
4. If counsel selects a backup imprint, change only `brand_config.json`, any cleared series configuration, domain/route configuration, and reviewed documents; then run `python build_catalog.py` **before** QR stamping. A rebuilt file set is still reversible. The first branded, QR-stamped physical proof is the practical switching-cost threshold.

## Name decision log fields

| Candidate | Counsel search requested | Clearance decision | Domain decision | Imprint / series implementation | Owner / date |
|---|---|---|---|---|---|
| Stillwork Studio | | | | | |
| Calyven Studio | Conflict-history only | Do-not-deploy / domain unavailable | — | — | See `D-2026-08-28-12` |
| Linden Quiet Press | | | | | |
| Norvale Paper Co. | | | | | |
