from django.apps import AppConfig

from apps.core.translations import translate_lazy as _


class SupportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.support'
    label = 'support'
    verbose_name = _('پشتیبانی')
