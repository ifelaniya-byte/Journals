# Build history — The Ritual Library KDP Catalog

## Batch 01 — August 28, 2026

**Scope:** Established the complete 18-SKU KDP scout catalog and two deluxe-hero source packages.

### Delivered
- 18 full paperback interiors across Pace & Progress (A01–A09) and Stillwork Editions (B10–B18).
- 18 KDP white-paper, black-and-white, no-bleed paperback cover wraps calculated from final page counts.
- Seven listing-image assets per SKU: front cover, four interior previews, format/price callout, and collection card.
- Per-product `metadata.txt` files with Amazon title, cover title, subtitle, format, trim, pages, price, categories, seven keyword phrases, description, and release boundary.
- `CATALOG.csv`, 19-page `LOOKBOOK.pdf`, upload checklist, marketing plan, claims-control guide, source build harness, packaging script, and structural validator.
- Deluxe hero content/art packages for *Dose & Breathe* and *Pocket of Calm*.

### QA performed
`python validate_catalog.py` completed successfully after generation. It verifies file inventory, final PDF page count and trim, cover wrap size/spine math, metadata field set, exactly seven keywords, listing image dimensions, upload checklist sections, operating docs, and lookbook page count.

### Explicitly not represented as complete
This batch is not legal/medical/trademark clearance, a KDP Previewer pass, a physical proof approval, a vendor-dieline approval, or an inventory authorization. Every release blocker remains visible in `LEGAL_AND_CLAIMS.md`, product metadata, and the main README.

## Change-control policy
- Log any title, subtitle, price, page-count, trim, paper, cover, keyword, or customer-facing claims change here and rerun `validate_catalog.py`.
- A changed page count requires a regenerated cover wrap and a fresh KDP Cover Calculator check.
- A changed print vendor requires new deluxe dielines/proof approval; do not force-fit a prior case-wrap or card-imposition file.
- Archive superseded listing images and PDFs outside the release folder or in a tagged repository release; avoid committing large redundant raster exports to the main branch.
