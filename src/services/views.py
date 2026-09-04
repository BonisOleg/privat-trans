from django.shortcuts import get_object_or_404, render

from src.core.models import PageSEO
from src.leads.forms import LeadForm
from src.services.models import Service


def service_list(request):
    seo = PageSEO.objects.filter(slug="services").first()
    services = Service.objects.filter(is_published=True)
    return render(
        request,
        "services/list.html",
        {
            "page_title": seo.title if seo else "Послуги",
            "meta_description": seo.description if seo else "",
            "page_h1": seo.h1 if seo else "",
            "services": services,
        },
    )


def service_detail(request, slug: str):
    service = get_object_or_404(Service, slug=slug, is_published=True)
    form = LeadForm(initial={"service": service.title, "cargo": service.title})
    return render(
        request,
        "services/detail.html",
        {
            "page_title": service.title,
            "meta_description": service.teaser,
            "service": service,
            "lead_form": form,
        },
    )
