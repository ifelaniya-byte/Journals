# Quiet Mind Press — start here

18 paperbacks, all validated and upload-ready. Built 2026 by the in-repo engines.

## Format inventory (per title)

| File | Purpose | In repo |
|---|---|---|
| `<dir>/<dir>_interior.pdf` | KDP interior upload | 18/18 |
| `<dir>/<dir>_cover_wrap.pdf` | KDP cover upload (spine-exact, barcode reserved) | 18/18 |
| `<dir>/<dir>_cover.jpg` | marketing image (1800×2700) for stores/social | 18/18 |
| `<dir>/metadata.txt` | paste-ready listing: keywords, categories, description, price | 18/18 |
| `CATALOG.csv` | whole catalog, one row per title | 1 |
| `LOOKBOOK.pdf` | visual catalog with specs | 1 |
| zips | on demand — `python make_zips.py all` | generated |

## Upload settings (all titles)

- Paperback · B&W interior · **no bleed** · matte cover · expanded distribution ON
- Paper: cream (journals) / white (coloring + grid trackers) — per `CATALOG.csv`
- Fonts embedded in every interior; validators: `python validate_nine.py` / `validate_batch4.py`

## Staging plan (protects account health)

1. Days 1–3: Core Line journals (dump, parallel, night) + Settle
2. Days 4–6: Rising Niche journals (middle, dopamine, slow, soft)
3. Days 7–10: coloring line B3 (firststroke → architect)
4. Days 11–14: fine-line B4 (cozy, botanical, celestial, tidal)

## Pricing

See CATALOG.csv. Journal premiums are backed by page depth + architecture;
pocket/impulse formats sit at $9.99. Reprice any time — it is listing-side only.

## Rebuild after changes

```
python build_nine_products.py      # batch 3
python build_batch4.py             # batch 4
python gen_catalog.py              # ALWAYS last: metadata + CATALOG + LOOKBOOK
python make_zips.py all            # optional upload zips
```
