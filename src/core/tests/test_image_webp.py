import shutil
import tempfile
from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase, override_settings
from PIL import Image

from src.core.models import SiteSettings
from src.social_proof.models import GalleryWork, Partner

MEDIA_ROOT = Path(tempfile.mkdtemp(prefix="pt-webp-"))


def _jpeg() -> bytes:
    buffer = BytesIO()
    Image.new("RGB", (6, 4), (19, 78, 112)).save(buffer, format="JPEG")
    return buffer.getvalue()


def _png_alpha() -> bytes:
    buffer = BytesIO()
    Image.new("RGBA", (6, 4), (19, 78, 112, 128)).save(buffer, format="PNG")
    return buffer.getvalue()


def _webp() -> bytes:
    buffer = BytesIO()
    Image.new("RGB", (6, 4), (19, 78, 112)).save(buffer, format="WEBP")
    return buffer.getvalue()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class UploadedImageWebpTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def test_png_with_alpha_becomes_webp(self):
        partner = Partner(name="IWT")
        partner.logo.save("logo.png", ContentFile(_png_alpha()), save=False)
        partner.save()

        self.assertTrue(partner.logo.name.endswith(".webp"))
        with Image.open(partner.logo.path) as image:
            self.assertEqual(image.format, "WEBP")
            self.assertEqual(image.mode, "RGBA")
            self.assertEqual(image.getpixel((0, 0))[3], 128)

    def test_jpeg_becomes_webp_and_repeat_save_keeps_bytes(self):
        work = GalleryWork(alt_uk="Склад")
        work.image.save("work.jpg", ContentFile(_jpeg()), save=False)
        work.save()
        stored = Path(work.image.path).read_bytes()

        work.alt_uk = "Склад 2"
        work.save()

        self.assertTrue(work.image.name.endswith(".webp"))
        self.assertEqual(Path(work.image.path).read_bytes(), stored)
        with Image.open(work.image.path) as image:
            self.assertEqual(image.format, "WEBP")
            self.assertEqual(image.mode, "RGB")

    def test_existing_jpeg_converts_on_full_save_not_on_other_fields(self):
        stored = default_storage.save("gallery/old.jpg", ContentFile(_jpeg()))
        GalleryWork.objects.bulk_create([GalleryWork(image=stored, alt_uk="старе")])
        work = GalleryWork.objects.get(alt_uk="старе")

        work.alt_uk = "підпис"
        work.save(update_fields=["alt_uk"])
        work.refresh_from_db()
        self.assertTrue(work.image.name.endswith(".jpg"))
        self.assertTrue(default_storage.exists(stored))

        work.save()
        self.assertTrue(work.image.name.endswith(".webp"))
        self.assertFalse(default_storage.exists(stored))

    def test_webp_upload_is_not_reencoded(self):
        original = _webp()
        settings_obj = SiteSettings.get_solo()
        settings_obj.hero_poster.save("poster.webp", ContentFile(original), save=False)
        settings_obj.save()

        self.assertTrue(settings_obj.hero_poster.name.endswith(".webp"))
        self.assertEqual(Path(settings_obj.hero_poster.path).read_bytes(), original)
