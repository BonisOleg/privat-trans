from django.db import models

from src.core.utils import localized


class Review(models.Model):
    quote_uk = models.TextField()
    quote_en = models.TextField(blank=True)
    author = models.CharField(max_length=120)
    flag = models.CharField(max_length=160, blank=True)
    source = models.CharField(max_length=80, blank=True)
    source_url = models.URLField(blank=True)
    reviewed_on = models.DateField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

    def __str__(self) -> str:
        return self.author

    @property
    def quote(self) -> str:
        return localized(self, "quote")


class GalleryWork(models.Model):
    image = models.ImageField(upload_to="gallery/")
    alt_uk = models.CharField(max_length=180)
    alt_en = models.CharField(max_length=180, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Фото галереї"
        verbose_name_plural = "Галерея робіт"

    def __str__(self) -> str:
        return self.alt_uk

    @property
    def alt(self) -> str:
        return localized(self, "alt")


class Partner(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to="partners/", blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Партнер"
        verbose_name_plural = "Партнери"

    def __str__(self) -> str:
        return self.name
