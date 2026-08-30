# SELL HUB — 54 SKUs, two imprints, one operating law

**This file is the only briefing an AI (or a human) needs to list, price, and sequence the catalogs.**  
Do not invent a third imprint. Do not merge branches. Do not mix series pages. Do not paste a B&N floor onto KDP. Do not dose, diagnose, or name a manufacturer in a title.

Verified against live trees **2026-08-28**:

| Imprint | Git branch | Tip SHA | Source of truth |
|---|---|---|---|
| **Quiet Mind Press** (ours, 18) | `ADHD-Journals` | `3feca69` | `/tmp/qmp-adhd/CATALOG.csv`, `EDITIONS_MATRIX.csv`, `PLATFORM_DECISIONS.md`, `release3/` + `release4/` |
| **Range Band Press** (the other line, 36) | `Range-Band` | `8562469` | `/tmp/Journals-remote/range-band/KDP-Complete-Kit/METADATA.csv`, `SELLING_AND_VALUATION.md`, `CASHFLOW.md`, numbered folders `01_`–`36_` |
| Pointer only | `main` | `8cc3ab5` | No books. Do not upload from `main`. |

Owner rules still in force: **do not merge** the two lines; **do not Compare & pull request**; **do not force-push**; interiors stay English; medical copy is **tracking / management only**; **keep GLP-1** as the stem (no Ozempic / Wegovy / Mounjaro / Mounjaro-class brand in titles).

---

## 0. Operating law (floors, waves, language)

### 0.1 KDP paperback (both imprints)

US list **$9.99** on every paperback that is allowed to list. That is the first price that unlocks **60% − print** on Amazon.com (50% at $9.98 and below). Cite: `range-band/KDP-Complete-Kit/SELLING_AND_VALUATION.md`; Quiet Mind `CATALOG.csv` column `price` = `$9.99` × 18; Range Band `METADATA.csv` column `price` = `9.99` × 36.

Usual 60% floors to match at KDP upload (confirm live): UK **£7.99**, euro **€9.99**, CA/AU typically **C$13.99 / A$13.99**.

Bleed **OFF**. Interior **black & white**. KDP free ISBN is fine. Never upload a merged interior+cover PDF.

### 0.2 Store floors that are not $9.99

| Channel | Floor / rule | Quiet Mind cite | Range Band cite |
|---|---|---|---|
| B&N Press print | **$14.99** hard floor since 22 Apr 2026 | `markets/bn-print/` + `PLATFORM_DECISIONS.md` | `MARKETS/BN-Press/` + `MARKETS/PRODUCTS.csv` column `BN` |
| Lulu Global print | **max(KDP, 2× print, $9.99)** | `MARKETS/PRODUCTS.csv` LULU-GLOBAL $9.99–$11.99 | `MARKETS/PRODUCTS.csv` — title **30 = $11.99**, other 35 = $9.99 |
| KDP hardcover | cost/0.60 then next x.99 with ≥ $1 royalty | `markets/kdp-hardcover/` + `EDITIONS_MATRIX.csv` | **not built** |
| Blurb trade | 5×8 / 6×9 / 8×10 only; entry ≈ base+$1 | 6 titles in `markets/blurb/` | **not built** |
| Digital PDF | Quiet Mind: **$4.99 × 5 attractors + $6.99 × 12**, Middle **print-only**. Range Band: **$9.99 × 36** | `EDITIONS_MATRIX.csv`, `markets/digital/`, `PLATFORM_DECISIONS.md` | `MARKETS/DIGITAL-9.99/` |
| IngramSpark paperback | formula min under $10 on these page counts; **parked** (Bowker ISBN is upfront money) | `MARKETS/Ingram-PARKED/` | `MARKETS/Ingram-PARKED/` |
| Kobo / Apple / StreetLib | **parked** — no EPUB product | `PLATFORM_DECISIONS.md` | `SELLING_AND_VALUATION.md` §6 |
| Whop | skip | `PLATFORM_DECISIONS.md` | — |

**Never put a B&N $14.99 onto Amazon. Never put a digital $4.99 onto KDP print.**

### 0.3 Waves (do not skip; do not ads-blast)

**Quiet Mind** — `MARKETING.md` + `PLATFORM_DECISIONS.md` + `PLATFORM_PLAYBOOK.md`:

1. Wave 1 (now): **KDP paperback only**. Ads only on **Dopamine Menu, 75 Soft, The Middle Season, Cozy Corners**. Then 5 titles/week.
2. Wave 2 (after two weeks of clean KDP data on the four): digital (Payhip / Google Play / Lemon Squeezy), then 7 journal hardcovers, then B&N **thick 11**, then Etsy (owner fee OK), then Blurb experiment (Middle + Settle), then Ingram after ISBN money.

**Range Band** — `CASHFLOW.md`:

| Wave | Titles | Money |
|---|---|---|
| 1 — cash | 01 Meal, 09 Calendar, 05 Craving, 30 PMDD, 10 Sober, 12 Migraine | Ads live here |
| 2 — also-bought | 02, 19, 08, 25, 07, 24, 22 | No ads until Wave 1 has ~10 reviews |
| 3 — companions | 03, 06, 23, 27, 20, 11, 15, 18 | Series page only |
| 4 — deep / quiet | the rest | **No ads** |

**Do not bid Quiet Mind queries against Range Band queries** (`CASHFLOW.md` “Do not bid against Quiet Mind”). Two imprints, two query families, also-bought never mixes them.

### 0.4 Language that is banned in listings and ads

Quiet Mind `niche_upgrades.py` `BANNED_FRAGMENTS` + `MARKETING.md`: no vagus-nerve stimulation, no polyvagal exercises, no sleep-disorders browse node, no “elderly coloring book”, no **75 Hard** / 75 Medium, no 75 Hard bids on 75 Soft.

Range Band `BRAND.md` + every `listing.txt`: tracking/management only; no “treats nausea”; no “dose 0.25 mg”; no manufacturer in the **title**. GLP-1 stem sentence belongs on GLP-1 volumes only (titles **01–09 and 19–27**, plus 08 NSV in the GLP-1 tracking series). Non-GLP titles 10–18 and 28–36 must **not** say “GLP-1 is the stem on the cover” (fixed `Range-Band` `be620dc`).

---

## 1. Are the books identically prepared?

**No. Within each imprint’s KDP paperback kit, yes. Across imprints, and across Quiet Mind’s own market packs, no.**

### 1.1 Quiet Mind — KDP paperback kit is identical × 18

Every title under `release3/<slug>/` or `release4/<slug>/` has all ten files (audit 2026-08-28, zero misses):

| File | Role |
|---|---|
| `<slug>_interior.pdf` | KDP interior (locked) |
| `<slug>_cover_wrap.pdf` | KDP wrap only (do not send to B&N / Ingram / Blurb / Etsy POD) |
| `<slug>_cover.jpg` | Amazon image 1 |
| `listing_02`–`05_interior.jpg` | Amazon images 2–5 (coloring: design pages, not blank backs) |
| `listing_06_callout.jpg` | trim / paper / difficulty / **$9.99** — **do not use on digital listings** (`make_digital_kits.py` warning) |
| `listing_07_series.jpg` | Quiet Mind Journals stack **or** Quiet Mind Color ladder |
| `metadata.txt` | Amazon title (≤200), subtitle, 7 unique keywords, 2 categories, plain + HTML, **$9.99** |

Keyword guard: **18 × 7 = 126 keywords, all unique** (`gen_catalog.py` `keyword_guard`). Cover PDF keeps the short brand word; the listing uses `CATALOG.csv` `amazon_title`. Paste the Amazon title, not the cover word (`00_START_HERE.md`).

Paper: cream for journals except **Middle Season = white** (grids). White for all 10 coloring books. Trim exceptions: Dump **5.5×8.5** (not 5.5×8 — `CATALOG.csv` row 1, QA `774b35e`), Night **5×8**, Parallel **7×10**, coloring **8.5×11**, remaining journals **6×9**.

### 1.2 Quiet Mind — two market trees, now stamped to `PLATFORM_DECISIONS.md`

There are **two market trees** on `ADHD-Journals`. Same policy; different files.

| Tree | What it is | Digital | B&N | Hardcover | Blurb | i18n |
|---|---|---|---|---|---|---|
| **Uppercase `MARKETS/`** | $0-to-list census pack (`make_markets.py`) | **17** listings. `PRODUCTS.csv` DIGITAL = **$4.99 × 5 / $6.99 × 12 / Middle print-only**. | **18** listings at **$14.99**. Thin 7 stamped **HOLD** (do not upload). | none | none | **zh/hi/es/fr/ha/yo × 17** (Middle omitted). Interiors stay English. |
| **Lowercase `markets/`** | Matched-minimum kits | **17** PDFs: attractors **dump, dopamine, cozy, soft, settle = $4.99**; other 12 = **$6.99**; Middle **print-only** | **18** kits (`bn_front.jpg` + `bn_back.jpg` + `metadata-bn.txt`). Thin 7 banner **HOLD — DO NOT UPLOAD**. | **17** `metadata-hc.txt` only (**Night excluded**). **10 coloring HCs stamped HOLD.** 7 journals LIST. **No case-laminate wrap PDF.** | **6** `metadata-blurb.txt` only: night, settle, middle, dopamine, slow, soft. **No Blurb cover.** | none |

**`PLATFORM_DECISIONS.md` is the seller’s answer sheet. Disk now matches:**

| Decision | `PLATFORM_DECISIONS.md` | On disk |
|---|---|---|
| B&N | List **11 titles ≥120pp** at $14.99. **Hold 7 thin** | Kits exist for all 18. Thin 7 = HOLD in listing + `00_VERSIONS.md` Go? column |
| KDP hardcover | **7 journals only**. **Hold 10 coloring HCs.** Night impossible. | 17 metadata kits. Coloring = HOLD. Night omitted |
| Digital | $4.99 × 5 + $6.99 × 12, Middle print-only | Both trees match |
| KDP Expanded Distribution | **OFF** | `MARKETING.md`, `00_START_HERE.md`, checklists, `MARKETS_PLAYBOOK.md` = **OFF** |
| Digital editions | Approved, Wave 2 | `PLATFORM_PLAYBOOK.md` §0 = RESOLVED 2026-08-28 |

**Hardcover and Blurb are listing-only.** There is no KDP hardcover wrap and no Blurb template cover in the repo. `markets/kdp-hardcover/*/metadata-hc.txt` tells you to download KDP’s hardcover template and rebuild from `markets/bn-print/<slug>/` 300 DPI panels.

**i18n is sales copy, not a translated book.** `MARKETS/i18n/<lang>/00_README.md`: do **not** set Google Play book-language to Chinese/Hindi/Spanish/French/Hausa/Yorùbá. PDF remains English. Imprint stays Quiet Mind Press.

### 1.3 Range Band — KDP kit is identical × 36, and thinner than Quiet Mind

Every `KDP-Complete-Kit/NN_<stem>/` has exactly four files:

| File | Role |
|---|---|
| `*_interior.pdf` | KDP interior |
| `*_COVER_WRAP.pdf` | KDP wrap (spine + barcode box) |
| `*_COVER_FRONT.pdf` | Mockups / ads / Etsy POD front **only** — never as KDP cover (`00_START_HERE.md`) |
| `listing.txt` | Title, subtitle, HTML, 7 keywords, two BISAC, spine math, **$9.99** |

**Missing versus Quiet Mind (all 36):**

- No `listing_02`–`07` Amazon images. Conversion will be cover-only unless you add interiors later. Quiet Mind `MARKETING.md`: “If you only upload the cover, the book dies” — that warning was written for coloring, but it is a **real Range Band gap** on Amazon.
- No `cover.jpg` derived listing set (front PDF exists).
- No i18n pack.
- No hardcover pack.
- No Blurb pack.
- No BN front/back JPG panels (B&N listings exist as `listing.txt` only in `MARKETS/BN-Press/`; you still need to split the wrap or use B&N’s tool).
- Digital is **$9.99 print-at-home**, not the Quiet Mind $4.99/$6.99 ladder (`MARKETS/DIGITAL-9.99/`).
- B&N **$14.99 × 36**, including **78-page 5×8** (07) and other sub-120 titles. Quiet Mind’s `PLATFORM_DECISIONS.md` would have **held** those thin books. Range Band did not hold them. Note it at upload: $14.99 on 78pp next to a $9.99 Amazon twin will look expensive.

**Trim exceptions (identical rule, three SKUs):** 07 and 25 = **5×8** (KDP has no 4×6). 09 = **8.5×11**. Else **6×9**. Paper **white** all 36. Spine type **off** on 07 (78pp < 79). Title 25 is 79pp — spine ON (`00_START_HERE.md`).

**Dashed QR boxes** on 03, 09, 17 are empty on purpose — paste your own URL later. Do not invent a URL.

### 1.4 Head-to-head SKUs (do not list both into the same ads query)

From `CASHFLOW.md` and `RANKING.md`:

| Range Band | Quiet Mind | Rule |
|---|---|---|
| 13 ADHD Medication & Focus Log | The Dopamine Menu | 13 is dose-as-prescribed + Pomodoro. Dopamine is a restaurant-menu stimulation journal. **Different queries.** |
| 14 Perimenopause Symptom & Mood Chart (107pp) | The Middle Season (160pp) | **Hold 14** or list without ads. Middle is the deeper peri book. |
| 29 Sleep Window & Wind-Down (WASO fields) | The Night Pages (5×8 3 a.m.) | 29 is clinical sleep fields. Night is a pocket 3 a.m. journal. |
| 27 GLP-1 Five-Minute Morning Pages | The 5-Minute Dump | 27 is GLP-1 shot/protein compact. Dump is ADHD micro-journal. |
| — | Quiet Mind Color (10) | Range Band has **zero coloring books**. Do not dump coloring into Range Band series pages. |

### 1.5 Shared parked / not-ready work (both imprints)

- **No EPUB.** Kobo / Apple / StreetLib stay closed.
- **IngramSpark parked** until Bowker ISBNs exist. Never reuse a KDP wrap on Ingram.
- **No live storefront automation.** Preparation is automated; publication is human-gated (`PLATFORM_DECISIONS.md` last bullet).
- Mainland China retail: no $0 indie door. Kindle China shut. Do not set KDP language to Chinese.
- Google Play Books: not Nigeria, not mainland CN. Nigeria Jumia needs NG business + inventory — skip.

---

## 2. Quiet Mind Press — the 18 (ours)

Series to create on KDP (`MARKETING.md`): **Quiet Mind Journals** (8) and **Quiet Mind Color** (10). Do not mix.

Color ladder, printed on every coloring listing (`niche_upgrades.py` `LADDER`):  
First Strokes → Easy Garden → Cozy Corners → Woodland Wonders → Mosaic Mind → Botanical Ink → Tidal Ink → Celestial Atlas → Fractal Dreams → Architectural Visions.

Ads launch four: **dopamine, soft, middle, cozy**.

Digital attractors ($4.99, `make_digital_kits.py` `POOL_499`): **dump, dopamine, cozy, soft, settle**.  
Digital $6.99: the other 12 that are not Middle.  
Digital none: **middle**.

Hardcover entry prices (`EDITIONS_MATRIX.csv`): dump $15.99; settle/parallel/middle/dopamine $14.99; slow/soft + coloring HCs $13.99 if you ignore the hold; night — no HC.

B&N decision (follow `PLATFORM_DECISIONS.md`, not the fact that kits exist for the thin 7): list the **11 ≥120pp**. Hold firststroke, garden, cozy, botanical, celestial, tidal, soft.

### Specs (from `CATALOG.csv`)

| n | slug | Amazon title | Cover word | Pages | Trim | Paper | Series | Difficulty | KDP | Digital (EDITIONS) | BN decision | HC | Blurb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | dump | The 5-Minute Dump: Micro-Journal for People Who Hate Journaling | The 5-Minute Dump | 200 | 5.5×8.5 | cream | Journals | — | 9.99 | **4.99** | LIST (200pp) | 15.99 | no (trim) |
| 02 | parallel | Parallel Lives: A Split-Page Therapy Journal | Parallel Lives | 160 | 7×10 | cream | Journals | — | 9.99 | 6.99 | LIST | 14.99 | no (trim) |
| 03 | night | The Night Pages: An Insomnia Journal for 3 A.M. | The Night Pages | 120 | 5×8 | cream | Journals | — | 9.99 | 6.99 | LIST | **none** | 12.99 |
| 04 | firststroke | First Strokes: Easy Coloring Book for Adult Beginners | First Strokes | 100 | 8.5×11 | white | Color | Beginner | 9.99 | 6.99 | **HOLD** | HOLD coloring HC | no |
| 05 | garden | Easy Garden: Bold and Easy Flower Coloring Book for Adults | Easy Garden | 100 | 8.5×11 | white | Color | Beginner | 9.99 | 6.99 | **HOLD** | HOLD | no |
| 06 | mosaic | Mosaic Mind: Geometric Coloring Book for Adults | Mosaic Mind | 120 | 8.5×11 | white | Color | Intermediate | 9.99 | 6.99 | LIST | HOLD | no |
| 07 | woodland | Woodland Wonders: Forest Animals Coloring Book for Adults | Woodland Wonders | 120 | 8.5×11 | white | Color | Intermediate | 9.99 | 6.99 | LIST | HOLD | no |
| 08 | fractal | Fractal Dreams: Advanced Mathematical Coloring Book | Fractal Dreams | 140 | 8.5×11 | white | Color | Advanced | 9.99 | 6.99 | LIST | HOLD | no |
| 09 | architect | Architectural Visions: Cathedral and Cityscape Coloring Book for Adults | Architectural Visions | 140 | 8.5×11 | white | Color | Advanced | 9.99 | 6.99 | LIST | HOLD | no |
| 10 | settle | Settle: A Somatic Journal for a Wired Nervous System | Settle | 172 | 6×9 | cream | Journals | — | 9.99 | **4.99** | LIST | 14.99 | 13.99 |
| 11 | middle | The Middle Season: Perimenopause Symptom Tracker & Journal | The Middle Season | 160 | 6×9 | **white** | Journals | — | 9.99 | **none** | LIST | 14.99 | 13.99 |
| 12 | dopamine | The Dopamine Menu: An ADHD Journal for Ordering Your Stimulation | The Dopamine Menu | 150 | 6×9 | cream | Journals | — | 9.99 | **4.99** | LIST | 14.99 | 13.99 |
| 13 | slow | The Slow Page: A Slow Living Journal for Four Seasons | The Slow Page | 144 | 6×9 | cream | Journals | — | 9.99 | 6.99 | LIST | 13.99 | 12.99 |
| 14 | soft | The 75 Soft Journal | The 75 Soft Journal | 96 | 6×9 | cream | Journals | — | 9.99 | **4.99** | **HOLD B&N** (96pp) | 13.99 | 11.99 |
| 15 | cozy | Cozy Corners: Cozy Spaces Coloring Book for Adults | Cozy Corners | 104 | 8.5×11 | white | Color | Beginner–Easy | 9.99 | **4.99** | **HOLD B&N** | HOLD HC | no |
| 16 | botanical | Botanical Ink: Fine-Line Floral Coloring Book for Adults | Botanical Ink | 104 | 8.5×11 | white | Color | Fine line | 9.99 | 6.99 | **HOLD B&N** | HOLD | no |
| 17 | celestial | Celestial Atlas: Constellation Coloring Book for Adults | Celestial Atlas | 104 | 8.5×11 | white | Color | Fine line | 9.99 | 6.99 | **HOLD B&N** | HOLD | no |
| 18 | tidal | Tidal Ink: Jellyfish and Deep-Sea Fine-Line Coloring Book for Adults | Tidal Ink | 104 | 8.5×11 | white | Color | Fine line | 9.99 | 6.99 | **HOLD B&N** | HOLD | no |

Upload path: `release3/` for n=01–09, `release4/` for n=10–18. Metadata: `releaseN/<slug>/metadata.txt`.

Interior notes that are not listing-side:

- Dopamine howto: menu is **pages 5–6** (fixed `774b35e`).
- Night keyword 3: `can't sleep notebook` (fixed `774b35e`).
- Settle daily body row uses **`shldr`** as a space-fit abbreviation next to jaw/chest/gut/hands — not a listing typo; leave the interior.
- Dump catalog trim is **5.5×8.5** (`CATALOG.csv`; wrap_h 8.750). Do not enter 5.5×8 in KDP.

Lulu Global (`MARKETS/PRODUCTS.csv`): dump/fractal/architect **$11.99**; mosaic/woodland/parallel/settle/middle **$10.99**; others **$9.99**. Confirm in Lulu’s calculator.

---

## 3. Range Band Press — the 36 (the other line)

Four KDP series (`CASHFLOW.md`): **GLP-1 Tracking (01–09)**, **Wellness Tracking (10–18)**, **GLP-1 Companion (19–27)**, **Wellness Companion (28–36)**.

KDP **$9.99 × 36**. B&N **$14.99 × 36**. Digital PDF **$9.99 × 36**. Lulu Global **$9.99** except **30 PMDD = $11.99** (`MARKETS/PRODUCTS.csv`). Ingram parked.

Upload: `KDP-Complete-Kit/NN_<stem>/listing.txt` + interior + **WRAP**. Author field **Range Band Press**.

Royalty estimates at $9.99 (formula in `SELLING_AND_VALUATION.md`: print ≈ $0.85+$0.012×pages; Amazon 60% − print): catalog one-of-each ≈ **$139.18**. 09 large-trim may print a few cents more. Order proofs of **01 (6×9), 07 (5×8), 09 (8.5×11)** before ads.

| n | Folder | KDP title | Pages | Trim | Series | Wave | Notes |
|---|---|---|---|---|---|---|---|
| 01 | `01_GLP1_Meal_and_Satiety` | GLP-1 Meal & Satiety Journal | 131 | 6×9 | Tracking | **1 ads** | Flagship two-page daily |
| 02 | `02_GLP1_Side_Effect_Diary` | GLP-1 Side Effect Tracker | 92 | 6×9 | Tracking | 2 | Thin at B&N $14.99 |
| 03 | `03_GLP1_Plateau_Breaker` | GLP-1 Plateau Breaker 30-Day Challenge Planner | 107 | 6×9 | Tracking | 3 | Empty QR box |
| 04 | `04_GLP1_Maintenance` | GLP-1 Maintenance Phase Tracker | 85 | 6×9 | Tracking | 4 | Thin |
| 05 | `05_GLP1_Hunger_Craving` | GLP-1 Hunger & Craving Mood Log | 113 | 6×9 | Tracking | **1 ads** | |
| 06 | `06_GLP1_Fitness` | GLP-1 Fitness & Step Companion | 85 | 6×9 | Tracking | 3 | Thin |
| 07 | `07_GLP1_Titration_Pocket` | GLP-1 Titration Log (Pocket 5x8) | 78 | **5×8** | Tracking | 2 | **No spine type.** Legend line fixed `5e31aa5` (was clipping “instructe”) |
| 08 | `08_GLP1_NSV_Gratitude` | Non-Scale Victories Gratitude Journal | 131 | 6×9 | Tracking | 2 | GLP-1 series; title has no “GLP-1” |
| 09 | `09_GLP1_Injection_Calendar` | GLP-1 Injection Sticker Calendar | 98 | **8.5×11** | Tracking | **1 ads** | Empty QR. Only large-trim in the 36 |
| 10 | `10_Sobriety_90` | Sober Curious 90-Day Journal | 113 | 6×9 | Wellness T | **1 ads** | Not 12-step branded |
| 11 | `11_IF_Window_Tracker` | Intermittent Fasting Window Tracker | 107 | 6×9 | Wellness T | 3 | 24-hour bars |
| 12 | `12_Migraine_Weather` | Migraine Weather & Trigger Diary | 97 | 6×9 | Wellness T | **1 ads** | |
| 13 | `13_ADHD_Focus_Log` | ADHD Medication & Focus Log | 113 | 6×9 | Wellness T | 4 | Do not bid vs Dopamine Menu |
| 14 | `14_Perimenopause_Chart` | Perimenopause Symptom & Mood Chart | 107 | 6×9 | Wellness T | 4 | **HOLD vs Middle Season** |
| 15 | `15_FODMAP_Gut_Diary` | Low FODMAP Food & Symptom Diary | 88 | 6×9 | Wellness T | 3 | Thin |
| 16 | `16_Digital_Detox_30` | Digital Detox 30-Day Screen Time Workbook | 96 | 6×9 | Wellness T | 4 | Thin |
| 17 | `17_Postpartum_Recovery` | Postpartum Recovery Planner | 102 | 6×9 | Wellness T | 4 | Empty QR. PT homework, not a program |
| 18 | `18_Autoimmune_Flare` | Autoimmune Flare & Energy Journal | 113 | 6×9 | Wellness T | 3 | |
| 19 | `19_GLP1_Protein_Grocery` | GLP-1 High-Protein Grocery & Meal Prep Planner | 136 | 6×9 | Companion | 2 | Deepest grocery SKU |
| 20 | `20_GLP1_Out_and_About` | GLP-1 Restaurant, Travel & Social Event Log | 85 | 6×9 | Companion | 3 | Thin |
| 21 | `21_GLP1_Archive` | GLP-1 Measurements, Photos & Lab Archive | 85 | 6×9 | Companion | 4 | Utility archive |
| 22 | `22_GLP1_Sleep_Bowel_Water` | GLP-1 Sleep, Bowel & Hydration Companion | 110 | 6×9 | Companion | 2 | |
| 23 | `23_GLP1_Body_Image` | GLP-1 Body Image & Mindset Journal | 110 | 6×9 | Companion | 3 | |
| 24 | `24_GLP1_Weekly_Brief` | GLP-1 Weekly Review & Clinic Brief Binder | 115 | 6×9 | Companion | 2 | |
| 25 | `25_GLP1_Shot_Day_Pocket` | GLP-1 Shot Day 0-48 Hour Pocket Log | 79 | **5×8** | Companion | 2 | Spine ON (79pp) |
| 26 | `26_GLP1_Protein_Kitchen` | GLP-1 Protein Kitchen Recipe & Leftover Log | 98 | 6×9 | Companion | 4 | Not a cookbook |
| 27 | `27_GLP1_Five_Minute` | GLP-1 Five-Minute Morning Pages | 130 | 6×9 | Companion | 3 | Do not bid vs Dump |
| 28 | `28_Anxiety_Panic` | Anxiety & Panic Sensation Log | 110 | 6×9 | Wellness C | 4 | Crowded shelf |
| 29 | `29_Sleep_Window` | Sleep Window & Wind-Down Diary | 104 | 6×9 | Wellness C | 4 | WASO; do not bid vs Night Pages |
| 30 | `30_PMDD_Cycle` | PMDD & Cycle Mood Chart | 188 | 6×9 | Wellness C | **1 ads** | Deepest kit book. Lulu **$11.99** |
| 31 | `31_Glucose_Meal` | Glucose & Meal Timing Log | 110 | 6×9 | Wellness C | 4 | Copy sheets, not a dosing protocol |
| 32 | `32_Chronic_Pain` | Chronic Pain Body Map & Flare Diary | 92 | 6×9 | Wellness C | 4 | Thin at B&N |
| 33 | `33_Grief_Loss` | Grief & Loss 90-Day Journal | 117 | 6×9 | Wellness C | 4 | No stages, no silver lining |
| 34 | `34_Habit_OS` | 12-Week Habit Operating System | 117 | 6×9 | Wellness C | 4 | Crowded habit shelf |
| 35 | `35_Burnout_Energy` | Burnout & Energy Budget Journal | 104 | 6×9 | Wellness C | 4 | |
| 36 | `36_Bladder_Pelvic` | Bladder & Pelvic Symptom Diary | 88 | 6×9 | Wellness C | 4 | Clinic 3-day voiding format. Thin |

Full titles, subtitles, keywords, BISAC: `KDP-Complete-Kit/METADATA.csv` and each `listing.txt`.

---

## 4. Ranked least → greatest (54 = sell first)

Rank is **sell sequence**, not craft contempt. It folds: (a) owner ads/wave designation, (b) page depth, (c) niche intent, (d) uniqueness vs a sibling SKU, (e) kit completeness for the channel you are about to open, (f) B&N thin-book risk, (g) `RANKING.md` 2026-08-28 scores where they still match the trees.

**1 = sell last / hold. 54 = sell first / ads.**

### 1 — Range Band 14 · Perimenopause Symptom & Mood Chart
**Hold.** 107pp 6×9 vs Quiet Mind Middle Season 160pp. `CASHFLOW.md` and `RANKING.md` (old 32/50, last place) agree. Files: `14_Perimenopause_Chart/` complete 4-file kit. Do not ads. If you list at all, do it after Middle Season has reviews, different keywords (hot flash tally / sleep wheel — already in `METADATA.csv`).

### 2 — Range Band 21 · Measurements, Photos & Lab Archive
85pp utility binder. `RANKING.md` 33/50. Few repeat opens. Wave 4. B&N $14.99 on 85pp is a bad look (`PLATFORM_DECISIONS.md` logic). KDP $9.99 only until data.

### 3 — Range Band 20 · Restaurant, Travel & Social Event Log
85pp, narrow use. Wave 3. Same B&N thin-book problem. Complete 4-file kit, no listing images.

### 4 — Range Band 04 · Maintenance Phase Tracker
85pp range-band log. Smart idea, short book. Wave 4. KDP $9.99.

### 5 — Range Band 06 · Fitness & Step Companion
85pp. Wave 3. Ordinary weekly log (`RANKING.md` 34/50).

### 6 — Range Band 07 · Titration Log (Pocket 5×8)
78pp, **no spine type**, 5×8. Correct “dose as prescribed” (`CASHFLOW.md` G#13 fix history). Legend overflow fixed `5e31aa5`. Wave 2 companion, not ads. B&N $14.99 on 78pp is the worst floor mismatch in either catalog.

### 7 — Range Band 25 · Shot Day 0–48h Pocket
79pp 5×8, spine ON. Clever window. Wave 2. Same B&N thin risk.

### 8 — Quiet Mind 05 · Easy Garden
100pp 8.5×11 Beginner. `release3/garden/` **full 10-file kit**. Crowded flower-coloring shelf (`RANKING.md` 33/50). **HOLD B&N.** Digital $6.99. Ladder: too hard → First Strokes; too easy → Cozy. Do not ads.

### 9 — Range Band 36 · Bladder & Pelvic Symptom Diary
88pp clinic 3-day voiding. Underserved but short. Wave 4. No listing images.

### 10 — Range Band 15 · Low FODMAP Food & Symptom Diary
88pp. Reintroduction cards are the differentiator (`RANKING.md` 36/50). Wave 3. Thin at B&N.

### 11 — Range Band 02 · Side Effect Tracker
92pp. Wave 2 also-bought from 01. Severity grids + clinic prep. B&N thin.

### 12 — Range Band 32 · Chronic Pain Body Map
92pp, 72 flare maps. Wave 4. Body maps are the product. B&N thin.

### 13 — Quiet Mind 04 · First Strokes
100pp Beginner, 37 designs of 3–5 shapes (`CATALOG.csv` subtitle). Full 10-file kit. Real senior/rehab query (`large print coloring book for seniors` keyword 2) but simplest interior by design. **HOLD B&N.** Digital $6.99.

### 14 — Range Band 16 · Digital Detox 30-Day
96pp. Wave 4. Screen-time bars. B&N thin.

### 15 — Quiet Mind 06 · Mosaic Mind
120pp Intermediate. Full kit. Geometric shelf is packed (`RANKING.md` 34/50). B&N LIST (≥120). Digital $6.99. No Blurb (8.5×11).

### 16 — Range Band 26 · Protein Kitchen Recipe & Leftover Log
98pp, not a cookbook. Wave 4. 60 blank cards.

### 17 — Range Band 13 · ADHD Medication & Focus Log
113pp dose-as-Rx + Pomodoro. **Do not bid vs Dopamine Menu** (`CASHFLOW.md`). Wave 4. Complete kit, no listing images.

### 18 — Range Band 28 · Anxiety & Panic Sensation Log
110pp, 90 unique prompts. Crowded anxiety shelf. Wave 4.

### 19 — Range Band 34 · 12-Week Habit Operating System
117pp contracts / minima. Habit shelf packed. Wave 4.

### 20 — Range Band 31 · Glucose & Meal Timing Log
110pp meter/CGM **copy sheets**, not a dosing protocol (`listing.txt` + `METADATA.csv` keyword “not a dosing protocol log”). Wave 4.

### 21 — Range Band 29 · Sleep Window & Wind-Down Diary
104pp WASO / latency / rise time. **Do not bid vs Night Pages.** Wave 4.

### 22 — Quiet Mind 09 · Architectural Visions
140pp Advanced, 67 designs. Full 10-file kit. Medium demand (`RANKING.md` 35/50). B&N LIST. Digital $6.99. HC pack exists on disk — **do not list coloring HC** (`PLATFORM_DECISIONS.md`).

### 23 — Range Band 17 · Postpartum Recovery Planner
102pp, PT homework only, empty QR. Wave 4. Not an exercise program.

### 24 — Quiet Mind 08 · Fractal Dreams
140pp Advanced, real Sierpinski/Julia/Koch (`CATALOG.csv` subtitle). Smallest coloring audience, boldest art. B&N LIST. Digital $6.99.

### 25 — Quiet Mind 02 · Parallel Lives
160pp 7×10 split-page. Unique mechanic, niche taste. Full kit. Digital $6.99. No Blurb (7×10). HC $14.99 if Wave 2 journals.

### 26 — Range Band 11 · Intermittent Fasting Window Tracker
107pp, 24-hour bars. Wave 3. Strong interior idea, crowded IF query.

### 27 — Range Band 23 · Body Image & Mindset
110pp, 90 unique prompts. Wave 3. Needed GLP-1 companion, not a flagship.

### 28 — Range Band 35 · Burnout & Energy Budget
104pp meeting-cost / resentment. Wave 4. Fresh frame, knowledge-work query.

### 29 — Range Band 03 · Plateau Breaker 30-Day
107pp + encore cycle, empty QR. Wave 3.

### 30 — Range Band 22 · Sleep, Bowel & Hydration
110pp Bristol + water tally. Wave 2 also-bought.

### 31 — Quiet Mind 16 · Botanical Ink
104pp fine-line, real phyllotaxis (`CATALOG.csv` subtitle). Full 10-file kit (listing interiors matter here). **HOLD B&N.** Digital $6.99. Etsy-adjacent printable art (`PLATFORM_DECISIONS.md` Etsy first color: cozy + botanical).

### 32 — Quiet Mind 03 · Night Pages
120pp 5×8 cream. Full kit. Pocket 3 a.m. (`metadata.txt`). **No hardcover.** Blurb $12.99. Digital $6.99. Insomnia shelf crowded. Pair with Settle (`niche_upgrades.py` `JOURNAL_STACKS`).

### 33 — Quiet Mind 13 · The Slow Page
144pp four season gates. Full kit. Blurb $12.99. Digital $6.99. Gift with Cozy (`JOURNAL_STACKS`). Softer demand. B&N LIST.

### 34 — Range Band 08 · Non-Scale Victories Gratitude
131pp. Wave 2. Warm daily. GLP-1 tracking series without GLP-1 in the title — keep the stem footer.

### 35 — Range Band 10 · Sober Curious 90-Day
113pp, gender-neutral, not AA. **Wave 1 ads.** Complete kit, no listing images — add interior JPGs before spending ad dollars if you can.

### 36 — Range Band 18 · Autoimmune Flare & Energy
113pp spoon counts. Wave 3.

### 37 — Quiet Mind 18 · Tidal Ink
104pp fine-line, real logarithmic spirals. Full 10-file kit. **HOLD B&N.** Digital $6.99. Unique art (`RANKING.md` 38/50).

### 38 — Quiet Mind 07 · Woodland Wonders
120pp Intermediate cottagecore. Full kit. B&N LIST. Digital $6.99. Pinterest.

### 39 — Range Band 05 · Hunger & Craving Mood Log
113pp four-quadrant. **Wave 1 ads.**

### 40 — Range Band 12 · Migraine Weather & Trigger Diary
97pp barometric + pain map. **Wave 1 ads.** B&N thin — KDP first.

### 41 — Range Band 19 · High-Protein Grocery & Meal Prep
136pp. Wave 2. Deepest practical companion (`RANKING.md` 38/50).

### 42 — Quiet Mind 01 · The 5-Minute Dump
200pp 5.5×8.5 cream. Full 10-file kit. Digital **$4.99 attractor**. B&N LIST. HC $15.99 (Wave 2 journals). Broad “hate journaling” hook (`CATALOG.csv`). Do not ads in week 1 (`MARKETING.md` staging: week 2). Pair with Dopamine.

### 43 — Range Band 09 · Injection Sticker Calendar
98pp **8.5×11**. **Wave 1 ads.** Only sticker-calendar format in either catalog. Empty QR. Proof this trim. Digital $9.99. B&N $14.99 on 98pp is soft — KDP first.

### 44 — Quiet Mind 15 · Cozy Corners
104pp Beginner–Easy, 49 spaces. Full 10-file kit. Digital **$4.99 attractor**. **HOLD B&N.** **Wave 1 ads** (`MARKETING.md`). Pinterest / cottagecore. Etsy first-color with botanical.

### 45 — Quiet Mind 14 · The 75 Soft Journal
96pp, Day 76 in the book (`CATALOG.csv` subtitle). Digital **$4.99**. **HOLD B&N** (96pp). **Wave 1 ads.** Do not bid 75 Hard. Launch January (`MARKETING.md`). Blurb $11.99.

### 46 — Quiet Mind 17 · Celestial Atlas
104pp, real star positions (`CATALOG.csv`). Full 10-file kit. **HOLD B&N.** Digital $6.99. Fine-line + astronomy query (`RANKING.md` 41/50).

### 47 — Range Band 30 · PMDD & Cycle Mood Chart
188pp, 6 cycles. **Wave 1 ads.** Deepest Range Band interior. Lulu Global **$11.99**. KDP $9.99 still prints a royalty (`SELLING_AND_VALUATION.md` est. $2.89). No listing images — interiors would help conversion on a chart book.

### 48 — Range Band 27 · GLP-1 Five-Minute Morning Pages
130pp compact dailies. Wave 3. **Do not bid vs The 5-Minute Dump** (`CASHFLOW.md`). GLP-1 shot/protein, not an ADHD dump. 4-file kit only.

### 49 — Range Band 33 · Grief & Loss 90-Day Journal
117pp, 90 unique prompts, no stages, no silver lining (`METADATA.csv` keywords). Wave 4. Complete 4-file kit, no listing images.

### 50 — Range Band 24 · Weekly Review & Clinic Brief Binder
115pp, 52 weeks + one-page clinician briefs. Wave 2. High-intent clinic query. `listing.txt` in `24_GLP1_Weekly_Brief/`.

### 51 — Quiet Mind 10 · Settle
172pp somatic, no streaks, tracking-only language (`release4/settle/metadata.txt`). Full 10-file kit. Digital **$4.99 attractor**. B&N LIST. Blurb $13.99. HC $14.99 Wave 2. Pair with Night or Middle (`niche_upgrades.py` `JOURNAL_STACKS`). Interior `shldr` stays.

### 52 — Range Band 01 · GLP-1 Meal & Satiety Journal
131pp two-page dailies. **Wave 1 ads. Range Band flagship.** Proof the 6×9 on this SKU (`SELLING_AND_VALUATION.md`). Digital $9.99 (Range Band scheme). `01_GLP1_Meal_and_Satiety/`.

### 53 — Quiet Mind 12 · The Dopamine Menu
150pp five courses + daily order ticket (`CATALOG.csv` n=12). Full 10-file kit. Digital **$4.99 attractor**. **Wave 1 ads.** TikTok “dopamine menu” (`MARKETING.md`). Pair with Dump. Do not let Range Band 13 ride this query. Blurb $13.99. HC $14.99 Wave 2. `release4/dopamine/`.

### 54 — Quiet Mind 11 · The Middle Season
160pp white grids, clinic file, **print-only digital** (`EDITIONS_MATRIX.csv`: `no digital (print-only flagship lane)`). Full 10-file **print** kit. **Wave 1 ads.** Deepest peri tracker. Beats Range Band 14 on depth. Blurb $13.99. HC $14.99. B&N LIST. Do not upload `listing_06_callout.jpg` as a PDF price. Do not create a Gumroad/Payhip PDF. `release4/middle/`.

**This hour, upload only Wave 1:**

- Quiet Mind KDP: Dopamine Menu → 75 Soft → The Middle Season → Cozy Corners (`release4/`).
- Range Band KDP: 01 Meal → 09 Calendar → 05 Craving → 30 PMDD → 10 Sober → 12 Migraine (`KDP-Complete-Kit/`).

---

## 5. Paste map (so the next AI does not open the wrong folder)

### Quiet Mind, one title

```
KDP print $9.99
  interior:  release{3|4}/<slug>/<slug>_interior.pdf
  wrap:      release{3|4}/<slug>/<slug>_cover_wrap.pdf
  copy:      release{3|4}/<slug>/metadata.txt
  images:    cover.jpg + listing_02..07  (skip 06 on digital)

B&N $14.99 (if ≥120pp per PLATFORM_DECISIONS)
  interior:  same PDF
  covers:    markets/bn-print/<slug>/bn_front.jpg + bn_back.jpg
  copy:      markets/bn-print/<slug>/metadata-bn.txt   (Price line is $14.99)

Digital PDF (not Middle)
  file:      markets/digital/<slug>/<slug>_digital.pdf   (gitignored; regenerate: python3 make_digital_kits.py)
  copy:      markets/digital/<slug>/metadata-digital.txt  ($4.99 or $6.99)
  images:    cover + 02-05 + 07 only

i18n (not Middle)
  MARKETS/i18n/{zh,hi,es,fr,ha,yo}/NN_<slug>.txt
  PDF stays English
```

### Range Band, one title

```
KDP print $9.99
  interior:  KDP-Complete-Kit/NN_<stem>/NN_<stem>_interior.pdf
  wrap:      KDP-Complete-Kit/NN_<stem>/NN_<stem>_COVER_WRAP.pdf
  copy:      KDP-Complete-Kit/NN_<stem>/listing.txt
  images:    NONE in kit — cover wrap/front only. Do not upload COVER_FRONT as the cover.

B&N $14.99
  copy:      MARKETS/BN-Press/NN_<stem>/listing.txt
  PDFs:      same interiors; split wrap or B&N tool (no bn_front.jpg in this line)

Digital $9.99
  MARKETS/DIGITAL-9.99/NN_<stem>/
```

### Series pages to create before the second title goes live

- Quiet Mind Journals  
- Quiet Mind Color  
- GLP-1 Tracking Series  
- GLP-1 Companion Series  
- Wellness Tracking Series  
- Wellness Companion Series  

Six series. Zero coloring SKUs in a Range Band series. Zero GLP-1 SKUs in a Quiet Mind series.

---

## 6. Conflicts the next AI must not “fix” by blending

1. **Quiet Mind digital prices agree.** `MARKETS/PRODUCTS.csv` + `markets/digital/` + `EDITIONS_MATRIX.csv` + `PLATFORM_DECISIONS.md` = $4.99/$6.99, Middle print-only. Do **not** flatten Range Band digital to that ladder (RB stays **$9.99 × 36**).
2. **B&N 11 vs 18.** Kits exist for all 18 Quiet Mind titles. **List 11.** Hold the thin 7 (stamped HOLD on disk).
3. **Coloring hardcovers.** `metadata-hc.txt` exists and is stamped HOLD. **Do not list** until a coloring paperback clearly outsells peers.
4. **Expanded Distribution.** **OFF** everywhere that used to disagree (`PLATFORM_DECISIONS.md`, `MARKETING.md`, checklists, playbooks).
5. **Digital approval.** Wave 2. `PLATFORM_PLAYBOOK.md` §0 is RESOLVED.
6. **Range Band B&N on thin books.** Allowed by their pack; economically ugly. Prefer KDP-only on <120pp until data. Do **not** force Quiet Mind thick-only onto Range Band unless the owner says so.
7. **Middle digital.** `MARKETS/by-title/11_middle/DIGITAL/PRINT_ONLY.txt` exists. There is no PDF. Do not invent one.
8. **Branches.** Quiet Mind commits only to `ADHD-Journals`. Range Band commits only to `Range-Band`. `main` is a pointer. Do not merge.
9. **Range Band 14 ads.** `listing.txt` + `CASHFLOW.md` = **ADS HOLD** vs Quiet Mind The Middle Season. KDP $9.99 listing still allowed.

---

## 7. What “thought ahead” already covers (use it; don’t rebuild it)

- 60% KDP floor at $9.99 on all 54 paperbacks.  
- B&N $14.99 separate editions.  
- Lulu 2× print (Quiet Mind dump/fractal/architect $11.99; Range Band 30 $11.99).  
- Ingram parked, not paid.  
- No EPUB, so no Kobo/Apple yet.  
- i18n listings for Quiet Mind digital stores, PDF English.  
- Medical copy pre-stripped (tracking/management; dose-as-Rx; no manufacturer in titles).  
- Color ladder and journal stacks on Quiet Mind listings.  
- Also-bought sibling bullets on every Range Band `listing.txt`.  
- 7 Amazon images on every Quiet Mind title.  
- Wave lists so ads money is not sprayed across 54 SKUs.  
- Dual-imprint query firewall (`CASHFLOW.md`).  

**Still not ready (do not tell a client these exist as uploadable products):** KDP hardcover wraps, Blurb covers, Ingram wraps, EPUB, Quiet Mind listing images on Range Band, filled QR URLs, Bowker ISBNs, Nigeria/mainland-China storefronts, Whop.

---

## 8. First actions (this week, no improvisation)

1. Create the six series pages.  
2. Quiet Mind: upload Dopamine, 75 Soft, Middle Season, Cozy Corners from `release4/` (+ Cozy `release4/cozy/`). $9.99. Bleed OFF. Paste `metadata.txt` Amazon title. Seven images in order. ED **off**.  
3. Range Band: upload 01, 09, 05, 30, 10, 12 from `KDP-Complete-Kit/`. $9.99. WRAP not FRONT. Proof 01, 07, 09 before ads.  
4. Do not open B&N, Lulu, digital, or Ingram until Wave 1 has clean data (`PLATFORM_PLAYBOOK.md` Wave 1).  
5. Do not list Range Band 14. Do not PDF Middle Season. Do not ads-blast the other 44 SKUs.

Sources for every number in this file: `CATALOG.csv`, `EDITIONS_MATRIX.csv`, `MARKETS/PRODUCTS.csv` (both trees), `METADATA.csv`, `PLATFORM_DECISIONS.md`, `MARKETING.md`, `CASHFLOW.md`, `SELLING_AND_VALUATION.md`, `make_digital_kits.py`, git `3feca69` / Range-Band (14 ads-hold). If a platform’s live calculator disagrees, the platform wins.
