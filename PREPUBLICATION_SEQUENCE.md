# Corrected Wave 1 sequence — no uploads authorized

**Current date:** August 28, 2026  
**Scope:** Six potential Wave 1 scouts only: A01, A04, A05, B10, B12, B18.  
**Current state:** Prepublication. A completed file, branded cover, ZIP, test landing page, or KDP draft does **not** authorize a public upload, publication, ad, or inventory order.

## The actual release constraint

This is a six-product research program, not an eighteen-product drip campaign. The repository intentionally retains 10 Wave 2 options and two KDP Vault products so they can move quickly **only** when a signed portfolio gate opens a slot. Do not allocate the Phase 1 budget across 18 live items.

A01 *Dose & Breathe* is the sole GLP-1-specific Wave 1 product. A04 and A05 are in the Pace & Progress collection but are not GLP-1 products. Do not describe a three-title collection batch as “three GLP-1 scouts.”

## Blocking work — complete before any KDP title record

1. **Identity:** The working imprint is **Stillwork Studio**, subject to trademark/name clearance. Finalize its legal use, KDP account spelling, copyright wording, customer-service contact, and KDP series naming. See `TRADEMARK_SCREENING.md`.
2. **Domain + QR/audio:** Register the exact domain under the business owner; deploy and test the first-party redirect and audio landing pages; record it in `brand_config.json`; stamp and proof-test only the six Wave 1 QR codes using `QR_AND_AUDIO.md`.
3. **Claims and ad-policy review:** Complete the scope-specific review for every Wave 1 title, its metadata, keywords, listing images, QR landing transcript, and any paid creative. A01 may not proceed without its GLP-1/healthcare-marketing clearance.
4. **Human QA:** Obtain the signed cover-to-cover editorial and usability forms in `WAVE1_HUMAN_QA.md`.
5. **Final build:** Run `python build_catalog.py`, then complete the real-domain QR stamp after deployment, then run `python validate_catalog.py` and `python audit_metadata_claims.py`. Structural success is not clearance.

## On individual clearance — the operational sequence

1. Compare every final Wave 1 wrap against the current KDP Cover Calculator/template at 30% opacity; record each result.
2. Create the actual KDP series page only after names are cleared. Set up listings for no more than three titles that individually meet every upload gate.
3. Use a 48-hour pause before a second group of up to three **only if** their individual gates also pass. The pause is a deliberate operational review interval, not a claimed Amazon entitlement or a workaround for a platform limit.
4. Choose group membership by clearance state, not by a calendar, collection count, or perceived speed. If A01’s review is incomplete, it stays out. A cleared Stillwork or general-reflection title may not inherit A01’s clearance.
5. On KDP approval, order proof/author copies. Do not activate ads on approval alone.
6. Approve every physical proof: trim/spine/margins, matte scuffing, navy/solid-ink coverage, gel-pen bleed, listing truthfulness, and **printed QR scan under warm indoor light using a current phone and an older phone**.
7. Enable only the title’s allocated ad test after proof approval and a recorded stop rule.

## Account limits and launch pace

KDP’s published help currently states a limit of 10 title creations per book format per week; it does not publish a reset time. Verify the current in-account/help notice at the time of use and keep a rolling seven-day title-creation ledger. That limit is not the release plan: the portfolio caps the campaign at six potential scouts.

Do not document claims about Amazon “velocity scoring” as a known rule unless a current, authoritative source or account notice supports them. The two-group pace here is justified by claims QA, KDP preflight, proof handling, and clean test data.

## Gate 1 timing and Q4 treatment

- Tag all sales and list data dated **November 1 or later** as Q4-influenced.
- Evaluate Gate 1 both across the valid full period and on the pre-November subset.
- A title that passes only with Q4 data is **Hold: Q4 Retest**, not an inventory green light.
- A failure despite Q4 tailwinds is a high-confidence kill/retire review.
- A September 15 live date reaches only 47 calendar days by October 31 (48 inclusive), not 60 clean pre-November days. Any full 60-day test begun in mid-September necessarily contains November/Q4 observations. Preserve the pre-November subset rather than claiming an impossible 60-day clean window.

## Gate 1: two reads, not a shortened 60-day verdict

**Read 1 — October 31 interim:** The Scorecard’s date-bounded fields make this a clean-season kill / iterate / continue meeting. A KDP trajectory passes when weekly organic units are non-decreasing from weeks 3–6 with week 6 above week 3, **or** the final 14 fully logged KDP days average at least two organic units per day. With adequate pre-cutoff ad volume, weak CTR/attention triggers a cover/concept retire review; strong CTR plus weak paid conversion triggers at most one 30-day listing/price iteration. Read 1 never authorizes deluxe funding, inventory, or a shortened substitute for the 60-day threshold.

**Read 2 — November 28 final:** Reconcile the existing full-period and pre-November Gate 1 calculations, plus the observed Oct 15–Nov 15 gifting-potential comparison. A measured period lift is not automatically causal; the Founder must mark the manual gift-thesis review `CONFIRMED` only with actual buyer language/qualitative evidence. A KDP adjusted advance requires the original full/pre-Nov computation, a Read 1 trajectory pass, and the documented Read 2 review. Q4-only results remain `Hold: Q4 Retest`.

The formulas, thresholds, and pre-created Gate Log rows live in `/home/user/ritual-library-launch-kit/gate-1-validation-scorecard.xlsx` and are documented in `SCORECARD_READ1_READ2_SPEC.md` beside the workbook.

## Paid social / creator boundary

Collection A paid creative and targeting remain an open policy-verification item in `LEGAL_AND_CLAIMS.md`. Do not target, imply, solicit, or profile a person’s medical condition or prescription use; do not use prescription-drug brand names, weight-loss outcomes, before/after imagery, body shaming, or restricted prescription-drug content. Until a reviewer verifies the platform and account-specific approach, use no paid Meta/TikTok campaign for A01. Collection-neutral creator seeding is not a substitute for platform policy review.
