# Portfolio — canonical product and release register

**Status:** private prepublication system. `Built` never means approved for KDP, ads, a public website, or inventory.
**Decision owner:** Founder / brand lead.
**Live record for commercial decisions:** `DECISIONS.md`; per-test evidence and Gate 1 meetings: `ritual-library-launch-kit/gate-1-validation-scorecard.xlsx` → Gate Log.
**Source hierarchy:** this register governs product status and commercial posture; `CATALOG.csv` is the generated technical manifest; `metadata.txt` is a generated upload artifact, never independent authority for a price or release decision.

## Portfolio snapshot

| Classification | Count | IDs | Rule |
|---|---:|---|---|
| Wave 1 KDP scouts | 6 | A01, A04, A05, B10, B12, B18 | Each needs its own gates clear; a three-title operational group is a maximum, never a quota. |
| Wave 2 conditional options | 9 | A02, A06–A08, B11, B13–B16 | Requires an open slot, documented hypothesis, and applicable review. |
| Vault — not a KDP product / no public KDP | 3 | A03, A09, B17 | Test the actual object or digital analogue; a paperback surrogate does not validate it. |
| Total product concepts | **18** | A01–A09, B10–B18 | The catalog is an option library, not an 18-SKU launch plan. |

## Identity architecture — counsel candidates only

| Layer | Current candidate | Decision state | Decision record |
|---|---|---|---|
| Imprint / operating umbrella | **Calyven Studio** | **Do-not-deploy / counsel-comparison only.** Active exact-root domain/business surfaced after the initial screen; neither cleared nor registrable as the desired root `.com`. | `D-2026-08-28-07`, `D-2026-08-28-12` |
| Editorial customer-facing line | **The Ritual Library** | Counsel search required at the same depth as the imprint. | `D-2026-08-28-07` |
| Collection A | **Pace & Progress** | Candidate collection/series name; search with the package. | `D-2026-08-28-07` |
| Collection B | **Quiet Practice** | Proposed decoupled collection/series name; not cleared or deployed. | `D-2026-08-28-07` |
| Earlier working candidate | Stillwork Studio / Stillwork Editions | Retained only for counsel comparison and legacy private files; no assumption of clearance. | `D-2026-08-28-02`, `D-2026-08-28-07` |

There is **no long-lived branding Git branch**. A name approved by counsel is changed on `main`, rebuilt, validated, and tagged in one controlled change. A physical proof bearing a QR that resolves through a branded buyer-controlled domain is the name/domain switching-cost point. `Calyven Studio` is not currently that approved name; see `DOMAIN_DUE_DILIGENCE.md`.

## Pricing control

The generated repository entered its first tracked commit with unapproved lower price defaults hard-coded in `build_catalog.py`. Those defaults are not a commercial pricing decision. The user-reconfirmed Wave 1 price decisions are recorded in `DECISIONS.md` and enforced by `verify_pricing.py`.

| Wave 1 SKU | Authorized paperback scout price | Current price-control state |
|---|---:|---|
| A01 — *Dose & Breathe* | $16.99 | Confirmed; generated files still require governed rebuild. |
| A04 — *Softer Words* | $17.99 | Confirmed; generated files still require governed rebuild. |
| A05 — *Night Harbor* | $15.99 | Confirmed; generated files still require governed rebuild. |
| B10 — *Rest & Regulate* | $17.99 | Confirmed; generated files require governed rebuild. |
| B12 — *Back to Enough* | $18.99 | Confirmed; generated files still require governed rebuild. |
| B18 — *Enough Money, Enough Calm* | $18.99 | Confirmed; generated files still require governed rebuild. |

No other displayed historical KDP price in a generated artifact is an authorized future price. Wave 2 book prices are set only when that product has an approved open-slot hypothesis. Premium-object and waitlist prices below are product tests, not paperback defaults.

## The darling clause — complete before any Gate 1 read

**Founder’s personal-favorite concept:** ______________________________
**Pre-committed kill / hold criterion:** ________________________________________________

> I will apply this product’s documented Gate 1 rule exactly as I would to every other SKU. If it does not produce its stated valid signal and does not qualify for the one documented strong-attention/weak-conversion iteration, I will hold or retire it without new inventory funding.

Founder signature: ______________________________  Date: __________________

## Gate legend

| Gate | What “clear” means |
|---|---|
| Content QA | Human cover-to-cover tone, prompt, claims, layout, and expectation review complete. |
| Legal / claims / naming | Product-specific copy and the required name search/review are marked clear; no SKU inherits another SKU’s clearance. |
| Identity / QR | Where selected, the final buyer-controlled domain, first-party route, reviewed audio and visible transcript are live; no tracker/health-data/fingerprinting conflict remains. |
| KDP technical | Current Cover Calculator and Previewer pass, final cleared identity is inserted, and proof is ordered. |
| Proof | Physical proof passes trim, pen, cover, listing-truthfulness, and (where selected) warm-indoor-light/older-phone QR scan controls. |
| Gate 1 | Valid sales/waitlist/Etsy evidence is recorded in the Scorecard. October 31 is an interim clean-season read; November 28 is the Q4-flagged full decision. |

**Status terms:** `Built` = private assets/specifications exist; `Hard hold` = no upload, public page, paid media, or inventory; `Vault` = no public KDP path; `Retired` = learning retained but no new spend without a new business case.

## Full inventory

| ID | Product | Collection / intended branch | Niche / customer job | Intended format or actual test object | Price / test posture | Classification & current gate status | Validation / next decision | Pre-committed kill or hold rule | Decision ref |
|---|---|---|---|---|---|---|---|---|---|
| A01 | *Dose & Breathe* | Pace & Progress | GLP-1-adjacent weekly reflection; space for care-team questions without medical guidance. | 6 × 8 in. paperback scout; premium hardcase is separate. | **$16.99** KDP scout | Wave 1 — Built / hard hold; all pre-upload gates open. | KDP + price-visible waitlist; Oct. 31 Read 1, Nov. 28 Read 2 when valid. | Hold/retire if no valid Gate 1 signal; one documented listing/price iteration only on strong attention + weak conversion. | `D-2026-08-28-08` |
| A02 | *Color Your Way Forward* | Pace & Progress | Mindful coloring plus low-pressure routine reflection. | Wire-bound coloring object; book-form test only if an open slot proves appropriate. | No authorized KDP price. | Wave 2 — Built / hard hold. | Specific creative/wellness demand hypothesis. | No spend or upload without signed open-slot decision and claims review. | `D-2026-08-28-04` |
| A03 | *The Scent of a Steady Year* | Pace & Progress | Year-at-a-glance planning and sensory-cue ritual. | **10 × 12 in. wire-bound wall calendar with reinforced hanger; calendar printer.** | $26 standard / $29 reviewed sensory-sticker edition; no KDP price. | **Vault — not a KDP product.** | Digital calendar demand, then physical-calendar production review. | A paperback surrogate is not a concept verdict; hold physical inventory if digital demand is absent. | `D-2026-08-28-09` |
| A04 | *Softer Words* | Pace & Progress | Broad gratitude/self-talk diary for ordinary hard days and gifting. | 6 × 8 in. paperback scout; premium hardcase separate. | **$17.99** KDP scout | Wave 1 — Built / hard hold. | KDP evidence under two-read Gate 1. | Hold/retire if no signal; one controlled iteration only for strong attention + weak conversion. | `D-2026-08-28-08` |
| A05 | *Night Harbor* | Pace & Progress | Bedside wind-down reflection without sleep-treatment claims. | 6 × 8 in. paperback scout; premium bedside object separate. | **$15.99** KDP scout | Wave 1 — Built / hard hold. | KDP evidence under two-read Gate 1. | Hold/retire if no signal; never intensify sleep or medical claims to rescue sales. | `D-2026-08-28-08` |
| A06 | *Stillness & Stretch* | Pace & Progress | Gentle movement and body-scan reflection. | Wire-bound movement object; paperback only after review. | No authorized KDP price. | Wave 2 — Built / hard hold. | Named movement-reflection hypothesis. | No “post-injection safe” or medical movement promise; no release before review/open slot. | `D-2026-08-28-04` |
| A07 | *Steady Signal* | Pace & Progress | Optional observation/pulse notes without device or diagnosis positioning. | Premium journal; book form only after clinical/claims review. | No authorized KDP price. | Wave 2 — Built / hard hold. | Non-device observation demand hypothesis. | Hold unless pulse/device wording and urgent-care boundary are reviewed. | `D-2026-08-28-04` |
| A08 | *The Unhurried Year* | Pace & Progress | Capacity-respecting executive planning / premium planner. | Premium undated planner. | $28–30 price-visible waitlist; no authorized KDP price. | Wave 2 — Built / hard hold. | Both 25%+ qualified conversion and 400+ leads. | Hold if either requirement fails; do not make dated inventory. | `D-2026-08-28-04` |
| A09 | *Pocket of Calm* | Collection-neutral core | 54-prompt deck and gift object for moments a blank page is too much. | 54-card boxed deck + companion logbook. | $30 object hypothesis. | Vault — no public KDP; collection-neutral. | Paid digital card sample + waitlist/presale; no earlier public presale than Jan.–Feb. 2027 and Gates 2–3. | One card/gift-proposition revision after failed digital test, then retire deck; a KDP companion is not a product verdict. | `D-2026-08-28-01` |
| B10 | *Rest & Regulate* | Quiet Practice (proposed) | Optional grounding/breath-paced reflection without physiological outcome claims. | 6 × 8 in. paperback scout; premium journal separate. | **$17.99** KDP scout | Wave 1 — Built / hard hold; all pre-upload gates open. | KDP evidence under two-read Gate 1 after all gates are clear. | Hold/retire if no signal; no vagus, HRV, nervous-system, or treatment language to force fit. | `D-2026-08-28-08` |
| B11 | *Under the Covers* | Quiet Practice (proposed) | Weighted-blanket comfort/sleep diary for existing users. | Specialty diary; book form only after safety review. | No authorized KDP price. | Wave 2 — Built / hard hold. | Specific comfort-diary demand hypothesis. | No blanket-weight recommendation/treatment claim; book-form failure is not the physical object’s final verdict. | `D-2026-08-28-04` |
| B12 | *Back to Enough* | Quiet Practice (proposed) | Low-capacity task triage and compassionate productivity reflection. | 6 × 8 in. paperback scout; wire-bound workbook separate. | **$18.99** KDP scout | Wave 1 — Built / hard hold. | KDP evidence under two-read Gate 1. | Hold/retire if no signal; only one controlled listing/price iteration on strong attention + weak conversion. | `D-2026-08-28-08` |
| B13 | *The Breathwork Integration Book* | Quiet Practice (proposed) | Session reflection/integration, not intense-breathwork instruction. | A4 specialty book; possible book form only after qualified review. | No authorized KDP price. | Wave 2 — Built / hard hold. | Practitioner/creator demand test with safety/naming review. | Remain held without qualified review and a clear naming path. | `D-2026-08-28-04` |
| B14 | *Among the Trees* | Quiet Practice (proposed) | Forest-bathing/photo-reflection keepsake and visual gift. | 8 × 8 in. boutique photo journal. | No authorized KDP price. | Wave 2 — Built / hard hold. | Etsy / visual-retail paid demand signal. | No paid test before an open slot; no therapeutic forest-bathing outcome claim. | `D-2026-08-28-04` |
| B15 | *Color & Check In* | Quiet Practice (proposed) | Mandala coloring plus mood reflection; not art therapy. | Twin-wire specialty coloring object. | No authorized KDP price. | Wave 2 — Built / hard hold. | Distinct coloring/mood demand hypothesis. | Hold unless the art/value proposition differentiates in test images and claims are reviewed. | `D-2026-08-28-04` |
| B16 | *Us, In Balance* | Quiet Practice (proposed) | Consent-aware couples’ check-ins and repair reflection. | Hardcase workbook + reset cards. | No authorized KDP price. | Wave 2 — Built / hard hold. | Relationship-audience demand test with safety review. | No couples-therapy claim; hold without resource/safety framing approval. | `D-2026-08-28-04` |
| B17 | *One Minute at My Desk* | Quiet Practice (proposed) | Visible 30–90-second desk resets / corporate-gift object. | Freestanding easel + refillable tear-pad. | $24 object hypothesis. | Vault — no public KDP. | Paid digital desk-practice test, then physical-object demand. | Book-form result is directional only; do not kill the easel object because a paperback surrogate fails. | `D-2026-08-28-04` |
| B18 | *Enough Money, Enough Calm* | Quiet Practice (proposed) | Emotional-finance reflection: facts, feelings, one next step; no advice. | 6 × 8 in. paperback scout; gift hardcase separate. | **$18.99** KDP scout | Wave 1 — Built / hard hold. | KDP evidence under two-read Gate 1. | Hold/retire if no signal; never add financial, legal, tax, investment, or mental-health outcomes to rescue conversion. | `D-2026-08-28-08` |

## Signed decision controls

1. Before any status change, record date, evidence, decision owner, next action, budget, and condition in the Scorecard Gate Log.
2. Record durable portfolio, identity, price, QR/domain, and public-exposure decisions in `DECISIONS.md`.
3. A Wave 1 SKU can become `Clear for upload` only after every product-specific gate is clear, including live QR/audio and physical proof where selected.
4. A Wave 2 SKU needs both a signed open-slot decision and a testable, differentiated hypothesis. It is never activated because its files already exist.
5. Vault products are never uploaded to KDP. Their designated actual-object/digital validation vehicle is the only relevant early proof.
6. A Q4-only result remains `Hold: Q4 retest`; the Oct. 31 interim cannot authorize deluxe funding; a Nov. 28 advance remains subject to the two-read policy and Gates 2–3.
