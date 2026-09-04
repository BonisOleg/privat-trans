from django import forms
from django.utils.translation import gettext_lazy as _

from src.leads.models import Lead


class LeadForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        label=_("Погоджуюсь на обробку персональних даних"),
    )

    class Meta:
        model = Lead
        fields = (
            "name",
            "phone",
            "email",
            "from_city",
            "to_city",
            "cargo",
            "service",
            "message",
            "consent",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "field__input", "autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"class": "field__input", "type": "tel", "autocomplete": "tel"}),
            "email": forms.EmailInput(attrs={"class": "field__input", "autocomplete": "email"}),
            "from_city": forms.TextInput(attrs={"class": "field__input", "list": "pt-cities"}),
            "to_city": forms.TextInput(attrs={"class": "field__input", "list": "pt-cities"}),
            "cargo": forms.TextInput(attrs={"class": "field__input"}),
            "service": forms.HiddenInput(),
            "message": forms.Textarea(attrs={"class": "field__textarea", "rows": 3}),
        }
        labels = {
            "name": _("Ім’я"),
            "phone": _("Телефон"),
            "email": _("Email"),
            "from_city": _("Звідки"),
            "to_city": _("Куди"),
            "cargo": _("Тип вантажу"),
            "message": _("Коментар"),
        }
