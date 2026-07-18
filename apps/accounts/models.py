from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.translations import translate_lazy as _


class User(AbstractUser):
    """
    Custom user model for ACD Zone.

    We start the project with our own user model (even though today it just
    extends AbstractUser) so that later additions such as an avatar, national
    ID, or address fields for order shipping don't require the painful
    "swap the user model mid-project" migration. See project README for the
    membership / profile roadmap.
    """

    # NOTE: this used to be wrapped in Django's real gettext_lazy('phone
    # number') — that needs a compiled .mo catalog to actually translate,
    # which this project doesn't have (see apps/core/translations.py), so
    # it silently always showed the English msgid regardless of the admin's
    # active language. translate_lazy is backed by our own dict instead and
    # actually switches.
    phone_number = models.CharField(_('شماره موبایل'), max_length=20, blank=True)

    def __str__(self):
        return self.get_username()
