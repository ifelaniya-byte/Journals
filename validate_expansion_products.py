"""Fail-closed structural QC for the 36 controlled local expansion prototypes."""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "EXPANSION_36_CONCEPT_REGISTER.csv"
OUT = ROOT / "expansion-release"
STATUS = "LOCAL PROTOTYPE PACKAGE - HOLD - NOT FOR SALE, UPLOAD, OR MANUFACTURE"
DIRECT_FIRST = {"E03", "E14", "E19", "E21", "E25", "E27", "E32", "E34"}
FORBIDDEN = ("Mike Lowrey", "ChampagnePapi", "example.com", "YOUR AUTHOR", "Author Name")


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower().replace("&", "and")).strip("-")


def fail(message: str) -> None:
    print("FAIL", message)
    raise SystemExit(1)


def main() -> None:
    candidates = list(csv.DictReader(SOURCE.open(encoding="utf-8", newline="")))
    expected_ids = [f"E{i:02d}" for i in range(1, 37)]
    if [row["candidate_id"] for row in candidates] != expected_ids:
        fail("source candidate register must be E01 through E36 in order")
    if not OUT.is_dir():
        fail("expansion-release directory missing")
    readme = OUT / "README.md"
    if not readme.is_file() or STATUS not in readme.read_text(encoding="utf-8"):
        fail("expansion-release README missing or does not retain the complete hold notice")
    folders = sorted(path for path in OUT.iterdir() if path.is_dir())
    if len(folders) != 36:
        fail(f"expected 36 prototype directories; found {len(folders)}")
    total_pages = 0
    for candidate in candidates:
        ident, title = candidate["candidate_id"], candidate["working_title"]
        folder = OUT / f"{ident}-{slugify(title)}"
        if not folder.is_dir():
            fail(f"{ident}: expected folder missing: {folder.name}")
        direct = ident in DIRECT_FIRST
        cover = folder / ("front_cover_concept.pdf" if direct else "paperback_cover_wrap.pdf")
        forbidden_cover = folder / ("paperback_cover_wrap.pdf" if direct else "front_cover_concept.pdf")
        required = [
            folder / "interior_prototype.pdf", cover, folder / "cover_preview.jpg",
            folder / "interior_sample.jpg", folder / "PRODUCT_BRIEF.md",
            folder / "PRODUCTION_ROUTE.md", folder / "package_manifest.json",
        ]
        missing = [path.name for path in required if not path.is_file()]
        if missing:
            fail(f"{ident}: missing {', '.join(missing)}")
        if forbidden_cover.exists():
            fail(f"{ident}: incorrect route cover asset exists: {forbidden_cover.name}")
        manifest = json.loads((folder / "package_manifest.json").read_text(encoding="utf-8"))
        if manifest.get("candidate_id") != ident or manifest.get("working_title") != title:
            fail(f"{ident}: manifest identity does not match the source register")
        if manifest.get("status") != STATUS:
            fail(f"{ident}: manifest has an unsafe or unexpected status")
        if manifest.get("author") != "Arden Vellor":
            fail(f"{ident}: manifest author is not configured provisional author")
        if manifest.get("route_asset") != cover.name:
            fail(f"{ident}: manifest route asset does not match package")
        interior = folder / "interior_prototype.pdf"
        doc = fitz.open(interior)
        pages = len(doc)
        trim = tuple(float(value) for value in manifest.get("prototype_trim_inches", []))
        interior_rect = doc[0].rect
        if len(trim) != 2 or abs(interior_rect.width / 72 - trim[0]) > .02 or abs(interior_rect.height / 72 - trim[1]) > .02:
            fail(f"{ident}: interior trim does not match manifest")
        if pages < 60 or pages % 2:
            fail(f"{ident}: interior must be 60+ pages and even; got {pages}")
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        cover_doc = fitz.open(cover)
        cover_rect = cover_doc[0].rect
        cover_text = "\n".join(page.get_text() for page in cover_doc)
        if len(cover_doc) != 1:
            fail(f"{ident}: route cover asset must be exactly one page")
        if direct:
            cover_size_ok = abs(cover_rect.width / 72 - trim[0]) < .02 and abs(cover_rect.height / 72 - trim[1]) < .02
        else:
            expected_w = 2 * .125 + 2 * trim[0] + pages * .002252
            expected_h = 2 * .125 + trim[1]
            cover_size_ok = abs(cover_rect.width / 72 - expected_w) < .02 and abs(cover_rect.height / 72 - expected_h) < .02
        if not cover_size_ok:
            fail(f"{ident}: route cover geometry does not match the declared prototype path")
        cover_doc.close()
        for content_name, content in (("interior", text), ("cover", cover_text)):
            if title not in content:
                fail(f"{ident}: {content_name} missing exact working title")
            if "Arden Vellor" not in content:
                fail(f"{ident}: {content_name} missing provisional local author")
            for blocked in FORBIDDEN:
                if blocked.casefold() in content.casefold():
                    fail(f"{ident}: {content_name} contains forbidden literal {blocked!r}")
        if "NOT FOR SALE, UPLOAD, OR MANUFACTURE" not in text:
            fail(f"{ident}: interior does not carry the complete hold notice")
        if ("NOT FOR MANUFACTURE" not in cover_text if direct else "NOT FOR UPLOAD" not in cover_text):
            fail(f"{ident}: cover lacks route-specific hold notice")
        if manifest.get("prototype_page_count") != pages:
            fail(f"{ident}: manifest page count does not match interior")
        for image_path in (folder / "cover_preview.jpg", folder / "interior_sample.jpg"):
            with Image.open(image_path) as image:
                if image.width < 500 or image.height < 500:
                    fail(f"{ident}: preview image is too small: {image_path.name}")
        brief = (folder / "PRODUCT_BRIEF.md").read_text(encoding="utf-8")
        route = (folder / "PRODUCTION_ROUTE.md").read_text(encoding="utf-8")
        if STATUS not in brief or candidate["core_job"] not in brief or candidate["claims_boundary"] not in brief:
            fail(f"{ident}: product brief is incomplete")
        if "not" not in route.casefold() or "proof" not in route.casefold():
            fail(f"{ident}: production route note does not retain gating language")
        total_pages += pages
    inventory = (ROOT / "EXPANSION_36_LOCAL_PROTOTYPES.md").read_text(encoding="utf-8")
    register = list(csv.DictReader((ROOT / "EXPANSION_36_LOCAL_PRODUCTION_REGISTER.csv").open(encoding="utf-8", newline="")))
    if STATUS not in inventory or len(register) != 36:
        fail("root expansion inventory/register is incomplete")
    if [row["candidate_id"] for row in register] != expected_ids:
        fail("root local-production register IDs differ from source register")
    if any(row["status"] != STATUS for row in register):
        fail("root local-production register contains an unexpected release status")
    print(f"PASS  36/36 controlled local prototype packages; {total_pages} interior pages; all required route assets, author notices, hold boundaries, and preview assets verified.")


if __name__ == "__main__":
    main()
