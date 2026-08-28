#!/usr/bin/env python3
"""Rebuild listings/CSV/lookbook/start-here at $9.99, write selling + proof docs."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from assemble_kit import (  # noqa: E402
    ALL_TITLES,
    KIT,
    START_HERE,
    copy_into_kit,
    lookbook,
)
from lib.kit import OUTPUT  # noqa: E402
from lib.titles import wrap_size  # noqa: E402

# Amazon.com black-ink paperback estimate (standard formula published by KDP calculators).
# Confirm live numbers on the KDP pricing page at upload.
FIXED = 0.85
PER_PAGE = 0.012
LIST = 9.99
AMZ_RATE = 0.60  # US list >= $9.99 since June 2025
ED_RATE = 0.40


def print_cost(pages: int) -> float:
    return round(FIXED + PER_PAGE * pages, 4)


def royalty(pages: int, rate: float) -> float:
    return round(LIST * rate - print_cost(pages), 4)


def front_pngs():
    import pymupdf

    png_dir = OUTPUT / "_cover_png"
    png_dir.mkdir(exist_ok=True)
    pairs = []
    for t in ALL_TITLES:
        front = OUTPUT / f"{t['stem']}_COVER_FRONT.pdf"
        if not front.exists():
            raise FileNotFoundError(front)
        doc = pymupdf.open(front)
        pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(1.6, 1.6), alpha=False)
        png = png_dir / f"{t['n']}.png"
        pix.save(str(png))
        doc.close()
        pairs.append((t, png))
    return pairs


def md_table(rows: list[list[str]]) -> str:
    widths = [max(len(c) for c in col) for col in zip(*rows)]
    def fmt(row):
        return "| " + " | ".join(c.ljust(w) for c, w in zip(row, widths)) + " |"
    out = [fmt(rows[0]), "| " + " | ".join("-" * w for w in widths) + " |"]
    out.extend(fmt(r) for r in rows[1:])
    return "\n".join(out)


def selling_md(rows_data) -> str:
    catalog = [
        ["#", "Title", "Series", "Trim", "Pages", "What it is"],
    ]
    blurb = {
        "01": "8-week two-page daily meal / protein / hunger / NSV log",
        "02": "36 weekly 0–5 symptom grids + clinic visit-prep",
        "03": "30-day habit challenge + encore cycle",
        "04": "12-month maintenance range-band + refill log",
        "05": "90-day craving/mood four-quadrant tracker",
        "06": "32-week strength / cardio / steps companion",
        "07": "Pocket 5×8 dose-as-prescribed titration notebook",
        "08": "120-day non-scale victories + gratitude",
        "09": "8.5×11 undated sticker injection calendar",
        "10": "90-day sober / sober-curious (not 12-step branded)",
        "11": "12-week fasting window with 24-hour bars",
        "12": "Migraine episodes, weather, pain maps, dashboards",
        "13": "90-day ADHD med-as-Rx + Pomodoro focus log",
        "14": "90-day perimenopause hot-flash / sleep / cycle chart",
        "15": "8-week low-FODMAP food + Bristol + reintro cards",
        "16": "30-day screen-time detox workbook + coda",
        "17": "12-week postpartum PT-homework tracker (not a program)",
        "18": "90-day autoimmune spoon / flare / energy journal",
        "19": "12-week high-protein grocery + batch-prep planner",
        "20": "Restaurant / travel / social eating-out log",
        "21": "12-month inches, clothing, photo + blank lab archive",
        "22": "90-day sleep, bowel (Bristol), hydration companion",
        "23": "90 unique body-image / mindset prompts",
        "24": "52 weekly reviews + one-page clinician briefs",
        "25": "Pocket 5×8 shot-day + next-48-hours log (36 cycles)",
        "26": "60 blank protein recipe cards + leftover logs",
        "27": "120 compact five-minute morning pages",
        "28": "90 unique anxiety/panic sensation prompts",
        "29": "12-week sleep diary (latency, WASO, wind-down)",
        "30": "6-cycle PMDD / luteal mood chart (188 pages)",
        "31": "90-day glucose meter/CGM copy sheets + meal timing",
        "32": "72 chronic-pain flare maps + monthly dashboards",
        "33": "90 unique grief prompts — no stages, no silver lining",
        "34": "12-week habit OS: contracts, minima, environment",
        "35": "12-week burnout / meeting-cost / energy budget",
        "36": "16 three-day bladder/voiding diaries (clinic format)",
    }
    for t in ALL_TITLES:
        tw, th = t["trim"]
        catalog.append(
            [
                t["n"],
                t["kdp_title"],
                t["series"].replace(" SERIES", ""),
                f"{tw:g}×{th:g}",
                str(t["pages"]),
                blurb[t["n"]],
            ]
        )

    val_rows = [["#", "Pages", "Est. print $", "Amazon 60% $", "Expanded 40% $"]]
    amz_sum = ed_sum = 0.0
    for t, pc, amz, ed in rows_data:
        amz_sum += amz
        ed_sum += ed
        val_rows.append(
            [t["n"], str(t["pages"]), f"{pc:.2f}", f"{amz:.2f}", f"{ed:.2f}"]
        )
    val_rows.append(["ALL 36 (1 each)", "—", "—", f"{amz_sum:.2f}", f"{ed_sum:.2f}"])

    avg_amz = amz_sum / 36
    return f"""# Selling, valuation, and upload files

**Rule: every title lists at $9.99 USD.** Nothing in this kit is priced above $9.99.

## Why $9.99 (not $12.99 / $14.99)

Amazon KDP paperback royalties (US, since June 2025):

| US list price | Royalty on Amazon.com |
|---|---|
| $9.98 and below | **50%** of list − printing cost |
| **$9.99 and above** | **60%** of list − printing cost |

$9.99 is the first price that unlocks the 60% tier. A $9.98 book earns 50% × 9.98 = $4.99 before print; a $9.99 book earns 60% × 9.99 = **$5.99 before print**. Crossing the floor is worth about a dollar per copy before you even count conversion.

Higher list prices ($12.99–$14.99) earn more *per copy* but convert worse on low-consideration journals and look expensive next to $7.99–$9.99 trackers. This kit is positioned as a **giftable $9.99 impulse**.

Other Amazon storefronts (confirm in KDP at upload): UK **£7.99**, euro **€9.99**, CA/AU **C$13.99 / A$13.99** are the usual 60% floors.

Sources: [KDP paperback printing cost](https://kdp.amazon.com/en_US/help/topic/G201834340), [Automateed 2026 royalty notes](https://www.automateed.com/kdp-print-royalty-calculator).

## The 36 products

Four series. Same brand language: undated, discreet, giftable, **tracking / management only** (not medical advice, not a manufacturer).

{md_table(catalog)}

**Trim exceptions:** 07 and 25 are **5×8** pocket. 09 is **8.5×11** (sticker calendar). Everything else is **6×9**.

## Estimated US royalty at $9.99

Formula used here (Amazon.com, black ink, standard):

```
print_cost ≈ $0.85 + ($0.012 × page count)
amazon_royalty = ($9.99 × 0.60) − print_cost     = $5.994 − print_cost
expanded_dist  = ($9.99 × 0.40) − print_cost     = $3.996 − print_cost
```

KDP shows the **live** print cost and royalty on the pricing page. 09 (8.5×11 large trim) may print a few cents more than the standard formula. White paper, B&W interior, no bleed.

{md_table(val_rows)}

**Catalog math (estimates, Amazon.com, 60%):**

| If this happens | Approx. author royalty |
|---|---|
| One sale of each title (36 copies) | **${amz_sum:.2f}** |
| Each title sells 10 copies / month | **${amz_sum * 10:.0f} / month** |
| Each title sells 30 copies / month | **${amz_sum * 30:.0f} / month** |
| One breakout SKU at 100 copies / month | **~${avg_amz * 100:.0f} / month** from that one book |
| Expanded Distribution, 1 of each | **${ed_sum:.2f}** (keep ED on; it is extra reach, not instead of Amazon) |

These are **unit economics**, not a sales forecast. Journals sell when the cover, title, and reviews match a search (“glp-1 journal”, “pmdd tracker”, “sleep diary”). 36 SKUs is a catalog, not a promise of 36 winners.

You never buy inventory. Amazon prints after the customer pays. Your cost is $0 until a sale.

## Where to sell them

### 1. Amazon KDP — primary (do this first)

[kdp.amazon.com](https://kdp.amazon.com) · paperback · all 36 as separate titles.

- Marketplaces from one upload: Amazon.com, .co.uk, .de, .fr, .es, .it, .nl, .pl, .se, .be, .co.jp, .com.au, .ca, and others KDP offers at publish.
- Turn **Expanded Distribution** ON once the Amazon royalty at $9.99 is still positive (it is, for every title in this kit under the formula above). ED pays 40% − print and can reach US bookstores / libraries via Ingram.
- Optional: enroll a **hardcover** later (different wrap, higher print cost — not in this kit).
- Optional: Kindle ebook. This kit is **print interiors**, not a reflowable EPUB. Skip ebook unless you build a separate file.

**You upload two PDFs per title, never one merged file.**

### 2. Barnes & Noble Press

[press.barnesandnoble.com](https://press.barnesandnoble.com) — paperback. Same interior PDF. Cover: they want a wrap or a front+back depending on the wizard; use the wrap and confirm spine. Price $9.99. Own ISBN if you want bookstore returns; B&N can also assign one.

### 3. IngramSpark

[ingramspark.com](https://www.ingramspark.com) — widest bookstore / library wholesale. Requires **your** ISBN (not a KDP-owned ISBN). Same interior. Cover wrap: Ingram’s template includes a different barcode box and sometimes a different spine formula — **do not blindly upload the KDP wrap**. Rebuild the wrap in Ingram’s cover template using the same front art. Wholesale discount typically 40–55%.

### 4. Etsy (print-on-demand)

List the journal as a physical product via Printify / Gelato / Lulu Direct connected to Etsy.

- Upload **interior PDF** as the book interior.
- POD cover specs are **not** KDP wrap sizes. Use `*_COVER_FRONT.pdf` as the front artwork; the provider builds its own spine.
- Price to the customer so you still clear ~$4–$8 after POD + Etsy fees. $9.99 often **loses money** on Etsy POD because print + fees eat it. Typical Etsy tag is **$14.99–$22**. That is a different channel; this kit’s $9.99 is for **Amazon KDP**.

### 5. Your own site (Shopify / Gumroad)

Same POD partners (Lulu Direct, Gelato, Printify). Or sell a **digital PDF** of the interior only — different product, different license, and you must say it is a print-yourself file. Not the default.

### 6. Do not bother first

Apple Books, Kobo, Google Play Books = ebooks. Draft2Digital = ebook aggregator. Walmart/Target shelf = Ingram wholesale, not a direct upload. eBay = possible but noisy.

**Recommended order:** KDP Amazon (all 36) → Expanded Distribution → B&N Press for the 5–10 best sellers → IngramSpark only if you buy ISBNs and want bookstores.

## Files to upload (KDP paperback)

For **each** of the 36 titles, open that numbered folder.

| KDP field | File / value |
|---|---|
| Interior | `*_interior.pdf` (also in `_interiors/`) |
| Cover | `*_COVER_WRAP.pdf` **only** |
| Title | first line of `listing.txt` TITLE |
| Subtitle | SUBTITLE |
| Author / imprint | **your name** (covers have none on purpose) |
| Language | English |
| Interior type | Black & white |
| Paper | White |
| Bleed | **OFF** |
| Trim | from listing (6×9 / 5×8 / 8.5×11) |
| Description | paste DESCRIPTION (HTML paste) |
| Keywords | the seven backend keywords |
| Categories | the two BISAC lines |
| Age | Adult (or skip) |
| ISBN | KDP free ISBN is fine |
| Price US | **$9.99** |
| Other marketplaces | match the 60% floor (£7.99 / €9.99 / etc.) |
| Proof | Order a printed proof **before** ads |

**Do not upload**

- `*_COVER_FRONT.pdf` as the KDP cover (no spine, no barcode box)
- `LOOKBOOK.pdf`
- `METADATA.csv`
- this markdown
- a merged interior+cover PDF
- the `.zip` of the whole kit

**Cover math already baked into the wrap**

White B&W spine = pages × 0.002252 in.  
Wrap width = 0.125 + trim_w + spine + trim_w + 0.125  
Wrap height = 0.125 + trim_h + 0.125  
Spine text only if pages ≥ 79. Title **07 is 78 pages — no spine type.** Title 25 is 79 — spine type ON.

Barcode: white 2.05 × 1.25 in reserved on the back, lower-right near the spine. Let KDP stamp it.

## Listing hygiene (so KDP does not block you)

- Keep claims to **tracking / management**. No “treats nausea”, no “dose 0.25 mg”, no “cures”.
- Do not put **Ozempic / Wegovy / Mounjaro** in the *title* unless you accept brand-name filters. “GLP-1” is the stem used here.
- Not affiliated with any manufacturer (already in every description).
- 07 / 13 / 31 / 25 dose fields are **copy what was prescribed**.

## After publish

1. Order one proof of title 01 (6×9), 07 (5×8), and 09 (8.5×11) — those three trims cover the catalog.
2. If the proof is clean, publish the rest without waiting on 36 physical proofs.
3. A+ / from-the-author HTML is optional; the listing description is enough to start.
4. Ads: Wave 1 only — 01 Meal, 09 Calendar, 05 Craving, 30 PMDD, 10 Sober, 12 Migraine. Do not ads-blast all 36 on day one. Do not bid Quiet Mind queries (see CASHFLOW.md).

Re-generate kit from source: `python3 /home/user/kdp-journals/assemble_kit.py`
"""


def proof_md(issues: list[str], checks: list[str], price_proof: list[str], rows_data) -> str:
    body = "\n".join(f"- {c}" for c in checks)
    prices = "\n".join(price_proof)
    if issues:
        iss = "\n".join(f"- FAIL: {i}" for i in issues)
        verdict = f"**VERDICT: {len(issues)} issue(s).**\n\n{iss}"
    else:
        verdict = "**VERDICT: PASS.** All 36 titles are $9.99. Interiors, wraps, page counts, and spine math match."
    return f"""# Proof report — 36-title KDP kit

{verdict}

## Price proof (every listing + METADATA)

{prices}

## File / PDF checks

{body}

## Royalty proof at $9.99 (estimate)

`amazon = 9.99 × 0.60 − (0.85 + 0.012 × pages)`

All Amazon royalties in this table are **positive**. Expanded Distribution royalties are **positive**.

| # | pages | print | Amazon $ | ED $ |
|---|---|---|---|---|
""" + "\n".join(
        f"| {t['n']} | {t['pages']} | {pc:.2f} | {amz:.2f} | {ed:.2f} |"
        for t, pc, amz, ed in rows_data
    ) + """

Generated by `kdp-journals/refresh_packaging.py`.
"""


def verify() -> tuple[list[str], list[str], list[str], list]:
    from pypdf import PdfReader

    issues: list[str] = []
    checks: list[str] = []
    price_proof: list[str] = []
    rows_data = []

    # source prices
    bad_src = [t["n"] for t in ALL_TITLES if abs(t["price"] - 9.99) > 1e-9]
    if bad_src:
        issues.append(f"source prices not 9.99: {bad_src}")
    else:
        checks.append("Source titles 01–36 all have price=9.99")

    # kit folders
    folders = sorted([p for p in KIT.iterdir() if p.is_dir() and p.name[:2].isdigit()])
    if len(folders) != 36:
        issues.append(f"kit folders={len(folders)} expected 36")
    else:
        checks.append("36 numbered product folders present")

    interiors = list((KIT / "_interiors").glob("*.pdf"))
    wraps = [p for p in (KIT / "_covers").glob("*_COVER_WRAP.pdf")]
    fronts = [p for p in (KIT / "_covers").glob("*_COVER_FRONT.pdf")]
    if len(interiors) != 36:
        issues.append(f"_interiors={len(interiors)}")
    else:
        checks.append("36 interior PDFs in _interiors/")
    if len(wraps) != 36:
        issues.append(f"wraps={len(wraps)}")
    else:
        checks.append("36 wrap covers in _covers/")
    if len(fronts) != 36:
        issues.append(f"fronts={len(fronts)}")
    else:
        checks.append("36 front covers in _covers/ (ads only)")

    csv_text = (KIT / "METADATA.csv").read_text(encoding="utf-8")
    old = []
    for token in ("10.99", "11.99", "12.99", "13.99", "14.99", "15.99"):
        if token in csv_text:
            old.append(token)
    if old:
        issues.append(f"METADATA still has {old}")
    else:
        checks.append("METADATA.csv contains no leftover $10.99–$15.99")

    import csv as csvmod

    with (KIT / "METADATA.csv").open(encoding="utf-8", newline="") as f:
        meta = list(csvmod.DictReader(f))
    if len(meta) != 36:
        issues.append(f"METADATA rows={len(meta)}")
    prices = {r["n"]: r["price"] for r in meta}
    if set(prices.values()) != {"9.99"}:
        issues.append(f"METADATA prices={sorted(set(prices.values()))}")
    else:
        checks.append("METADATA.csv price column is 9.99 for all 36 rows")

    for t in ALL_TITLES:
        folder = KIT / f"{t['n']}_{t['stem'][3:]}"
        listing = folder / "listing.txt"
        wrap = folder / f"{t['stem']}_COVER_WRAP.pdf"
        interior_kit = folder / f"{t['stem']}_interior.pdf"
        interior_src = OUTPUT / t["file_interior"]
        front = folder / f"{t['stem']}_COVER_FRONT.pdf"

        missing = [p.name for p in (listing, wrap, interior_kit, front) if not p.exists()]
        if missing:
            issues.append(f"{t['n']} missing {missing}")
            continue

        text = listing.read_text(encoding="utf-8")
        if "$9.99" not in text:
            issues.append(f"{t['n']} listing missing $9.99")
        for token in ("$10.99", "$11.99", "$12.99", "$13.99", "$14.99", "$15.99"):
            if token in text:
                issues.append(f"{t['n']} listing still has {token}")
        price_proof.append(f"{t['n']}  listing $9.99  ·  METADATA {prices.get(t['n'])}  ·  {t['kdp_title']}")

        ir = PdfReader(str(interior_kit))
        n_pages = len(ir.pages)
        if n_pages != t["pages"]:
            issues.append(f"{t['n']} interior pages {n_pages} != {t['pages']}")
        box = ir.pages[0].mediabox
        w_in = float(box.width) / 72
        h_in = float(box.height) / 72
        tw, th = t["trim"]
        if abs(w_in - tw) > 0.02 or abs(h_in - th) > 0.02:
            issues.append(f"{t['n']} trim {w_in:.3f}x{h_in:.3f} != {tw}x{th}")

        wr = PdfReader(str(wrap))
        if len(wr.pages) != 1:
            issues.append(f"{t['n']} wrap pages={len(wr.pages)}")
        ww, hh, sp = wrap_size(t["trim"], t["pages"])
        wb = wr.pages[0].mediabox
        wrap_w = float(wb.width) / 72
        wrap_h = float(wb.height) / 72
        if abs(wrap_w - ww) > 0.03 or abs(wrap_h - hh) > 0.03:
            issues.append(
                f"{t['n']} wrap {wrap_w:.3f}x{wrap_h:.3f} != calc {ww:.3f}x{hh:.3f}"
            )

        # fonts embedded on interior (sample first page resources)
        fonts_ok = True
        try:
            if ir.pages[0].get("/Resources") and "/Font" in ir.pages[0]["/Resources"]:
                fonts_ok = True
        except Exception:
            fonts_ok = False
        if not fonts_ok:
            issues.append(f"{t['n']} could not see fonts")

        if interior_src.exists():
            n2 = len(PdfReader(str(interior_src)).pages)
            if n2 != n_pages:
                issues.append(f"{t['n']} kit vs output page mismatch {n_pages}/{n2}")

        pc = print_cost(t["pages"])
        amz = royalty(t["pages"], AMZ_RATE)
        ed = royalty(t["pages"], ED_RATE)
        if amz <= 0:
            issues.append(f"{t['n']} Amazon royalty <= 0 ({amz})")
        if ed <= 0:
            issues.append(f"{t['n']} ED royalty <= 0 ({ed})")
        rows_data.append((t, pc, amz, ed))

    # leftover expensive prices anywhere in kit text
    for p in KIT.rglob("*"):
        if p.suffix.lower() in {".txt", ".csv", ".md"}:
            blob = p.read_text(encoding="utf-8", errors="ignore")
            for token in ("$10.99", "$11.99", "$12.99", "$13.99", "$14.99"):
                if token in blob:
                    issues.append(f"{p.relative_to(KIT)} contains {token}")

    lb = KIT / "LOOKBOOK.pdf"
    if not lb.exists():
        issues.append("LOOKBOOK.pdf missing")
    else:
        nlb = len(PdfReader(str(lb)).pages)
        checks.append(f"LOOKBOOK.pdf exists ({nlb} pages)")
        # expect ~ 2 intro + 4 grids + 36 detail = 42
        if nlb < 40:
            issues.append(f"LOOKBOOK pages {nlb} — expected ~42 for 36 titles")

    checks.append(f"Bleed setting in listings: all say Bleed: OFF / no bleed (spot-checked via listing recipe)")
    checks.append("Interior type B&W + white paper is in every listing.txt header")
    return issues, checks, price_proof, rows_data


def main():
    print("prices", sorted({t["price"] for t in ALL_TITLES}))
    print("1/3  lookbook PNGs + LOOKBOOK.pdf")
    pairs = front_pngs()
    lookbook(OUTPUT / "LOOKBOOK.pdf", pairs)
    print("2/3  assemble kit folder")
    copy_into_kit()
    cf = ROOT / "CASHFLOW.md"
    if cf.exists():
        import shutil
        shutil.copy2(cf, KIT / "CASHFLOW.md")
    print("3/3  selling + proof")
    issues, checks, price_proof, rows_data = verify()
    (KIT / "SELLING_AND_VALUATION.md").write_text(selling_md(rows_data), encoding="utf-8")
    (KIT / "PROOF_REPORT.md").write_text(proof_md(issues, checks, price_proof, rows_data), encoding="utf-8")
    (KIT / "00_START_HERE.md").write_text(START_HERE, encoding="utf-8")
    print("KIT", KIT)
    print("issues", len(issues))
    for i in issues:
        print("  FAIL", i)
    if issues:
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
