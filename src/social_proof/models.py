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
