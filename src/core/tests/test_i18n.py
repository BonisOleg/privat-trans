from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext

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
        self.assertContains(response, 'href="#lead-form"')
        self.assertContains(response, 'data-qa="hero-quote-open"')
        self.assertContains(response, 'data-qa="calc-teaser-cta"')
        self.assertContains(response, 'hero__badge-lead')
        self.assertContains(response, 'hero__badge-rest')
        self.assertNotContains(response, "data-hero-sheet-open")
        self.assertNotContains(response, 'data-qa="nav-calculator"')

    def test_home_en(self):
        response = self.client.get("/en/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Services")
        self.assertContains(response, "Fleet")
        self.assertNotContains(response, ">Послуги<")

    def test_en_chrome_not_in_admin(self):
        contacts = self.client.get("/en/contacts/")
        self.assertEqual(contacts.status_code, 200)
        self.assertContains(contacts, "Country of origin")
        self.assertContains(contacts, "Destination country")
        self.assertContains(contacts, 'placeholder="Country"')
        self.assertContains(contacts, "EDRPOU")
        self.assertContains(contacts, "Tax ID")
        self.assertNotContains(contacts, "Країна звідки")
        self.assertNotContains(contacts, "ЄДРПОУ")

        faq = self.client.get("/en/faq/")
        self.assertContains(faq, "Frequently asked questions")
        self.assertNotContains(faq, "Часті запитання")

        privacy = self.client.get("/en/privacy/")
        self.assertContains(privacy, "Documents")
        self.assertContains(privacy, "EDRPOU")
        self.assertNotContains(privacy, ">Документи<")

        with translation.override("en"):
            self.assertEqual(gettext("Послуга"), "Service")
            self.assertEqual(gettext("Розрахунок"), "Estimate")
            self.assertEqual(gettext("Вкажіть місто"), "Enter a city")
            self.assertEqual(gettext("Вкажіть країну"), "Enter a country")
            self.assertEqual(gettext("Місто"), "City")

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

    def test_canonical_and_hreflang_strip_query(self):
        response = self.client.get("/about/?utm_source=ad")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rel="canonical" href="http://testserver/about/"')
        self.assertNotContains(response, 'rel="canonical" href="http://testserver/about/?utm')
        self.assertContains(response, 'hreflang="uk" href="http://testserver/about/"')
        self.assertContains(response, 'hreflang="en" href="http://testserver/en/about/"')
        self.assertContains(response, 'hreflang="x-default" href="http://testserver/about/"')
        self.assertContains(response, 'property="og:image"')
        self.assertContains(response, 'property="og:url" content="http://testserver/about/"')
        self.assertContains(response, '"@type": "Organization"')
        self.assertContains(response, '"addressCountry": "UA"')
        self.assertContains(response, '"vatID"')
        self.assertContains(response, '"taxID"')
        self.assertNotContains(response, '"addressLocality": "Rivne"')

    def test_sitemap_lists_uk_and_en(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("http://testserver/about/", content)
        self.assertIn("http://testserver/en/about/", content)
        self.assertIn('hreflang="uk"', content)
        self.assertIn('hreflang="en"', content)
        self.assertIn('hreflang="x-default"', content)
        self.assertIn("<lastmod>", content)
