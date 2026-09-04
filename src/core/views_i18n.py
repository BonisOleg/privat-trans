from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation
from django.views.decorators.http import require_POST

from src.core.i18n import localize_path


@require_POST
def set_language(request):
    lang = request.POST.get("language", settings.LANGUAGE_CODE)
    allowed = {code for code, _name in settings.LANGUAGES}
    if lang not in allowed:
        lang = settings.LANGUAGE_CODE

    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    target = localize_path(next_url, lang)

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
