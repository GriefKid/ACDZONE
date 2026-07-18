from django import forms

from apps.core.translations import translate


class BootstrapStyledFormMixin:
    """Injects Bootstrap-friendly CSS classes into every field's widget,
    and runs every field's label through translate() (apps/core/
    translations.py) so English pages show English labels.

    Shared by apps/accounts/forms.py and apps/shop/forms.py — any form
    that mixes this in picks up the modern .form-control / .form-check-input
    styling already defined in static/css/style.css, instead of the
    completely unstyled <input> tags that plain {{ form.as_p }} produces
    on its own.

    Safe on fields we didn't define ourselves too (e.g. username,
    password1, password2 from Django's own AuthenticationForm /
    UserCreationForm) — translate() only ever acts on strings it
    recognizes in its own Persian-keyed table, so it's a no-op for
    anything else.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = translate(str(field.label))
            widget = field.widget
            existing = widget.attrs.get('class', '')
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = (existing + ' form-check-input').strip()
            else:
                widget.attrs['class'] = (existing + ' form-control').strip()
                widget.attrs.setdefault('placeholder', field.label)
