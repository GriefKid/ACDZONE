from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from apps.core.forms import BootstrapStyledFormMixin

from .models import User


class LoginForm(BootstrapStyledFormMixin, AuthenticationForm):
    pass


class SignUpForm(BootstrapStyledFormMixin, UserCreationForm):
    email = forms.EmailField(required=True, label='ایمیل')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number')
