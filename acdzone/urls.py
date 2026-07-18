"""
Root URL configuration for acdzone.

Admin stays outside i18n_patterns (plain /admin/ path); Unfold has its own
in-panel language switcher. Every public-facing page is wrapped in
i18n_patterns so Persian is served at the site root (/) and English under
/en/ (prefix_default_language=False keeps the default language, Persian,
unprefixed).
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # provides the set_language view
]

urlpatterns += i18n_patterns(
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.shop.urls')),
    path('', include('apps.blog.urls')),
    path('', include('apps.support.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
