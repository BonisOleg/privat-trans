from django.test import SimpleTestCase

from src.calculator.quote import calc_range


class QuoteTests(SimpleTestCase):
    def test_range_positive(self):
        quote = calc_range(1000, 4, "ltl", "tent")
        self.assertGreaterEqual(quote.max_eur, quote.min_eur)
        self.assertGreaterEqual(quote.min_eur, 60)

    def test_adr_costs_more_than_tent(self):
        tent = calc_range(2000, 8, "ftl", "tent")
        adr = calc_range(2000, 8, "ftl", "adr")
        self.assertGreater(adr.min_eur, tent.min_eur)
