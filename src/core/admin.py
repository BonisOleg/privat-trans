from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.urls import reverse
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from src.core.admin_mixins import (
    ReadableUnfoldFieldsMixin,
    SingletonModelAdminMixin,
    TinyMCEAdminMixin,
)
from src.core.admin_site_content import site_content_section_view
from src.core.models import (
    AboutPageSettings,
    CalculatorPageSettings,
    ContactsPageSettings,
    FaqPageSettings,
    HomeHeroSettings,
    HomeScenariosSettings,
    PageSEO,
    PrivacyPageSettings,
    ServicesPageSettings,
    SiteSettings,
)

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(SiteSettings)
class SiteSettingsAdmin(
    ReadableUnfoldFieldsMixin,
    TinyMCEAdminMixin,
    SingletonModelAdminMixin,
    ModelAdmin,
):
    tinymce_fields = ("default_description_uk", "default_description_en")
    fieldsets = (
        (
            "Основне",
            {
                "fields": (
                    "brand_name",
                    "phone",
                    "phone_href",
                    "email",
                    "telegram",
                    "edrpou",
                    "ipn",
                    "map_embed_url",
                    "ga4_id",
                    "gtm_id",
                )
            },
        ),
        (
            "Hero-відео",
            {
                "fields": (
                    "hero_video",
                    "hero_video_webm",
                    "hero_poster",
                )
            },
        ),
        (
            "Українська",
            {
                "classes": ["tab"],
                "fields": (
                    "slogan_uk",
                    "address_uk",
                    "vat_note_uk",
                    "default_title_uk",
                    "default_description_uk",
                ),
            },
        ),
        (
            "English",
            {
                "classes": ["tab"],
                "fields": (
                    "slogan_en",
                    "address_en",
                    "vat_note_en",
                    "default_title_en",
                    "default_description_en",
                ),
            },
        ),
    )


@admin.register(PageSEO)
class PageSEOAdmin(ReadableUnfoldFieldsMixin, ModelAdmin):
    list_display = ("slug", "title_uk")
    search_fields = ("slug", "title_uk", "title_en")
    fieldsets = (
        (None, {"fields": ("slug",)}),
        (
            "Українська",
            {"classes": ["tab"], "fields": ("title_uk", "description_uk", "h1_uk")},
        ),
        (
            "English",
            {"classes": ["tab"], "fields": ("title_en", "description_en", "h1_en")},
        ),
    )


def _register_cms_section(model, page_slug: str, section_slug: str):
    @admin.register(model)
    class CmsSectionAdmin(SingletonModelAdminMixin, ModelAdmin):
        def changelist_view(self, request, extra_context=None):
            SiteSettings.objects.get_or_create(pk=1)
            return site_content_section_view(
                request,
                page_slug,
                section_slug,
                model_admin=self,
            )

        def change_view(self, request, object_id, form_url="", extra_context=None):
            opts = self.model._meta
            return HttpResponseRedirect(
                reverse(f"admin:{opts.app_label}_{opts.model_name}_changelist")
            )

        def has_module_permission(self, request):
            return request.user.is_staff

    CmsSectionAdmin.__name__ = f"{model.__name__}Admin"
    return CmsSectionAdmin


_register_cms_section(HomeHeroSettings, "home", "hero")
_register_cms_section(HomeScenariosSettings, "home", "scenarios")
_register_cms_section(AboutPageSettings, "about", "page")
_register_cms_section(ContactsPageSettings, "contacts", "page")
_register_cms_section(PrivacyPageSettings, "privacy", "page")
_register_cms_section(ServicesPageSettings, "services", "page")
_register_cms_section(FaqPageSettings, "faq", "page")
_register_cms_section(CalculatorPageSettings, "calculator", "page")
