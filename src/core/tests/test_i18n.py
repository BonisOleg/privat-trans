from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from src.core.i18n import collapse_double_prefix, localize_path, strip_language_prefix


class I18nPathTests(SimpleTestCase):
    def test_uk_has_no_prefix(self):
        self.assertEqual(localize_path("/services/", "uk"), "/services/")

    def test_en_adds_prefix(self):
        self.assertEqual(localize_path("/services/", "en"), "/en/services/")

    def test_strip_en_prefix(self):
        self.assertEqual(strip_language_prefix("/en/about/"), "/about/")

    def test_home_en(self):
        self.assertEqual(localize_path("/", "en"), "/en/")

    def test_collapse_double_prefix(self):
        self.assertEqual(collapse_double_prefix("/en/en/about/"), "/en/about/")


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
        self.assertContains(response, "Services")
        self.assertContains(response, "Fleet")
        self.assertNotContains(response, ">Послуги<")

    def test_set_language_roundtrip(self):
        to_en = self.client.post(
            "/i18n/setlang/",
            {"language": "en", "next": "/en/about/"},
        )
        self.assertEqual(to_en.status_code, 302)
        self.assertEqual(to_en["Location"], "/en/about/")
        self.assertEqual(to_en.cookies["django_language"].value, "en")

        to_uk = self.client.post(
            "/i18n/setlang/",
            {"language": "uk", "next": "/about/"},
        )
        self.assertEqual(to_uk.status_code, 302)
        self.assertEqual(to_uk["Location"], "/about/")
        self.assertEqual(to_uk.cookies["django_language"].value, "uk")

    def test_lang_switch_next_values(self):
        response = self.client.get("/en/services/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="next" value="/services/"')
        self.assertContains(response, 'name="next" value="/en/services/"')

    def test_robots(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sitemap:", response.content)

    def test_lead_form_url(self):
        from django.utils import translation

        with translation.override("uk"):
            self.assertEqual(reverse("leads:create"), "/leads/create/")
