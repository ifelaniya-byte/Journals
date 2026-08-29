# Platform Playbook: Selling Our 18 Books With Zero Upfront Fees

Verified: 2026-08-28; fee-fact corrections absorbed same day. Per-platform listing
decisions (what lists where, what is held back and why) live in PLATFORM_DECISIONS.md. This document is the WAVE 2 DISTRIBUTION MAP.
WAVE 1 (now): Amazon KDP only - launch four first, 5 titles/week max. No other platform opens until the launch four have at least two weeks of clean KDP sales data (signal purity: scattered early sales wreck the only data that tells us what to widen).
WAVE 2 (after): everything below, winners first.
Written for someone who has never seen this repo. Read section 0 before touching anything.

------------------------------------------------------------------------------------
## 0. READ THIS FIRST

WHAT WE SELL: 18 print books (8 journals + 10 coloring books) under two series, Quiet Mind Journals and Quiet Mind Color, imprint Quiet Mind Press. Every book's complete file kit already exists in this repo, validated, on branch ADHD-Journals (the only branch we ever write to).

WHERE THE FILES LIVE: release3/<name>/ and release4/<name>/. Each folder holds:
- <name>_interior.pdf  (the finished book block; NEVER modify or reupload variants of this)
- <name>_cover_wrap.pdf  (full print cover, sized for Amazon KDP's spine formula only)
- <name>_cover.jpg  (front cover image for listings)
- listing_02 to listing_07 jpgs (interior preview images)
- metadata.txt  (paste-ready title, subtitle, 7 keywords, 2 categories, plain + HTML descriptions, price)

THE RULES (owner-set, non-negotiable):
1. Price is $9.99 everywhere it is allowed. Exceptions only by owner decision (see decision box).
2. Interiors are locked. No book block changes, ever.
3. Cover wraps are KDP-calculated. Never upload our wrap PDF to a non-KDP printer without regenerating (section 4).
4. Only branch ADHD-Journals gets our commits. The other lines in the repo belong to a separate publisher line; do not merge or touch.
5. No paid services. If a site asks for money to list, it goes in the blacklist (section 7), not on a card.

DECISION BOX (needs owner sign-off before those steps):
- RESOLVED 2026-08-28: owner chose market entry. A separate B&N-only edition at $14.99 exists at markets/bn-print/ (per-book front + back cover panels at 300 DPI and metadata-bn.txt). The main catalog stays $9.99 everywhere else and its validators are unchanged.
- IngramSpark requires an ISBN per title. Options: their paid ISBN ($85 each, or possibly a free non-transferable one, sources conflict, ask at signup), or our own Bowker block ($295 for 10). ISBNs are the only money that might ever need spending, and only for non-Amazon print expansion.
- RESOLVED 2026-08-28: digital PDFs are approved. Prices and holds are in PLATFORM_DECISIONS.md and EDITIONS_MATRIX.csv ($4.99 attractors / $6.99 rest / Middle Season print-only). Kits: markets/digital/. Wave 2 only — do not open digital during Wave 1 KDP.

FEES CHANGE. Every number below was verified on 2026-08-28 from current sources (section 9). Older guides are wrong about several of these. Re-check the platform's own pricing page at signup; if it differs from this document, the platform is right.

------------------------------------------------------------------------------------
## 1. MASTER TABLE (all verified 2026-08-28)

Tier A: zero upfront, our print files work TODAY
| # | Platform | Sells | Upfront cost | Royalty / net to us | Our status |
|---|----------|-------|--------------|--------------------|------------|
| 1 | Amazon KDP | print + ebooks + HARDCOVER | $0 | print 60% list minus print cost; ebook 70% under $9.99 | READY NOW; hardcover via markets/kdp-hardcover |
| 2 | Google Play Books | PDFs as-is | $0 | 70% of list (accept new TOS) | READY (Wave 2) via markets/digital |
| 3 | Gumroad | direct PDF/downloads | $0 | 90% minus $0.50 per sale | READY (Wave 2) via markets/digital |
| 4 | Payhip | direct PDF/downloads | $0 (free plan) | 95% | READY (Wave 2) via markets/digital |
| 4b | Ko-fi Shop | direct PDFs | $0 | 95% (5% fee) | READY (Wave 2) via markets/digital |
| 4c | Whop | direct PDFs | $0 | ~97% (verify exact fee at signup) | READY (Wave 2) via markets/digital |
| 4d | Lemon Squeezy | direct PDFs, merchant of record | $0 | 95% minus $0.50 | READY (Wave 2) via markets/digital |

Tier B: zero upfront, but needs cover regeneration or an ISBN first
| # | Platform | Sells | Upfront cost | Royalty / net | Our status |
|---|----------|-------|--------------|---------------|------------|
| 5 | IngramSpark | print to 40,000+ stores | NOT zero-upfront (ISBN required) | wholesale terms minus print minus 1.875% market access fee | Deferred to Wave 2 - see 6.5 |
| 6 | Barnes & Noble Press | print + ebooks | $0 | print 55% minus print cost; ebook 70% | READY via markets/bn-print ($14.99 edition) |
| 7 | Lulu | print (their store + retail) | $0 | 80% of margin on Lulu store; retail much less | Needs their cover setup; ebook side costs money, avoid |
| 8 | Blurb | print (their store + Amazon via their channel) | $0 | author sets margin above print cost | READY via markets/blurb (matched minimums) |

Tier C: zero upfront, but ebooks need EPUB conversion we have not built
| # | Platform | Sells | Upfront | Royalty | Our status |
|---|----------|-------|---------|---------|------------|
| 9 | Kobo Writing Life | ebooks | $0 | 70% in the 2.99 to 12.99 band, else 45% | Blocked: needs valid EPUB |
| 10 | Apple Books | ebooks | $0 | flat 70% | Blocked: needs EPUB3 + Mac/iDevice once + free Apple ISBN |
| 11 | StreetLib | ebooks (aggregator) | $0 | ~90% of retailer net | Blocked: needs EPUB |
| 12 | PublishDrive | ebooks (aggregator) | $0 free plan (1 ebook, 3 channels) | 100% net on free plan | Blocked: needs EPUB; free tier is tiny |

Near-free / flagged (know before using)
| Platform | Catch | Call |
|----------|-------|------|
| Etsy | $0.20 per listing (4-month renewal) | OK for PDF packs if owner approves digital; it is not strictly zero |
| Draft2Digital | $20 one-time activation + $12/yr fee for accounts under $100/yr (added 2026) | MOVED OFF the free list; use StreetLib or go direct instead |
| Smashwords | Now Draft2Digital's storefront | Not a separate channel anymore |
| PublishDrive paid tiers | From $13.99/month | Not needed for us |

------------------------------------------------------------------------------------
## 1B. MINIMUM-PRICE MARKETS (platform floors over $10) - READY

Some platforms' minimum list prices sit above our $9.99. We enter each at a matched price from a SEPARATE kit, so the main line and its $9.99 validators never change:

| Market | Floor rule | Our entry prices | Kit |
|---|---|---|---|
| B&N Press print | $14.99 flat minimum (Apr 2026) | all 18 at $14.99 | markets/bn-print/ |
| Amazon KDP hardcover | cost/0.60 = $11.33-$13.42 for our page counts | $13.99-$15.99, 17 titles (Night Pages out: 5x8 is not a KDP HC trim) | markets/kdp-hardcover/ |
| Blurb trade B&W | base cost ~$10.96-$13.05 | $11.99-$14.99 (base + $1) | markets/blurb/ |
| Lulu hardcover | ~$21+ (breakeven at floor) | NOT ENTERED: $0 royalty at minimum | documented in kit README |
| IngramSpark hardcover | ~$23.56 (breakeven at floor) | NOT ENTERED: $0 royalty at minimum | documented in kit README |
| IngramSpark paperback | under $10 for all 18 | no barrier; standard $9.99 | n/a |

Cover art for all these markets: the 300 DPI panels in markets/bn-print/<book>/ (regenerate with make_bn_kits.py). Interiors are unchanged everywhere.

## 2. WHAT TO UPLOAD WHERE (the short answer)

1. Amazon KDP paperback: all 18, exactly as built. Start with the four launch titles: The Dopamine Menu, The 75 Soft Journal, The Middle Season, Cozy Corners. Then 4 to 5 per week.
2. Digital PDFs: BUILT at markets/digital/ - 17 titles, two $-bundles (Starter Shelf $11.99, Color Complete $39.99), two free samplers as lead magnets, $4.99 attractors x5 / $6.99 x12, Middle Season print-only by design. Stores ranked least-to-most popular in markets/digital/README.md. Opens in Wave 2 (or earlier by owner call); materialize PDFs with make_digital_kits.py before uploading.
3. IngramSpark: the expansion path for bookstores and libraries. Worth it only after KDP proves sales. Requires ISBN decision.
4. B&N print: READY now via markets/bn-print ($14.99 edition). Lulu and Blurb: optional, weak retail payouts, cost nothing.
5. EPUB stores (Kobo, Apple, StreetLib, PublishDrive): our write-in journals and coloring pages are poor reflow ebooks. Do not convert for these until a real ebook product is designed (fixed-layout). Skip for now; revisit later.

------------------------------------------------------------------------------------
## 3. FILE PACKAGE, PER PLATFORM (exact files from the repo)

A. PRINT ON AMAZON KDP (per book)
- Interior: releaseN/<name>/<name>_interior.pdf
- Cover: releaseN/<name>/<name>_cover_wrap.pdf
- Listing images: <name>_cover.jpg (main) + listing_02..07 jpgs
- Text: everything in metadata.txt, pasted field by field (see section 5)
- Settings per book: B&W interior, white or cream paper as stated in metadata.txt, trim as stated, bleed OFF, matte finish, paperback, free KDP ISBN.

B. PRINT ON INGRAMSPARK / B&N / LULU / BLURB
- Interior: same PDF, unchanged.
- Cover: DO NOT reuse the KDP wrap. Each printer's spine math differs. Two routes:
  Route 1 (easiest, B&N only): upload separate FRONT and BACK covers; B&N builds the spine itself from your page count.
  Route 2 (all printers): download that printer's cover template for the exact trim + page count, rebuild the wrap at that size. Our covers are generated from scripts in this repo (build_nine_products.py / build_batch4.py drive texture + title art); regenerate at the new template size rather than stretching the old file.
- Text: same metadata.txt fields.

C. PDF DOWNLOAD STORES (Google Play, Gumroad, Payhip, Etsy)
- Product file: the interior PDF, plus a one-page license/terms sheet (does not exist yet; create before first upload: personal use only, no resale, no commercial redistribution).
- Cover image: <name>_cover.jpg.
- Preview images: listing_02..07.
- Text: same metadata.txt fields, price replaced by the digital price the owner sets.

D. EPUB STORES (Kobo, Apple, StreetLib, PublishDrive)
- We have no EPUB files. Building a proper fixed-layout EPUB of a coloring book is a design project, not a conversion. Park these platforms until then.

------------------------------------------------------------------------------------
## 4. SPINE WIDTH TABLE (our books, from CATALOG.csv, KDP formula)

Use with each printer's template generator; their spine number may differ slightly. Never mix printers' wraps.

| Book | Trim | Pages | KDP spine (in) |
|---|---|---|---|
| The 5-Minute Dump | 5.5 x 8.5 | 200 | 0.500 |
| Parallel Lives | 7 x 10 | 160 | 0.400 |
| The Night Pages | 5 x 8 | 120 | 0.300 |
| Settle | 6 x 9 | 172 | 0.430 |
| The Middle Season | 6 x 9 | 160 | 0.360 |
| The Dopamine Menu | 6 x 9 | 150 | 0.375 |
| The Slow Page | 6 x 9 | 144 | 0.360 |
| The 75 Soft Journal | 6 x 9 | 96 | 0.240 |
| First Strokes | 8.5 x 11 | 100 | 0.225 |
| Easy Garden | 8.5 x 11 | 100 | 0.225 |
| Mosaic Mind | 8.5 x 11 | 120 | 0.270 |
| Woodland Wonders | 8.5 x 11 | 120 | 0.270 |
| Fractal Dreams | 8.5 x 11 | 140 | 0.315 |
| Architectural Visions | 8.5 x 11 | 140 | 0.315 |
| Cozy Corners | 8.5 x 11 | 104 | 0.234 |
| Botanical Ink | 8.5 x 11 | 104 | 0.234 |
| Celestial Atlas | 8.5 x 11 | 104 | 0.234 |
| Tidal Ink | 8.5 x 11 | 104 | 0.234 |

------------------------------------------------------------------------------------
## 5. METADATA MAPPING (metadata.txt to any platform's form)

| Our metadata.txt field | Where it goes on the platform |
|---|---|
| AMAZON TITLE line | Title field (everywhere, not just Amazon) |
| SUBTITLE | Subtitle field; omit on platforms without subtitles |
| AUTHOR / IMPRINT | Author: Quiet Mind Press |
| SERIES | Series field (create the series first if the platform supports it) |
| TRIM / PAGE COUNT / INTERIOR | Print setup steps (match exactly) |
| CATEGORIES | Category picker; choose nearest match per platform |
| SEVEN BACKEND KEYWORDS | Keyword field where one exists (Apple, Kobo, KDP, B&N); ignore on stores without keywords |
| DESCRIPTION (plain) | Use this on Kobo (plain text only, no HTML allowed), Gumroad, Payhip, Etsy |
| DESCRIPTION (HTML paste) | Use on KDP, B&N, Apple, Google Play where HTML is accepted |
| SUGGESTED PRICE | $9.99, unless the platform forces otherwise (B&N print minimum; digital editions per owner decision) |

------------------------------------------------------------------------------------
## 6. PLATFORM CHAPTERS (details, steps, pitfalls)

### 6.1 Amazon KDP (kdp.amazon.com) - START HERE
- Cost: $0 to publish. Free KDP ISBN. No exclusivity for print. (Ebook 70% royalty needs a $2.99 to $9.99 price; we are print-first.)
- Steps: Create account + tax interview + bank details. Create paperback. Paste title, subtitle, author, series. Enter the 7 keywords + 2 categories from metadata.txt. Upload interior PDF and cover wrap PDF. Choose trim/paper/bleed OFF/matte exactly as metadata.txt says. Set $9.99. Order a proof on the first title only. Publish.
- Pitfalls: do not enable KDP Select (it makes ebooks exclusive). Do not turn on expanded distribution (that is what IngramSpark does better later). Upload a print proof check: spine text must sit centered; our wraps were built for exactly these page counts, so never upload a wrap with a different page count interior.
- Fees note: none. KDP takes printing cost from the 60% royalty share only when a book sells.

### 6.2 Google Play Books (play.google.com/books/publish)
- Cost: $0, no ISBN required (free GGKEY identifier). Verified: they accept BOTH .epub and .pdf; with PDF, readers get the original layout. Royalty 70% of list in 60+ countries after accepting the updated Terms (default 52% if not). No exclusivity.
- Our angle: the only major store where our print-layout PDFs can be sold as-is, no conversion. Best digital fit for the coloring line (tablets + home printing).
- Steps: sign in with a Google account, complete the publisher profile (tax interview + bank), Add Book, enter metadata, upload the interior PDF as the book file plus cover jpg, set price per country (suggest digital price, owner decision), accept updated TOS for the 70% split, submit.
- Pitfalls: account vetting can take days. Price is per country; set the US price first then let auto-pricing fill others. The 52% default applies until the new TOS is accepted.

### 6.3 Gumroad (gumroad.com) - direct sales, we own the customer
- Cost: $0 monthly; fee is 10% + $0.50 per sale. No listing fees.
- Steps: create account, New Product, type Digital Download, upload the PDF + license sheet, cover image + preview jpgs, paste plain-text description, set price, publish. Payouts to bank/PayPal.
- Pitfalls: traffic is 100% ours to bring (ads, social). Gumroad is a storefront, not a marketplace with its own shoppers. Discover-fee differs (30%) if sales come through their Discover feed.

### 6.4 Payhip (payhip.com) - direct sales, cheapest fees; designated redundancy if Gumroad ever flags a health-adjacent item (mirror the same products here)
- Cost: Free Forever plan, 5% fee, no per-transaction fixed fee. Paid plans exist; ignore them.
- Steps: sign up, Add Product, Digital Download, upload PDF + license sheet, add cover + previews, paste description, set price, connect PayPal/Stripe.
- Pitfalls: same as Gumroad, we bring the traffic. Instant payouts via Stripe/PayPal are the plus.

### 6.5 IngramSpark (ingramspark.com) - bookstore and library reach
- Cost: title setup is free, but NOT since Feb 2026 as some guides claim - the setup fee ended with IngramSpark's 2023 anniversary initiatives; the Feb 2026 rate sheet only repriced other items. Real costs: 1.875% Market Access Fee on every distributed sale (rate sheet effective Feb 1, 2026), $25 per revision after the first 60 days, and an ISBN per title (roughly $85 each via IS or a Bowker 10-pack at $295) - which is why IngramSpark fails the strict no-upfront rule and sits in Wave 2.
- Steps: account + tax/bank. Buy/assign ISBNs. Create title, enter metadata from metadata.txt (their form is detailed; take it slowly), upload interior PDF, download their cover template for exact trim + page count + paper, rebuild the wrap (section 3B route 2), upload, set wholesale discount (55% standard; 40% costs us placement) and returns (make it NO initially; bookstores prefer yes but that risks returned inventory cost - owner decision later), price $9.99 (verify their minimum for our page counts; if $9.99 is below their minimum, escalate to owner before pricing higher).
- Pitfalls: their review is pickier than KDP; embed fonts, exact template size, no crop marks. This is the platform where a wrong wrap wastes the most time.

### 6.6 Barnes & Noble Press (press.barnesandnoble.com)
- KIT READY: markets/bn-print/<book>/ holds bn_front.jpg, bn_back.jpg (300 DPI, bleed) and metadata-bn.txt at $14.99. Upload the interior PDF from release3/4 unchanged.
- Constraints (verified 2026-08-28): $14.99 floor effective Apr 22, 2026, with sub-$14.99 titles removed from sale from May 14, 2026; one B&N Press account is capped at 100 titles (our 18 fit comfortably); ISBN must be unique/never-used - the free B&N ISBN qualifies but is B&N-only.
- Cost: $0. Free B&N ISBN. Ebook royalty 70% at $2.99+. Print royalty 55% minus print cost. IMPORTANT: print minimum list price $14.99 since April 2026 - conflicts with our $9.99 cap, see decision box.
- Steps: account, Create Print Book, enter details, download their cover template (6 inputs: page count, trim, color, format, finish, paper), or use the separate front/back upload route and let them build the spine (easiest for us), upload interior PDF, set price (pending owner decision), publish. Ebooks via the same portal need EPUB.
- Pitfalls: their spine math is not KDP's; never reuse our KDP wrap. Page count must match the template exactly.

### 6.7 Lulu (lulu.com)
- Cost: $0 to publish print; ~$0.02/page B&W print cost; their store pays ~80% of margin; retail distribution (Global Reach) takes Lulu 20% of net plus the retailer's 40-55% - thin for us, optional. Ebook distribution costs $4.99 one-time per title: blacklisted (section 7).
- Steps: account, Start a Project, choose print format, upload interior PDF, use their cover wizard or upload a built wrap from their template, set price with their revenue calculator, publish to their store (and optionally retail).
- Pitfalls: free Lulu ISBN lists Lulu as publisher; retail distribution really wants our own ISBN. Print cost per page is higher than KDP/IS; at $9.99 the margin is near zero on retail channels - treat Lulu store-only unless numbers say otherwise.

### 6.8 Blurb (blurb.com)
- Cost: $0 to publish; buyers pay print cost plus the profit we set. Distribution to their bookstore and Amazon via their channel.
- Steps: account, choose trade book, upload interior PDF, use their cover template tool, set profit, publish.
- Pitfalls: Blurb's printing is premium-priced; a $9.99 list may sit below their minimum for 100+ page color. Check their calculator first; if uneconomic, skip without spending anything.

### 6.9 Kobo Writing Life (kobo.com/writinglife) - parked (needs EPUB)
- $0, 70% royalty in the $2.99 to $12.99 band (45% outside), no ISBN required, no exclusivity. Accepts EPUB (fixed-layout EPUB3 supported for visual books) - descriptions must be PLAIN TEXT, they strip HTML. When a fixed-layout ebook exists, this is the first EPUB store to open.

### 6.10 Apple Books (authors.apple.com) - parked (needs EPUB + Apple device)
- $0, flat 70%. EPUB3 that passes EPUBCheck. Cover 1400px minimum shortest side (2400+ recommended), under 10MB to be safe. ISBN required but Apple supplies one free (lists Apple as publisher). One-time account setup needs a Mac, iPhone, or iPad. Parked until a real ebook edition exists.

### 6.11 StreetLib (streetlib.com) - parked (aggregator, needs EPUB)
- $0, ~10% commission on retailer net, wide reach incl. libraries. Alternative to Draft2Digital now that D2D charges activation.

### 6.12 PublishDrive (publishdrive.com) - parked
- Free plan covers 1 ebook on 3 channels, no commission; paid tiers from $13.99/mo (skip). Only worth it if we want one aggregator test title.

------------------------------------------------------------------------------------
## 7. BLACKLIST AND FEES TO REFUSE

- Draft2Digital: $20 one-time activation + $12/yr maintenance for accounts earning under $100/yr (both announced Apr 15, 2026; the yearly fee waives at $100+ net royalties). Not free anymore; StreetLib covers the same job.
- Lulu ebook distribution: $4.99/title.
- Lulu Author Spotlight ($299) and similar "marketing packages" everywhere: no.
- BookBaby and any "publishing package" company (hundreds to thousands upfront): vanity tier, no.
- ISBNs from anyone except Bowker (US) or the platform's free option: overpriced resellers.
- Anyone charging "listing fees", "review fees" or "account fees" not listed in section 1: the answer is no, and log it in the watch log.

------------------------------------------------------------------------------------
## 8. LAUNCH ORDER AND WEEKLY RHYTHM

Week 1: KDP - The Dopamine Menu, The 75 Soft Journal, The Middle Season, Cozy Corners (the ad-launch four). Order one proof of Middle Season.
Week 2: KDP - Settle, The Slow Page, 5-Minute Dump, Night Pages.
Week 3: KDP - Easy Garden, First Strokes, Mosaic Mind, Woodland Wonders.
Week 4: KDP - Cozy line finishes (Botanical Ink, Celestial Atlas, Tidal Ink), Fractal Dreams, Architectural Visions, Parallel Lives.
Week 5+: owner decisions land (digital, B&N price, ISBNs) and Tier B opens accordingly.
Never upload more than 5 books in a week; batch reviews stay clean and mistakes stay traceable.

------------------------------------------------------------------------------------
## 8B. AUTOMATION RULE (standing)

Any future tooling follows one pattern: automated preparation, human-gated publication.
The repo may draft packages, listings, and promotional copy; a human approves before
anything is published or posted, on any platform. This mirrors validate-before-push.
Autonomous mass-posting agents and "invisible to spam filters" designs are rejected:
they violate platform ToS and risk the brand's ability to advertise later.

Promo-copy guardrail (extends the catalog's BANNED_FRAGMENTS discipline to marketing
text): never drug brand names (Ozempic, Wegovy, Mounjaro), never cure / treatment /
prescription / guarantee language, never weight-loss promises. Use wellness journey,
self-care routine, tracking, steady progress.

## 9. SOURCES (verified 2026-08-28)

- IngramSpark: setup fee elimination dates to their 2023 anniversary initiatives (Feb 2026 guides that claim the elimination are misdated); 1.875% market access fee + current rates from the price sheet effective Feb 1, 2026; $25 post-60-day revisions.
- B&N Press free, 70% ebook, 55% print, $14.99 print minimum April 2026: writersofthewest.net guide July 2026; press.barnesandnoble.com cover template generator.
- Google Play Books accepts PDF + EPUB, 70%/52% split, free GGKEY: support.google.com/books Partner Center help pages.
- Draft2Digital $20 activation + $12/yr fee: draft2digital.com/faq (Apr 2026) and publishdrive.com comparison (Apr 2026).
- Apple Books free ISBN, EPUB-only, 1400px cover, device requirement: scribecount.com Apple guide July 2026; help.apple.com Books Publisher guide.
- Kobo EPUB-only, plain-text descriptions, 70% band: cambric.pub Kobo requirements; keachpublishingagency.com Kobo guide Aug 2026.
- Lulu free print, $4.99 ebook distribution, 20% distribution share: writtenwordmedia.com; aceworldpgs.com comparison Jan 2026; ghostwritingllc.com calculator guide July 2026.
- Gumroad 10% + $0.50, Payhip free/5%: platform comparisons Jan 2026 (zanfia.com, barkerbooks.com).
- Smashwords merged into Draft2Digital: publishing news summaries Feb 2026.
Fees drift. The signup screen always wins over this document. Re-verify anything older than a quarter.
