from __future__ import annotations

import html
import re
from typing import Any

from django.core.cache import cache
from django.utils.html import escape, strip_tags
from django.utils.safestring import SafeString, mark_safe

from src.core.block_defaults import BLOCK_DEFAULTS
from src.core.models import SiteBlock
from src.core.utils import active_lang

SITE_BLOCKS_CACHE_KEY = "privattrans_site_blocks_v1"
SITE_BLOCKS_CACHE_TTL = 60

_BLANK_HTML_RE = re.compile(r"^(?:\s|&nbsp;|<br\s*/?>|</?p\b[^>]*>)*$", re.I)
_BLOCK_BREAK_RE = re.compile(
    r"<br\s*/?>|</p>|</div>|</h[1-6]>|</li>|</tr>",
    re.IGNORECASE,
)


def is_blank_cms_text(value: str | None) -> bool:
    if value is None:
        return True
    text = str(value).strip()
    if not text:
        return True
    if _BLANK_HTML_RE.fullmatch(text):
        return True
    return not strip_tags(html.unescape(text)).replace("\xa0", " ").strip()


def normalize_cms_text(value: str | None) -> str:
    if is_blank_cms_text(value):
        return ""
    # Keep HTML from TinyMCE, but decode entities like &harr; → ↔
    return html.unescape(str(value).strip())


def html_to_plain(value: str | None) -> str:
    """TinyMCE Enter (`<p>`/`<br>`) і textarea `\\n` → звичайний текст із переносами."""
    if value is None:
        return ""
    text = _BLOCK_BREAK_RE.sub("\n", str(value))
    text = html.unescape(strip_tags(text)).replace("\xa0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def plain_with_breaks(value: str | None) -> str | SafeString:
    """Plain CMS-текст для шаблону: escape + `\\n` → `<br>` (валідно всередині `<p>`)."""
    text = html_to_plain(value)
    if not text:
        return ""
    return mark_safe(escape(text).replace("\n", "<br>"))


def normalize_cms_plain(value: str | None) -> str:
    if is_blank_cms_text(value):
        return ""
    return html_to_plain(value)


def ensure_block(page: str, key: str) -> SiteBlock:
    defaults = BLOCK_DEFAULTS.get((page, key), {})
    obj, _ = SiteBlock.objects.get_or_create(
        page=page,
        key=key,
        defaults={
            "label": defaults.get("label", key),
            "content_type": defaults.get("content_type", SiteBlock.ContentType.TEXT),
            "text_uk": defaults.get("text_uk", ""),
            "text_en": defaults.get("text_en", ""),
            "sort_order": defaults.get("sort_order", 0),
            "is_active": True,
        },
    )
    return obj


def load_section_blocks(page: str, keys: list[str]) -> dict[str, SiteBlock]:
    """Ensure blocks for a single page (legacy helper). Prefer load_section_pairs."""
    return load_section_pairs([(page, key) for key in keys])


def load_section_pairs(pairs: list[tuple[str, str]]) -> dict[str, SiteBlock]:
    result: dict[str, SiteBlock] = {}
    for page, key in pairs:
        result[key] = ensure_block(page, key)
    return result


def _block_payload(block: SiteBlock) -> dict[str, Any]:
    return {
        "text_uk": block.text_uk or "",
        "text_en": block.text_en or "",
        "is_active": block.is_active,
    }


def get_site_blocks_map(*, force: bool = False) -> dict[str, dict[str, Any]]:
    """Cached map: 'page.key' → {text_uk, text_en, is_active} (not model instances)."""
    if not force:
        cached = cache.get(SITE_BLOCKS_CACHE_KEY)
        if isinstance(cached, dict):
            return cached
    payload = {
        b.cache_key: _block_payload(b)
        for b in SiteBlock.objects.filter(is_active=True)
    }
    cache.set(SITE_BLOCKS_CACHE_KEY, payload, SITE_BLOCKS_CACHE_TTL)
    return payload


def invalidate_site_blocks_cache() -> None:
    cache.delete(SITE_BLOCKS_CACHE_KEY)


def _text_from_payload(data: dict[str, Any], language: str | None = None) -> str:
    lang = active_lang(language)
    value = (data.get(f"text_{lang}") or "").strip()
    if value:
        return normalize_cms_text(value)
    return normalize_cms_text(data.get("text_uk") or "")


def get_block_text(
    page: str,
    key: str,
    *,
    site_blocks: dict[str, Any] | None = None,
    fallback: str | None = None,
) -> str:
    """
    If a SiteBlock row exists — return its localized text (even empty).
    Defaults apply only when the row is missing (pre-seed).
    """
    cache_key = f"{page}.{key}"
    data = None
    if site_blocks is not None:
        data = site_blocks.get(cache_key)

    if data is None:
        block = SiteBlock.objects.filter(page=page, key=key, is_active=True).first()
        if block is not None:
            data = _block_payload(block)
    elif isinstance(data, SiteBlock):
        data = _block_payload(data)

    if data is not None:
        text = _text_from_payload(data)
        if fallback is not None and is_blank_cms_text(text):
            return fallback
        return text

    if fallback is not None:
        return fallback

    defaults = BLOCK_DEFAULTS.get((page, key), {})
    lang = active_lang()
    return defaults.get(f"text_{lang}") or defaults.get("text_uk", "")


def is_section_visible(
    page: str,
    visibility_key: str,
    *,
    site_blocks: dict[str, Any] | None = None,
) -> bool:
    value = get_block_text(page, visibility_key, site_blocks=site_blocks, fallback="1")
    return value not in {"0", "false", "False", ""}


def seed_default_blocks() -> int:
    created = 0
    for (page, key), meta in BLOCK_DEFAULTS.items():
        _, was_created = SiteBlock.objects.get_or_create(
            page=page,
            key=key,
            defaults={
                "label": meta.get("label", key),
                "content_type": meta.get("content_type", SiteBlock.ContentType.TEXT),
                "text_uk": meta.get("text_uk", ""),
                "text_en": meta.get("text_en", ""),
                "sort_order": meta.get("sort_order", 0),
                "is_active": True,
            },
        )
        if was_created:
            created += 1
    invalidate_site_blocks_cache()
    return created
