#!/usr/bin/env python3
"""Prepublication metadata boundary audit.

This is a conservative editorial flagger, not legal advice or a marketplace-policy oracle. It
checks title/subtitle/keywords/description blocks for terms that require a reviewer decision.
It deliberately permits the generic phrase “GLP-1” only in A01’s reviewed candidate context;
all findings must be read by a human.
"""
from pathlib import Path
import csv, re, sys

ROOT = Path(__file__).resolve().parent
ROWS = list(csv.DictReader((ROOT / "CATALOG.csv").open(encoding="utf-8")))

# Third-party medication marks should not silently migrate into customer-facing metadata.
TRADEMARK_OR_MEDICATION = re.compile(r"\b(ozempic|wegovy|mounjaro|zepbound|rybelsus|saxenda)\b", re.I)
# Outcome / advice language requires an explicit reviewer decision in this category.
OUTCOME_OR_ADVICE = re.compile(r"\b(treats?|cures?|diagnos(?:e|es|ed|ing)|medical[- ]grade|guarantee(?:s|d)?|clinically proven|injection instructions?|investment advice|tax advice|legal advice)\b", re.I)
THERAPY_LANGUAGE = re.compile(r"\b(art therapy|couples therapy|therapy journal|hypnotherapy|sleep treatment|anxiety treatment|vagus nerve stimulation|improve[sd]? hrv)\b", re.I)
# These terms are not automatically prohibited, but they are especially important in health-adjacent copy.
ROUTINE_REVIEW = re.compile(r"\b(dose(?:s|d|ing)?|prescrib(?:e|ing)|medication|injection)\b", re.I)

fails = []
flags = []
print(f"{'ID':<4} {'PRODUCT':<30} STATUS")
for row in ROWS:
    folder = ROOT / row["folder"]
    text = (folder / "metadata.txt").read_text(encoding="utf-8")
    # Metadata text intended for KDP and advertising begins before the release-boundary section.
    public = text.split("CLAIMS / RELEASE BOUNDARY:", 1)[0]
    hits = []
    for label, rx in [("trademark/medication", TRADEMARK_OR_MEDICATION), ("outcome/advice", OUTCOME_OR_ADVICE), ("therapy/treatment", THERAPY_LANGUAGE), ("routine-context", ROUTINE_REVIEW)]: 
        found = sorted({x.group(0) for x in rx.finditer(public)})
        if found:
            hits.append(f"{label}: {', '.join(found)}")
    # GLP-1 requires review but is not automatically an error for the dedicated candidate scout.
    if re.search(r"\bGLP-?1\b", public, re.I):
        hits.append("GLP-1: verify healthcare-marketing review")
    if hits:
        flags.append((row["id"], row["cover_title"], hits))
        print(f"{row['id']:<4} {row['cover_title'][:30]:<30} REVIEW — {'; '.join(hits)}")
    else:
        print(f"{row['id']:<4} {row['cover_title'][:30]:<30} CLEAR OF AUTOMATED FLAGS")

print("\nRESULT")
if flags:
    print(f"{len(flags)} SKU(s) require human review. This is expected for health-adjacent products; it does not authorize release.")
    # Trade marks and outcome/advice phrases are hard stops; generic GLP-1-only marker is a required legal review.
    hard = [f for f in flags if any('trademark/medication' in x or 'outcome/advice' in x or 'therapy/treatment' in x for x in f[2])]
    if hard:
        print("HARD-STOP FLAGS:", "; ".join(x[0] for x in hard)); sys.exit(1)
    print("No hard-stop string flags. Complete documented human/legal review before release.")
else:
    print("No automated flags found. Complete documented human/legal review before release.")
