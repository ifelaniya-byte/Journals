# Translation handoff package — six future bilingual pairs
## Controlled source, qualified human translation, independent proofreading, and per-edition release gates

**Status:** preparation only; no translation text, bilingual cover, EPUB, PDF, ISBN, store listing, or release approval is created by this package.
**Source of truth:** `PORTFOLIO.md` → canonical product table; `TRANSLATION_SOURCE_MANIFEST.csv` → exact English source paths and SHA-256 digests.
**Target pairs:** English + Spanish, French, Hindi, Simplified Chinese, Hausa, or Yorùbá.
**Scope:** all 18 product concepts are accounted for below. Work priority is not release approval.

## 1. Non-negotiable framing

A bilingual edition is a new product edition. It is **not** a translated storefront listing, a machine-translated PDF, or a cover change. Each approved future pair needs:

1. a qualified literary/editorial translator for the target language;
2. a different, qualified in-market proofreader;
3. product-specific claims/title/keyword review, including the translated title/subtitle;
4. a re-typeset interior built from the approved target text—not a reused English PDF;
5. final page-count, trim, cover/wrap, accessibility, identifier, printer/platform, and proof checks; and
6. a named human decision before a listing, price, social post, upload, spend, domain/QR change, or release.

No AI draft, passing spell-check, language model, or source-file hash can replace any of those approvals. Do not send customer/health/prescription/financial data or credentials to translators or an AI tool.

## 2. Source-lock and translation status

`verify_translation_manifest.py` validates the manifest against the canonical table and the current file digest. If the English source changes after a translator has started, stop work, issue a new dated source manifest, identify the changed passages, and obtain a documented translator/proofreader revision before layout resumes.

| SKU | English source / intended product | Current wave | Required translation source | Current translation state | Earliest handoff condition |
|---|---|---|---|---|---|
| A01 | *Dose & Breathe* — GLP-1 companion paperback | Wave 1 | English interior PDF | Not started | Individual English name/GLP-1/claims gates clear; then translation brief approved. |
| A02 | *Color Your Way Forward* — GLP-1 coloring workbook | Wave 2 | English interior PDF | Not started | Signed open slot, GLP-1 language review, and differentiated creative hypothesis. |
| A03 | *The Scent of a Steady Year* — 10 × 12 wire calendar | Vault / non-KDP | Calendar product brief, not a paperback | Not started | Actual calendar format/printer and dated-inventory decision approved. |
| A04 | *Softer Words* — self-talk diary | Wave 1 | English interior PDF | Not started | Individual English name/general claims gates clear. |
| A05 | *Night Harbor* — sleep reflection companion | Wave 1 | English interior PDF | Not started | Individual English sleep-adjacent review and proof gates clear. |
| A06 | *Stillness & Stretch* — movement reflection companion | Wave 2 | English interior PDF | Not started | Signed open slot and movement/health review; no post-injection safety language. |
| A07 | *Steady Signal* — optional pulse observation journal | Wave 2 | English interior PDF | Not started | Signed open slot and clinical/claims review. |
| A08 | *The Unhurried Year* — executive wellness planner | Wave 2 | English interior PDF | Not started | $28–30 waitlist threshold and open-slot decision. |
| A09 | *Pocket of Calm* — neutral boxed-deck concept | Vault / non-KDP | English companion/reference source only | Not started | Paid digital card sample + boxed-deck/waitlist decision; no automatic paperback translation. |
| B10 | *Rest & Regulate* — breath-paced planner | Wave 1 | English interior PDF | Not started | Individual breathwork/physiological-claims review and proof gates clear. |
| B11 | *Under the Covers* — weighted-blanket diary | Wave 2 | English interior PDF | Not started | Signed open slot, sleep/blanket review, and final safety-note decision. |
| B12 | *Back to Enough* — productivity reflection workbook | Wave 1 | English interior PDF | Not started | Individual burnout/mental-health boundary review and proof gates clear. |
| B13 | *The Breathwork Integration Book* — session log | Wave 2 | English interior PDF | Not started | Signed open slot, facilitation/naming/safety review. |
| B14 | *Among the Trees* — forest reflection journal | Wave 2 | English interior PDF | Not started | Paid visual/gift demand signal, claims review, and open slot. |
| B15 | *Color & Check In* — mandala mood diary | Wave 2 | English interior PDF | Not started | Distinct creative hypothesis and no-art-therapy claims review. |
| B16 | *Us, In Balance* — couples workbook | Wave 2 | English interior PDF | Not started | Safety/resource review, relationship-audience evidence, and open slot. |
| B17 | *One Minute at My Desk* — desk-reset easel/pad concept | Vault / non-KDP | English companion/reference source only | Not started | Paid digital desk-practice test and physical-object decision; no automatic KDP translation. |
| B18 | *Enough Money, Enough Calm* — financial-anxiety workbook | Wave 1 | English interior PDF | Not started | Individual finance/mental-health boundary review and proof gates clear. |

## 3. Work order and capacity control

The requested six language pairs represent **up to 108 future product editions** (18 concepts × 6 pairs), not one 108-language book. That is a planning ceiling, not a batch authorization.

1. **Queue 0 — no translation work now:** all 18 while name/claims/format gates remain unresolved.
2. **Queue 1 — only after individual English clearance:** the six Wave 1 candidates. Commission a single product-language pilot first; do not release all six languages at once.
3. **Queue 2 — only after an open-slot decision:** Wave 2 titles receive no translation work merely because English files exist.
4. **Queue 3 — actual object first:** A03, A09, and B17 require a calendar/deck/easel-specific localization brief rather than a book-PDF translation shortcut.

Do not let a translation supplier, an existing English file, a price-planning row, or a calendar deadline create a de facto release decision.

## 4. Language-pair requirements

| Pair | Language code | Required linguistic/layout specialty | Required final reviewer |
|---|---|---|---|
| English + Spanish | `en` + `es` | Editorial Spanish appropriate to selected market/region; natural non-clinical phrasing | Independent in-market Spanish proofreader |
| English + French | `en` + `fr` | Editorial French, terminology/tone consistency, French typographic conventions | Independent in-market French proofreader |
| English + Hindi | `en` + `hi` | Devanagari shaping/font handling; expansion-aware layout | Hindi translator and separate Devanagari-capable proofreader |
| English + Simplified Chinese | `en` + `zh-Hans` | Qualified Simplified-Chinese translation; CJK font, line break, and punctuation control | Independent Simplified-Chinese proofreader/typesetter |
| English + Hausa | `en` + `ha` | Qualified Hausa terminology and natural prompt phrasing | Independent in-market Hausa proofreader |
| English + Yorùbá | `en` + `yo` | Yoruba diacritics and tone-mark accuracy across all surfaces | Independent Yorùbá proofreader who checks every diacritic |

Each pair must use one consistent bilingual layout pattern—English prompt and approved translation together—rather than mixed languages or a seven-language omnibus interior.

## 5. Translator brief template

The named human supplies this package **only after the row’s earliest-handoff condition is met**:

```text
Product / edition ID:
English source-manifest row and SHA-256:
Target language pair:
Approved English source version / date:
Translation audience and country/region:
Required bilingual layout pattern:
Non-translatable items / brand terms:
Claims boundary to preserve exactly:
Terms requiring localized rewrite rather than literal translation:
Accessibility and typography requirements:
Deliverables: editable translated text, translator query log, terminology list,
  self-review certificate, and source-change reconciliation.
Excluded: legal opinion, medical/financial advice, title clearance, store upload,
  payment/account action, and use of customer data.
```

The translator must flag—not silently resolve—ambiguous health, prescription, sleep, breathwork, anxiety, finance, relationship, or safety language. The human reviewer decides whether counsel/product review is needed.

## 6. Acceptance checklist per bilingual edition

A language pair may proceed from draft to proof only when each box is documented:

- [ ] Exact English source digest from `TRANSLATION_SOURCE_MANIFEST.csv` is confirmed.
- [ ] Named translator’s scope, rights, compensation, and confidentiality terms are executed by the accountable human.
- [ ] Translator delivered editable text, terminology sheet, query log, and self-review.
- [ ] Independent in-market proofreader has reviewed the final text.
- [ ] All titles, subtitles, product descriptors, keyword/category terms, claims boundaries, safety notes, and QR-page text have a documented localized review.
- [ ] Product-specific counsel/qualified review cleared the localized claims and title where applicable.
- [ ] New edition ID/identifier and price approach are recorded; no existing English identifier is silently reused.
- [ ] Bilingual typesetting is rendered with correct diacritics/script shaping and no clipped/overflow text.
- [ ] Final pagination, trim, cover/wrap, barcode area, accessibility, file format, and printer/retailer requirements pass.
- [ ] A physical or platform proof is reviewed by a human fluent in the target language.
- [ ] Retail currency, current printer/platform floor, territory rights, tax/privacy/account requirements, and distribution conflict choice are documented.
- [ ] Named human records a release decision. `PASS_CANDIDATE` or a validator pass is not release authorization.

## 7. Excluded work

This package does not create localization content; it does not produce automatic translated text, translated listing copy, titles, searchable metadata, retailer prices, or bilingual files. It must not be used to claim that the portfolio is multilingual today.

See `MULTILINGUAL_MULTICHANNEL_MODEL.md` for channel/price planning, `SALE_READINESS_COMPLETION_MATRIX.md` for product-level release completion, and `AUTOMATION_POLICY.md` for the human-execution boundary.
