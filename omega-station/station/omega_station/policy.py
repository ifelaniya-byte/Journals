from __future__ import annotations

import json
import re
from pathlib import Path

DEFAULT_BANNED = [
    "cure", "cures", "guarantee", "guaranteed", "miracle", "overnight",
    "instantly", "ozempic", "wegovy", "mounjaro", "fda approved",
    "clinically proven", "doctor recommended", "medical advice",
    "treats", "treats depression", "diagnose", "prescription",
    "side-effect free", "no side effects", "100% safe",
]
REQUIRED_DISCLAIMER = "not medical advice"


class PolicyVerifier:
    """Hostile policy verifier for seller/marketing assets.

    Same asymmetry as the code verifiers: assume the copy is guilty
    until it survives the audit. Checks banned phrases, price drift
    against a catalog of record, and (optionally) required elements
    such as the disclaimer line.
    """

    def __init__(self, banned=None, prices=None, require_disclaimer=False):
        self.banned = [b.lower() for b in (banned or DEFAULT_BANNED)]
        self.prices = {k.lower(): v for k, v in (prices or {}).items()}
        self.require_disclaimer = require_disclaimer

    @classmethod
    def from_files(cls, banned_file: Path | None, prices_file: Path | None,
                   require_disclaimer: bool = False) -> "PolicyVerifier":
        banned = None
        if banned_file and Path(banned_file).exists():
            banned = [w.strip() for w in
                      Path(banned_file).read_text(encoding="utf-8").splitlines()
                      if w.strip() and not w.startswith("#")]
        prices = None
        if prices_file and Path(prices_file).exists():
            prices = json.loads(Path(prices_file).read_text(encoding="utf-8"))
        return cls(banned=banned, prices=prices,
                   require_disclaimer=require_disclaimer)

    def check(self, text: str, title: str | None = None) -> dict:
        violations: list[dict] = []
        lowered = text.lower()
        # negation guard: "not medical advice" is the compliant use of
        # "medical advice"; scrub explicit negations before matching
        scrubbed = lowered
        for phrase in self.banned:
            scrubbed = re.sub(
                r"\bnot\s+" + re.escape(phrase), " ", scrubbed)
        for phrase in self.banned:
            if phrase in scrubbed:
                i = scrubbed.find(phrase)
                violations.append({
                    "rule": "banned_phrase",
                    "match": phrase,
                    "context": text[max(0, i - 30):i + len(phrase) + 30],
                })
        for m in re.finditer(r"\$\s?(\d+(?:\.\d{2})?)", text):
            price = m.group(1)
            if not price.endswith(".99"):
                violations.append({
                    "rule": "odd_price",
                    "match": price,
                    "context": text[max(0, m.start() - 30):m.end() + 30],
                })
        if self.prices and title:
            want = self.prices.get(title.lower())
            if want is not None:
                found = re.findall(r"\$\s?(\d+(?:\.\d{2})?)", text)
                wrong = [p for p in found
                         if abs(float(p) - float(want)) > 0.001]
                if wrong:
                    violations.append({
                        "rule": "price_drift",
                        "match": f"listed {wrong} but catalog says {want}",
                        "context": title,
                    })
        if self.require_disclaimer and \
                REQUIRED_DISCLAIMER not in lowered:
            violations.append({
                "rule": "missing_disclaimer",
                "match": REQUIRED_DISCLAIMER,
                "context": "",
            })
        return {"pass": not violations, "violations": violations}
