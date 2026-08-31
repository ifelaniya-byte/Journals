#!/usr/bin/env python3
"""Structural QC for the 18-concept Ritual Library catalog and 36 held local prototypes.

The canonical catalog has six Wave 1 KDP upload candidates, nine held book-form options,
two private book-form reference assets, and one non-KDP calendar (A03). This validator
confirms that canonical book artifacts agree with CATALOG.csv, that A03 remains non-KDP,
and that pricing, multichannel-model, translation-source, candidate-research, author, and
local-prototype guards pass. The 36 expansion packages remain held outside the canonical
portfolio. Structural QC is not KDP Previewer, physical proofing, translation review, legal
review, or release authorization.
"""
from pathlib import Path
import csv
import json
import re
import subprocess
import sys

import fitz
from PIL import Image

R = Path(__file__).resolve().parent
CAT = R / "CATALOG.csv"
BRAND = json.loads((R / "brand_config.json").read_text(encoding="utf-8"))
IMPRINT = BRAND.get("imprint", "").strip()
AUTHOR = BRAND.get("author", "").strip()
DOMAIN = BRAND.get("domain", "").strip()
BLEED = 0.125
PPI = 0.002252
fails: list[str] = []
passed = 0


def check(ok: bool, label: str) -> None:
    global passed
    if ok:
        passed += 1
    else:
        fails.append(label)


def is_non_kdp(row: dict[str, str]) -> bool:
    return row["publication_status"].startswith("NOT A KDP PRODUCT")


rows = list(csv.DictReader(CAT.open(encoding="utf-8")))
check(len(rows) == 18, "catalog must have 18 product concepts")
required_policy_fields = {"release_wave", "publication_status", "primary_validation", "release_trigger"}
check(required_policy_fields.issubset(rows[0].keys()), "catalog release-policy columns present")
check(sum(r.get("release_wave") == "Wave 1" for r in rows) == 6, "exactly six Wave 1 candidates")
check(sum(r.get("release_wave") == "Wave 2" for r in rows) == 9, "exactly nine Wave 2 conditional options")
check(sum(r.get("release_wave") == "Vault" for r in rows) == 3, "exactly three Vault/non-KDP products")
check(bool(IMPRINT) and IMPRINT not in {"[Author / Imprint]", "Author / Imprint"}, "working imprint is configured")
check(bool(AUTHOR) and AUTHOR not in {"[Author / Imprint]", "Author / Imprint"}, "owner-directed provisional author attribution is configured")

print(f"{'ID':<4} {'PRODUCT':<32} {'PG':>4} {'TRIM':>10} {'INT':>3} {'WRAP':>4} {'META':>4} {'IMG':>3}")
for row in rows:
    if is_non_kdp(row):
        brief = R / row["folder"] / "PRODUCT_BRIEF.md"
        ok = (
            row["id"] == "A03"
            and row["release_wave"] == "Vault"
            and row["price"].startswith("N/A")
            and row["trim"] == "10x12"
            and "wire-bound wall calendar" in row["format"].lower()
            and brief.is_file()
        )
        check(ok, "A03 remains a non-KDP calendar with its product brief")
        print(f"{row['id']:<4} {row['cover_title'][:32]:<32} {'N/A':>4} {'10x12':>10} {'N/A':>3} {'N/A':>4} {'N/A':>4} {'N/A':>3}")
        continue

    folder = R / row["folder"]
    trim = tuple(map(float, row["trim"].split("x")))
    pages = int(row["pages"])
    required = [
        "interior.pdf", "cover_wrap.pdf", "cover.jpg", "listing_02_interior.jpg",
        "listing_03_interior.jpg", "listing_04_interior.jpg", "listing_05_interior.jpg",
        "listing_06_callout.jpg", "listing_07_series.jpg", "metadata.txt",
    ]
    inventory_ok = all((folder / name).exists() for name in required)
    interior_ok = wrap_ok = metadata_ok = images_ok = identity_ok = False
    if inventory_ok:
        interior = fitz.open(folder / "interior.pdf")
        rect = interior[0].rect
        interior_ok = (
            len(interior) == pages
            and abs(rect.width / 72 - trim[0]) < 0.02
            and abs(rect.height / 72 - trim[1]) < 0.02
            and bool(interior[0].get_text().strip())
        )
        first_pages = "\n".join(interior[i].get_text() for i in range(min(2, len(interior))))
        interior.close()
        wrap = fitz.open(folder / "cover_wrap.pdf")
        rect = wrap[0].rect
        spine = pages * PPI
        expected_w = 2 * BLEED + 2 * trim[0] + spine
        expected_h = 2 * BLEED + trim[1]
        wrap_text = wrap[0].get_text()
        wrap_ok = (
            len(wrap) == 1
            and abs(rect.width / 72 - expected_w) < 0.02
            and abs(rect.height / 72 - expected_h) < 0.02
            and "BARCODE KEEP-CLEAR AREA" in wrap_text
        )
        wrap.close()
        metadata = (folder / "metadata.txt").read_text(encoding="utf-8")
        fields = [
            "AMAZON TITLE:", "COVER TITLE:", "SUBTITLE:", "AUTHOR:", "SERIES:",
            "FORMAT:", "TRIM:", "PAGES:", "PRICE:", "CATEGORIES:", "KEYWORDS:",
            "DESCRIPTION:", "CLAIMS / RELEASE BOUNDARY:",
        ]
        match = re.search(r"^KEYWORDS:\s*(.*)$", metadata, re.M)
        keywords = [part.strip() for part in match.group(1).split(",") if part.strip()] if match else []
        metadata_ok = all(field in metadata for field in fields) and len(keywords) == 7
        identity_ok = (
            f"AUTHOR: {AUTHOR}" in metadata
            and AUTHOR in first_pages
            and AUTHOR.lower() in wrap_text.lower()
            and not any(token in (first_pages + "\n" + metadata + "\n" + wrap_text) for token in ("[Author / Imprint]", "[yourdomain.example]", "yourdomain.example", "[URL]"))
        )
        images_ok = True
        for name in required[2:9]:
            try:
                image = Image.open(folder / name)
                if image.width < 900 or image.height < 900:
                    images_ok = False
            except Exception:
                images_ok = False
    check(inventory_ok and interior_ok and wrap_ok and metadata_ok and images_ok and identity_ok, row["id"])
    print(f"{row['id']:<4} {row['cover_title'][:32]:<32} {pages:>4} {trim[0]:>4g}x{trim[1]:<4g} {'OK' if interior_ok else 'NO':>3} {'OK' if wrap_ok else 'NO':>4} {'OK' if metadata_ok else 'NO':>4} {'OK' if images_ok else 'NO':>3}")

upload = (R / "UPLOAD_CHECKLIST.md").read_text(encoding="utf-8")
check(len(re.findall(r"^## [AB]\d+", upload, re.M)) == 6, "upload checklist must list only six Wave 1 KDP scouts")
check("## A03" not in upload and "## A09" not in upload and "## B17" not in upload, "non-Wave-1 products are excluded from upload checklist")
lookbook = fitz.open(R / "LOOKBOOK.pdf")
check(len(lookbook) == 18, "lookbook must have title + 17 book-format reference pages; A03 is a calendar brief")
lookbook.close()
check(all((R / name).exists() for name in [
    "MARKETING.md", "LEGAL_AND_CLAIMS.md", "00_START_HERE.md", "RELEASE_POLICY.md",
    "PORTFOLIO.md", "WAVE1_HUMAN_QA.md", "KDP_ACCOUNT_OPERATIONS.md", "POLISH_NOTES.md",
    "PREPUBLICATION_SEQUENCE.md", "QR_AND_AUDIO.md", "QR_AUDIO_REVIEW.md", "TRADEMARK_SCREENING.md",
    "DECISIONS.md", "verify_pricing.py", "verify_canonical.py", "AUTOMATION_POLICY.md", "COUNSEL_ENGAGEMENT_EMAIL.md", "GITHUB_PUBLIC_EXPOSURE_AUDIT.md",
    "MULTILINGUAL_MULTICHANNEL_MODEL.md", "BILINGUAL_LANGUAGE_REGISTER.csv", "MULTICHANNEL_PRICING_MODEL.csv",
    "SALE_READINESS_COMPLETION_MATRIX.md", "WAVE1_COUNSEL_AND_FINALIZATION_PACKET.md", "TRANSLATION_HANDOFF_PACKAGE.md", "TRANSLATION_SOURCE_MANIFEST.csv",
    "EXPANSION_36_RESEARCH_AND_STAGE_GATE.md", "EXPANSION_36_CONCEPT_REGISTER.csv", "EXPANSION_36_LOCAL_PROTOTYPES.md", "EXPANSION_36_LOCAL_PRODUCTION_REGISTER.csv",
    "build_expansion_products.py", "validate_expansion_products.py", "verify_expansion_36.py", "verify_author_attribution.py",
    "build_multichannel_pricing.py", "verify_multichannel_pricing.py", "build_translation_manifest.py", "verify_translation_manifest.py",
]), "operating, price-control, multilingual, readiness, and expansion-control docs present")
check((R / "configure_wave1_qr.py").is_file() and (R / "qr-routing" / "worker.js").is_file(), "QR routing/stamp tooling present")
if DOMAIN:
    route_file = R / "qr-routing" / "routes.json"
    route_data = json.loads(route_file.read_text(encoding="utf-8")) if route_file.exists() else {}
    check(route_data.get("domain") == DOMAIN and len(route_data.get("routes", [])) == 6, "configured QR route map has six candidate routes")
    check(all((R / "qr-routing" / "site" / "audio" / name).is_file() for name in [
        "A01-arrive.mp3", "A04-soften.mp3", "A05-harbor.mp3", "B10-settle.mp3", "B12-enough.mp3", "B18-clarity.mp3",
    ]), "six Wave 1 draft audio files present")
    check(all((R / "qr-routing" / "site" / "listen" / name / "index.html").is_file() for name in [
        "arrive", "soften", "harbor", "settle", "enough", "clarity",
    ]), "six Wave 1 candidate landing pages present")

price_check = subprocess.run([sys.executable, str(R / "verify_pricing.py")], cwd=R, text=True, capture_output=True)
print("\n--- Wave 1 price-control guard ---")
print(price_check.stdout.rstrip())
if price_check.stderr:
    print(price_check.stderr.rstrip())
check(price_check.returncode == 0, "Wave 1 prices match the canonical DECISIONS.md table")

canonical_check = subprocess.run([sys.executable, str(R / "verify_canonical.py")], cwd=R, text=True, capture_output=True)
print("\n--- Canonical product-control guard ---")
print(canonical_check.stdout.rstrip())
if canonical_check.stderr:
    print(canonical_check.stderr.rstrip())
check(canonical_check.returncode == 0, "all decision-bound catalog fields match PORTFOLIO.md")

market_model_check = subprocess.run([sys.executable, str(R / "verify_multichannel_pricing.py")], cwd=R, text=True, capture_output=True)
print("\n--- Multichannel pricing-model guard ---")
print(market_model_check.stdout.rstrip())
if market_model_check.stderr:
    print(market_model_check.stderr.rstrip())
check(market_model_check.returncode == 0, "multichannel model retains canonical Wave 1 anchors and non-live bilingual scope")

translation_check = subprocess.run([sys.executable, str(R / "verify_translation_manifest.py")], cwd=R, text=True, capture_output=True)
print("\n--- Translation-source lock guard ---")
print(translation_check.stdout.rstrip())
if translation_check.stderr:
    print(translation_check.stderr.rstrip())
check(translation_check.returncode == 0, "translation handoff manifest retains frozen English source digests and non-live status")

author_check = subprocess.run([sys.executable, str(R / "verify_author_attribution.py")], cwd=R, text=True, capture_output=True)
print("\n--- Provisional author-attribution guard ---")
print(author_check.stdout.rstrip())
if author_check.stderr:
    print(author_check.stderr.rstrip())
check(author_check.returncode == 0, "owner-directed provisional author attribution is consistent across governed local products")

expansion_check = subprocess.run([sys.executable, str(R / "verify_expansion_36.py")], cwd=R, text=True, capture_output=True)
print("\n--- Expansion-candidate guard ---")
print(expansion_check.stdout.rstrip())
if expansion_check.stderr:
    print(expansion_check.stderr.rstrip())
check(expansion_check.returncode == 0, "36 expansion candidates remain unique, low-claim research records outside the governed portfolio")

prototype_check = subprocess.run([sys.executable, str(R / "validate_expansion_products.py")], cwd=R, text=True, capture_output=True)
print("\n--- Expansion local-prototype guard ---")
print(prototype_check.stdout.rstrip())
if prototype_check.stderr:
    print(prototype_check.stderr.rstrip())
check(prototype_check.returncode == 0, "36 expansion packages are complete controlled local prototypes with hold boundaries")

print(f"\nChecks passed: {passed}/40")
if fails:
    print("FAILURES:", "; ".join(fails))
    raise SystemExit(1)
print("STRUCTURAL QC PASSED — 18 canonical concepts / 36 held local prototypes; not release authorization.")
