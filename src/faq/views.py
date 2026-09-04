from django.shortcuts import render

from src.core.models import PageSEO
from src.faq.models import FaqItem
from src.leads.forms import LeadForm


def faq_list(request):
    seo = PageSEO.objects.filter(slug="faq").first()
    items = FaqItem.objects.filter(is_published=True)
    return render(
        request,
        "faq/list.html",
        {
            "page_title": seo.title if seo else "FAQ",
            "meta_description": seo.description if seo else "",
            "page_h1": seo.h1 if seo else "",
            "faq_items": items,
            "lead_form": LeadForm(),
        },
    )
