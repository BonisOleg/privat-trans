from django.http import HttpResponseRedirect
from django.urls import reverse
from tinymce.widgets import TinyMCE

from src.core.admin_site_content_widgets import apply_readable_widget


class SingletonModelAdminMixin:
    """Redirect changelist → change pk=1; no delete; add only if empty."""

    def has_add_permission(self, request) -> bool:
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = self.model.objects.get_or_create(pk=1)
        opts = self.model._meta
        return HttpResponseRedirect(
            reverse(f"admin:{opts.app_label}_{opts.model_name}_change", args=[obj.pk])
        )


class TinyMCEAdminMixin:
    """Attach TinyMCE to listed TextField names."""

    tinymce_fields: tuple[str, ...] = ()

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in self.tinymce_fields:
            kwargs["widget"] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class ReadableUnfoldFieldsMixin:
    """Dark-readable text inputs for Unfold (skip TinyMCE / file / select)."""

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if formfield is not None and hasattr(formfield, "widget"):
            apply_readable_widget(formfield.widget)
        return formfield
