from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from src.leads.models import Lead
from src.leads.services import LEAD_RATE_MAX, lead_notify_recipients


def _lead_payload(**overrides):
    data = {
        "name": "Олена",
        "phone": "+380670000000",
        "email": "test@example.com",
        "from_city": "Київ",
        "from_country": "Україна",
        "to_city": "Warsaw",
        "to_country": "Poland",
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
        self.assertContains(response, "Заявка відправлена")

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
        self.assertContains(response, "Заявка відправлена")

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
        self.assertContains(response, 'hx-disabled-elt="find .lead-form__submit"')
        self.assertContains(response, 'data-qa="lead-submit-spinner"')
        self.assertContains(response, 'name="cargo"')
        self.assertContains(response, "data-pt-select")
        self.assertContains(response, 'value="ltl"')
        self.assertContains(response, 'value="ftl"')
        self.assertContains(response, 'value="turnkey"')
        self.assertContains(response, "id_from_city")
        self.assertContains(response, "id_from_country")
        self.assertContains(response, "id_to_city")
        self.assertContains(response, "id_to_country")

    def test_invalid_phone_rejected(self):
        response = self.client.post(reverse("leads:create"), _lead_payload(phone="abc"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)
        self.assertContains(response, "Перевірте поля форми")

    def test_missing_city_rejected(self):
        response = self.client.post(reverse("leads:create"), _lead_payload(from_city="", to_city=""))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)

    def test_missing_country_rejected(self):
        response = self.client.post(
            reverse("leads:create"),
            _lead_payload(from_country="", to_country=""),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)

    def test_free_city_accepted(self):
        response = self.client.post(
            reverse("leads:create"),
            _lead_payload(
                from_city="Рівне",
                from_country="Україна",
                to_city="Відень",
                to_country="Австрія",
            ),
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        lead = Lead.objects.get()
        self.assertEqual(lead.from_city, "Рівне")
        self.assertEqual(lead.from_country, "Україна")
        self.assertEqual(lead.to_city, "Відень")
        self.assertEqual(lead.to_country, "Австрія")
        self.assertContains(response, "Заявка відправлена")

    def test_unknown_cargo_rejected(self):
        response = self.client.post(reverse("leads:create"), _lead_payload(cargo="LTL"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)

    def test_invalid_email_rejected(self):
        response = self.client.post(reverse("leads:create"), _lead_payload(email="not-an-email"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)

    @override_settings(LEAD_NOTIFY_EMAIL="privat_trans@ukr.net")
    def test_notify_email_sends_to_lead_notify(self):
        response = self.client.post(reverse("leads:create"), _lead_payload(), HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        lead = Lead.objects.get()
        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        self.assertEqual(sent.to, ["privat_trans@ukr.net"])
        self.assertEqual(sent.subject, f"Нова заявка #{lead.pk}")
        self.assertEqual(sent.reply_to, ["test@example.com"])
        self.assertIn("Олена", sent.body)
        self.assertIn("+380670000000", sent.body)

    @override_settings(LEAD_NOTIFY_EMAIL="")
    def test_notify_email_skipped_without_recipient(self):
        response = self.client.post(reverse("leads:create"), _lead_payload())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(
        LEAD_NOTIFY_EMAIL="ptinfo@ukr.net, prometeylabsandriir@gmail.com, ptinfo@ukr.net"
    )
    def test_notify_email_sends_to_several_recipients(self):
        response = self.client.post(reverse("leads:create"), _lead_payload(), HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].to,
            ["ptinfo@ukr.net", "prometeylabsandriir@gmail.com"],
        )

    def test_lead_notify_recipients_splits_and_dedupes(self):
        self.assertEqual(lead_notify_recipients(""), [])
        self.assertEqual(
            lead_notify_recipients("a@x.test; b@x.test, a@x.test, "),
            ["a@x.test", "b@x.test"],
        )

    @override_settings(LEAD_NOTIFY_EMAIL="privat_trans@ukr.net")
    def test_honeypot_does_not_send_email(self):
        response = self.client.post(
            reverse("leads:create"),
            _lead_payload(honeypot="http://spam.example"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
