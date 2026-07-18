from django import forms

from apps.core.forms import BootstrapStyledFormMixin

from .models import Order


class OrderRequestForm(BootstrapStyledFormMixin, forms.ModelForm):
    """Collected when a logged-in user clicks "خرید" on a product. This
    only registers the purchase *request* (stage defaults to 'submitted')
    — the actual payment happens manually afterwards, via WhatsApp/
    Telegram/Bale, per the sales process documented in models.py."""

    class Meta:
        model = Order
        fields = ('full_name', 'contact_number', 'email')
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'contact_number': 'شماره واتساپ/تلگرام/بله',
            'email': 'ایمیل',
        }
