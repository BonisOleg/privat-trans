from django.db import models

from src.core.utils import localized


class Vacancy(models.Model):
    title_uk = models.CharField(max_length=160)
    title_en = models.CharField(max_length=160, blank=True)
    text_uk = models.TextField()
    text_en = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Вакансія"
        verbose_name_plural = "Вакансії"

    def __str__(self) -> str:
        return self.title_uk

    @property
    def title(self) -> str:
        return localized(self, "title")

    @property
    def text(self) -> str:
        return localized(self, "text")
