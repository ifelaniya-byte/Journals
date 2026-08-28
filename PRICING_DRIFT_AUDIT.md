# Pricing-drift audit — Wave 1

**Audit date:** August 28, 2026
**Scope:** every local commit/ref, `build_catalog.py`, `CATALOG.csv`, current and baseline Wave 1 `metadata.txt`, launch-kit documents, and the separately public `ifelaniya-byte/Journals` repository visible without authentication.

## Conclusion

The lower local prices were **not introduced by a later commit in this repository**. They already exist in the root tracked commit `643502a` (`v1.0-prepublication`) and remain unchanged through `82aa07c`.

The price-generation mechanism is the literal `PRODUCTS` table in `build_catalog.py`; its price field is used to generate `CATALOG.csv`, each `metadata.txt`, the upload checklist, lookbook, and price callouts. This is a hard-coded generator default, not a marketplace price or a later template rewrite.

| SKU | Lower price embedded since `643502a` | Reconfirmed authorized scout price | State |
|---|---:|---:|---|
| A01 | $14.99 | $16.99 | Repair required. |
| A04 | $14.99 | $17.99 | Repair required. |
| A05 | $14.99 | $15.99 | Repair required. |
| B10 | $14.99 | $17.99 | Founder-confirmed agreed scout price; repair required. |
| B12 | $15.99 | $18.99 | Repair required. |
| B18 | $14.99 | $18.99 | Repair required. |

No local Git commit contains the $16.99/$17.99/$18.99 decisions, so there is no in-repository “change commit” to revert. The discrepancy predates available tracked history / entered through the initial generated source set. The external untracked source product-development catalog corroborates five of the premium-price decisions but does not state a B10 KDP price; the founder subsequently confirmed B10 at $17.99.

## Commit-level result

| Local ref | Price change compared with root commit? | Result |
|---|---|---|
| `643502a` / `v1.0-prepublication` | N/A — root tracked commit | Lower defaults already present in generator, CSV, current metadata, baseline metadata, upload checklist, and price imagery. |
| `487d2b1` / `v1.1-branded` | No | Branding/QR changes; no price configuration change. |
| `5e44405` / `v1.1.1-qr-audio-draft` | No | QR/audio work; no price configuration change. |
| `e0ffd58` / `v1.1.2-gate1-counsel-prep` | No | Counsel/Gate 1 work; no price configuration change. |
| `82aa07c` | No | Inventory report repeated the inherited values; report is superseded by `PORTFOLIO.md`. |

## External `$9.99` finding

The `$9.99` distribution playbook is **not in this controlled local repository**. It is publicly visible in the separate GitHub repository `ifelaniya-byte/Journals`, branch `Range-Band`, which describes 36 GLP-1/wellness trackers and a `$9.99` KDP price. That repository has no configured remote relationship to this local catalog. Treat it as an external public-exposure issue, not a price source. See `GITHUB_PUBLIC_EXPOSURE_AUDIT.md`.

## Containment already added

- `DECISIONS.md` records all six founder-confirmed Wave 1 paperback prices.
- `verify_pricing.py` fails if a governed Wave 1 price is `TBD`, missing, or differs among the generator, `CATALOG.csv`, current metadata, or preserved baseline metadata.
- `validate_catalog.py` invokes the guard, so a structural validation pass cannot mask price drift.
- No rebuild, upload, pricing test, price-sensitive scorecard interpretation, or public release was authorized until B10 was confirmed and all derived files were regenerated together.

## Scorecard-assumption check

The Gate 1 scorecard has no paperback price, royalty, print-cost, margin, or contribution formula. Its only price references are the separate `$28–30` deluxe/waitlist-intent tests and the governance rule allowing at most one documented listing/price iteration. The corrected $15.99–$18.99 Wave 1 paperback prices therefore require **no formula or threshold change** to the Oct. 31 / Nov. 28 Gate 1 workbook.

Operational implication: record any future controlled price iteration in the Scorecard Gate Log, but do not reinterpret paperback sales as deluxe funding evidence without the existing price-visible deluxe-intent, Q4, and Gate 2/3 controls.

## Controlled repair — completed

1. Recorded B10’s approved price in the canonical table in `DECISIONS.md` at $17.99.
2. Updated only the six Wave 1 price values in `build_catalog.py`.
3. Rebuilt derived artifacts; did not hand-patch only `metadata.txt`.
4. Ran `verify_pricing.py`, `verify_canonical.py`, `validate_catalog.py`, and `audit_metadata_claims.py`; the first three passed and the metadata audit had no hard-stop strings.
5. Confirmed the six price values in listing callouts, lookbook, `CATALOG.csv`, current metadata, preserved baseline metadata, and the Wave 1-only KDP upload checklist.
6. Committed the repaired state. A price correction never clears naming, claims, QR, KDP technical, proof, or release gates.
