import json

from django.templatetags.static import static
from django.utils.translation import get_language

from src.core.i18n import localize_path


def absolute_url(request, path: str) -> str:
    if path.startswith(("http://", "https://")):
        return path
    return f"{request.scheme}://{request.get_host()}{path}"


def page_canonical_url(request) -> str:
    return absolute_url(request, request.path)


def og_image_meta(request, settings_obj) -> dict:
    if settings_obj.og_image:
        return {
            "url": absolute_url(request, settings_obj.og_image.url),
            "width": 1200,
            "height": 630,
        }
    if settings_obj.hero_poster:
        return {
            "url": absolute_url(request, settings_obj.hero_poster.url),
            "width": 1920,
            "height": 1080,
        }
    return {
        "url": absolute_url(request, static("media/hero-poster.jpg")),
        "width": 1920,
        "height": 1080,
    }


def og_locales(language: str | None) -> tuple[str, str]:
    if (language or "uk").split("-")[0] == "en":
        return "en_US", "uk_UA"
    return "uk_UA", "en_US"


def organization_json_ld(request, settings_obj) -> str:
    lang = get_language() or "uk"
    home = localize_path("/", lang)
    payload = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": settings_obj.brand_name,
        "url": absolute_url(request, home),
        "telephone": settings_obj.phone,
        "email": settings_obj.email,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": settings_obj.address,
            "addressCountry": "UA",
        },
        "vatID": settings_obj.ipn,
        "taxID": settings_obj.edrpou,
        "logo": absolute_url(request, static("media/logo-pt.svg")),
    }
    return json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
