from django.apps import AppConfig

from apps.core.translations import translate_lazy as _


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.shop'
    label = 'shop'
    verbose_name = _('شاپ')
