# Quiet Mind Press — $0-to-list, one min per store

Verified **28 August 2026**. Branch **`ADHD-Journals`**. Do not merge with `Range-Band`.

Imprint: **Quiet Mind Press**. 18 paperbacks (8 journals + 10 coloring). Interiors stay **English**. Listings exist in English plus **简体中文, हिन्दी, español, français, Hausa, Yorùbá**.

No money before a sale. Cut-on-sale is fine. Monthly, listing fees, ISBN packs, and vanity are out.

KDP is **$9.99 on every title** (catalog-wide cap). Other stores get **that title’s own floor**, not one shared $14.99 catalog except B&N, which *is* a catalog floor.

| Pack | Price rule | Use on |
|---|---|---|
| `release3/` + `release4/` | existing US list | Amazon KDP paperback |
| `MARKETS/BN-Press/` | **max(KDP, $14.99)** | B&N Press (catalog floor 22 Apr 2026) |
| `MARKETS/Lulu-Global/` | **max(KDP, round_99(2 × Lulu print))** | Lulu print Global Dist. |
| `MARKETS/DIGITAL/` | **$4.99 attractors / $6.99 rest / Middle print-only** | PDF: Google Play, Gumroad, Payhip, Ko-fi, itch.io… (Wave 2) |
| `MARKETS/Ingram-PARKED/` | formula min, **do not upload** | After Bowker ISBNs |
| `MARKETS/by-title/` | all of the above | One product, every floor |
| `MARKETS/i18n/` | same PDFs, translated copy | zh / hi / es / fr / ha / yo |
| `MARKETS/PRODUCTS.csv` | spreadsheet | |

PDFs are **not copied**. Each market folder points at `release3/` or `release4/`. Upload those interiors + wraps.

---

## Go — $0 until a copy sells

### Print

1. **Amazon KDP paperback** — do this first. `release*/` + `metadata.txt`. Bleed OFF. Matte. Expanded Distribution **OFF**. Author: Quiet Mind Press. Create series **Quiet Mind Journals** and **Quiet Mind Color**. Do not mix SKUs.
   - Turn **every** KDP paperback marketplace ON: US, UK, DE, FR, ES, IT, NL, PL, SE, JP, CA, AU (and any new ones on the pricing page).
   - 60% floors (confirm live): US **$9.99** · UK **£7.99** · euro **€9.99** · CA/AU **13.99** · JP **¥1,000** · PL **40 zł** · SE **110 kr**.
   - **No KDP paperback POD in India, Nigeria, Mexico, or mainland China.** Readers there cannot order our paperback from a local Amazon print plant. English paperbacks still sell on .com / .co.uk / .fr / .es with international shipping where Amazon allows it.
   - Do **not** enroll Kindle Select if Google Play PDFs are live.

2. **B&N Press print** — `MARKETS/BN-Press/`. Floor **$14.99**. **LIST the 11 titles ≥120pp. HOLD the 7 thin** (firststroke, garden, cozy, botanical, celestial, tidal, soft). Free B&N ISBN. Never paste that price into KDP.

3. **Lulu print Global Dist.** — `MARKETS/Lulu-Global/`. List ≥ 2× print, never under the KDP list. Skip Lulu *ebook* Global Dist ($4.99). Lulu’s own bookstore can use the KDP price.

4. **Pothi.com store (India print)** — $0 on **Pothi’s own store**. Skip paid Flipkart/Amazon.in “extended distribution.” Confirm their calculator; 8.5×11 coloring may cost more. English interiors.

### Digital PDF (same files, `MARKETS/DIGITAL/`)

Google Play, Gumroad, Payhip Free, Ko-fi Shop, itch.io (type: book), Lemon Squeezy. **Skip Whop** (`PLATFORM_DECISIONS.md`). Prices: **$4.99** dump/dopamine/cozy/soft/settle; **$6.99** the other 12; **Middle Season print-only**. Description must say **print-at-home PDF of the paperback**, not a reflowable ebook. Wave 2 only.

**Google Play Books countries (official, paid ebooks):** includes **India, Mexico, Spain, France, Hong Kong, Taiwan, Singapore, Malaysia, Brazil, South Africa, UAE…** Does **not** include **Nigeria** or **mainland China**. Turn on every country Google offers.

Paste **`MARKETS/i18n/`** copy on Gumroad / Payhip / Ko-fi / itch.io (those pages are yours). Keep Google Play’s book language **English** (the PDF is English). Do not clone three Google Play SKUs of the same file.

---

## Chinese, Hindi, Spanish, French, Nigeria

| Audience | $0 door that actually works | Listing language | What does not work |
|---|---|---|---|
| **Spanish** | KDP print **Amazon.es** (and .com shipping). Google Play **Spain + Mexico + LATAM** in Google’s list. Gumroad/Payhip. | `i18n/es/` | KDP has **no** Mexico paperback plant |
| **French** | KDP print **Amazon.fr** (+ .ca readers via CA marketplace). Google Play France. Gumroad/Payhip. Kobo/Fnac = EPUB, parked | `i18n/fr/` | Fnac shelf is Kobo/aggregator, not a PDF upload |
| **Hindi / India** | Google Play **India**. Gumroad/Payhip. Pothi store print. Amazon.in **Kindle** parked until EPUB | `i18n/hi/` | KDP **paperback not on Amazon.in**. Notion Press packages = pay. Pothi Flipkart add-on = pay |
| **Chinese** | Google Play **HK, TW, SG, MY**. Gumroad/Payhip (diaspora + cards). itch.io | `i18n/zh/` | **Mainland PRC: no $0 self-pub retail door.** Kindle China store closed. Google Play blocked. JD/Dangdang/WeChat 读书 need a Chinese publisher or a paid aggregator (PublishDrive monthly = no) |
| **Nigeria** | Gumroad, Payhip, Ko-fi, itch.io (card/PayPal). English KDP paperbacks where Amazon will ship. | `i18n/ha/` Hausa · `i18n/yo/` Yorùbá | Google Play Books **not** in Nigeria. Jumia wants a Nigerian business + stock. No KDP NG print plant. Konga monthly = no |

Nigeria’s two main indigenous languages are **Hausa** and **Yorùbá** (English is already the book). Listings are translated. Interiors stay English — coloring books do not need words; journals are English tracking pages.

---

## Parked

| Platform | Why | Reopen |
|---|---|---|
| Apple Books / Kobo / Nook ebook | EPUB. $0, 70% | After EPUB |
| KDP Kindle | PDF journals/coloring look bad; Select fights Google Play | After EPUB, never Select if Play is live |
| IngramSpark / Bookshop.org / Libby | Bowker ISBN is money | After you buy ISBNs |
| Draft2Digital | **$20** new + **$12/yr** under $100 | Never on this budget |
| StreetLib Pro / PublishDrive | monthly or $99/yr | Never |
| Notion Press / Pothi extended | pay to reach Flipkart | Never |
| Jumia / Konga | NG business + inventory or monthly | Never |

---

## Order

Week 1 — KDP ads-four: Dopamine Menu, 75 Soft, Middle Season, Cozy Corners. Proof trims (Night 5×8, Dump 5.5×8.5, Settle 6×9, Parallel 7×10, one 8.5×11 coloring).

Week 2–3 — rest of KDP 18. All KDP paperback marketplaces ON. Expanded Dist **OFF**.

Week 4 — Google Play PDFs (Wave titles first). Enable India, MX, ES, FR, HK, TW. Then **one** checkout: Payhip or Gumroad. Add es/fr/zh/hi/ha/yo text on that checkout.

Week 5 — B&N Press: the 11 thick titles only, at $14.99.

Week 6 — Lulu Global. Optional: Pothi store, itch.io, Ko-fi.

Never: Quiet Mind ads on Range Band queries (GLP-1, Ozempic). Never merge branches. Never $14.99 on KDP because B&N said so.

---

## Blacklist

Draft2Digital · Etsy $0.20 listing · TPT $29 · Stan Store / Shopify monthly · Lulu ebook Global $4.99 · vanity · PublishDrive China as a paid door · putting B&N prices on Amazon
