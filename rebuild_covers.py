"""Rebuild covers only (interiors untouched, already validated).

Covers-only driver for ALL 18 books:
  - release3 nine (B.PRODUCTS)        -> cover_wrap.pdf + cover.png
  - release4 batch-4 nine (PRODUCTS4) -> cover_wrap.pdf + cover.jpg

Back-cover blurbs now go through B.back_blurb() (sentence-boundary
truncation) instead of the old desc[:250] mid-word slice.

KDP zips are NOT rebuilt here (on-demand via make_zips.py, untracked).
Verify with: python3 validate_nine.py && python3 validate_batch4.py
"""
from pathlib import Path

from pypdf import PdfReader

import build_nine_products as B
import build_batch4 as B4

B.register_fonts()

for key, prod in B.PRODUCTS.items():
    d = B.RELEASE / prod["dir"]
    prefix = prod["dir"]
    pages = len(PdfReader(str(d / f"{prefix}_interior.pdf")).pages)
    print(f"\n▸ [{key}] {prod['title']} ({pages}pp)")
    tex = B.ASSETS / f"{prefix}_linen.jpg"
    B.make_texture(tex, 3900, 3375, prod["tex_rgb"], prod["tex_seed"])
    ppi = B.WHITE_PPI if prod["paper"] == "white" else B.CREAM_PPI
    B.generate_wrap(d / f"{prefix}_cover_wrap.pdf", prod["trim"], pages, tex,
                    prod["title_lines"], prod["subtitle"],
                    B.back_blurb(prod["desc"]), prod["features"], ppi)
    B.generate_png(d / f"{prefix}_cover.png", tex, prod["title_lines"],
                   prod["subtitle"], prod.get("badge"))

for key, p in B4.PRODUCTS4.items():
    d = B4.RELEASE / p["dir"]
    pages = len(PdfReader(str(d / f"{p['dir']}_interior.pdf")).pages)
    print(f"\n▸ [{key}] {p['title']} ({pages}pp)")
    tex = B4.ASSETS / f"{p['dir']}_linen.jpg"
    B.make_texture(tex, 3900, 3375, p["tex_rgb"], p["tex_seed"])
    ppi = B.WHITE_PPI if p["paper"] == "white" else B.CREAM_PPI
    B.generate_wrap(d / f"{p['dir']}_cover_wrap.pdf", p["trim"], pages, tex,
                    p["title_lines"], p["subtitle"],
                    B.back_blurb(p["desc"]), p["features"], ppi)
    B4.generate_cover_jpg(d / f"{p['dir']}_cover.jpg", tex,
                          p["title_lines"], p["subtitle"], p.get("badge"))

print("\nCOVER REBUILD DONE (18 books, interiors untouched)")
