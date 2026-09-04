from django.test import TestCase
from django.urls import reverse

from src.leads.models import Lead


class LeadFormTests(TestCase):
    def test_create_lead_htmx(self):
        response = self.client.post(
            reverse("leads:create"),
            {
                "name": "Олена",
                "phone": "+380670000000",
                "email": "test@example.com",
                "from_city": "Kyiv",
                "to_city": "Warsaw",
                "cargo": "LTL",
                "consent": "on",
            },
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 1)
        self.assertContains(response, "Дякуємо")

    def test_invalid_lead(self):
        response = self.client.post(reverse("leads:create"), {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)
