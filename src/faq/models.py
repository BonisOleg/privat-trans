from django.db import models

from src.core.utils import localized


class FaqItem(models.Model):
    question_uk = models.CharField(max_length=240)
    question_en = models.CharField(max_length=240, blank=True)
    answer_uk = models.TextField()
    answer_en = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    show_on_home = models.BooleanField(default=False)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Питання FAQ"
        verbose_name_plural = "FAQ"

    def __str__(self) -> str:
        return self.question_uk

    @property
    def question(self) -> str:
        return localized(self, "question")

    @property
    def answer(self) -> str:
        return localized(self, "answer")
