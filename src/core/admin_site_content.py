from __future__ import annotations

from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from tinymce.widgets import TinyMCE

from src.core.admin_site_content_widgets import CmsAdminTextareaWidget, CmsAdminTextInputWidget
from src.core.block_defaults import (
    BLOCK_DEFAULTS,
    INLINE_KEYS,
    MULTILINE_KEYS,
    TINYMCE_KEYS,
    is_visibility_key,
)
from src.core.site_blocks import (
    invalidate_site_blocks_cache,
    load_section_blocks,
    normalize_cms_plain,
    normalize_cms_text,
)
from src.core.site_content_registry import ContentSection, get_section


def _field_name(page: str, key: str, suffix: str) -> str:
    return f"block__{page}__{key}__{suffix}"


def _widget_for_key(key: str):
    if key in TINYMCE_KEYS:
        height = 220 if key in {"about_infra_body", "about_geo_body", "privacy_body"} else 140
        return TinyMCE(attrs={"cols": 80, "rows": 4}, mce_attrs={"height": height})
    if key in MULTILINE_KEYS:
        return CmsAdminTextareaWidget(attrs={"rows": 4})
    if key in INLINE_KEYS:
        return CmsAdminTextInputWidget()
    return CmsAdminTextareaWidget(attrs={"rows": 2})


class SitePageContentForm(forms.Form):
    """CMS form with UK / EN fields; template shows language tabs."""

    def __init__(self, section: ContentSection, blocks: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.section = section
        self.blocks = blocks
        self.uk_field_names: list[str] = []
        self.en_field_names: list[str] = []

        if section.visibility_key:
            vis = blocks.get(section.visibility_key)
            raw = (vis.text_uk if vis else "1") or "1"
            self.fields["section_visible"] = forms.BooleanField(
                required=False,
                initial=raw not in {"0", "false", "False", ""},
                label="Показувати секцію на сайті",
            )

        for page, key in section.blocks:
            block = blocks[key]
            label = block.label or BLOCK_DEFAULTS.get((page, key), {}).get("label", key)

            if is_visibility_key(key):
                continue

            uk_name = _field_name(page, key, "text_uk")
            en_name = _field_name(page, key, "text_en")
            allow_html = key in TINYMCE_KEYS
            uk_initial = block.text_uk if allow_html else normalize_cms_plain(block.text_uk)
            en_initial = block.text_en if allow_html else normalize_cms_plain(block.text_en)
            self.fields[uk_name] = forms.CharField(
                required=False,
                label=label,
                initial=uk_initial,
                widget=_widget_for_key(key),
            )
            self.fields[en_name] = forms.CharField(
                required=False,
                label=label,
                initial=en_initial,
                widget=_widget_for_key(key),
            )
            self.uk_field_names.append(uk_name)
            self.en_field_names.append(en_name)

    @property
    def uk_fields(self):
        return [self[name] for name in self.uk_field_names]

    @property
    def en_fields(self):
        return [self[name] for name in self.en_field_names]

    def save(self) -> None:
        cleaned = self.cleaned_data
        section = self.section

        if section.visibility_key:
            vis = self.blocks.get(section.visibility_key)
            if vis is None:
                from src.core.site_blocks import ensure_block

                vis = ensure_block(section.page_slug, section.visibility_key)
            vis.text_uk = "1" if cleaned.get("section_visible") else "0"
            vis.text_en = vis.text_uk
            vis.save(update_fields=["text_uk", "text_en"])

        for page, key in section.blocks:
            if is_visibility_key(key):
                continue
            block = self.blocks[key]
            normalize = normalize_cms_text if key in TINYMCE_KEYS else normalize_cms_plain
            block.text_uk = normalize(cleaned.get(_field_name(page, key, "text_uk"), ""))
            block.text_en = normalize(cleaned.get(_field_name(page, key, "text_en"), ""))
            block.save(update_fields=["text_uk", "text_en"])

        invalidate_site_blocks_cache()


def site_content_section_view(request, page_slug: str, section_slug: str, *, model_admin):
    section = get_section(page_slug, section_slug)
    if section is None:
        messages.error(request, "Секцію не знайдено.")
        return HttpResponseRedirect(reverse("admin:index"))

    keys = [key for _, key in section.blocks]
    if section.visibility_key:
        keys = [section.visibility_key, *keys]
    blocks = load_section_blocks(section.page_slug, keys)

    if request.method == "POST":
        form = SitePageContentForm(section, blocks, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Збережено.")
            opts = model_admin.model._meta
            return HttpResponseRedirect(
                reverse(f"admin:{opts.app_label}_{opts.model_name}_changelist")
            )
    else:
        form = SitePageContentForm(section, blocks)

    media = form.media
    if hasattr(model_admin, "media"):
        media = model_admin.media + media

    context = {
        **model_admin.admin_site.each_context(request),
        "title": section.title,
        "section": section,
        "form": form,
        "media": media,
        "opts": model_admin.model._meta,
        "has_view_permission": True,
        "has_change_permission": True,
        "preview_url": section.preview_url,
    }
    return render(request, "admin/site_content_page.html", context)
