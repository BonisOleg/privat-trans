from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from src.core.admin_mixins import ReadableUnfoldFieldsMixin
from src.social_proof.models import GalleryWork, Partner, Review


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
    list_display = ("thumb", "name", "order", "is_published")
    list_editable = ("order", "is_published")
    search_fields = ("name",)
    fields = ("name", "logo", "order", "is_published")

    @admin.display(description="Лого")
    def thumb(self, obj: Partner) -> str:
        if not obj.logo:
            return "—"
        return format_html(
            '<img src="{}" alt="" width="72" height="36">',
            obj.logo.url,
        )


@admin.register(GalleryWork)
class GalleryWorkAdmin(ReadableUnfoldFieldsMixin, ModelAdmin):
    list_display = ("thumb", "alt_uk", "order", "is_published")
    list_editable = ("order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("alt_uk", "alt_en")
    fieldsets = (
        (None, {"fields": ("image", "order", "is_published")}),
        ("Українська", {"classes": ["tab"], "fields": ("alt_uk",)}),
        ("English", {"classes": ["tab"], "fields": ("alt_en",)}),
    )

    @admin.display(description="Фото")
    def thumb(self, obj: GalleryWork) -> str:
        if not obj.image:
            return "—"
        return format_html(
            '<img src="{}" alt="" width="56" height="70">',
            obj.image.url,
        )
