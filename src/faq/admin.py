from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_mixins import ReadableUnfoldFieldsMixin, TinyMCEAdminMixin
from src.faq.models import FaqItem


@admin.register(FaqItem)
class FaqItemAdmin(ReadableUnfoldFieldsMixin, TinyMCEAdminMixin, ModelAdmin):
    tinymce_fields = ("answer_uk", "answer_en")
    list_display = ("question_uk", "order", "show_on_home", "is_published")
    list_editable = ("order", "show_on_home", "is_published")
    fieldsets = (
        (None, {"fields": ("order", "show_on_home", "is_published")}),
        (
            "Українська",
            {"classes": ["tab"], "fields": ("question_uk", "answer_uk")},
        ),
        (
            "English",
            {"classes": ["tab"], "fields": ("question_en", "answer_en")},
        ),
    )
