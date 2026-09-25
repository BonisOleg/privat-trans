from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from src.core.sitemaps import sitemaps
from src.core.views import healthz
from src.core.views_i18n import set_language

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("healthz/", healthz, name="healthz"),
    path("i18n/setlang/", set_language, name="set_language"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt", include("src.core.robots_urls")),
]

urlpatterns += i18n_patterns(
    path("", include("src.pages.urls")),
    path("services/", include("src.services.urls")),
    path("faq/", include("src.faq.urls")),
    path("calculator/", include("src.calculator.urls")),
    path("leads/", include("src.leads.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
