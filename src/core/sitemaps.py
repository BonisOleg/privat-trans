from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from src.core.models import SiteSettings
from src.services.models import Service

STATIC_PRIORITIES = {
    "pages:home": 1.0,
    "services:list": 0.8,
    "pages:about": 0.7,
    "pages:fleet": 0.7,
    "pages:contacts": 0.7,
    "faq:list": 0.6,
    "pages:privacy": 0.3,
}


class I18nSitemap(Sitemap):
    i18n = True
    alternates = True
    x_default = True


class StaticViewSitemap(I18nSitemap):
    changefreq = "weekly"
    protocol = None

    def items(self):
        return list(STATIC_PRIORITIES)

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return STATIC_PRIORITIES.get(item, 0.5)

    def lastmod(self, item):
        return SiteSettings.get_solo().updated_at


class ServiceSitemap(I18nSitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_published=True)

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {
    "static": StaticViewSitemap,
    "services": ServiceSitemap,
}
