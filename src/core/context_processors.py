from pathlib import Path

from django.conf import settings
from django.urls import reverse
from django.utils.translation import get_language

from src.core.cities import CITIES
from src.core.i18n import lang_switch_map
from src.core.models import SiteSettings
from src.core.seo import (
    og_image_meta,
    og_locales,
    organization_json_ld,
    page_canonical_url,
    request_origin,
)
from src.core.site_blocks import get_site_blocks_map
from src.services.models import Service


def _hero_static_v() -> str:
    path = Path(settings.BASE_DIR) / "static" / "media" / "hero-video.mp4"
    try:
        return str(int(path.stat().st_mtime))
    except OSError:
        return "1"


def _static_asset_v() -> str:
    static_root = Path(settings.BASE_DIR) / "static"
    mtimes = [
        int(path.stat().st_mtime)
        for pattern in ("css/**/*.css", "js/**/*.js")
        for path in static_root.glob(pattern)
    ]
    return str(max(mtimes) if mtimes else 1)


def site_chrome(request):
    settings_obj = SiteSettings.load()
    services = Service.objects.filter(is_published=True)
    language = get_language() or "uk"
    og_locale, og_locale_alternate = og_locales(language)
    return {
        "site_settings": settings_obj,
        "site_blocks": get_site_blocks_map(),
        "nav_services": services,
        "lang_switch_urls": lang_switch_map(request.path),
        "current_language": language,
        "canonical_url": page_canonical_url(request),
        "public_origin": request_origin(request),
        "og_image": og_image_meta(request, settings_obj),
        "og_locale": og_locale,
        "og_locale_alternate": og_locale_alternate,
        "organization_schema": organization_json_ld(request, settings_obj),
        "pt_cities": CITIES,
        "home_url": reverse("pages:home"),
        "hero_static_v": _hero_static_v(),
        "static_asset_v": _static_asset_v(),
    }
