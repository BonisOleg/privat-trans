from django.test import SimpleTestCase, TestCase

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


class CalculatorPageTests(TestCase):
    def test_page_redirects_to_lead_form(self):
        response = self.client.get("/calculator/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/#lead-form")
