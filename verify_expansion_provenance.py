"""Verify the locally generated asset chain recorded in expansion package manifests."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "expansion-release"
SOURCE = ROOT / "EXPANSION_36_CONCEPT_REGISTER.csv"


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower().replace("&", "and")).strip("-")


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def fail(message: str) -> None:
    print("FAIL", message)
    raise SystemExit(1)


def main() -> None:
    rows = list(csv.DictReader(SOURCE.open(encoding="utf-8", newline="")))
    if len(rows) != 36:
        fail("source register must retain 36 candidates")
    verified = 0
    for row in rows:
        ident = row["candidate_id"]
        folder = OUT / f"{ident}-{slugify(row['working_title'])}"
        manifest_path = folder / "package_manifest.json"
        if not manifest_path.is_file():
            fail(f"{ident}: package manifest missing")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        files = manifest.get("files")
        if not isinstance(files, dict) or len(files) != 6:
            fail(f"{ident}: manifest must carry six generated asset hashes")
        for name, expected in files.items():
            path = folder / name
            if not path.is_file():
                fail(f"{ident}: asset missing from manifest chain: {name}")
            actual = digest(path)
            if actual != expected:
                fail(f"{ident}: SHA-256 mismatch for {name}")
            verified += 1
    print(f"PASS  local generated-asset provenance is intact: {verified}/216 package assets match their package manifests. Commercial rights/title clearance remains pending human review.")


if __name__ == "__main__":
    main()
