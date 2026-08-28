#!/usr/bin/env python3
"""Generate the controlled multilingual / multichannel planning price model.

The canonical PORTFOLIO.md table is the only input for sellable US paperback
anchors.  This generator intentionally emits rows only for the six Wave 1
books with a canonical dollar price.  A generated planning row never changes a
KDP price, creates a listing, or authorizes translation, upload, spend, or
public deployment.

The CSV is an internal *planning model*: only its Amazon KDP paperback US
anchor rows restate currently authorized prices, and those books remain on
HOLD.  Every other row is conditional on its own file, rights, translator,
claims, distributor, pricing-floor, and named-human approvals.
"""
from __future__ import annotations

import csv
from pathlib import Path

from verify_canonical import canonical_rows

ROOT = Path(__file__).resolve().parent
PRICE_OUT = ROOT / "MULTICHANNEL_PRICING_MODEL.csv"
LANGUAGE_OUT = ROOT / "BILINGUAL_LANGUAGE_REGISTER.csv"

# Deliberate planning tiers, not catalog-wide public prices.  The values retain
# the agreed $15.99–$18.99 premium Wave 1 print positioning rather than copying
# the unrelated public repository's $9.99 price model.
PRICE_TIERS = {
    "$15.99": {"digital_en": "$8.99", "digital_bilingual": "$10.99", "bilingual_print_start": "$18.99"},
    "$16.99": {"digital_en": "$9.99", "digital_bilingual": "$11.99", "bilingual_print_start": "$19.99"},
    "$17.99": {"digital_en": "$9.99", "digital_bilingual": "$11.99", "bilingual_print_start": "$20.99"},
    "$18.99": {"digital_en": "$10.99", "digital_bilingual": "$12.99", "bilingual_print_start": "$21.99"},
}

# "State" documents whether a channel is in scope for a future model; none of
# these states means operationally live.  Platform/currency pricing must be
# confirmed in the current platform calculator by the accountable human.
CHANNELS = [
    # print/POD and print distribution
    ("Amazon KDP paperback", "English paperback", "en", "Paperback POD", "print_anchor", "US anchor only; set and verify each marketplace local price in the live KDP pricing page", "CURRENT PRICE ANCHOR / HOLD"),
    ("Amazon KDP paperback", "Bilingual paperback", "en + approved target language", "Paperback POD", "bilingual_print", "Starting point; final count, print cost, each marketplace minimum, proof, and translation QA must pass", "PLANNING ONLY"),
    ("Barnes & Noble Press", "English paperback", "en", "Paperback POD", "print_anchor", "Must be at least the current B&N print minimum; use B&N-specific cover template and proof", "PLANNING ONLY"),
    ("Barnes & Noble Press", "Bilingual paperback", "en + approved target language", "Paperback POD", "bilingual_print", "Must be at least the current B&N print minimum; separate final file, cover, proof, and rights review", "PLANNING ONLY"),
    ("Lulu Bookstore", "English paperback", "en", "Paperback POD", "print_anchor", "Use only if live Lulu print cost permits the anchor; independently confirm current calculator", "PLANNING ONLY"),
    ("Lulu Bookstore", "Bilingual paperback", "en + approved target language", "Paperback POD", "bilingual_print", "Use final bilingual page count and Lulu calculator; no auto-upload", "PLANNING ONLY"),
    ("Lulu Global Distribution", "English paperback", "en", "Paperback POD / distribution", "lulu_global", "Price must cover current Lulu Global minimum; do not create a duplicate Amazon/B&N/Ingram listing", "PARKED — CHANNEL CONFLICT REVIEW"),
    ("Lulu Global Distribution", "Bilingual paperback", "en + approved target language", "Paperback POD / distribution", "lulu_global_bilingual", "Price must cover current Lulu Global minimum after final page count; do not create duplicate retail listings", "PARKED — CHANNEL CONFLICT REVIEW"),
    ("IngramSpark", "English paperback", "en", "Paperback POD / distribution", "ingram", "Requires a publisher-owned ISBN, wholesale/returns decision, current print quote, and no duplicate distributor path", "PARKED — ISBN / DISTRIBUTION REVIEW"),
    ("IngramSpark", "Bilingual paperback", "en + approved target language", "Paperback POD / distribution", "ingram_bilingual", "Requires a separate ISBN, final bilingual pagination, wholesale/returns decision, print quote, and no duplicate distributor path", "PARKED — ISBN / DISTRIBUTION REVIEW"),
    ("Pothi store (India)", "English paperback", "en", "Paperback POD", "local_print_quote", "India route; price and eligibility require a current Pothi calculator/account review", "PARKED — REGIONAL ELIGIBILITY REVIEW"),
    ("Pothi store (India)", "Bilingual paperback", "en + Hindi", "Paperback POD", "local_print_quote", "Hindi pairing only after qualified Hindi review; current local quote/account review required", "PARKED — REGIONAL ELIGIBILITY REVIEW"),
    ("Blurb Bookstore", "English paperback", "en", "Print on demand", "local_print_quote", "Use only if current project format, print quote, and value proposition pass; no duplicate distribution setup", "PARKED — ECONOMICS REVIEW"),
    ("Bookvault + owned checkout", "English paperback", "en", "Fulfilment, not a retail store", "fulfilment_quote", "Requires an approved owned checkout, tax/privacy review, and fulfilment quote", "PARKED — OWNED-STORE REVIEW"),
    # retailer e-books (new, separately approved fixed-layout/reflowable editions)
    ("Amazon Kindle", "English eBook", "en", "EPUB / Kindle eBook", "digital_en", "A separately built accessible digital edition; no KDP Select while the same digital edition is non-exclusively sold elsewhere", "PARKED — DIGITAL FILE / RIGHTS REVIEW"),
    ("Amazon Kindle", "Bilingual eBook", "en + approved target language", "EPUB / Kindle eBook", "digital_bilingual", "One language pair per distinct edition; final language metadata, accessibility, claims, and rights review required", "PARKED — DIGITAL FILE / RIGHTS REVIEW"),
    ("Apple Books", "English eBook", "en", "EPUB", "digital_en", "Requires a validated EPUB and Apple account/tax setup; do not use a PDF as a substitute", "PARKED — DIGITAL FILE / ACCOUNT REVIEW"),
    ("Apple Books", "Bilingual eBook", "en + approved target language", "EPUB", "digital_bilingual", "Separate ISBN/identifier where required, validated EPUB, language metadata, and qualified language review", "PARKED — DIGITAL FILE / RIGHTS REVIEW"),
    ("Google Play Books", "English digital edition", "en", "EPUB preferred; PDF only when appropriate", "digital_en", "Set country rights and local currency prices in Partner Center; final format/accessibility/territory review required", "PARKED — DIGITAL FILE / TERRITORY REVIEW"),
    ("Google Play Books", "Bilingual digital edition", "en + approved target language", "EPUB preferred; PDF only when appropriate", "digital_bilingual", "Set language and territory rights per edition; final format/accessibility/claims/translation review required", "PARKED — DIGITAL FILE / TERRITORY REVIEW"),
    ("Kobo Writing Life", "English eBook", "en", "EPUB", "digital_en", "Requires validated EPUB, country rights, tax/payment setup, and store metadata review", "PARKED — DIGITAL FILE / ACCOUNT REVIEW"),
    ("Kobo Writing Life", "Bilingual eBook", "en + approved target language", "EPUB", "digital_bilingual", "One language pair per edition; requires a validated EPUB and language/rights/claims review", "PARKED — DIGITAL FILE / RIGHTS REVIEW"),
    ("Barnes & Noble Press eBook", "English eBook", "en", "EPUB", "digital_en", "Separate eBook project/file and current B&N platform validation required", "PARKED — DIGITAL FILE / ACCOUNT REVIEW"),
    ("Barnes & Noble Press eBook", "Bilingual eBook", "en + approved target language", "EPUB", "digital_bilingual", "Separate language-pair eBook project; final accessibility and translation QA required", "PARKED — DIGITAL FILE / RIGHTS REVIEW"),
    # controlled direct sales: same approved digital edition, not duplicate physical listings
    ("Payhip", "English print-at-home PDF", "en", "PDF", "digital_en", "Requires approved accessible PDF, rights/tax/privacy policy, and human-owned checkout", "PARKED — DIRECT-COMMERCE REVIEW"),
    ("Payhip", "Bilingual print-at-home PDF", "en + approved target language", "PDF", "digital_bilingual", "Requires final bilingual PDF, translation QA, rights/tax/privacy policy, and human-owned checkout", "PARKED — DIRECT-COMMERCE REVIEW"),
    ("Gumroad", "English print-at-home PDF", "en", "PDF", "digital_en", "Requires approved accessible PDF, rights/tax/privacy policy, and human-owned checkout", "PARKED — DIRECT-COMMERCE REVIEW"),
    ("Gumroad", "Bilingual print-at-home PDF", "en + approved target language", "PDF", "digital_bilingual", "Requires final bilingual PDF, translation QA, rights/tax/privacy policy, and human-owned checkout", "PARKED — DIRECT-COMMERCE REVIEW"),
    ("Ko-fi Shop", "English print-at-home PDF", "en", "PDF", "digital_en", "Requires approved accessible PDF, rights/tax/privacy policy, and human-owned checkout", "PARKED — DIRECT-COMMERCE REVIEW"),
    ("Ko-fi Shop", "Bilingual print-at-home PDF", "en + approved target language", "PDF", "digital_bilingual", "Requires final bilingual PDF, translation QA, rights/tax/privacy policy, and human-owned checkout", "PARKED — DIRECT-COMMERCE REVIEW"),
    ("itch.io", "English print-at-home PDF", "en", "PDF", "digital_en", "Use only if current content/category/account terms suit a book; rights/tax/privacy review required", "PARKED — PLATFORM-FIT REVIEW"),
    ("itch.io", "Bilingual print-at-home PDF", "en + approved target language", "PDF", "digital_bilingual", "Use only if current content/category/account terms suit a book; translation/rights/tax/privacy review required", "PARKED — PLATFORM-FIT REVIEW"),
    ("Lemon Squeezy", "English print-at-home PDF", "en", "PDF", "digital_en", "Requires human-approved merchant-of-record, tax, privacy, and file-delivery setup", "PARKED — DIRECT-COMMERCE REVIEW"),
    ("Lemon Squeezy", "Bilingual print-at-home PDF", "en + approved target language", "PDF", "digital_bilingual", "Requires human-approved merchant-of-record, tax, privacy, and final translation/file QA", "PARKED — DIRECT-COMMERCE REVIEW"),
    ("Whop", "English print-at-home PDF", "en", "PDF", "digital_en", "Requires human-approved marketplace fit, tax/privacy, and file-delivery setup", "PARKED — PLATFORM-FIT REVIEW"),
    ("Whop", "Bilingual print-at-home PDF", "en + approved target language", "PDF", "digital_bilingual", "Requires human-approved marketplace fit, tax/privacy, and final translation/file QA", "PARKED — PLATFORM-FIT REVIEW"),
    ("Buy Me a Coffee", "English print-at-home PDF", "en", "PDF", "digital_en", "Requires current platform-fit, tax/privacy, and human-owned checkout review", "PARKED — PLATFORM-FIT REVIEW"),
    ("Buy Me a Coffee", "Bilingual print-at-home PDF", "en + approved target language", "PDF", "digital_bilingual", "Requires current platform-fit, tax/privacy, and final translation/file QA", "PARKED — PLATFORM-FIT REVIEW"),
    ("Etsy", "English print-at-home PDF", "en", "PDF", "digital_en", "Requires current seller-fee, tax, IP, marketplace-policy, and human-owned-shop review", "PARKED — MARKETPLACE REVIEW"),
    ("Etsy", "Bilingual print-at-home PDF", "en + approved target language", "PDF", "digital_bilingual", "Requires current seller-fee, tax, IP, marketplace-policy, and translation QA review", "PARKED — MARKETPLACE REVIEW"),
    ("Shopify / WooCommerce / Big Cartel", "Owned-checkout digital edition", "en or approved bilingual pair", "Owned checkout", "digital_by_edition", "Not retailers; only consider after domain, hosting, payment, tax, privacy, customer-data, and security approvals", "PARKED — OWNED-STORE REVIEW"),
]

LANGUAGES = [
    ("Spanish", "es", "Latin", "English + Spanish", "Qualified Spanish literary/editorial translator plus in-market proofreader", "No live text yet"),
    ("French", "fr", "Latin", "English + French", "Qualified French literary/editorial translator plus in-market proofreader", "No live text yet"),
    ("Hindi", "hi", "Devanagari", "English + Hindi", "Qualified Hindi translator, Devanagari typesetter, and in-market proofreader", "No live text yet"),
    ("Simplified Chinese", "zh-Hans", "Simplified Han", "English + Simplified Chinese", "Qualified Simplified-Chinese translator, CJK typesetter, and in-market proofreader", "No live text yet"),
    ("Hausa", "ha", "Latin", "English + Hausa", "Qualified Hausa translator and in-market proofreader", "No live text yet"),
    ("Yorùbá", "yo", "Latin with tonal diacritics", "English + Yorùbá", "Qualified Yorùbá translator and proofreader who checks all tonal diacritics", "No live text yet"),
]


def list_price(rule: str, tier: dict[str, str], anchor: str) -> str:
    if rule == "print_anchor":
        return anchor
    if rule == "bilingual_print":
        return tier["bilingual_print_start"]
    if rule in {"lulu_global", "ingram"}:
        return anchor
    if rule in {"lulu_global_bilingual", "ingram_bilingual"}:
        return tier["bilingual_print_start"]
    if rule == "digital_en":
        return tier["digital_en"]
    if rule == "digital_bilingual":
        return tier["digital_bilingual"]
    return "TBD — live local calculator / approved economics required"


def price_posture(rule: str) -> str:
    if rule == "print_anchor":
        return "Canonical US Wave 1 anchor; listing still HOLD"
    if rule in {"bilingual_print", "lulu_global_bilingual", "ingram_bilingual"}:
        return "Proposed bilingual starting point; final page-count/cost calculation controls"
    if rule in {"lulu_global", "ingram"}:
        return "Proposed only; live distributor price floor and no-duplicate rule control"
    if rule in {"digital_en", "digital_bilingual"}:
        return "Proposed digital-edition price; no approved digital edition exists"
    return "No price set; channel-specific quote / approval required"


def main() -> None:
    canonical = canonical_rows()
    wave1 = {
        sku: row for sku, row in canonical.items()
        if row["release_wave"] == "Wave 1" and row["price"] in PRICE_TIERS
    }
    if len(wave1) != 6:
        raise ValueError(f"Expected six priced Wave 1 rows, found {len(wave1)}")

    with PRICE_OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "sku", "canonical_title", "release_wave", "publication_status", "edition", "language_scope",
            "channel", "delivery_format", "planned_list_price_usd", "price_posture",
            "channel_floor_or_dependency", "operational_state",
        ])
        writer.writeheader()
        for sku, product in sorted(wave1.items()):
            tier = PRICE_TIERS[product["price"]]
            for channel, edition, language_scope, fmt, rule, dependency, state in CHANNELS:
                writer.writerow({
                    "sku": sku,
                    "canonical_title": product["amazon_title"],
                    "release_wave": product["release_wave"],
                    "publication_status": product["publication_status"],
                    "edition": edition,
                    "language_scope": language_scope,
                    "channel": channel,
                    "delivery_format": fmt,
                    "planned_list_price_usd": list_price(rule, tier, product["price"]),
                    "price_posture": price_posture(rule),
                    "channel_floor_or_dependency": dependency,
                    "operational_state": state,
                })

    with LANGUAGE_OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "target_language", "language_code", "script", "bilingual_pair", "required_qualified_review", "current_state",
        ])
        writer.writeheader()
        for language, code, script, pair, review, state in LANGUAGES:
            writer.writerow({
                "target_language": language,
                "language_code": code,
                "script": script,
                "bilingual_pair": pair,
                "required_qualified_review": review,
                "current_state": state,
            })

    print(f"Wrote {PRICE_OUT.name}: {len(wave1) * len(CHANNELS)} rows")
    print(f"Wrote {LANGUAGE_OUT.name}: {len(LANGUAGES)} target languages")


if __name__ == "__main__":
    main()
