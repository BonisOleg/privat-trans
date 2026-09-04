from django.contrib.admin.widgets import AdminTextareaWidget, AdminTextInputWidget

try:
    from unfold.widgets import INPUT_CLASSES, TEXTAREA_CLASSES
except ImportError:  # pragma: no cover
    INPUT_CLASSES = []
    TEXTAREA_CLASSES = []

_SKIP_CLASSES = frozenset(
    {
        "bg-white",
        "text-font-default-light",
        "border-base-200",
        "dark:bg-base-900",
        "dark:border-base-700",
        "dark:text-font-default-dark",
    }
)
_FORCE_CLASSES = ("bg-base-900", "text-base-100", "border-base-700", "placeholder-base-400")


def cms_control_classes(base_classes) -> list[str]:
    cleaned = [c for c in list(base_classes or []) if c not in _SKIP_CLASSES]
    for cls in _FORCE_CLASSES:
        if cls not in cleaned:
            cleaned.append(cls)
    return cleaned


class CmsAdminTextInputWidget(AdminTextInputWidget):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs["class"] = " ".join(cms_control_classes(INPUT_CLASSES))


class CmsAdminTextareaWidget(AdminTextareaWidget):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs["class"] = " ".join(cms_control_classes(TEXTAREA_CLASSES))


def apply_readable_widget(widget) -> None:
    from django.forms.widgets import CheckboxInput, ClearableFileInput, Select, SelectMultiple
    from tinymce.widgets import TinyMCE

    if isinstance(widget, (CheckboxInput, Select, SelectMultiple, ClearableFileInput, TinyMCE)):
        return
    classes = widget.attrs.get("class", "")
    parts = classes.split() if isinstance(classes, str) else list(classes or [])
    widget.attrs["class"] = " ".join(cms_control_classes(parts))
