from django.apps import AppConfig

from apps.core.translations import translate_lazy as _


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    label = 'accounts'
    verbose_name = _('حساب‌های کاربری')
