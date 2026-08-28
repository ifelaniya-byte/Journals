"""Print-price floors by channel. Verified 28 Aug 2026.

Hard catalog floors (same number for every title) vs formula floors
(each title gets its own minimum). Round every list price up to x.99.
Never go below $9.99 on a store that allows it — that is our KDP 60% house floor.
B&N Press is the exception: the form refuses anything under $14.99.
"""

from __future__ import annotations

import math
from typing import Callable

HOUSE = 9.99
BN_FLOOR = 14.99  # B&N Press, 22 Apr 2026


def round_99(x: float) -> float:
    """Smallest N.99 that is >= x."""
    if x <= 0.99:
        return 0.99
    n = math.floor(x)
    cand = n + 0.99
    if cand + 1e-9 < x:
        cand += 1.0
    return round(cand, 2)


def kdp_print(pages: int) -> float:
    return round(0.85 + 0.012 * pages, 4)


def lulu_print(t: dict) -> float:
    """Estimate. Confirm in Lulu's calculator before upload.
    2026 B&W 6×9 comps: ~$3.74 @ 100p, ~$5.84 @ 200p.
    """
    pages = t["pages"]
    tw, th = t["trim"]
    base = 1.64 + 0.021 * pages
    if tw >= 8.0 or th >= 10.5:
        base *= 1.22
    return round(base, 2)


def ingram_print(t: dict) -> float:
    """Estimate. Confirm in Ingram compensation calculator.
    2026 B&W 6×9 comps: ~$2.79 @ 100p, ~$4.25 @ 200p.
    """
    pages = t["pages"]
    tw, _ = t["trim"]
    base = 1.33 + 0.0146 * pages
    if tw >= 8.0:
        base *= 1.15
    return round(base, 2)


def price_kdp(_t: dict) -> float:
    return HOUSE


def price_bn(_t: dict) -> float:
    return BN_FLOOR


def price_lulu_global(t: dict) -> float:
    # Official: list >= 2 × print cost for Global Distribution.
    return round_99(max(2.0 * lulu_print(t), HOUSE))


def price_lulu_bookstore(_t: dict) -> float:
    return HOUSE


def price_digital(_t: dict) -> float:
    return HOUSE


def price_ingram(t: dict) -> float:
    # 55% wholesale + 1.875% market access ≈ 0.43125 left for print + royalty.
    # Minimum for non-negative compensation, then house floor.
    p = ingram_print(t) / 0.43125
    return round_99(max(p, HOUSE))


CHANNELS = [
    {
        "id": "KDP",
        "name": "Amazon KDP paperback",
        "price_fn": price_kdp,
        "go": True,
        "pack": "KDP-Complete-Kit",
        "why": "No catalog floor. $9.99 unlocks 60% royalty. Print-cost min is well below that for these page counts.",
        "upfront": "$0",
        "cut": "40% of list (60% royalty) + print",
    },
    {
        "id": "BN",
        "name": "Barnes & Noble Press paperback",
        "price_fn": price_bn,
        "go": True,
        "pack": "MARKETS/BN-Press",
        "why": "Hard floor $14.99 since 22 Apr 2026. Same price on every title. Free account, free B&N ISBN.",
        "upfront": "$0",
        "cut": "~55% of list − print",
    },
    {
        "id": "LULU-STORE",
        "name": "Lulu Bookstore (direct)",
        "price_fn": price_lulu_bookstore,
        "go": True,
        "pack": "KDP-Complete-Kit",
        "why": "No $14.99 floor. Setup $0. Do not turn on ebook Global Dist ($4.99 fee).",
        "upfront": "$0",
        "cut": "print + Lulu share on their store",
    },
    {
        "id": "LULU-GLOBAL",
        "name": "Lulu print Global Distribution",
        "price_fn": price_lulu_global,
        "go": True,
        "pack": "MARKETS/Lulu-Global",
        "why": "List must be at least 2× Lulu print cost. Each title gets its own minimum, rounded to x.99, never under $9.99.",
        "upfront": "$0 for print global (ebook global is $4.99 — skip)",
        "cut": "50% wholesale + Lulu 20% of remainder",
    },
    {
        "id": "DIGITAL",
        "name": "Google Play / Gumroad / Payhip PDF",
        "price_fn": price_digital,
        "go": True,
        "pack": "MARKETS/DIGITAL-9.99",
        "why": "No print floor. Google Play min about $0.05. We stay $9.99.",
        "upfront": "$0",
        "cut": "Google ~30%; Gumroad 10%+$0.50; Payhip Free 5%+Stripe",
    },
    {
        "id": "INGRAM",
        "name": "IngramSpark paperback",
        "price_fn": price_ingram,
        "go": False,
        "pack": "MARKETS/Ingram-PARKED",
        "why": "No catalog $14.99 floor. Formula floor after 55% wholesale. PARKED: Bowker ISBN is upfront money ($125 / $295 per 10).",
        "upfront": "ISBN (not $0)",
        "cut": "55% wholesale + 1.875% market access + print",
    },
]


def prices_for(t: dict) -> dict[str, float]:
    return {ch["id"]: float(ch["price_fn"](t)) for ch in CHANNELS}
