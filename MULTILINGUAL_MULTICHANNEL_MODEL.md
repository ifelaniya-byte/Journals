# Multilingual + multichannel controlled operating model
## Six bilingual language pairs, all practical direct sales paths, and no unauthorized market action

**Status:** planning architecture only; created 2026-08-28.  
**Applies first to:** the six existing Wave 1 paperback candidates only.  
**Does not authorize:** translations, bilingual interiors, ISBN acquisition, file conversion, listing creation, price changes, KDP upload, account creation, spend, domain deployment, customer-data collection, or use/merger of any public repository.

This model responds to the request for bilingual editions in **Spanish, French, Hindi, Simplified Chinese, Hausa, and Yorùbá**, and for an all-feasible direct-channel price model. It deliberately preserves the agreed current US paperback anchors for Wave 1 rather than importing the public `Journals` repository’s $9.99 catalog strategy.

## 1. Decision boundary and provenance firewall

The public `ifelaniya-byte/Journals` repository is an unverified potential parallel commercial operation. Its public branch documentation itself says not to merge its product branches. The only permitted use here is **read-only capability comparison**. No title, copy, translation, PDF, cover, asset, code, pricing, seller account, ISBN, customer list, or branch history is imported, copied, or treated as owned.

Before any later content-level reuse can even be considered, the authenticated owner must complete the relationship, rights, fork/network, and private-evidence steps in `GITHUB_PUBLIC_EXPOSURE_AUDIT.md`, then record an explicit merge-under-governance or firewall/separation decision. Until then, this repository remains independent.

`AUTOMATION_POLICY.md` controls execution. A generated row with a price is not an approval to sell it.

## 2. Read-only capability comparison: what the separate public branches appear to have

| Public branch observed | Capability observed at a high level | Controlled response in this catalog | Transfer status |
|---|---|---|---|
| `ADHD-Journals` | Separate series, retailer-ready file inventories, channel playbook, B&N/PDF paths, and localized *listing* copy while source interiors remain English | Add independent channel registry, pricing model, bilingual-edition gate, and a no-duplicate-distribution rule | Capability only; no files/copy/titles imported |
| `Range-Band` | Per-title / per-channel price-floor idea across a larger health-adjacent catalog | Use a canonical-source-linked price model, but preserve existing premium Wave 1 anchors and retain all claims gates | Capability only; do not adopt its $9.99 strategy or health-title inventory |
| `Market-Files` | Separate B&N cover-panel, printable-PDF, and lead-magnet workstreams | Require a separate, approved edition/file path per channel; do not infer rights to any public asset | Capability only; no assets imported |
| `main` | Pointer/index branch | No product source is taken from a pointer branch | No transfer |

**Key improvements over a simple branch merge:** this model distinguishes a store from a fulfilment service, preserves per-edition identifiers, blocks duplicate print distribution, records the format actually required, and prevents localized listing text from being mistaken for a translated/bilingual product.

## 3. Product and language architecture

### Source edition
The governed English paperback is the source edition. Its exact title, pages, trim, collection, current price posture, wave, and status remain governed by the machine-readable table in `PORTFOLIO.md` and guarded by `verify_canonical.py`.

### Bilingual editions
Each approved future bilingual edition is a **new, separate edition**, not a new cover slapped onto the English interior:

1. English remains the source text; pair it with **one** target language per edition.
2. Use prompt-by-prompt paired presentation, with the English prompt and its translation together. Do not mix all seven languages in one interior.
3. Assign a new edition identifier and, where required, a separate ISBN/retailer identifier after the final translated page count exists.
4. Rebuild the interior and wrap from the target-language text. The English cover wrap cannot be reused blindly.
5. Run language rendering, typography, diacritic, page-flow, accessibility, claims, title/subtitle, category/keyword, proof, and platform checks for that particular edition.
6. Create no translation from an AI draft alone. A qualified translator and an independent in-market proofreader must approve the final text.

The language registry is generated at `BILINGUAL_LANGUAGE_REGISTER.csv`.

| Target language | Code | Specific non-negotiable QA |
|---|---|---|
| Spanish | `es` | Qualified editorial translation and regional reading for neutral, non-medical wording |
| French | `fr` | Qualified editorial translation and regional reading for tone, terminology, and typography |
| Hindi | `hi` | Devanagari-capable typesetting, shaping/font proof, and in-market review |
| Simplified Chinese | `zh-Hans` | CJK-capable typesetting/font proof, qualified translation, and in-market review |
| Hausa | `ha` | Qualified Hausa translator and in-market proofreader; no assumed terminology equivalence |
| Yorùbá | `yo` | Qualified reviewer must proof every tonal diacritic in cover, interior, metadata, and QR page |

A bilingual edition does **not** become eligible because the English edition is eligible. Health-, sleep-, breathwork-, finance-, and relationship-adjacent language requires a fresh claims/translation review. B10, B12, and B18 therefore retain every existing product-specific gate.

## 4. Price architecture

### 4.1 Current price authority
Only six current **US KDP paperback anchors** are authorized as conditional listing hypotheses, and all are still `HOLD — awaiting release gates`:

| SKU | English paperback US anchor |
|---|---:|
| A01 | $16.99 |
| A04 | $17.99 |
| A05 | $15.99 |
| B10 | $17.99 |
| B12 | $18.99 |
| B18 | $18.99 |

All Wave 2 and Vault products retain `TBD`/`N/A` price posture. This model will not invent a market price for them.

### 4.2 Proposed edition-level planning tiers
These are not public prices and do not supersede the canonical table. They are the starting values emitted for a future approved edition, subject to live platform floors and named human approval.

| Existing English paperback anchor | Future English digital edition | Future bilingual digital edition | Future bilingual paperback starting point |
|---:|---:|---:|---:|
| $15.99 | $8.99 | $10.99 | $18.99 |
| $16.99 | $9.99 | $11.99 | $19.99 |
| $17.99 | $9.99 | $11.99 | $20.99 |
| $18.99 | $10.99 | $12.99 | $21.99 |

For a bilingual paperback, the final list price is **at least** the displayed starting point and must be increased if the final translated page count or the live printer’s minimum makes that necessary. The value is not valid until actual final pagination and the applicable platform calculator are recorded.

### 4.3 Store-by-store pricing rule
`MULTICHANNEL_PRICING_MODEL.csv` supplies a row for each of the six priced Wave 1 SKUs and each channel/edition combination. It gives the exact USD planning price where one can responsibly be stated and the governing rule where a live printer quote or local-currency setting controls.

| Channel group | Price rule in the model | Why it is conditional |
|---|---|---|
| Amazon KDP paperback | Exact canonical US anchor for the English paperback; bilingual edition uses bilingual starting point | Every local marketplace price and printing-cost minimum must be confirmed in the live KDP pricing page; books remain HOLD |
| B&N Press print | English anchor if it is not below B&N’s current minimum; bilingual starting point otherwise | Current B&N print minimum, final production spec, B&N template, and proof control |
| Lulu Bookstore | English anchor / bilingual starting point only if live print cost permits | Lulu calculator and final page count control |
| Lulu Global Distribution | `max(anchor or bilingual start, current Lulu Global floor)` | Do not open alongside another route that duplicates Amazon/B&N/Ingram retail listing availability |
| IngramSpark | `max(anchor or bilingual start, live wholesale/distributor minimum)` | Requires publisher-owned ISBN, discount/returns decision, file rework, and one distributor route only |
| Pothi, Blurb, Bookvault | Live local printer/fulfilment quote required | Regional eligibility, account terms, customer experience, and no-duplicate-route decision control |
| Kindle, Apple Books, Google Play Books, Kobo, B&N eBook | Future English/bilingual digital planning tier | A validated accessible EPUB/fixed-layout edition, rights/territory decision, and retailer metadata are prerequisites |
| Payhip, Gumroad, Ko-fi, itch.io, Lemon Squeezy, Whop, Buy Me a Coffee, Etsy | Future English/bilingual digital planning tier | Requires an approved PDF, current seller fees/terms, human-owned checkout, tax, privacy, and delivery policy |
| Shopify, WooCommerce, Big Cartel | Same future digital tier for the actual edition | These are owned-checkout tools, not retailer shelves; they require domain, deployment, payment, security, privacy, tax, and customer-data approvals |

The spreadsheet is deliberately in USD for comparable internal planning. It does **not** set foreign-currency retail prices. The accountable human must set each retailer’s current local-currency price and confirm the current print-cost/royalty result immediately before any approved listing is submitted. This matters because tax treatment, exchange conversion, print cost, local price floors, and platform terms change.

## 5. Practical direct-channel register

“Every store” is not a finite global category. The controlled scope is **every practical direct sales path relevant to a US-based rights holder selling a book, fixed-layout eBook/PDF, or owned-checkout product**, plus the essential indirect/distribution paths that could conflict with a direct listing. Regional marketplaces requiring local inventory, a local entity, or unverified eligibility remain conditional rather than falsely labelled available.

### Tier 1 — direct print / retailer paths
- Amazon KDP paperback — all currently supported Amazon print marketplaces, one deliberate local-price review per marketplace.
- Barnes & Noble Press print.
- Lulu Bookstore print.
- Lulu Global Distribution — parked until a single-distribution-route decision.
- IngramSpark — parked until publisher-owned ISBN, wholesale/returns, and duplicate-channel review.
- Pothi store (India) — parked pending current seller eligibility and print quote.
- Blurb Bookstore — parked pending format/economics review.
- Bookvault paired with a human-approved owned checkout — parked; it is fulfilment, not a retail store.

### Tier 2 — direct eBook paths (new files, not the existing paperback PDFs)
- Amazon Kindle
- Apple Books
- Google Play Books
- Kobo Writing Life
- Barnes & Noble Press eBook

### Tier 3 — direct PDF/download paths (new, approved, accessible print-at-home PDF only)
- Payhip
- Gumroad
- Ko-fi Shop
- itch.io
- Lemon Squeezy
- Whop
- Buy Me a Coffee
- Etsy

### Tier 4 — owned-checkout infrastructure, not independent book retailers
- Shopify
- WooCommerce
- Big Cartel

### Conditional / indirect paths, recorded so they are not double-counted as stores
- Draft2Digital, StreetLib, and PublishDrive: aggregator/distribution choices, not a reason to upload duplicate editions to the stores they serve.
- Library channels (for example, OverDrive, hoopla, Bibliotheca, BorrowBox): use only through an approved eligible distributor and rights/identifier route.
- Amazon Expanded Distribution, Lulu Global, and IngramSpark: choose deliberately; do not activate overlapping routes simply because each says it adds reach.
- Regional physical marketplaces: add only after the accountable human confirms seller eligibility, local fulfilment/inventory, tax, language, and rights requirements.

## 6. Mandatory order of operations per edition and channel

1. **Rights and portfolio gate:** named human confirms the source text, ownable assets, collection/imprint status, and individual SKU eligibility.
2. **Translation gate:** qualified translator + separate qualified proofreader approve the full paired text. Preserve their dated deliverables and scope.
3. **Claims and title gate:** counsel/qualified reviewer signs off on the localized title, subtitle, claims boundary, categories, keywords, and sales description.
4. **Edition gate:** final pagination, trim, accessibility, file rendering, cover template, barcode/identifier, QR, proof, and metadata are specific to the target language and store.
5. **Price gate:** reviewer records current printer/retailer floor, retail currency, royalty/economics, price source, date, and approving human. The CSV row is only a starting point.
6. **Channel-conflict gate:** one human records the single selected print/distribution path and digital exclusivity status. Do not use KDP Select if the same digital edition is sold non-exclusively elsewhere.
7. **Commerce gate:** human approves payout, tax, privacy, customer-data, refund, accessibility, and customer-support arrangements.
8. **Release gate:** named human alone submits, publishes, spends, or deploys after the preceding controls are complete.

## 7. Official pricing / format checkpoints (verify again at action time)

The following are reference points for the model, not a substitute for current account-side confirmation:

- KDP paperback royalty and marketplace pricing rules: <https://kdp.amazon.com/en_US/help/topic/G201834330>
- KDP print book pricing page and marketplace/local-price behavior: <https://kdp.amazon.com/en_US/help/topic/G8BKPU9AGVZSF9QF>
- B&N Press print pricing and current $14.99 minimum: <https://help-press.barnesandnoble.com/hc/en-us/articles/5358788362907-Print-Book-Pricing-and-Printing-Costs>
- Lulu print revenue and Global Distribution price requirements: <https://help.lulu.com/en/support/solutions/articles/64000262744-creator-revenue-guide>
- Google Play Books accepted formats: <https://support.google.com/books/partner/answer/166501>
- Google Play territories, local prices, and effective-price review: <https://support.google.com/books/partner/answer/3157413>
- Apple Books direct publishing overview: <https://authors.apple.com/>
- Kobo Writing Life direct publishing overview: <https://help.kobo.com/hc/en-us/articles/360017771754-What-is-Kobo-Writing-Life>

## 8. Non-implementation statement

No bilingual text, cover, interior, EPUB, PDF edition, ISBN, local-currency price, checkout, store account, listing, campaign, or distribution activation has been created by this model. It is a controlled specification and generated planning grid only.
