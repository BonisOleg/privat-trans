from django.shortcuts import redirect
from django.urls import reverse


def calculator_page(request):
    return redirect(f"{reverse('pages:home')}#lead-form")
