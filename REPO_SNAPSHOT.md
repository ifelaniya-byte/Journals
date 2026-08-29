# Repo snapshot - 2026-08-28 (after the flat $9.99 cap)

## Branch layout

The second agent reorganized the repo. main no longer holds any books; it is just a pointer page.

| Branch | What is there | Status |
|---|---|---|
| main | One 10-line README that routes to the two catalog branches | Pointer only. We leave it alone. |
| ADHD-Journals | All 18 of OUR books | Our line. Listing upgrades, the marketing system, and today's flat $9.99 cap all live here. |
| Range-Band | Range Band Press 36-book kit line | Theirs, all at $9.99. Untouched by us. |

## Quality of our line

- validate_nine.py: ALL 9 PRODUCTS PERFECT (interiors, wraps, zips, metadata, checklist)
- validate_batch4.py: ALL 9 BATCH-4 PRODUCTS PERFECT
- Pricing: flat $9.99 on all 18 books. The validators now enforce this; if any price drifts away from $9.99, validation fails.
- Metadata: all 18 use the evolved KDP listing format (Amazon search title, series, 7-image stack, HTML description)
- Every title ships: interior PDF, wrap PDF, cover.jpg, metadata.txt, and 6 listing images
- Catalog files: CATALOG.csv, LOOKBOOK.pdf, MARKETING.md, 00_START_HERE.md. Zips are built on demand.
- Zero pull requests, zero merges between branches. The lines stay clean and separate, as instructed.

## Watch items

1. Kit books 14, 27 and 29 still compete head-on with our Middle Season, 5-Minute Dump and Night Pages.
2. The flat $9.99 price caps the margin on the 140-to-200-page titles. Revisit after 90 days of sales data.
3. If the other agent starts working on main again, remind them: catalog work belongs on the catalog branches, and main stays a pointer.
