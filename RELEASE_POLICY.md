# Release policy — built is not published

**Status:** `v1.0-prepublication`  
**Applies to:** every KDP, Etsy, presale, creator, and paid-media asset in this repository.

The repository contains a pre-built option library. It does **not** authorize an 18-title release. The validation plan remains a focused six-scout experiment: publish six only after their reviewed customer-facing copy is cleared, then let evidence—not the existence of assets—open the next slot.

## Non-negotiable rules

1. **No public KDP upload unless a SKU is in Wave 1 or explicitly advanced in a signed Portfolio decision.**
2. **No paid campaign before the required claims/naming review for that specific SKU is clear.**
3. A KDP paperback tests its own paperback promise; it must never imply the materials or components of a deluxe product.
4. A product that only passes during Q4 is marked **Hold: Q4 Retest**, not “ready for inventory.”
5. A vault asset is a speed advantage, not a launch obligation.
6. The founder’s named “darling” is subject to the same pre-committed kill rule as every other product. The founder must record and sign that criterion in `PORTFOLIO.md` by September 6, 2026.

---

# Wave assignments

## Wave 1 — publish only after clearance

**Target window:** September 2026  
**Trigger:** required legal/claims/name review is marked **Clear**, author/imprint and final upload metadata are inserted, KDP Previewer passes, and an author proof is ordered. Ads start only after physical proof approval.

| ID | Product | Why it is in Wave 1 | Required review before upload |
|---|---|---|---|
| A01 | *Dose & Breathe* | Focused GLP-1 scout with the clearest ritual/weekly use case. | GLP-1/healthcare-marketing wording + trademark/name review. |
| A04 | *Softer Words* | Broad daily-reflection/gifting scout; lower regulatory burden. | General claims/name review. |
| A05 | *Night Harbor* | Bedside ritual offers a clear use case, but must stay out of sleep-treatment language. | Sleep-adjacent copy review. |
| B10 | *Rest & Regulate* | Strongest non-GLP-1 calming-routine scout. | Breathwork/anxiety-adjacent copy review; no vagus/HRV claims. |
| B12 | *Back to Enough* | Clear low-capacity productivity problem and broad audience. | Burnout/mental-health claims review. |
| B18 | *Enough Money, Enough Calm* | Distinct emotional-finance reflection scout. | Financial/mental-health boundary review. |

**Wave 1 spend policy:** The Phase 1 media budget is allocated across these six only. Publishing six is not permission to advertise all six equally; the Scorecard controls which 3–4 receive sustained spend.

## Wave 2 — conditional hold

**Trigger:** a Day 90 Gate 1 decision, an approved 30-day iteration hypothesis, and any required review. A Wave 2 slot opens only when a Wave 1 SKU is retired, deliberately paused, or has completed its specified test.

| ID | Product | Current status | Opening condition |
|---|---|---|---|
| A02 | *Color Your Way Forward* | Pre-built KDP option; no active test. | Opens only if an adjacent creative/wellness hypothesis needs a book-form test. |
| A03 | *The Scent of a Steady Year* | Etsy/digital-first / physical calendar concept. | Do not use paperback as primary concept test; evaluate undated digital calendar demand first. |
| A06 | *Stillness & Stretch* | Review-heavy movement product. | Legal/movement review clear and an active Wave 1 slot opens. |
| A07 | *Steady Signal* | Review-heavy pulse/observation product. | Clinical/claims wording clear and an active Wave 1 slot opens. |
| A08 | *The Unhurried Year* | Waitlist-first planner concept. | 25%+ price-visible conversion **and** 400+ email leads; then decide book vs. deluxe format. |
| B11 | *Under the Covers* | Review-heavy weighted-blanket concept. | Product/claims safety review clear and a verified demand hypothesis exists. |
| B13 | *The Breathwork Integration Book* | Facilitation/safety-sensitive concept. | Naming and safety review clear; no restricted method name. |
| B14 | *Among the Trees* | Future boutique / photo-journal option. | A visual-retail or Etsy demand signal opens a slot. |
| B15 | *Color & Check In* | Future creative-practice option. | Distinct mood/coloring hypothesis and claims boundary reviewed. |
| B16 | *Us, In Balance* | Relationship-sensitive concept. | Safety/resource review clear and a specific audience hypothesis opens a slot. |

## Vault — no KDP publication

| ID | Product | Correct validation instrument | Policy |
|---|---|---|---|
| A09 | *Pocket of Calm* | Paid digital card sample + price-visible waitlist / January–February 2027 presale | **Collection-neutral flagship.** The KDP companion is retained as a private content/proof asset, not an active scout. Physical cards and boxed format are the product being validated. |
| B17 | *One Minute at My Desk* | Paid digital desk-practice sample; later physical easel/pad demand test | The paperback adaptation is format-degraded. Retain it as a reference, but do not treat its sales/failure as proof of the easel object. |

---

# Format-degradation rule

A paperback is a valid scout only when it preserves the customer’s core job-to-be-done. A card deck, hanging calendar, and desk easel are not automatically validated by a bound book substitute.

- **Pocket of Calm:** test card choice, gift intent, deck + logbook experience, and boxed-object price—not a paperback.
- **The Scent of a Steady Year:** test undated planning and sensory-cue content digitally before considering physical calendar production.
- **One Minute at My Desk:** test the quick desk-reset ritual through a paid digital sample before physical-object production.

A “fail” on a format-degraded version is **directional feedback**, not an automatic concept kill.

---

# Gate-to-release workflow

1. **Content QA:** Wave 1 title receives a cover-to-cover human read-through using `WAVE1_HUMAN_QA.md`.
2. **Claims/name audit:** Run `audit_metadata_claims.py` and conduct the appropriate legal/claims review.
3. **KDP identity setup:** Finalize author/imprint and create collection/series pages before first listings go live. Do not imply a KDP Series link exists until it does.
4. **Technical preflight:** Replace placeholders, run `validate_catalog.py`, use KDP’s current Cover Calculator/Previewer, and order a proof.
5. **Proof decision:** Approve/revise physical proof. Only then enable the specific title’s ad test.
6. **Gate 1:** Use the Scorecard’s full-period + Q4-adjusted decision, not instinct or number of files built.

# Repository status labels

- **Built:** content/assets exist; no publication permission.
- **QA complete:** automated structural QC passes; still no publication permission.
- **Clear for upload:** content QA, required claims/name review, final metadata, and KDP Previewer conditions are met.
- **Proof approved:** physical proof has passed; eligible for assigned ad test.
- **Active test:** receiving its approved budget/measurement plan.
- **Hold / Vault / Retired:** no public or paid action except documented exception.
