from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation
from django.views.decorators.http import require_POST
from urllib.parse import urlparse

from src.core.i18n import collapse_double_prefix, localize_path


def _extract_next(request) -> str:
    """Same-origin relative path only; fall back to /."""
    candidates = [
        request.POST.get("next"),
        request.GET.get("next"),
        request.META.get("HTTP_REFERER"),
    ]
    for raw in candidates:
        if not raw:
            continue
        parsed = urlparse(raw)
        # Reject absolute URLs to other hosts.
        if parsed.scheme or parsed.netloc:
            host = request.get_host()
            if parsed.netloc and parsed.netloc != host:
                continue
            path = parsed.path or "/"
            if parsed.query:
                path = f"{path}?{parsed.query}"
            return path
        if raw.startswith("/"):
            return raw
    return "/"


@require_POST
def set_language(request):
    lang = request.POST.get("language", settings.LANGUAGE_CODE)
    allowed = {code for code, _name in settings.LANGUAGES}
    if lang not in allowed:
        lang = settings.LANGUAGE_CODE

    target = collapse_double_prefix(localize_path(_extract_next(request), lang))

    translation.activate(lang)
    response = HttpResponseRedirect(target)
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        lang,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
        secure=settings.LANGUAGE_COOKIE_SECURE,
        httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
        samesite=settings.LANGUAGE_COOKIE_SAMESITE,
    )
    return response
