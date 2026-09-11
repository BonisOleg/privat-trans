from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from src.leads.models import Lead
from src.leads.services import LEAD_RATE_MAX


def _lead_payload(**overrides):
    data = {
        "name": "Олена",
        "phone": "+380670000000",
        "email": "test@example.com",
        "from_city": "Київ",
        "to_city": "Warsaw",
        "cargo": "ltl",
        "consent": "on",
    }
    data.update(overrides)
    return data


class LeadFormTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_create_lead_htmx(self):
        response = self.client.post(
            reverse("leads:create"),
            _lead_payload(),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 1)
        self.assertContains(response, "Дякуємо")

    def test_invalid_lead(self):
        response = self.client.post(reverse("leads:create"), {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)

    def test_honeypot_discards_without_saving(self):
        response = self.client.post(
            reverse("leads:create"),
            _lead_payload(honeypot="http://spam.example"),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)
        self.assertContains(response, "Дякуємо")

    def test_rate_limit_blocks_extra_submissions(self):
        for index in range(LEAD_RATE_MAX):
            response = self.client.post(
                reverse("leads:create"),
                _lead_payload(name=f"Олена {index}"),
            )
            self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), LEAD_RATE_MAX)
        blocked = self.client.post(reverse("leads:create"), _lead_payload(name="Ще одна"))
        self.assertEqual(blocked.status_code, 200)
        self.assertEqual(Lead.objects.count(), LEAD_RATE_MAX)
        self.assertContains(blocked, "Забагато заявок")

    def test_lead_form_renders_cargo_select(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="cargo"')
        self.assertContains(response, "data-pt-select")
        self.assertContains(response, 'value="ltl"')
        self.assertContains(response, 'value="ftl"')
        self.assertContains(response, 'value="turnkey"')
        self.assertContains(response, "id_from_city")
        self.assertContains(response, "id_to_city")

    def test_invalid_phone_rejected(self):
        response = self.client.post(reverse("leads:create"), _lead_payload(phone="abc"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)
        self.assertContains(response, "Перевірте поля форми")

    def test_missing_city_rejected(self):
        response = self.client.post(reverse("leads:create"), _lead_payload(from_city="", to_city=""))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)

    def test_unknown_cargo_rejected(self):
        response = self.client.post(reverse("leads:create"), _lead_payload(cargo="LTL"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)

    def test_invalid_email_rejected(self):
        response = self.client.post(reverse("leads:create"), _lead_payload(email="not-an-email"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)
