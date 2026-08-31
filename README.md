# Range Band Press

**Live inside the range.**

Undated GLP-1, chronic-condition and wellness tracking journals. **108 paperbacks** in three kit volumes. KDP list **$9.99**. Other stores get **that title’s own minimum**, not one shared $14.99 catalog.

A range is not a cage. It is the band you already chose — protein, sleep, a shot day, a quiet Tuesday.

| | |
|---|---|
| Imprint (KDP author field) | **Range Band Press** |
| GitHub branch | [`Range-Band`](https://github.com/ifelaniya-byte/Journals/tree/Range-Band) |
| Volume 1 · core 36 (frozen) | [`range-band/KDP-Complete-Kit/`](range-band/KDP-Complete-Kit/) |
| Volume 2 · products 37–72 (new) | [`range-band/VOLUME-3/`](range-band/VOLUME-3/) |
| Volume 3 · products 73–108 (new) | [`range-band/VOLUME-4/`](range-band/VOLUME-4/) |
| Final catalog & upload docs (54) | [`range-band/CATALOG-54/`](range-band/CATALOG-54/) |
| Per-title floors | [`range-band/MARKETS/by-title/`](range-band/MARKETS/by-title/) · [`PRODUCTS.csv`](range-band/MARKETS/PRODUCTS.csv) |
| Brand | [`range-band/KDP-Complete-Kit/BRAND.md`](range-band/KDP-Complete-Kit/BRAND.md) |
| Sister imprint | Quiet Mind Press on [`ADHD-Journals`](https://github.com/ifelaniya-byte/Journals/tree/ADHD-Journals) — **do not merge** |

## Catalog

Every kit folder carries its own `listing.txt` (title, subtitle, author, BISAC, 7 backend keywords, $9.99, description), an interior PDF, a KDP wrap cover, and a front-only cover for mockups. All volumes: paperback · bleed OFF · B&W · white paper · interior PDF + wrap cover · **no Expanded Distribution**.

| Volume | Products | Kits | Series | Verification |
|---|---|---|---|---|
| **1 — core** (frozen) | 1–36 | [`KDP-Complete-Kit/`](range-band/KDP-Complete-Kit/) | GLP-1 Tracking · Wellness Tracking · GLP-1 Companion · Wellness Companion | shipped at branch `8562469` |
| **2 — new** | 37–72 | [`VOLUME-3/`](range-band/VOLUME-3/) | Chronic Care (20) · Inner Range (16) | `verify_vol3.py` **PASS** — 36 kits × 4 files, 252 unique keywords, 83–118 pp, wrap math exact, zero policy hits |
| **3 — new** | 73–108 | [`VOLUME-4/`](range-band/VOLUME-4/) | Deep Health (18) · Life Range (18) | `verify_vol4.py` **PASS** — 36 kits × 4 files, 252 unique keywords (zero overlap with Vol-2), 83–118 pp, wrap math exact, zero policy hits |

Inventory docs live beside each volume (`INVENTORY_VOL3.md`, `INVENTORY_VOL4.md`) with the per-title core recording mechanic — no two titles share a mechanic, and all 504 Vol-2 + Vol-3 backend keywords are distinct.

**Status: candidate-only.** Books are built and verified but nothing has been published. Upload is a human gate; no KDP/B&N account or API is used from here.

## Markets (no monthly, no setup fee)

Amazon KDP **$9.99** · B&N Press **$14.99** (`MARKETS/BN-Press/`) · Lulu Global **per title, 2× print** (`MARKETS/Lulu-Global/`) · Google Play / Gumroad / Payhip PDFs **$9.99**. IngramSpark listings are parked until ISBN. Read [`range-band/MARKETS/PLAYBOOK.md`](range-band/MARKETS/PLAYBOOK.md).
