from django import forms
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

from src.core.cities import CARGO_FTL, CARGO_LTL, CARGO_TURNKEY, CITIES
from src.leads.models import Lead

HONEYPOT_FIELD = "honeypot"
PHONE_VALIDATOR = RegexValidator(
    regex=r"^\+?[0-9\s\-()]{9,20}$",
    message=_("Введіть коректний номер телефону"),
)
SELECT_ATTRS = {
    "class": "field__select pt-select__native",
    "data-pt-select-native": "",
}


def is_honeypot_filled(data) -> bool:
    return bool(str(data.get(HONEYPOT_FIELD, "")).strip())


def city_choices():
    return [("", _("Оберіть місто")), *[(city, city) for city in CITIES]]


def cargo_choices():
    return [
        ("", _("Оберіть тип вантажу")),
        (CARGO_LTL, _("Збірний від 10 кг")),
        (CARGO_FTL, _("Повне авто (FTL) до 23 тонн")),
        (CARGO_TURNKEY, _("Під ключ (склад + митниця)")),
    ]


class LeadForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        label=_("Погоджуюсь на обробку персональних даних"),
    )
    from_city = forms.ChoiceField(
        choices=city_choices,
        required=True,
        label=_("Звідки"),
        widget=forms.Select(attrs=SELECT_ATTRS),
    )
    to_city = forms.ChoiceField(
        choices=city_choices,
        required=True,
        label=_("Куди"),
        widget=forms.Select(attrs=SELECT_ATTRS),
    )
    cargo = forms.ChoiceField(
        choices=cargo_choices,
        required=True,
        label=_("Тип вантажу"),
        widget=forms.Select(attrs=SELECT_ATTRS),
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
            "phone": forms.TextInput(
                attrs={
                    "class": "field__input",
                    "type": "tel",
                    "autocomplete": "tel",
                    "inputmode": "tel",
                }
            ),
            "email": forms.EmailInput(attrs={"class": "field__input", "autocomplete": "email"}),
            "service": forms.HiddenInput(),
            "message": forms.Textarea(attrs={"class": "field__textarea", "rows": 3}),
        }
        labels = {
            "name": _("Ім’я"),
            "phone": _("Телефон"),
            "email": _("Email"),
            "message": _("Коментар"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].validators.append(PHONE_VALIDATOR)
        self.fields["name"].validators.append(MinLengthValidator(2))
        self.fields["from_city"].choices = city_choices()
        self.fields["to_city"].choices = city_choices()
        self.fields["cargo"].choices = cargo_choices()
