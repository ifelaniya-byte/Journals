# Range Band Press — one minimum per title, per store

Verified **28 August 2026**. Zero monthly fees. Zero setup fees. Platforms that charge before a sale stay parked.

Imprint: **Range Band Press**. PDFs are the same book. **List price is not.** Each of the 36 titles has its own listing at **that store's print minimum**. There is no shared $14.99 catalog except B&N, which *is* a catalog-wide floor.

| Pack | What the price is | Use on |
|---|---|---|
| `KDP-Complete-Kit/` | **$9.99** every title | Amazon KDP paperback (60% royalty) |
| `MARKETS/BN-Press/` | **$14.99** every title | Barnes & Noble Press (hard floor since 22 Apr 2026) |
| `MARKETS/Lulu-Global/` | **per title** — `round_99(max(2 × Lulu print, 9.99))` | Lulu print Global Distribution |
| `MARKETS/DIGITAL-9.99/` | **$9.99** every title | Print-at-home PDF (Google Play, Gumroad, Payhip) |
| `MARKETS/Ingram-PARKED/` | **per title** formula min — **do not upload** | IngramSpark after you buy Bowker ISBNs |
| `MARKETS/by-title/` | all of the above, one folder per book | Look up *this* title's min on *this* store |
| `MARKETS/PRODUCTS.csv` | 36 rows × every channel price | Spreadsheet |
| `MARKETS/FLOORS.csv` | channel rules | Why each store is go / parked |

Covers do not print a dollar amount. Never paste a B&N $14.99 listing into KDP. Never paste a $9.99 print listing into B&N Press.

The old folder `MARKETS/FLOOR-14.99/` was the shared $14.99 pack. It is now **`BN-Press`**.

---

## How to pick a price for one book

Open `MARKETS/by-title/NN_…/00_VERSIONS.md`. That page is the product. Each subfolder (`KDP/`, `BN/`, `LULU-GLOBAL/`, …) is that product's listing at that store's floor.

Or open `MARKETS/PRODUCTS.csv`.

Lulu Global is the one that actually *moves* with page count. On this catalog, **30 PMDD (188 pages) lists at $11.99**; every other title's 2×-print estimate still rounds to **$9.99**. Confirm print cost in Lulu's calculator before you hit publish — the listing is an estimate.

Ingram's formula min also lands at **$9.99** for every title here (print ÷ 0.43125, then house floor). Still **parked** until ISBNs exist.

---

## Go list — no money until a copy sells

### 1. Amazon KDP print — do this first

[kdp.amazon.com](https://kdp.amazon.com) · pack **`KDP-Complete-Kit/`** · **$9.99**

- Paperback · bleed OFF · B&W · white paper
- Interior PDF + wrap PDF from each numbered folder
- Author: Range Band Press
- Turn **Expanded Distribution** ON (extra 40% − print; no extra fee)
- Other KDP storefronts: match their 60% floors (usually UK £7.99, euro €9.99) — confirm on the pricing page
- Do **not** enroll a Kindle of these journals in KDP Select if you also sell the PDF on Google Play (Select is ebook exclusivity)

No setup fee. No monthly fee. Amazon takes its cut when it sells.

### 2. Barnes & Noble Press print — $14.99, every title

[press.barnesandnoble.com](https://press.barnesandnoble.com) · pack **`MARKETS/BN-Press/`** · **$14.99**

B&N Press **will not create a paperback listing under $14.99** as of **22 April 2026**. Existing cheaper titles were pulled starting 14 May 2026. Official: [B&N Press pricing](https://help-press.barnesandnoble.com/hc/en-us/articles/5358788362907-Print-Book-Pricing-and-Printing-Costs). Reported: [Jane Friedman, 15 Apr 2026](https://janefriedman.com/barnes-noble-press-sets-minimum-paperback-price-of-14-99-among-other-new-guidelines/).

This is a **catalog floor**, not a formula. Title 07 (78 pages) and title 30 (188 pages) both list at $14.99 on B&N because the form refuses anything else.

- Free account. Free B&N-only ISBN. No monthly fee.
- Print royalty ~**55% of list − print cost** (confirm live)
- Account cap ~100 live titles; we have 36
- If their wizard rejects the KDP wrap, download **their** cover template and place `*_COVER_FRONT.pdf` on the front panel. Do not invent a new spine formula
- **Never** upload the $14.99 listing to KDP

### 3. Lulu print Global Distribution — per-title 2× print

[lulu.com](https://www.lulu.com) · pack **`MARKETS/Lulu-Global/`**

Official rule: list price must be **at least twice print cost** for print Global Dist. That number is different per book. We round up to x.99 and never go under $9.99.

- Print setup: **$0**. No monthly.
- Skip Lulu **ebook** Global Dist ($4.99 review fee — that is upfront money)
- Lulu's **own bookstore** can stay $9.99 — use the KDP kit PDFs + the `LULU-STORE` listing under `by-title/`
- Confirm print cost in Lulu's calculator. If they quote higher than our estimate, raise that title to `round_99(2 × their number)`
- B&N Press already covers the B&N shelf without Lulu. Lulu Global is extra reach (Ingram-fed stores, etc.), not a substitute for B&N Press

### 4. Google Play Books — PDF, $9.99

[play.google.com/books/publish](https://play.google.com/books/publish) · pack **`MARKETS/DIGITAL-9.99/`**

- Partner Center is free. ~**70%** of list, no delivery fee. Price band about $0.05–$200. [Prices](https://support.google.com/books/partner/answer/3238849) · [70% split](https://support.google.com/books/partner/answer/9331459)
- Upload `*_printathome.pdf` + `*_cover.jpg`
- Description must say: **print-at-home PDF of the paperback**, not a reflowable ebook
- Google can assign a free identifier; you do not need to buy an ISBN

### 5. Gumroad — PDF, $9.99

[gumroad.com](https://gumroad.com) · same digital pack

- No monthly fee. Direct sales **10% + $0.50**. Discover marketplace is 30% — leave Discover off until you want it
- Same PDF + JPG. Author Range Band Press

### 6. Payhip Free — PDF, $9.99

[payhip.com](https://payhip.com) · same digital pack

- Free plan: **$0/month**, ~**5%** + Stripe/PayPal processing
- Do not upgrade to $29/$99 plans. We have no monthly budget

---

## Parked — costs money before a sale, or needs a file we do not have

| Platform | Why parked | When to reopen |
|---|---|---|
| **Draft2Digital** | New accounts: **$20 activation** (Apr 2026) + **$12/year** if you earn under $100. [ALLi](https://selfpublishingadvice.org/what-the-draft2digital-fee-changes-mean-for-you-in-2026/) | Never, on this budget |
| **IngramSpark** | Setup fee is gone (Feb 2026) but a **Bowker ISBN is $125 / $295 per 10**. That is upfront. Market access fee ~1.875% of list on sales. Listings live in `Ingram-PARKED/` — formula min, not $14.99 | After you buy ISBNs. Rebuild the wrap in Ingram's template. Never reuse the KDP wrap blindly |
| **Lulu ebook Global Dist.** | **$4.99** per title review | Use Google Play instead |
| **PublishDrive / StreetLib Pro** | Monthly subscription | No monthly budget |
| **Apple Books** | Wants **EPUB**, not PDF. Free Apple ISBN exists, still need EPUB | After a fixed-layout EPUB exists |
| **Kobo Writing Life** | Free, but EPUB. 70% at $2.99+ | After EPUB |
| **Blurb / vanity / “marketing packages”** | Upfront packages / high unit print, not a catalog floor we can match for free | Never |

IngramSpark’s old **$49 setup fee** is dead. Guides that still quote it are stale. The live cost for *us* is the ISBN, which we will not pay until you say so.

---

## What you upload, per store

| Store | Interior | Cover | listing.txt from | Price |
|---|---|---|---|---|
| KDP | `*_interior.pdf` | `*_COVER_WRAP.pdf` | `KDP-Complete-Kit/` | $9.99 |
| B&N Press | same PDF | wrap, or their template + front | `BN-Press/` | $14.99 |
| Lulu Global Dist. | same PDF | wrap / their template + front | `Lulu-Global/` | that title's cell in `PRODUCTS.csv` |
| Lulu Bookstore | same PDF | front PDF | `by-title/…/LULU-STORE/` | $9.99 |
| Google Play | `*_printathome.pdf` | `*_cover.jpg` | `DIGITAL-9.99/` | $9.99 |
| Gumroad / Payhip | same PDF | same JPG | `DIGITAL-9.99/` | $9.99 |
| IngramSpark | same interior | **Ingram wrap**, not KDP wrap | `Ingram-PARKED/` | parked |

Author field everywhere: **Range Band Press**.

---

## Order of operations (stranger-proof)

Week 1 — Amazon only. Proof trims **01, 07, 09**. Publish Wave 1 at $9.99 (01, 09, 05, 30, 10, 12). See `CASHFLOW.md`.

Week 2 — Rest of KDP 36 at $9.99. Expanded Distribution ON.

Week 3 — Google Play: upload the six Wave 1 PDFs. Then Gumroad or Payhip (pick one; Payhip is cheaper per sale).

Week 4 — B&N Press: six Wave 1 titles from **BN-Press** at $14.99. Then the rest.

Week 5 — Lulu Global: start with title **30** ($11.99) so you see the 2×-print rule bite, then the $9.99 titles.

Never: ads on Wave 4, Quiet Mind queries, Ozempic in the title, Kindle Select if Google Play is live.

---

## Conflicts we already paid attention to

1. **$9.99 vs $14.99 vs Lulu's 2× print** — not a fight. One book, one minimum per store. KDP stays $9.99 to keep the 60% tier and the impulse price. B&N cannot list $9.99 print. Lulu Global cannot list below 2× print. Different stores, different SKUs in *their* catalogs; same pages inside.
2. **KDP Select vs Google Play** — Select would lock the ebook to Amazon. We skip Kindle Select.
3. **KDP wrap on B&N / Ingram / Lulu** — barcode box and spine math are KDP’s. Try the wrap; if rejected, rebuild on *that* store’s template using `*_COVER_FRONT.pdf`.
4. **ISBN** — KDP free ISBN and B&N free ISBN are each locked to that store. That is fine. Buying Bowker ISBNs is the Ingram door, and it costs money we do not have in the budget.

---

## Blacklist

- Draft2Digital activation / maintenance fees
- Lulu $4.99 ebook distribution
- Any “we’ll market your book” package
- IngramSpark until ISBNs are purchased
- Monthly aggregators
- Putting $14.99 on Amazon
- Putting $9.99 print on B&N Press (the form will refuse you)
- One shared $14.99 catalog on stores that do **not** have a $14.99 floor
