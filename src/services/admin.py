from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_mixins import ReadableUnfoldFieldsMixin, TinyMCEAdminMixin
from src.services.models import Service


@admin.register(Service)
class ServiceAdmin(ReadableUnfoldFieldsMixin, TinyMCEAdminMixin, ModelAdmin):
    tinymce_fields = ("teaser_uk", "teaser_en", "body_uk", "body_en")
    list_display = ("title_uk", "slug", "order", "is_published")
    list_editable = ("order", "is_published")
    prepopulated_fields = {"slug": ("title_uk",)}
    fieldsets = (
        (None, {"fields": ("slug", "icon_key", "order", "is_published")}),
        (
            "Українська",
            {"classes": ["tab"], "fields": ("title_uk", "teaser_uk", "body_uk")},
        ),
        (
            "English",
            {"classes": ["tab"], "fields": ("title_en", "teaser_en", "body_en")},
        ),
    )
