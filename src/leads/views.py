from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from src.leads.forms import LeadForm
from src.leads.services import notify_lead


@require_POST
def create_lead(request):
    form = LeadForm(request.POST)
    if not form.is_valid():
        return render(
            request,
            "leads/_form.html",
            {"lead_form": form, "form_error": _("Перевірте поля форми.")},
        )
    lead = form.save()
    notify_lead(lead)
    return render(
        request,
        "leads/_success.html",
        {"message": _("Дякуємо за заявку")},
    )
