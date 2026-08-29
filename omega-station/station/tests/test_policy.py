import unittest

from omega_station.policy import PolicyVerifier


class TestPolicy(unittest.TestCase):
    def test_banned_phrase(self):
        pv = PolicyVerifier()
        r = pv.check("This journal will cure your insomnia, guaranteed!")
        self.assertFalse(r["pass"])
        rules = {v["rule"] for v in r["violations"]}
        self.assertIn("banned_phrase", rules)

    def test_price_drift(self):
        pv = PolicyVerifier(prices={"the settle journal": "9.99"})
        r = pv.check("Get The Settle Journal today for just $14.99!",
                     title="The Settle Journal")
        self.assertTrue(any(v["rule"] == "price_drift"
                            for v in r["violations"]))

    def test_clean_copy_passes(self):
        pv = PolicyVerifier(prices={"the settle journal": "9.99"})
        r = pv.check(
            "The Settle Journal - a calm nightly companion. $9.99. "
            "Not medical advice.", title="The Settle Journal")
        self.assertTrue(r["pass"])

    def test_disclaimer_required(self):
        pv = PolicyVerifier(require_disclaimer=True)
        self.assertFalse(pv.check("a calm notebook")["pass"])
