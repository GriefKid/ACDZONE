from django.apps import AppConfig

from apps.core.translations import translate_lazy as _


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blog'
    label = 'blog'
    verbose_name = _('بلاگ')
