from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("django.contrib.sitemaps.views.sitemap"))
    body = "\n".join(
        [
            "User-agent: *",
            "Disallow: /admin/",
            "Disallow: /leads/",
            f"Sitemap: {sitemap_url}",
            "",
        ]
    )
    return HttpResponse(body, content_type="text/plain")
