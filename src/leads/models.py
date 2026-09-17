from django.db import models


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новий лід"
        IN_PROGRESS = "progress", "В роботі"
        DONE = "done", "Опрацьовано"

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    from_city = models.CharField(max_length=120, blank=True)
    from_country = models.CharField(max_length=120, blank=True)
    to_city = models.CharField(max_length=120, blank=True)
    to_country = models.CharField(max_length=120, blank=True)
    cargo = models.CharField(max_length=160, blank=True)
    service = models.CharField(max_length=160, blank=True)
    message = models.TextField(blank=True)
    consent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self) -> str:
        return f"{self.name} · {self.phone}"
