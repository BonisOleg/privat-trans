import html

from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from src.core.site_blocks import get_block_text, is_section_visible

register = template.Library()


@register.simple_tag(takes_context=True)
def block_plain(context, page: str, key: str) -> str:
    site_blocks = context.get("site_blocks")
    text = get_block_text(page, key, site_blocks=site_blocks)
    # TinyMCE may store &harr; etc.; unescape after strip so arrows render
    return html.unescape(strip_tags(text or ""))


@register.simple_tag(takes_context=True)
def block_html(context, page: str, key: str):
    site_blocks = context.get("site_blocks")
    return mark_safe(get_block_text(page, key, site_blocks=site_blocks))


@register.simple_tag(takes_context=True)
def section_visible(context, page: str, visibility_key: str) -> bool:
    site_blocks = context.get("site_blocks")
    return is_section_visible(page, visibility_key, site_blocks=site_blocks)
