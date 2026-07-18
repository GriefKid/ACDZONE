from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    """Django's UserAdmin behaviour, themed with django-unfold, with our
    own fieldsets (not just UserAdmin.fieldsets + one appended section) so
    related fields sit on the same row instead of every field getting its
    own — first_name/last_name together, phone_number folded into Personal
    info instead of a separate late section, the three permission
    checkboxes together, and the two date fields together.

    "Personal info" / "Permissions" / "Important dates" reuse Django's own
    real gettext_lazy — those three already have correct, bundled Persian
    translations shipped with Django itself, no compiled catalog of our
    own needed for them specifically."""

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (('first_name', 'last_name'), 'email', 'phone_number')}),
        (_('Permissions'), {
            'fields': (('is_active', 'is_staff', 'is_superuser'), 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': (('last_login', 'date_joined'),)}),
    )
