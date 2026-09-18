from django.shortcuts import render

from src.careers.models import Vacancy
from src.core.models import PageSEO, SiteSettings
from src.faq.models import FaqItem
from src.leads.forms import LeadForm
from src.services.models import Service
from src.social_proof.models import GalleryWork, Partner, Review


def _seo(slug: str, fallback_title: str, fallback_desc: str = ""):
    seo = PageSEO.objects.filter(slug=slug).first()
    if seo:
        return seo.title, seo.description, seo.h1
    return fallback_title, fallback_desc, ""


def home(request):
    settings_obj = SiteSettings.load()
    title, desc, h1 = _seo("home", settings_obj.default_title, settings_obj.default_description)
    context = {
        "page_title": title,
        "meta_description": desc,
        "page_h1": h1,
        "services": Service.objects.filter(is_published=True),
        "faq_home": FaqItem.objects.filter(is_published=True, show_on_home=True)[:5],
        "reviews": Review.objects.filter(is_published=True),
        "partners": Partner.objects.filter(is_published=True),
        "vacancies": Vacancy.objects.filter(is_published=True),
        "lead_form": LeadForm(),
    }
    return render(request, "pages/home.html", context)


def about(request):
    title, desc, h1 = _seo(
        "about",
        "Про нас — ПРИВАТ-ТРАНС",
        "З 2007 року на ринку міжнародних перевезень.",
    )
    return render(
        request,
        "pages/about.html",
        {
            "page_title": title,
            "meta_description": desc,
            "page_h1": h1,
            "vacancies": Vacancy.objects.filter(is_published=True),
            "gallery_works": GalleryWork.objects.filter(is_published=True),
        },
    )


def contacts(request):
    title, desc, h1 = _seo("contacts", "Контакти — ПРИВАТ-ТРАНС")
    return render(
        request,
        "pages/contacts.html",
        {
            "page_title": title,
            "meta_description": desc,
            "page_h1": h1,
            "lead_form": LeadForm(),
        },
    )


def privacy(request):
    title, desc, h1 = _seo("privacy", "Політика конфіденційності")
    return render(
        request,
        "pages/privacy.html",
        {
            "page_title": title,
            "meta_description": desc,
            "page_h1": h1,
        },
    )


def fleet(request):
    title, desc, h1 = _seo(
        "fleet",
        "Автопарк — ПРИВАТ-ТРАНС",
        "Власний автопарк і партнерський флот: тенти, рефрижератори, ізотерми, 10 кг–23 т.",
    )
    return render(
        request,
        "pages/fleet.html",
        {
            "page_title": title,
            "meta_description": desc,
            "page_h1": h1,
            "lead_form": LeadForm(),
        },
    )
