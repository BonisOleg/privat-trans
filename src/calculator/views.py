from django.shortcuts import render

from src.core.models import PageSEO
from src.leads.forms import LeadForm


def calculator_page(request):
    seo = PageSEO.objects.filter(slug="calculator").first()
    return render(
        request,
        "calculator/page.html",
        {
            "page_title": seo.title if seo else "Калькулятор",
            "meta_description": seo.description if seo else "",
            "page_h1": seo.h1 if seo else "",
            "lead_form": LeadForm(),
        },
    )
