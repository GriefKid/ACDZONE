from django.apps import AppConfig

from apps.core.translations import translate_lazy as _


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    label = 'core'
    verbose_name = _('مدیریت سایت')

    def ready(self):
        # Registered once, here, rather than inside a urls.py (as it used to
        # be, in apps/blog/urls.py) — django.urls.register_converter() only
        # warns (DeprecationWarning) if the same name is registered twice
        # today, but is documented to hard-fail with ValueError once Django
        # drops that grace period (see django/urls/converters.py). Both
        # apps/blog/urls.py and apps/core/urls.py need the same <uslug:...>
        # converter (Persian post slugs and Persian country slugs alike —
        # see apps/core/converters.py), so registering it twice was only a
        # matter of time.
        #
        # AppConfig.ready() is guaranteed by Django to run exactly once,
        # after every app's models are imported and before any URLconf
        # module is ever imported — so registering it here means it's
        # always in place first, regardless of which app's urls.py Django
        # happens to import first.
        from django.urls import register_converter

        from apps.core.converters import UnicodeSlugConverter
        register_converter(UnicodeSlugConverter, 'uslug')
