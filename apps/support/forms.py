from django import forms

from apps.core.forms import BootstrapStyledFormMixin
from apps.core.translations import translate_lazy as _


class TicketCreateForm(BootstrapStyledFormMixin, forms.Form):
    """Plain Form, not a ModelForm — a new ticket is really two objects at
    once (Ticket + its first TicketMessage), created together in
    views.ticket_create()."""
    subject = forms.CharField(label=_('موضوع'), max_length=200)
    body = forms.CharField(label=_('پیام'), widget=forms.Textarea(attrs={'rows': 5}))
