from django import forms
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

from src.core.cities import CARGO_FTL, CARGO_LTL, CARGO_TURNKEY
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
CITY_ATTRS = {
    "class": "field__input",
    "autocomplete": "address-level2",
    "maxlength": "120",
    "spellcheck": "false",
    "autocapitalize": "words",
    "enterkeyhint": "next",
}
COUNTRY_ATTRS = {
    **CITY_ATTRS,
    "autocomplete": "country-name",
}


def is_honeypot_filled(data) -> bool:
    return bool(str(data.get(HONEYPOT_FIELD, "")).strip())


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
    from_city = forms.CharField(
        required=True,
        max_length=120,
        min_length=2,
        label=_("Звідки"),
        widget=forms.TextInput(attrs={**CITY_ATTRS}),
    )
    to_city = forms.CharField(
        required=True,
        max_length=120,
        min_length=2,
        label=_("Куди"),
        widget=forms.TextInput(attrs={**CITY_ATTRS}),
    )
    from_country = forms.CharField(
        required=True,
        max_length=120,
        min_length=2,
        label=_("Країна звідки"),
        widget=forms.TextInput(attrs={**COUNTRY_ATTRS}),
    )
    to_country = forms.CharField(
        required=True,
        max_length=120,
        min_length=2,
        label=_("Країна куди"),
        widget=forms.TextInput(attrs={**COUNTRY_ATTRS}),
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
            "from_country",
            "to_city",
            "to_country",
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
        self.fields["from_city"].widget.attrs["placeholder"] = _("Місто")
        self.fields["to_city"].widget.attrs["placeholder"] = _("Місто")
        self.fields["from_country"].widget.attrs["placeholder"] = _("Країна")
        self.fields["to_country"].widget.attrs["placeholder"] = _("Країна")
        self.fields["cargo"].choices = cargo_choices()

    def clean_from_city(self):
        return self._clean_place("from_city", _("Вкажіть місто"))

    def clean_to_city(self):
        return self._clean_place("to_city", _("Вкажіть місто"))

    def clean_from_country(self):
        return self._clean_place("from_country", _("Вкажіть країну"))

    def clean_to_country(self):
        return self._clean_place("to_country", _("Вкажіть країну"))

    def _clean_place(self, key, message):
        value = (self.cleaned_data.get(key) or "").strip()
        if len(value) < 2:
            raise forms.ValidationError(message)
        return value
