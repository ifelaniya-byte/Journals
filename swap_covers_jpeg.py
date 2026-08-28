"""Regenerate batch-3 marketing covers as JPEG (same deterministic layout, ~85% smaller)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import build_nine_products as B

for key, prod in B.PRODUCTS.items():
    tex = B.ASSETS / f"{prod['dir']}_linen.jpg"
    B.generate_png(Path(f"/tmp/{key}.png"), tex, prod["title_lines"], prod["subtitle"], prod.get("badge"))
    Image.open(f"/tmp/{key}.png").convert("RGB").save(
        B.RELEASE / prod["dir"] / f"{prod['dir']}_cover.jpg", "JPEG", quality=90, optimize=True)
    (B.RELEASE / prod["dir"] / f"{prod['dir']}_cover.png").unlink()
    print(f"{key}: cover.jpg written")
