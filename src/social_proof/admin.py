from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_mixins import ReadableUnfoldFieldsMixin, TinyMCEAdminMixin
from src.social_proof.models import Partner, Review


@admin.register(Review)
class ReviewAdmin(ReadableUnfoldFieldsMixin, TinyMCEAdminMixin, ModelAdmin):
    tinymce_fields = ("quote_uk", "quote_en")
    list_display = ("author", "order", "is_published")
    list_editable = ("order", "is_published")
    fieldsets = (
        (None, {"fields": ("author", "flag", "order", "is_published")}),
        ("Українська", {"classes": ["tab"], "fields": ("quote_uk",)}),
        ("English", {"classes": ["tab"], "fields": ("quote_en",)}),
    )


@admin.register(Partner)
class PartnerAdmin(ReadableUnfoldFieldsMixin, ModelAdmin):
    list_display = ("name", "order", "is_published")
    list_editable = ("order", "is_published")
