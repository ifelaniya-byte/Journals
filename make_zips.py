#!/usr/bin/env python3
"""On-demand KDP zip packaging (kept out of the repo/tree to save space).
Usage: python make_zips.py [3|4|all]  -> writes releaseN/packagesZN/*.zip (not committed)."""
import sys, zipfile
from pathlib import Path
def pack(release: Path, products: dict):
    out = release / ("packages" if release.name == "release3" else "packages4")
    out.mkdir(exist_ok=True)
    for key, p in products.items():
        d = release / p["dir"]
        z = out / f"{p['dir']}_KDP.zip"
        with zipfile.ZipFile(z, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for f in (d/f"{p['dir']}_interior.pdf", d/f"{p['dir']}_cover_wrap.pdf", d/"metadata.txt"):
                zf.write(f, f.name)
        print(f"packed {z}")
if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("3", "all"):
        import build_nine_products as B; pack(B.RELEASE, B.PRODUCTS)
    if which in ("4", "all"):
        import build_batch4 as B4; pack(B4.RELEASE, B4.PRODUCTS4)
