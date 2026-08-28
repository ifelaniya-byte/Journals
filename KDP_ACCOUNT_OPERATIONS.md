# KDP account, series, and imprint setup

This is a release-control guide, not a reason to publish the vault.

## 1. Establish one consistent identity before first upload

Complete and document these decisions before creating a Wave 1 title record:

- **Author / publisher display name:** ______________________________
- **Imprint name:** ______________________________
- **Copyright-page wording:** ______________________________
- **Customer-service email / business contact:** ______________________________
- **Brand-owned domain and long-term QR redirect owner:** ______________________________
- **Series names:** `Pace & Progress` and `Stillwork Editions` (or final cleared alternatives)

Use the same approved author/imprint spelling in every KDP metadata entry, copyright page, cover, A+ content, business account, and eventual deluxe packaging.

## 2. Series setup

The KDP assets use collection/series imagery; configure actual KDP series records only once the title and series names are cleared.

| Candidate KDP series | Wave 1 member | Do not add yet |
|---|---|---|
| Pace & Progress | A01 *Dose & Breathe*, A04 *Softer Words*, A05 *Night Harbor* | A02, A03, A06–A09 remain held/vault. |
| Stillwork Editions | B10 *Rest & Regulate*, B12 *Back to Enough*, B18 *Enough Money, Enough Calm* | B11, B13–B17 remain held/vault. |

**Sequence:**
1. Finalize cleared series names and description.
2. Create only the Wave 1 title records after content QA/claims approval.
3. Create or link the KDP series using the account’s current series workflow.
4. Verify title order, cover, description, and cross-link display after books are live.
5. Do not state “part of a series” in listing copy until the actual link has been checked.

## 3. A+ content readiness

Prepare a single restrained brand module, then adapt it only after the relevant KDP title is live and eligible under the account’s current tools/policies.

**Core module blocks**
- The Ritual Library: “quiet, tactile tools for real life.”
- The product’s exact paperback contents, shown through actual interior pages.
- One short “how to use it” panel.
- A collection card containing **only currently live** books.
- A plain-language self-reflection / non-treatment note when relevant.

Never use A+ content to add unsupported claims, show a future deluxe box as if included, or advertise a vault product as available.

## 4. Upload cadence and account limits

The policy decision is **six Wave 1 scouts**, not eighteen. To protect QA and account operations, prepare three cleared titles first, verify metadata/Previewer/proof workflow, then prepare the next three.

Do not rely on an internet claim of a “three-title-per-day” KDP limit. Amazon’s KDP help page currently describes a title-creation limit of **10 titles per book format each week** and advises contacting KDP for a higher-volume exception; account behavior and policy can change. Verify the current help/account notice before creating titles: <https://kdp.amazon.com/en_US/help/topic/G202145060>

This repository’s Wave 1 policy is more restrictive by choice. It exists to protect data quality, claims review, and proof handling—not to exploit a platform limit.

## 5. Before creating each KDP title

- [ ] SKU is marked Wave 1 and `Clear for upload` in `PORTFOLIO.md` / Scorecard Gate Log.
- [ ] Human content-QA form is signed in `WAVE1_HUMAN_QA.md`.
- [ ] `audit_metadata_claims.py` has been run and all reviewer flags resolved.
- [ ] Author/imprint and contact/domain placeholders are replaced in the exact final files.
- [ ] Current KDP Cover Calculator template has been compared with the final cover wrap.
- [ ] KDP Print Previewer is clean and an author proof is ordered.
- [ ] Listing uses product-specific actual interior images; no future/degraded-format imagery.
- [ ] Ad keyword set has a separate policy review for health/weight-loss-adjacent terms.

## 6. Before turning on ads

- [ ] Physical proof approved for cover scuffing, page trim, spine, print contrast, pen performance, and listing truthfulness.
- [ ] Brand/series implementation checked on the actual Amazon detail page.
- [ ] Correct campaign, UTM/linking, product status, and budget cap are entered in the validation Scorecard.
- [ ] Product-specific stop rule is recorded before spend begins.
