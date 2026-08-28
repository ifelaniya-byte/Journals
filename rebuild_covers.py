"""Rebuild covers + zips only (interiors untouched, already validated). PATCH 5 driver."""
from pathlib import Path
from pypdf import PdfReader
import build_nine_products as B

B.register_fonts()
for key, prod in B.PRODUCTS.items():
    d = B.RELEASE / prod["dir"]; prefix = prod["dir"]
    interior = d / f"{prefix}_interior.pdf"
    pages = len(PdfReader(str(interior)).pages)  # source of truth = validated PDFs
    print(f"\n▸ [{key}] {prod['title']} ({pages}pp)")
    tex = B.ASSETS / f"{prefix}_linen.jpg"
    B.make_texture(tex, 3900, 3375, prod["tex_rgb"], prod["tex_seed"])
    ppi = B.WHITE_PPI if prod["paper"] == "white" else B.CREAM_PPI
    B.generate_wrap(d / f"{prefix}_cover_wrap.pdf", prod["trim"], pages, tex,
                    prod["title_lines"], prod["subtitle"], prod["desc"][:250], prod["features"], ppi)
    B.generate_png(d / f"{prefix}_cover.png", tex, prod["title_lines"], prod["subtitle"], prod.get("badge"))
    B.zip_pkg(B.RELEASE / "packages" / f"{prefix}_KDP.zip",
              [interior, d / f"{prefix}_cover_wrap.pdf", d / "metadata.txt"])
print("\nCOVER REBUILD DONE")
