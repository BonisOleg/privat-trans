from django.utils.translation import get_language

CMS_LANGS = ("uk", "en")
FALLBACK_LANG = "uk"


def active_lang(language: str | None = None) -> str:
    lang = (language or get_language() or FALLBACK_LANG).split("-")[0]
    return lang if lang in CMS_LANGS else FALLBACK_LANG


def localized(obj, field: str, language: str | None = None) -> str:
    """CMS field *_uk / *_en with fallback to Ukrainian."""
    lang = active_lang(language)
    value = getattr(obj, f"{field}_{lang}", None)
    if value:
        return value
    return getattr(obj, f"{field}_{FALLBACK_LANG}", "") or ""
