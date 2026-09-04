from django.urls import reverse
from django.utils.translation import get_language

from src.core.i18n import lang_switch_map
from src.core.models import SiteSettings
from src.core.site_blocks import get_site_blocks_map
from src.services.models import Service


def site_chrome(request):
    settings_obj = SiteSettings.load()
    services = Service.objects.filter(is_published=True)
    return {
        "site_settings": settings_obj,
        "site_blocks": get_site_blocks_map(),
        "nav_services": services,
        "lang_switch_urls": lang_switch_map(request.get_full_path()),
        "current_language": get_language() or "uk",
        "home_url": reverse("pages:home"),
    }
