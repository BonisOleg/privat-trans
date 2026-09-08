from pathlib import Path

from django.test import SimpleTestCase

PRODUCTION = Path(__file__).resolve().parents[3] / "config" / "settings" / "production.py"


class ProductionHttpFirstTests(SimpleTestCase):
    def test_cookie_and_ssl_flags_come_from_env(self):
        text = PRODUCTION.read_text(encoding="utf-8")
        self.assertIn('config("SESSION_COOKIE_SECURE"', text)
        self.assertIn('config("CSRF_COOKIE_SECURE"', text)
        self.assertIn('config("SECURE_SSL_REDIRECT"', text)
        self.assertNotIn("SESSION_COOKIE_SECURE = True", text)
        self.assertNotIn("CSRF_COOKIE_SECURE = True", text)
        self.assertNotIn("SECURE_SSL_REDIRECT = True", text)
