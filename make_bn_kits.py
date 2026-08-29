#!/usr/bin/env python3
"""Build the B&N Press minimum-price edition kits (markets/bn-print/).

Why this exists: B&N Press enforces a $14.99 minimum print list price
(April 2026). Our catalog price is $9.99 everywhere else. This script
produces a SEPARATE kit per book - front/back cover panels at 300 DPI
with bleed, extracted from our validated wrap PDFs, plus a patched
metadata file at $14.99 - so the main line and its $9.99 validators
stay untouched.

The easiest B&N cover route is the separate front/back upload: B&N
builds the spine itself from the page count (you pick a spine color).
That is what these files are for. Interior PDFs are UNCHANGED - use
the ones in release3/release4.

Deterministic: rerun any time after cover regeneration.
"""
import re
from pathlib import Path
import pymupdf

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "markets" / "bn-print"
DPI = 300
B = 0.125 * 72          # bleed on the outer edge of each panel
PRICE = "$14.99"        # B&N print minimum, owner-approved 2026-08-28
BN_HOLD = {"firststroke", "garden", "cozy", "botanical", "celestial", "tidal", "soft"}

# spine color suggestions = each book's cover texture tone
def spine_hexes():
    hexes = {}
    import build_nine_products as B9, build_batch4 as B4
    for src in (B9.PRODUCTS, B4.PRODUCTS4):
        for k, p in src.items():
            r, g, b = p["tex_rgb"]
            hexes[p["dir"]] = "#%02X%02X%02X" % (r, g, b)
    return hexes

def books():
    rows = []
    for rel in ("release3", "release4"):
        for d in sorted((ROOT / rel).iterdir()):
            if d.is_dir() and (d / "metadata.txt").exists():
                rows.append(d)
    return rows

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    hexes = spine_hexes()
    index = []
    for d in books():
        key = d.name
        wrap = next(d.glob(f"{key}_cover_wrap.pdf"))
        md = (d / "metadata.txt").read_text()
        trim = re.search(r'TRIM\s*\n\s*([\d.]+)"\s*×\s*([\d.]+)"', md)
        tw = float(trim.group(1)) * 72
        pages = re.search(r"PAGE COUNT\n(\d+)", md).group(1)
        paper = re.search(r"Paper: (\w+)", md).group(1)
        doc = pymupdf.open(str(wrap))
        p = doc[0]
        W, H = p.rect.width, p.rect.height
        front_r = pymupdf.Rect(W - tw - B, 0, W, H)
        back_r = pymupdf.Rect(0, 0, tw + B, H)
        od = OUT / key
        od.mkdir(exist_ok=True)
        for rect, name in ((front_r, "bn_front.jpg"), (back_r, "bn_back.jpg")):
            pix = p.get_pixmap(matrix=pymupdf.Matrix(DPI/72, DPI/72), clip=rect)
            pix.save(str(od / name), jpg_quality=82)
        # patched metadata: price, cover files, banner
        hold = key in BN_HOLD
        tag = "B&N PRINT EDITION ($14.99) HOLD — DO NOT UPLOAD" if hold else "B&N PRINT EDITION ($14.99 platform minimum)"
        bn = md.replace("KDP LISTING", tag + " - KDP LISTING", 1)
        bn = bn.replace(f"COVER FILE\n{key}_cover_wrap.pdf",
                        "COVER FILES (B&N separate-panel route; B&N builds the spine)\n"
                        f"bn_front.jpg (front with bleed)\nbn_back.jpg (back with bleed, barcode space reserved)")
        bn = bn.replace("SUGGESTED PRICE (US)\n$9.99", f"SUGGESTED PRICE (US)\n{PRICE}")
        bn = bn.replace("Price: $9.99", f"Price: {PRICE}")
        bn += f"""
--------------------------------------------------------------------------------
B&N PRESS NOTES (this edition only; everywhere else this book stays $9.99)
- {'HOLD — PLATFORM_DECISIONS.md: do not list this title at B&N (<120pp). Kit kept for the floor.' if hold else 'LIST — ≥120 pages; $14.99 is defensible heft.'}
- Price: {PRICE}. B&N print minimum list price is $14.99 since April 2026.
- Interior: upload release file {key}_interior.pdf UNCHANGED. B&W, bleed OFF.
- Cover route: upload bn_front.jpg + bn_back.jpg; set spine color {hexes[key]};
  add spine text only if B&N's tool asks (title, 14pt-class, centered).
- Free B&N ISBN at setup. Paper: {paper}. Finish: matte.
- Expected panel pixel size at 300 DPI: {round(front_r.width/72*DPI)} x {round(H/72*DPI)}.
"""
        (od / "metadata-bn.txt").write_text(bn)
        index.append((key, pages, f'{float(trim.group(1))}x{float(trim.group(2))}',
                      paper, hexes[key], f"{round(front_r.width/72*DPI)}x{round(H/72*DPI)}"))
        doc.close()
    # README index
    lines = ["# B&N Press kits - the $14.99 minimum-price edition (18 books)", "",
             "**LIST 11** (≥120pp). **HOLD 7** thin (firststroke, garden, cozy, botanical, celestial, tidal, soft).","",
             "This folder is a SEPARATE edition for the only platform whose minimum",
             "list price ($14.99 print, April 2026) is above our $9.99 catalog price.",
             "Everything else in the repo stays $9.99. Interiors are unchanged.",
             "", "Per-book kit: bn_front.jpg, bn_back.jpg (both 300 DPI, bleed included),",
             "metadata-bn.txt (paste-ready, $14.99).", "",
             "| Book | Pages | Trim | Paper | Spine color | Panel px |", "|---|---|---|---|---|---|"]
    for key, pages, tr, paper, hx, px in index:
        lines.append(f"| {key} | {pages} | {tr} | {paper} | {hx} | {px} |")
    lines += ["", "Upload steps: press.barnesandnoble.com -> Create -> Paperback ->",
              "enter metadata from metadata-bn.txt -> upload interior PDF from release3/4 ->",
              "choose separate front/back cover upload -> bn_front.jpg + bn_back.jpg ->",
              "spine color from the table -> price $14.99 -> publish.",
              "", "Regenerate any time: python3 make_bn_kits.py"]
    (OUT / "README.md").write_text("\n".join(lines) + "\n")
    print(f"built {len(index)} B&N kits in {OUT}")

if __name__ == "__main__":
    main()
