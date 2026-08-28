# Range Band Press — platform playbook

Verified **28 August 2026**. Zero monthly fees. Zero setup fees. Platforms that charge before a sale are blacklisted.

Imprint: **Range Band Press**. Two print prices, one digital price:

| Pack | Price | Use on |
|---|---|---|
| `KDP-Complete-Kit/` | **$9.99** | Amazon KDP paperback (60% royalty floor) |
| `MARKETS/FLOOR-14.99/` | **$14.99** | Stores whose print floor is $14.99 |
| `MARKETS/DIGITAL-9.99/` | **$9.99** | Print-at-home PDF (Google Play, Gumroad, Payhip) |

Same interiors. Same wraps. Only the **listing price** and the **store** change. Covers do not print a dollar amount.

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

### 2. Barnes & Noble Press print — $14.99 pack

[press.barnesandnoble.com](https://press.barnesandnoble.com) · pack **`MARKETS/FLOOR-14.99/`** · **$14.99**

B&N Press **will not create a paperback listing under $14.99** as of **22 April 2026**. Existing cheaper titles were pulled starting 14 May 2026. Official: [B&N Press pricing](https://help-press.barnesandnoble.com/hc/en-us/articles/5358788362907-Print-Book-Pricing-and-Printing-Costs). Reported: [Jane Friedman, 15 Apr 2026](https://janefriedman.com/barnes-noble-press-sets-minimum-paperback-price-of-14-99-among-other-new-guidelines/).

- Free account. Free B&N-only ISBN. No monthly fee.
- Print royalty ~**55% of list − print cost** (confirm live)
- Account cap ~100 live titles; we have 36
- If their wizard rejects the KDP wrap, download **their** cover template and place `*_COVER_FRONT.pdf` on the front panel. Do not invent a new spine formula
- **Never** upload the $14.99 listing to KDP

### 3. Google Play Books — PDF, $9.99

[play.google.com/books/publish](https://play.google.com/books/publish) · pack **`MARKETS/DIGITAL-9.99/`**

- Partner Center is free. ~**70%** of list, no delivery fee. Price band about $0.05–$200. [Prices](https://support.google.com/books/partner/answer/3238849) · [70% split](https://support.google.com/books/partner/answer/9331459)
- Upload `*_printathome.pdf` + `*_cover.jpg`
- Description must say: **print-at-home PDF of the paperback**, not a reflowable ebook
- Google can assign a free identifier; you do not need to buy an ISBN

### 4. Gumroad — PDF, $9.99

[gumroad.com](https://gumroad.com) · same digital pack

- No monthly fee. Direct sales **10% + $0.50**. Discover marketplace is 30% — leave Discover off until you want it
- Same PDF + JPG. Author Range Band Press

### 5. Payhip Free — PDF, $9.99

[payhip.com](https://payhip.com) · same digital pack

- Free plan: **$0/month**, ~**5%** + Stripe/PayPal processing
- Do not upgrade to $29/$99 plans. We have no monthly budget

### 6. Lulu Bookstore (direct only)

[lulu.com](https://www.lulu.com) · use **$9.99 kit interiors + fronts**

- Print setup: **$0**. No monthly. You pay print + shipping when *they* sell, or when you order a proof
- Sell on **Lulu’s own bookstore** only
- **Do not** turn on Lulu **ebook Global Distribution** ($4.99 review fee — that is upfront money)
- Lulu *print* Global Distribution forces list ≥ ~2× print cost and a 50% wholesale cut. Skip it until you want that fight. B&N Press already covers the B&N shelf without Lulu

---

## Parked — costs money before a sale, or needs a file we do not have

| Platform | Why parked | When to reopen |
|---|---|---|
| **Draft2Digital** | New accounts: **$20 activation** (Apr 2026) + **$12/year** if you earn under $100. [ALLi](https://selfpublishingadvice.org/what-the-draft2digital-fee-changes-mean-for-you-in-2026/) | Never, on this budget |
| **IngramSpark** | Setup fee is gone (Feb 2026) but a **Bowker ISBN is $125 / $295 per 10**. That is upfront. Market access fee ~1.875% of list on sales | After you buy ISBNs. Then use the **$9.99** interiors + a *new* wrap from Ingram’s template (never the KDP wrap) |
| **Lulu ebook Global Dist.** | **$4.99** per title review | Use Google Play instead |
| **PublishDrive / StreetLib Pro** | Monthly subscription | No monthly budget |
| **Apple Books** | Wants **EPUB**, not PDF. Free Apple ISBN exists, still need EPUB | After a fixed-layout EPUB exists |
| **Kobo Writing Life** | Free, but EPUB. 70% at $2.99+ | After EPUB |
| **Blurb / vanity / “marketing packages”** | Upfront packages | Never |

IngramSpark’s old **$49 setup fee** is dead. Guides that still quote it are stale. The live cost for *us* is the ISBN, which we will not pay until you say so.

---

## What you upload, per store

| Store | Interior | Cover | listing.txt from | Price |
|---|---|---|---|---|
| KDP | `*_interior.pdf` | `*_COVER_WRAP.pdf` | `KDP-Complete-Kit/` | $9.99 |
| B&N Press | same PDF | wrap, or their template + front | `FLOOR-14.99/` | $14.99 |
| Google Play | `*_printathome.pdf` | `*_cover.jpg` | `DIGITAL-9.99/` | $9.99 |
| Gumroad / Payhip | same PDF | same JPG | `DIGITAL-9.99/` | $9.99 |
| Lulu Bookstore | interior PDF | front PDF | $9.99 kit listing, ignore Amazon-only lines | $9.99 |

Author field everywhere: **Range Band Press**.

---

## Order of operations (stranger-proof)

Week 1 — Amazon only. Proof trims **01, 07, 09**. Publish Wave 1 at $9.99 (01, 09, 05, 30, 10, 12). See `CASHFLOW.md`.

Week 2 — Rest of KDP 36 at $9.99. Expanded Distribution ON.

Week 3 — Google Play: upload the six Wave 1 PDFs. Then Gumroad or Payhip (pick one; Payhip is cheaper per sale).

Week 4 — B&N Press: six Wave 1 titles from **FLOOR-14.99** at $14.99. Then the rest.

Never: ads on Wave 4, Quiet Mind queries, Ozempic in the title, Kindle Select if Google Play is live.

---

## Conflicts we already paid attention to

1. **$9.99 vs $14.99** — not a fight. Two packs. KDP must stay $9.99 to keep the 60% tier and the impulse price. B&N cannot list $9.99 print. Different stores, different SKUs in *their* catalogs; same book inside.
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
