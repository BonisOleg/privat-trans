from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from src.core.utils import localized


class Service(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    title_uk = models.CharField(max_length=160)
    title_en = models.CharField(max_length=160, blank=True)
    teaser_uk = models.TextField()
    teaser_en = models.TextField(blank=True)
    body_uk = models.TextField(blank=True)
    body_en = models.TextField(blank=True)
    icon_key = models.CharField(max_length=40, default="truck")
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Послуга"
        verbose_name_plural = "Послуги"

    def __str__(self) -> str:
        return self.title_uk

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_uk, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("services:detail", kwargs={"slug": self.slug})

    @property
    def title(self) -> str:
        return localized(self, "title")

    @property
    def teaser(self) -> str:
        return localized(self, "teaser")

    @property
    def body(self) -> str:
        return localized(self, "body")
