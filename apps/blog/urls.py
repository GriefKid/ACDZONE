from django.urls import path

from . import views

# <uslug:...> (unicode-aware slug matching, needed because Persian slugs
# don't match the built-in ASCII-only <slug:...> — see
# apps/core/converters.py) is registered once for the whole project in
# apps/core/apps.py's CoreConfig.ready(), not here — see that file for why.

app_name = 'blog'

urlpatterns = [
    path('acdnews/', views.acdnews, name='acdnews'),
    path('acdnews/<uslug:slug>/', views.news_detail, name='news_detail'),
    path('acdnotes/', views.acdnotes, name='acdnotes'),
    path('acdnotes/<uslug:slug>/', views.notes_detail, name='notes_detail'),
]
