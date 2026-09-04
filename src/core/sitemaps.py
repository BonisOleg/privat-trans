from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from src.faq.models import FaqItem
from src.services.models import Service


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return [
            "pages:home",
            "pages:about",
            "pages:contacts",
            "pages:privacy",
            "services:list",
            "faq:list",
            "calculator:page",
        ]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_published=True)

    def location(self, obj):
        return obj.get_absolute_url()


sitemaps = {
    "static": StaticViewSitemap,
    "services": ServiceSitemap,
}

# keep FaqItem import used for future expansion / seed integrity
_ = FaqItem
