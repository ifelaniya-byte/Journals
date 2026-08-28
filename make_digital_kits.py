#!/usr/bin/env python3
"""Build the DIGITAL PDF (print-at-home) editions: markets/digital/.

Owner architecture (2026-08-28):
- The Middle Season gets NO digital edition. It is the highest lane and
  stays print-only, by design, to keep the sub-$5 space unsaturated.
- Large-pool attractors at $4.99: dump, dopamine, cozy, soft, settle.
- Everything else at $6.99 (12 titles): parallel, night, slow, firststroke,
  garden, mosaic, woodland, fractal, architect, botanical, celestial, tidal.

Product file per book: <book>_digital.pdf = 1 license/title page (generated
at the book's trim size) + the validated interior, UNMODIFIED (pypdf merge).
The print interior file itself is never touched.

Space rule: the digital PDFs are .gitignored and NOT pushed (regenerable
deterministically from tracked files by running this script). Metadata,
README and this script are tracked.
"""
import re
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "markets" / "digital"

NO_PDF = {"middle"}                       # print-only lane (owner decision)
POOL_499 = {"dump", "dopamine", "cozy", "soft", "settle"}  # large pools
PRICE_499, PRICE_699 = "$4.99", "$6.99"


def license_page(path, title, trim_w, trim_h, price):
    c = canvas.Canvas(str(path), pagesize=(trim_w, trim_h))
    w, h = trim_w, trim_h
    c.setFont("Helvetica-Bold", h * 0.030)
    c.drawCentredString(w / 2, h * 0.82, "QUIET MIND PRESS")
    c.setFont("Helvetica-Bold", h * 0.042)
    for i, line in enumerate(title.split(":")[0].strip().split(" / ") or [title]):
        pass
    name = title.split(":")[0].strip()
    c.drawCentredString(w / 2, h * 0.74, name)
    c.setFont("Helvetica", h * 0.024)
    c.drawCentredString(w / 2, h * 0.69, "Digital Edition - Print at Home")
    c.setFont("Helvetica", h * 0.019)
    txt = [
        f"This PDF is the complete interior of the book, licensed for",
        f"personal use at {price}. You may print it at home or at a print",
        "shop for your own use, as many times as you like, for one",
        "household. You may not resell it, share the file, or use it",
        "commercially. The printed paperback edition is a separate",
        "product and the best way to use this book.",
        "",
        "Printing tips: print at 100% (actual size). US Letter or A4 both",
        "work. Single-sided pages are easiest for coloring and journaling.",
        "",
        "Thank you for supporting independent publishing.",
        "Quiet Mind Press - personal use license - no medical advice.",
    ]
    y = h * 0.60
    for line in txt:
        c.drawCentredString(w / 2, y, line)
        y -= h * 0.031
    c.showPage()
    c.save()


def main():
    if OUT.exists():
        for d in OUT.iterdir():
            if d.is_dir():  # wipe book dirs + samplers; KEEP README.md
                for f in d.iterdir():
                    f.unlink()
                d.rmdir()
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for rel in ("release3", "release4"):
        for d in sorted((ROOT / rel).iterdir()):
            if not (d.is_dir() and (d / "metadata.txt").exists()):
                continue
            key = d.name
            if key in NO_PDF:
                rows.append((key, None, None))
                continue
            md = (d / "metadata.txt").read_text()
            title = re.search(r"AMAZON TITLE[^\n]*\n(.+)", md).group(1).strip()
            pages = int(re.search(r"PAGE COUNT\s*\n\s*(\d+)", md).group(1))
            tw = float(re.search(r'TRIM\s*\n\s*([\d.]+)"', md).group(1)) * 72
            th = float(re.search(r'TRIM\s*\n\s*[\d.]+"\s*×\s*([\d.]+)"', md).group(1)) * 72
            price = PRICE_499 if key in POOL_499 else PRICE_699

            od = OUT / key
            od.mkdir(exist_ok=True)
            lic = od / "_license_tmp.pdf"
            license_page(lic, title, tw, th, price)
            interior = next(d.glob(f"{key}_interior.pdf"))
            w = PdfWriter()
            w.append(str(lic))
            w.append(str(interior))
            dig = od / f"{key}_digital.pdf"
            with open(dig, "wb") as f:
                w.write(f)
            lic.unlink()
            n = len(PdfReader(str(dig)).pages)

            dg = md.replace("KDP LISTING",
                            f"DIGITAL PDF EDITION (print-at-home, {price}) - KDP LISTING", 1)
            dg = dg.replace(
                "SUGGESTED PRICE (US)\n$9.99",
                f"SUGGESTED PRICE (DIGITAL)\n{price}   (same price on every PDF store; "
                "platform minimums: none on any eligible store - see markets/digital/README.md)")
            dg = dg.replace("Price: $9.99", f"Price: {price}")
            dg = dg.replace(
                f"INTERIOR FILE\n{key}_interior.pdf",
                f"PRODUCT FILE\n{key}_digital.pdf  (license page + the full validated interior, "
                f"{pages} pages + 1 license page = {n})")
            dg += (
                "\n" + "-" * 80 +
                "\nDIGITAL EDITION NOTES\n"
                f"- Buyer gets: {key}_digital.pdf, personal-use license, print-at-home.\n"
                "- The print edition stays $9.99 and separate; this file never goes to KDP.\n"
                "- Upload to the free PDF stores (see README matrix). Same price everywhere.\n"
                "- The Middle Season deliberately has NO digital edition (print-only lane).\n"
                "- Listing images: cover.jpg + listing_02-05 + listing_07. DO NOT use\n"
                "  listing_06_callout.jpg here (it shows the $9.99 print price).\n")
            (od / "metadata-digital.txt").write_text(dg)
            rows.append((key, price, n))
    built = [(k, p, n) for k, p, n in rows if p]
    print(f"built {len(built)} digital editions; "
          f"{PRICE_499}: {sum(1 for _,p,_ in built if p==PRICE_499)}, "
          f"{PRICE_699}: {sum(1 for _,p,_ in built if p==PRICE_699)}; "
          f"print-only: {[k for k,_,_ in rows if not _]}")


if __name__ == "__main__":
    main()
