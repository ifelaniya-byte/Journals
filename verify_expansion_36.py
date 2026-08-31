#!/usr/bin/env python3
"""Verify the non-production 36-candidate expansion register.

A passing result proves only that the research register is internally unique,
complete, and outside the governed 18-SKU portfolio. It never authorizes a
candidate for production, sale, upload, pricing, identity use, or translation.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REGISTER = ROOT / "EXPANSION_36_CONCEPT_REGISTER.csv"
EXPECTED = [f"E{number:02d}" for number in range(1, 37)]
STATUS = "CANDIDATE — not in portfolio; no production or sale authorization"
REQUIRED = {
    "candidate_id", "working_title", "subtitle_concept", "primary_niche", "core_job",
    "primary_format", "route_recommendation", "differentiation", "claims_boundary",
    "seasonality", "first_test", "production_status",
}
# Screen fields that define the offer, not the claims-boundary field that explicitly
# names excluded subject matter to prevent accidental drift into sensitive niches.
EXCLUDED_OFFER_TERMS = (
    "therapy", "medical", "health", "caregiv", "finance", "financial", "relationship",
    "mental", "diagnos", "treatment", "nutrition", "medication", "glp-1",
)


def norm(value: str) -> str:
    return " ".join(value.casefold().split())


def main() -> int:
    try:
        with REGISTER.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = set(reader.fieldnames or [])
            rows = list(reader)
        with (ROOT / "CATALOG.csv").open(encoding="utf-8", newline="") as handle:
            catalog = list(csv.DictReader(handle))
    except (OSError, csv.Error) as error:
        print(f"FAIL  cannot read expansion control source: {error}")
        return 1

    errors: list[str] = []
    if fields != REQUIRED:
        errors.append("register schema differs from the controlled 12-column schema")
    if len(rows) != 36:
        errors.append(f"register must contain 36 candidates, found {len(rows)}")
    ids = [row.get("candidate_id", "") for row in rows]
    if ids != EXPECTED:
        errors.append("candidate IDs must be exactly E01 through E36 in order")

    titles = [norm(row.get("working_title", "")) for row in rows]
    jobs = [norm(row.get("core_job", "")) for row in rows]
    if any(not title for title in titles):
        errors.append("every candidate must have a working title")
    if len(set(titles)) != len(titles):
        errors.append("working titles must be unique")
    if any(not job for job in jobs):
        errors.append("every candidate must have a primary customer job")
    if len(set(jobs)) != len(jobs):
        errors.append("primary customer jobs must be unique")

    governed_titles = {norm(row["amazon_title"]) for row in catalog}
    governed_titles.update(norm(row["cover_title"]) for row in catalog)
    collisions = sorted(set(titles) & governed_titles)
    if collisions:
        errors.append("candidate title collides with a governed catalog title: " + "; ".join(collisions))

    for row in rows:
        identifier = row.get("candidate_id", "unknown")
        for field in REQUIRED:
            if not row.get(field, "").strip():
                errors.append(f"{identifier}: required field {field} is blank")
        if row.get("production_status") != STATUS:
            errors.append(f"{identifier}: production status must remain the non-production candidate state")
        offer_text = " ".join(row.get(field, "") for field in (
            "working_title", "subtitle_concept", "primary_niche", "core_job",
        )).casefold()
        found = [term for term in EXCLUDED_OFFER_TERMS if term in offer_text]
        if found:
            errors.append(f"{identifier}: offer definition conflicts with sensitive-niche exclusion: {', '.join(found)}")

    if errors:
        for error in errors:
            print("FAIL ", error)
        print(f"\nExpansion-register verification blocked: {len(errors)} issue(s).")
        return 1
    print("PASS  36 unique, low-claim candidate concepts are complete in the expansion register and remain outside the governed 18-SKU portfolio.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
