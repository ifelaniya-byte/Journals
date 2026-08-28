# Release policy — built is not published

**Status:** private prepublication control. All identity, claims, price, domain, QR/audio, and proof gates remain open.
**Applies to:** every KDP, Etsy, presale, creator, paid-media, and domain-facing asset in this repository.
**Portfolio register:** `PORTFOLIO.md` is the canonical product/status table; `DECISIONS.md` is the durable decision record.

The repository is an 18-concept option library, not an upload queue: **6 Wave 1 KDP scouts / 9 Wave 2 holds / 3 Vault products**. The generated files do not authorize publication.

## Non-negotiable rules

1. No public KDP upload unless the exact SKU is Wave 1 or has a signed open-slot decision, and every applicable gate is clear.
2. No paid campaign before required product-specific claims/naming review is clear. A01/Collection A paid Meta/TikTok activity remains off pending policy/account/creative review.
3. Generated price text is not authority. `DECISIONS.md` is the price source; `verify_pricing.py` must pass before any Wave 1 price-sensitive test or interpretation.
4. A paperback must never imply deluxe materials or components it does not contain.
5. A Q4-only pass is `Hold: Q4 retest`, not inventory approval. A failure despite Q4 tailwinds is a high-confidence retire review.
6. A Vault product has no public KDP path. Test the actual object/digital analogue, not a format-degraded bound substitute.
7. The founder’s named darling must have a signed pre-committed kill/hold criterion in `PORTFOLIO.md` before the relevant Gate 1 read.
8. Never create a parallel long-lived naming branch. Counsel-cleared identity changes occur once on `main` with rebuild, validation, proof checks, and an annotated tag.

## Wave assignments

### Wave 1 — only after individual clearance

| ID | Product | Required review before upload |
|---|---|---|
| A01 | *Dose & Breathe* | GLP-1/healthcare-marketing wording, product claims, and naming review. |
| A04 | *Softer Words* | General claims/naming review. |
| A05 | *Night Harbor* | Sleep-adjacent copy review; no treatment language. |
| B10 | *Rest & Regulate* | Breathwork/anxiety-adjacent review; no vagus/HRV/treatment claims; canonical price confirmation. |
| B12 | *Back to Enough* | Burnout/mental-health boundary review. |
| B18 | *Enough Money, Enough Calm* | Financial/mental-health boundary review. |

A maximum of two operational groups of up to three individually cleared titles may be used, separated by a 48-hour review interval. This is internal QA/proof/data-quality discipline—not a KDP entitlement or workaround. Group membership follows clearance, not collection count or schedule pressure.

### Wave 2 — conditional hold

A Wave 2 slot opens only when a Wave 1 SKU is retired, deliberately paused, or completes its specified test; it also needs a signed open-slot decision and a distinct customer-demand hypothesis.

| IDs | Product family | Additional conditions |
|---|---|---|
| A02, B15 | Creative/coloring | Distinct book/object hypothesis and no art-therapy claim. |
| A06 | Movement reflection | Movement/health review; no post-injection safety promise. |
| A07 | Optional observation journal | Clinical/claims boundary, non-device framing, and urgent-care language. |
| A08 | Premium planner | Both 25%+ price-visible conversion and 400+ leads; then choose book vs. deluxe format. |
| B11 | Weighted-blanket diary | Safety/claims review and a specific comfort-diary hypothesis. |
| B13 | Breathwork integration | Qualified facilitation, safety, and naming review. |
| B14 | Forest/photo reflection | Visual-retail or Etsy paid-demand signal; no therapeutic claim. |
| B16 | Couples reflection | Safety/resource framing and named buyer hypothesis. |

### Vault — no public KDP publication

| ID | Product | Correct validation instrument |
|---|---|---|
| A03 | *The Scent of a Steady Year* | **Non-KDP** 10 × 12 wire-bound wall calendar with reinforced hanger. Test digital calendar demand, then use a calendar printer; do not validate with a paperback. |
| A09 | *Pocket of Calm* | Collection-neutral 54-card deck + logbook; paid digital sample and price-visible waitlist/presale. |
| B17 | *One Minute at My Desk* | Freestanding easel + tear-pad; paid digital desk-practice sample, then physical-object demand. |

## Gate-to-release workflow

1. **Content QA:** cover-to-cover human review using `WAVE1_HUMAN_QA.md`.
2. **Claims/naming/price:** required counsel/reviewer sign-off and a passing `verify_pricing.py` for Wave 1.
3. **Identity and QR:** final cleared identity; buyer-controlled domain; for selected QR/audio titles, reviewed first-party page, visible transcript/no-audio fallback, privacy posture, and live redirect checks.
4. **Technical preflight:** current KDP Cover Calculator/Previewer; final metadata; proof order.
5. **Proof:** pass physical proof and, for QR books, warm indoor-light plus older-phone scan control.
6. **Gate 1:** use the Scorecard’s Oct. 31 Read 1 and Nov. 28 Read 2 logic. Neither interim result nor Q4-only performance authorizes deluxe funding.

## Account, domain, and external-repository controls

- Current KDP guidance must be checked in the actual account before title creation; use a conservative rolling seven-day creation ledger. The account limit never overrides the six-scout policy.
- `calyven.com` is already registered and used by an active third-party business, so it is **not** a defensively registrable root. A one-year registration for a future counsel-approved replacement root requires the owner’s registrar/payment authorization and is not approval to deploy or publicly use a mark. See `DOMAIN_DUE_DILIGENCE.md`.
- `ifelaniya-byte/Journals` is a separate public repository and not a remote of this catalog. It contains unrelated public branches and must not supply pricing, claims, release instructions, or automation behavior. Account-owner containment is documented in `GITHUB_PUBLIC_EXPOSURE_AUDIT.md`.
