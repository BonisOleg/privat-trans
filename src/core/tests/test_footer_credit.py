from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from src.core.models import SiteSettings

CREDIT_URL = "https://www.prometeylabs.com/corporate-website-v2/"


class FooterDeveloperLinkTests(TestCase):
    def test_home_has_nofollow_credit_link(self):
        response = self.client.get(reverse("pages:home"))
        self.assertContains(response, CREDIT_URL)
        self.assertContains(response, "nofollow")
        self.assertContains(response, ">Prometey<span class=\"footer-credit__accent\">Labs</span></a>")

    def test_localized_home_keeps_credit_link(self):
        response = self.client.get("/en/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, CREDIT_URL)
        self.assertContains(response, "nofollow")

    def test_inner_pages_show_credit_without_link(self):
        for name in ("pages:about", "pages:privacy"):
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertContains(response, "footer-credit__name")
                self.assertContains(response, "Prometey")
                self.assertContains(response, "Labs")
                self.assertNotContains(response, CREDIT_URL)
                self.assertNotContains(response, "footer-credit__link")


class BrandNameI18nTests(TestCase):
    def test_brand_name_switches_with_language(self):
        settings = SiteSettings.load()
        settings.brand_name_uk = "ПРИВАТ-ТРАНС"
        settings.brand_name_en = "PRIVAT-TRANS"
        settings.save()

        with translation.override("uk"):
            self.assertEqual(settings.brand_name, "ПРИВАТ-ТРАНС")
        with translation.override("en"):
            self.assertEqual(settings.brand_name, "PRIVAT-TRANS")

    def test_brand_name_falls_back_to_uk(self):
        settings = SiteSettings.load()
        settings.brand_name_uk = "ПРИВАТ-ТРАНС"
        settings.brand_name_en = ""
        settings.save()

        with translation.override("en"):
            self.assertEqual(settings.brand_name, "ПРИВАТ-ТРАНС")
