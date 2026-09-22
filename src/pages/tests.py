from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.test import TestCase
from django.urls import reverse

from src.social_proof.models import GalleryWork, Partner


def _sample_image(name: str = "work-test.jpg") -> ContentFile:
    path = Path(settings.BASE_DIR) / "static" / "media" / "gallery" / "work-01.jpg"
    return ContentFile(path.read_bytes(), name=name)


class AboutGalleryTests(TestCase):
    def test_about_renders_published_gallery(self):
        GalleryWork.objects.create(
            image=_sample_image("work-01.jpg"),
            alt_uk="Генератор Kohler на напівпричепі",
            alt_en="Kohler generator on a semi-trailer",
            order=1,
            is_published=True,
        )
        hidden = GalleryWork.objects.create(
            image=_sample_image("work-hidden.jpg"),
            alt_uk="Приховане фото",
            order=2,
            is_published=False,
        )
        published = GalleryWork.objects.get(is_published=True)
        response = self.client.get(reverse("pages:about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="gallery"')
        self.assertContains(response, "Галерея робіт")
        self.assertContains(response, "Наші роботи")
        self.assertContains(response, published.image.url)
        self.assertContains(response, "Генератор Kohler на напівпричепі")
        self.assertNotContains(response, hidden.image.url)
        self.assertNotContains(response, "Приховане фото")

    def test_about_hides_gallery_when_empty(self):
        response = self.client.get(reverse("pages:about"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'id="gallery"')


class HomePartnersTests(TestCase):
    def test_home_renders_partner_logo(self):
        partner = Partner.objects.create(
            name="Lardi-Trans",
            logo=_sample_image("partner-lardi.png"),
            order=1,
            is_published=True,
        )
        Partner.objects.create(name="Без лого", order=2, is_published=True)
        hidden = Partner.objects.create(
            name="Прихований",
            logo=_sample_image("partner-hidden.png"),
            order=3,
            is_published=False,
        )
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="partners"')
        self.assertContains(response, 'data-qa="partners-marquee"')
        self.assertContains(response, "data-partners-marquee")
        self.assertContains(response, partner.logo.url)
        self.assertContains(response, 'alt="Lardi-Trans"')
        self.assertContains(response, "Без лого")
        self.assertNotContains(response, hidden.logo.url)
        self.assertNotContains(response, "Прихований")
