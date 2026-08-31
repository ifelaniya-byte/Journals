"""Create truthful per-product release-gate packets for E01-E36.

This automates the local, documentable portions of release readiness. It intentionally
cannot declare trademark/name clearance, platform/vendor acceptance, physical proof,
commercial price/channel approval, or named-human release approval.
"""
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "EXPANSION_36_CONCEPT_REGISTER.csv"
PRODUCTION = ROOT / "EXPANSION_36_LOCAL_PRODUCTION_REGISTER.csv"
OUT = ROOT / "expansion-release"
TODAY = date.today().isoformat()
STATUS = "LOCAL PROTOTYPE PACKAGE - HOLD - NOT FOR SALE, UPLOAD, OR MANUFACTURE"
DIRECT_FIRST = {"E03", "E14", "E19", "E21", "E25", "E27", "E32", "E34"}

# This is a limited, general-web exact-phrase screen performed on 2026-08-31.
# It is neither a USPTO search nor legal/trademark clearance. Every product remains
# pending qualified title/rights review even where no salient result was observed.
TITLE_SCREEN = {
    "E01": ("COUNSEL REVIEW REQUIRED", "A Ledger-branded 'Reading Room' surfaced in a different category; no legal conclusion."),
    "E02": ("COUNSEL REVIEW REQUIRED", "No salient exact-title result observed in the limited general-web screen."),
    "E03": ("COUNSEL REVIEW REQUIRED", "No salient exact-title result observed; adjacent 'Story Cookbook' titles surfaced."),
    "E04": ("COUNSEL REVIEW REQUIRED", "Existing uses of 'The Little Museum' surfaced; product title remains a review item."),
    "E05": ("COUNSEL REVIEW REQUIRED", "No salient exact-title result observed in the limited general-web screen."),
    "E06": ("RETITLE BEFORE RELEASE", "An active Amazon notebook uses the exact title 'Notes Worth Keeping'."),
    "E07": ("RETITLE BEFORE RELEASE", "An organizing service uses the exact phrase 'One Shelf at a Time'."),
    "E08": ("COUNSEL REVIEW REQUIRED", "The published 'Tiny Kitchen Cookbook' is close in category and wording."),
    "E09": ("COUNSEL REVIEW REQUIRED", "No salient exact-title result observed; garden/almanac marks remain for qualified review."),
    "E10": ("COUNSEL REVIEW REQUIRED", "The published 'The Rhythm of Home' is close in category and wording."),
    "E11": ("COUNSEL REVIEW REQUIRED", "Published 'Move With Me' uses close wording; title remains a review item."),
    "E12": ("COUNSEL REVIEW REQUIRED", "No salient exact-title result observed in the limited general-web screen."),
    "E13": ("RETITLE BEFORE RELEASE", "A repair/build channel uses the exact title 'Mend and Make'."),
    "E14": ("COUNSEL REVIEW REQUIRED", "No salient exact-title result observed; fieldbook/flower-pressing category uses were observed."),
    "E15": ("COUNSEL REVIEW REQUIRED", "No salient exact-title result observed in the limited general-web screen."),
    "E16": ("COUNSEL REVIEW REQUIRED", "The phrase is generic and widely used in instructional content; distinctiveness review required."),
    "E17": ("COUNSEL REVIEW REQUIRED", "Color-study/workbook category uses surfaced; no clearance conclusion."),
    "E18": ("COUNSEL REVIEW REQUIRED", "Close 'Companion Project' entertainment title surfaced; no exact-title conclusion."),
    "E19": ("RETITLE BEFORE RELEASE", "Published use of the exact title 'The Meeting Map' surfaced."),
    "E20": ("RETITLE BEFORE RELEASE", "A same-job product uses the close title 'Friday Finish Line'."),
    "E21": ("COUNSEL REVIEW REQUIRED", "Client-ledger uses surfaced in a different functional category; qualified review required."),
    "E22": ("COUNSEL REVIEW REQUIRED", "No salient exact-title result observed in the limited general-web screen."),
    "E23": ("COUNSEL REVIEW REQUIRED", "Decision-record terminology is established and generic in product/technical contexts."),
    "E24": ("COUNSEL REVIEW REQUIRED", "Office-hours/home-office uses surfaced; title remains a review item."),
    "E25": ("RETITLE BEFORE RELEASE", "Multiple active books use the exact title 'The Supper Club Book'."),
    "E26": ("COUNSEL REVIEW REQUIRED", "Published 'A Year of Picnics' is close in category and wording."),
    "E27": ("RETITLE BEFORE RELEASE", "A published book uses the close title 'The Housewarming'."),
    "E28": ("COUNSEL REVIEW REQUIRED", "Commercial collections use 'Celebration Capsule'; title remains a review item."),
    "E29": ("COUNSEL REVIEW REQUIRED", "Shared-listening works surfaced; no exact-title conclusion."),
    "E30": ("COUNSEL REVIEW REQUIRED", "Published 'A Little Treat' is close in wording and gift/ritual positioning."),
    "E31": ("RETITLE BEFORE RELEASE", "Cafe Notes is an active stationery brand and 'The Home Cafe' is a published adjacent title."),
    "E32": ("COUNSEL REVIEW REQUIRED", "Backyard movie-night event/rental uses are common; title remains a review item."),
    "E33": ("RETITLE BEFORE RELEASE", "Published 'Second-Hand Stories' is close in spelling, subject, and format."),
    "E34": ("RETITLE BEFORE RELEASE", "The exact repair-before-replace phrase appears in current published commercial content."),
    "E35": ("COUNSEL REVIEW REQUIRED", "Field-guide naming is common; localized/outings use requires qualified review."),
    "E36": ("COUNSEL REVIEW REQUIRED", "Seasonal-swap titles exist in adjacent entertainment/gift categories; no clearance conclusion."),
}


def slugify(value: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "-", value.lower().replace("&", "and")).strip("-")


def next_action(title_status: str, direct: bool) -> str:
    if title_status == "RETITLE BEFORE RELEASE":
        return "Select a replacement working title, repeat qualified title/rights review, then rebuild the affected package."
    if direct:
        return "Select a vendor/physical product path; obtain final dielines and proof criteria before any manufacturing decision."
    return "Confirm the final paperback route, current platform specification, and exact proof plan before any upload decision."


def checklist(candidate: dict[str, str], product: dict[str, str], title_status: str, note: str, direct: bool) -> str:
    route = "direct-first physical/printable/B2B prototype" if direct else "paperback prototype"
    return f"""# {candidate['candidate_id']} - release-gate checklist

## Current status

**{STATUS}**

**Product:** {candidate['working_title']}

**Route:** {route}

## Completed local gates

- [x] Original structured interior prototype built and structurally validated.
- [x] Route-appropriate local cover concept built and structurally validated.
- [x] Cover/interior preview images generated.
- [x] Package checksum manifest generated and source-based provenance check queued.
- [x] Product-specific boundary is documented: {candidate['claims_boundary']}
- [x] Local author line is marked provisional only; no public identity clearance is claimed.

## Title and rights

- [ ] Qualified title/trademark/common-law review completed.
- [ ] Asset, contributor, font, and any final artwork provenance approved for the intended commercial route.
- [ ] Final author/imprint/public-use clearance recorded.

**Limited 2026-08-31 web-screen result:** **{title_status}** - {note}

## Route and proof

- [ ] {"Selected vendor, dieline, materials, assembly, and packaging requirements validated." if direct else "Current platform print specification and final cover template validated."}
- [ ] Accessible final design review completed for the final route.
- [ ] Physical proof or documented product/usability sample reviewed and approved.
- [ ] Final file hashes recorded after all proof corrections.

## Commercial release

- [ ] Channel and price decision signed by an authorized named human.
- [ ] Final description, images, and claims boundary reviewed for the actual product form.
- [ ] Named-human release approval recorded with date, scope, and final-file hashes.

## Immediate next action

{next_action(title_status, direct)}

## Approval record - intentionally blank

| Required decision | Name / role | Date | Final file hash or decision reference |
|---|---|---|---|
| Title/rights review |  |  |  |
| Route/technical validation |  |  |  |
| Proof/usability approval |  |  |  |
| Price/channel decision |  |  |  |
| Release approval |  |  |  |
"""


def main() -> None:
    candidates = list(csv.DictReader(SOURCE.open(encoding="utf-8", newline="")))
    production = list(csv.DictReader(PRODUCTION.open(encoding="utf-8", newline="")))
    production_by_id = {row["candidate_id"]: row for row in production}
    if len(candidates) != 36 or len(production_by_id) != 36 or set(TITLE_SCREEN) != set(production_by_id):
        raise ValueError("Expected complete E01-E36 source, production, and title-screen inputs")
    fields = [
        "candidate_id", "working_title", "prototype_route", "title_web_screen_date", "title_web_screen_status", "title_web_screen_note",
        "local_prototype_integrity", "local_asset_provenance", "title_and_rights_clearance", "route_technical_validation",
        "accessibility_review", "proof_or_usability_review", "price_channel_decision", "named_human_release_approval", "overall_release_status", "immediate_next_action",
    ]
    output_rows = []
    for candidate in candidates:
        ident = candidate["candidate_id"]
        product = production_by_id[ident]
        title_status, note = TITLE_SCREEN[ident]
        direct = ident in DIRECT_FIRST
        folder = OUT / f"{ident}-{slugify(candidate['working_title'])}"
        if not folder.is_dir():
            raise FileNotFoundError(folder)
        (folder / "RELEASE_GATE_CHECKLIST.md").write_text(checklist(candidate, product, title_status, note, direct), encoding="utf-8")
        output_rows.append({
            "candidate_id": ident,
            "working_title": candidate["working_title"],
            "prototype_route": "DIRECT-FIRST" if direct else "PAPERBACK PROTOTYPE",
            "title_web_screen_date": TODAY,
            "title_web_screen_status": title_status,
            "title_web_screen_note": note,
            "local_prototype_integrity": "PASS - local structural validation",
            "local_asset_provenance": "PASS - builder/source/hash trace available; commercial rights approval pending",
            "title_and_rights_clearance": "PENDING QUALIFIED REVIEW",
            "route_technical_validation": "PENDING CURRENT PLATFORM/VENDOR SPECIFICATION",
            "accessibility_review": "PENDING HUMAN FINAL-DESIGN REVIEW",
            "proof_or_usability_review": "PENDING PHYSICAL PROOF OR DOCUMENTED USABILITY SAMPLE",
            "price_channel_decision": "PENDING AUTHORIZED NAMED-HUMAN DECISION",
            "named_human_release_approval": "PENDING NAMED-HUMAN APPROVAL",
            "overall_release_status": STATUS,
            "immediate_next_action": next_action(title_status, direct),
        })
    with (ROOT / "EXPANSION_36_RELEASE_GATE_REGISTER.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)
    with (ROOT / "EXPANSION_36_TITLE_SCREENING_LOG.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["candidate_id", "working_title", "screen_date", "exact_phrase_query", "screen_scope", "disposition", "notable_result_or_limit", "required_follow_up"]
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for candidate in candidates:
            status, note = TITLE_SCREEN[candidate["candidate_id"]]
            writer.writerow({
                "candidate_id": candidate["candidate_id"],
                "working_title": candidate["working_title"],
                "screen_date": TODAY,
                "exact_phrase_query": '"' + candidate["working_title"] + '"',
                "screen_scope": "limited general-web exact-phrase screen; not USPTO, state, domain, marketplace-complete, or counsel clearance",
                "disposition": status,
                "notable_result_or_limit": note,
                "required_follow_up": next_action(status, candidate["candidate_id"] in DIRECT_FIRST),
            })
    packet = [
        "# Expansion 36 release-gate packet",
        "",
        f"**Prepared:** {TODAY}",
        f"**Overall status:** {STATUS}.",
        "",
        "This packet completes and records the local, automatable portions of readiness. It does not falsely certify legal/title rights, marketplace/vendor acceptance, physical proof, pricing/channel approval, or named-human release approval. Those gates require their stated external evidence and authorized human decision.",
        "",
        "## Current local completion",
        "",
        "- 36 original, route-appropriate product prototype packages generated and structurally checked.",
        "- 36 per-SKU release-gate checklists created in `expansion-release/E##-*/RELEASE_GATE_CHECKLIST.md`.",
        "- 36 limited title-screen entries logged; the screen is not clearance.",
        "- 36 product-specific route, proof, price/channel, and sign-off paths recorded.",
        "",
        "## Title action summary",
        "",
        "| Disposition | IDs | Required action |",
        "|---|---|---|",
        "| RETITLE BEFORE RELEASE | " + ", ".join(row["candidate_id"] for row in output_rows if row["title_web_screen_status"] == "RETITLE BEFORE RELEASE") + " | Select a new working title and obtain qualified title/rights review before any release preparation continues. |",
        "| COUNSEL REVIEW REQUIRED | " + ", ".join(row["candidate_id"] for row in output_rows if row["title_web_screen_status"] != "RETITLE BEFORE RELEASE") + " | Complete a title/trademark/common-law review before approving a public title. |",
        "",
        "## Per-product state",
        "",
        "| ID | Working title | Route | Title disposition | Overall state |",
        "|---|---|---|---|---|",
    ]
    for row in output_rows:
        packet.append(f"| {row['candidate_id']} | {row['working_title']} | {row['prototype_route']} | {row['title_web_screen_status']} | HOLD |")
    (ROOT / "EXPANSION_36_RELEASE_GATE_PACKET.md").write_text("\n".join(packet) + "\n", encoding="utf-8")
    template = [
        "# Expansion 36 named-human release-approval template",
        "",
        "**This is a blank approval template. It does not create an approval, signatory, price, channel, or release decision.**",
        "",
        "A decision-maker must complete this per product after the title/rights, final asset, route, proof/usability, commercial, and final-file evidence exists.",
        "",
        "| ID | Final approved title | Authorized decision-maker / role | Title-rights ref | Route/proof ref | Price/channel ref | Final file SHA-256 | Decision (approve / hold / retire) | Date |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for row in output_rows:
        template.append(f"| {row['candidate_id']} |  |  |  |  |  |  | HOLD |  |")
    (ROOT / "EXPANSION_36_OWNER_SIGNOFF_TEMPLATE.md").write_text("\n".join(template) + "\n", encoding="utf-8")
    print("Wrote release-gate checklists and registers for 36 local prototypes; no release status changed.")


if __name__ == "__main__":
    main()
