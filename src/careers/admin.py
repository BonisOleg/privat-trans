from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_mixins import ReadableUnfoldFieldsMixin, TinyMCEAdminMixin
from src.careers.models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(ReadableUnfoldFieldsMixin, TinyMCEAdminMixin, ModelAdmin):
    tinymce_fields = ("text_uk", "text_en")
    list_display = ("title_uk", "order", "is_published")
    list_editable = ("order", "is_published")
    fieldsets = (
        (None, {"fields": ("order", "is_published")}),
        (
            "Українська",
            {"classes": ["tab"], "fields": ("title_uk", "text_uk")},
        ),
        (
            "English",
            {"classes": ["tab"], "fields": ("title_en", "text_en")},
        ),
    )
