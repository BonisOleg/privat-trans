from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from src.core.i18n import localize_path, strip_language_prefix


class I18nPathTests(SimpleTestCase):
    def test_uk_has_no_prefix(self):
        self.assertEqual(localize_path("/services/", "uk"), "/services/")

    def test_en_adds_prefix(self):
        self.assertEqual(localize_path("/services/", "en"), "/en/services/")

    def test_strip_en_prefix(self):
        self.assertEqual(strip_language_prefix("/en/about/"), "/about/")

    def test_home_en(self):
        self.assertEqual(localize_path("/", "en"), "/en/")


class HealthAndPagesTests(TestCase):
    def test_healthz(self):
        response = self.client.get("/healthz/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")

    def test_home_uk(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ПРИВАТ-ТРАНС")

    def test_home_en(self):
        response = self.client.get("/en/")
        self.assertEqual(response.status_code, 200)

    def test_robots(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sitemap:", response.content)

    def test_lead_form_url(self):
        self.assertEqual(reverse("leads:create"), "/leads/create/")
