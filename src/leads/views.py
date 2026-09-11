from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from src.leads.forms import LeadForm, is_honeypot_filled
from src.leads.services import (
    is_lead_rate_limited,
    notify_lead,
    record_lead_submission,
    request_ip,
)


def _lead_success(request):
    return render(
        request,
        "leads/_success.html",
        {"message": _("Заявка відправлена")},
    )


@require_POST
def create_lead(request):
    if is_honeypot_filled(request.POST):
        return _lead_success(request)
    form = LeadForm(request.POST)
    if not form.is_valid():
        return render(
            request,
            "leads/_form.html",
            {"lead_form": form, "form_error": _("Перевірте поля форми.")},
        )
    ip = request_ip(request)
    if is_lead_rate_limited(ip):
        return render(
            request,
            "leads/_form.html",
            {
                "lead_form": form,
                "form_error": _("Забагато заявок з вашої мережі. Спробуйте пізніше."),
            },
        )
    lead = form.save()
    record_lead_submission(ip)
    notify_lead(lead)
    return _lead_success(request)
