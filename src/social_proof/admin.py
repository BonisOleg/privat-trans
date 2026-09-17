from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_mixins import ReadableUnfoldFieldsMixin
from src.social_proof.models import Partner, Review


@admin.register(Review)
class ReviewAdmin(ReadableUnfoldFieldsMixin, ModelAdmin):
    list_display = ("author", "source", "reviewed_on", "flag", "order", "is_published")
    list_editable = ("order", "is_published")
    list_filter = ("is_published", "source")
    search_fields = ("author", "flag", "source", "quote_uk", "quote_en")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "author",
                    "flag",
                    "source",
                    "source_url",
                    "reviewed_on",
                    "order",
                    "is_published",
                )
            },
        ),
        ("Українська", {"classes": ["tab"], "fields": ("quote_uk",)}),
        ("English", {"classes": ["tab"], "fields": ("quote_en",)}),
    )


@admin.register(Partner)
class PartnerAdmin(ReadableUnfoldFieldsMixin, ModelAdmin):
    list_display = ("name", "order", "is_published")
    list_editable = ("order", "is_published")
