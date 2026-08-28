#!/usr/bin/env python3
"""Build the two free lead-magnet samplers for the Market-Files branch.

Recreates from CURRENT interiors (so a QA pass on interiors automatically
flows into the samplers on the next Market-Files rebuild):

  samplers/quiet-mind-color_sampler.pdf    letter trim, 9 pages
  samplers/quiet-mind-journals_sampler.pdf 6x9 trim, 9 pages

Layout: 1 title page + 7 sample pages + 1 call-to-action page.
Sample pages are copied vector-native from interiors via insert_pdf
(a previous one-off build rasterized them and shipped blank pages, and its
CTA line lost its first glyph to a negative-x clip - this script typesets
both pages with measured, centered text instead).

Run from the repo root:  python3 make_samplers.py [outdir]
Output defaults to markets/samplers/ (regenerable cache, untracked).
"""
import sys
from pathlib import Path

import pymupdf

import niche_upgrades as U

ROOT = Path(__file__).resolve().parent

# one interior page per book, in catalog order
COLOR_BOOKS = ["firststroke", "garden", "mosaic", "woodland",
               "fractal", "architect", "botanical"]
JOURNAL_PAGES = [("dump", 5), ("dump", 39), ("settle", 5), ("settle", 39),
                 ("dopamine", 5), ("dopamine", 39), ("night", 5)]

COLOR_W, COLOR_H = 612, 792   # letter, like the original color sampler
JRNL_W, JRNL_H = 432, 648     # 6x9, like the original journals sampler


def interior(key):
    for rel in ("release3", "release4"):
        p = ROOT / rel / key / f"{key}_interior.pdf"
        if p.exists():
            return pymupdf.open(str(p))
    raise FileNotFoundError(key)


def center(page, text, y, size, bold=False, gray=0.15):
    font = "hebo" if bold else "helv"
    W = page.rect.width
    w = pymupdf.get_text_length(text, fontname=font, fontsize=size)
    page.insert_text(((W - w) / 2, y), text, fontname=font,
                     fontsize=size, color=(gray,) * 3)


def left(page, text, y, size, bold=False, gray=0.2, x=None):
    x = 48 if x is None else x
    page.insert_text((x, y), text, fontname="hebo" if bold else "helv",
                     fontsize=size, color=(gray,) * 3)


def title_page(doc, heading, W, H, k=1.0):
    p = doc.new_page(width=W, height=H)
    center(p, "QUIET MIND PRESS", H * 0.19, 13 * k, bold=True, gray=0.4)
    center(p, heading, H * 0.38, 30 * k, bold=True)
    center(p, "Free sampler - a few pages from each book", H * 0.48, 13 * k)
    center(p, "Full editions: print paperback or print-at-home PDF",
           H * 0.51, 13 * k)


def cta_page(doc, heading, lines, W, H, k=1.0):
    p = doc.new_page(width=W, height=H)
    center(p, "Enjoyed the sample?", H * 0.165, 27 * k, bold=True)
    left(p, f"The complete {heading} editions - every page, "
            f"print-at-home PDF", H * 0.25, 13 * k)
    y = H * 0.315
    for text, bold in lines:
        left(p, text, y, 12.5 * k, bold=bold)
        y += 24 * k
    y += 24 * k
    left(p, "Paperbacks on Amazon. PDFs on your favorite digital store.",
         y, 12 * k)
    left(p, "Quiet Mind Press - personal use license", y + 26 * k,
         11 * k, gray=0.45)


def build_color(out):
    doc = pymupdf.open()
    title_page(doc, "Quiet Mind Color Sampler", COLOR_W, COLOR_H)
    for key in COLOR_BOOKS:
        src = interior(key)
        pi = next(i for i in range(2, len(src))
                  if len(src[i].get_drawings()) > 3)
        doc.insert_pdf(src, from_page=pi, to_page=pi)
    cta_page(doc, "Quiet Mind Color Sampler", [
        ("Easy Garden", True), ("$6.99  -  47 bold designs", False),
        ("Mosaic Mind", True), ("$6.99  -  57 designs", False),
        ("Celestial Atlas", True), ("$6.99  -  real star data", False),
        ("The whole 10-book Color line", True),
        ("$6.99 each - bundle inside stores", False)],
        COLOR_W, COLOR_H)
    doc.save(str(out), garbage=3, deflate=True)


def build_journals(out):
    doc = pymupdf.open()
    k = JRNL_W / COLOR_W
    title_page(doc, "Quiet Mind Journals Sampler", JRNL_W, JRNL_H, k)
    for key, pi in JOURNAL_PAGES:
        doc.insert_pdf(interior(key), from_page=pi, to_page=pi)
    cta_page(doc, "Quiet Mind Journals Sampler", [
        ("The 5-Minute Dump", True), ("$4.99  -  200 pages", False),
        ("The Dopamine Menu", True), ("$4.99  -  150 pages", False),
        ("Settle", True), ("$4.99  -  172 pages", False),
        ("The Middle Season", True),
        ("paperback only - the flagship stays print", False)],
        JRNL_W, JRNL_H, k)
    doc.save(str(out), garbage=3, deflate=True)


def verify(path, art_pages):
    d = pymupdf.open(str(path))
    assert len(d) == 9, f"{path}: {len(d)} pages"
    assert d[0].get_text().count("Sampler") == 1, "title"
    for i in art_pages:
        pm = d[i].get_pixmap(dpi=24)
        mean = sum(pm.samples) / len(pm.samples)
        assert mean < 254.5, f"{path} p{i+1} renders blank (mean {mean:.1f})"
    t = d[8].get_text()
    assert "The complete" in t, f"{path}: CTA first glyph clipped"
    assert "$6.99" in t or "$4.99" in t, "prices"
    for b in U.BANNED_FRAGMENTS:
        assert b not in t.lower(), "banned fragment"
    print(f"  {path.name}: 9pp, {len(art_pages)} sample pages render, "
          f"CTA intact")


def main():
    outdir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "markets" / "samplers"
    outdir.mkdir(parents=True, exist_ok=True)
    color = outdir / "quiet-mind-color_sampler.pdf"
    journals = outdir / "quiet-mind-journals_sampler.pdf"
    build_color(color)
    build_journals(journals)
    verify(color, range(1, 8))
    verify(journals, range(1, 8))
    print(f"samplers built + verified -> {outdir}")


if __name__ == "__main__":
    main()
