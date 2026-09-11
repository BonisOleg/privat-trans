from django.core.validators import FileExtensionValidator
from django.db import models

from src.core.utils import localized


class SiteSettings(models.Model):
    brand_name_uk = models.CharField(max_length=80, default="ПРИВАТ-ТРАНС")
    brand_name_en = models.CharField(max_length=80, default="PRIVAT-TRANS", blank=True)
    slogan_uk = models.CharField(max_length=160, default="Ваш надійний партнер")
    slogan_en = models.CharField(max_length=160, default="Your reliable partner")
    phone = models.CharField(max_length=40, default="(0362) 64-24-34")
    phone_href = models.CharField(max_length=40, default="+380362642434")
    email = models.EmailField(default="privat_trans@ukr.net")
    telegram = models.CharField(max_length=120, blank=True)
    address_uk = models.CharField(max_length=255, default="33023, м. Рівне, вул. Відінська, 10")
    address_en = models.CharField(max_length=255, default="33023, Rivne, Vidinska St. 10")
    edrpou = models.CharField(max_length=20, default="35148692")
    ipn = models.CharField(max_length=20, default="351486917163")
    vat_note_uk = models.CharField(
        max_length=255,
        default="Платник ПДВ. Платник податку на прибуток на загальних підставах.",
    )
    vat_note_en = models.CharField(
        max_length=255,
        default="VAT payer. Corporate income tax on general terms.",
    )
    map_embed_url = models.URLField(blank=True)
    ga4_id = models.CharField(max_length=32, blank=True)
    gtm_id = models.CharField(max_length=32, blank=True)
    hero_video = models.FileField(
        upload_to="hero/",
        blank=True,
        validators=[FileExtensionValidator(["mp4"])],
        help_text="MP4 H.264, 12–16 с, 1080p 24/30 fps, до 10 МБ. Fallback: static/media/hero-video.mp4",
    )
    hero_video_webm = models.FileField(
        upload_to="hero/",
        blank=True,
        validators=[FileExtensionValidator(["webm"])],
        help_text="WebM VP9, ті самі параметри. Fallback: static/media/hero-video.webm",
    )
    hero_poster = models.ImageField(
        upload_to="hero/",
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "webp", "png"])],
        help_text="Кадр-заставка (JPG/WEBP). Fallback: static/media/hero-poster.jpg",
    )
    og_image = models.ImageField(
        upload_to="seo/",
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "webp", "png"])],
        help_text="OG-прев’ю 1200×630. Якщо порожньо — hero poster або static/media/hero-poster.jpg",
    )
    default_title_uk = models.CharField(
        max_length=180,
        default="ПРИВАТ-ТРАНС — комплексна доставка вантажів Європа ↔️ Україна ↔️ Азія",
    )
    default_title_en = models.CharField(
        max_length=180,
        default="PRIVAT-TRANS — freight Europe ↔ Ukraine ↔ Asia",
    )
    default_description_uk = models.TextField(
        default="Повний логістичний супровід на всіх етапах роботи з вантажем. З 2007 року на ринку міжнародних перевезень.",
    )
    default_description_en = models.TextField(
        default="Full logistics support at every cargo stage. On the international freight market since 2007.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

    def __str__(self) -> str:
        return self.brand_name_uk

    @classmethod
    def get_solo(cls) -> "SiteSettings":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @classmethod
    def load(cls) -> "SiteSettings":
        return cls.get_solo()

    @property
    def brand_name(self) -> str:
        return localized(self, "brand_name")

    @property
    def slogan(self) -> str:
        return localized(self, "slogan")

    @property
    def address(self) -> str:
        return localized(self, "address")

    @property
    def vat_note(self) -> str:
        return localized(self, "vat_note")

    @property
    def default_title(self) -> str:
        return localized(self, "default_title")

    @property
    def default_description(self) -> str:
        return localized(self, "default_description")


class PageSEO(models.Model):
    slug = models.SlugField(unique=True)
    title_uk = models.CharField(max_length=180)
    title_en = models.CharField(max_length=180, blank=True)
    description_uk = models.TextField()
    description_en = models.TextField(blank=True)
    h1_uk = models.CharField(max_length=180, blank=True)
    h1_en = models.CharField(max_length=180, blank=True)

    class Meta:
        verbose_name = "SEO сторінки"
        verbose_name_plural = "SEO сторінок"

    def __str__(self) -> str:
        return self.slug

    @property
    def title(self) -> str:
        return localized(self, "title")

    @property
    def description(self) -> str:
        return localized(self, "description")

    @property
    def h1(self) -> str:
        return localized(self, "h1")


class SiteBlock(models.Model):
    class Page(models.TextChoices):
        HOME = "home", "Головна"
        ABOUT = "about", "Про нас"
        FLEET = "fleet", "Автопарк"
        CONTACTS = "contacts", "Контакти"
        PRIVACY = "privacy", "Політика"
        SERVICES = "services", "Послуги"
        FAQ = "faq", "FAQ"
        CALCULATOR = "calculator", "Калькулятор"
        SITE = "site", "Сайт"

    class ContentType(models.TextChoices):
        TEXT = "text", "Текст"
        IMAGE = "image", "Фото"
        URL = "url", "Посилання"
        VIDEO = "video", "Відео"

    page = models.CharField(max_length=32, choices=Page.choices)
    key = models.CharField(max_length=64)
    label = models.CharField(max_length=128)
    content_type = models.CharField(
        max_length=16,
        choices=ContentType.choices,
        default=ContentType.TEXT,
    )
    text_uk = models.TextField(blank=True)
    text_en = models.TextField(blank=True)
    image = models.ImageField(upload_to="blocks/", blank=True)
    link_url = models.CharField(max_length=512, blank=True)
    link_label = models.CharField(max_length=128, blank=True)
    video_embed_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to="blocks/video/", blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["page", "sort_order", "key"]
        verbose_name = "CMS-блок"
        verbose_name_plural = "CMS-блоки"
        constraints = [
            models.UniqueConstraint(fields=["page", "key"], name="unique_site_block_page_key"),
        ]

    def __str__(self) -> str:
        return f"{self.page}.{self.key}"

    @property
    def cache_key(self) -> str:
        return f"{self.page}.{self.key}"

    @property
    def text(self) -> str:
        return localized(self, "text")


class HomeHeroSettings(SiteSettings):
    """Proxy для CMS-секції «Головна — Hero» (не окрема таблиця)."""

    class Meta:
        proxy = True
        verbose_name = "Головна — Hero"
        verbose_name_plural = "Головна — Hero"


class HomeScenariosSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Три сценарії"
        verbose_name_plural = "Головна — Три сценарії"


class AboutPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Про нас"
        verbose_name_plural = "Про нас"


class ContactsPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Контакти"
        verbose_name_plural = "Контакти"


class PrivacyPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Політика конфіденційності"
        verbose_name_plural = "Політика конфіденційності"


class ServicesPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Послуги — сторінка"
        verbose_name_plural = "Послуги — сторінка"


class FaqPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "FAQ — сторінка"
        verbose_name_plural = "FAQ — сторінка"


class CalculatorPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Калькулятор"
        verbose_name_plural = "Калькулятор"


class FleetPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Автопарк"
        verbose_name_plural = "Автопарк"


class HomeGeographySettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Географія"
        verbose_name_plural = "Головна — Географія"


class HomeRoutesSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Маршрути"
        verbose_name_plural = "Головна — Маршрути"


class HomeMidSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Послуги та автопарк"
        verbose_name_plural = "Головна — Послуги та автопарк"


class HomeExperienceSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Переваги та процес"
        verbose_name_plural = "Головна — Переваги та процес"


class HomeSocialSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Головна — Калькулятор і соцблок"
        verbose_name_plural = "Головна — Калькулятор і соцблок"


class SiteChromeSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Сайт — CTA та форма"
        verbose_name_plural = "Сайт — CTA та форма"
