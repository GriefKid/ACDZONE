from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('countries/<uslug:slug>/', views.country_detail, name='country_detail'),
    path(
        'countries/<uslug:country_slug>/attractions/<uslug:attraction_slug>/',
        views.attraction_detail, name='attraction_detail',
    ),
    path(
        'countries/<uslug:country_slug>/hotels/<uslug:hotel_slug>/',
        views.hotel_detail, name='hotel_detail',
    ),
    path('representatives/<uslug:slug>/', views.representative_detail, name='representative_detail'),
    path('notifications/<int:pk>/open/', views.notification_open, name='notification_open'),
    path('notifications/mark-all-read/', views.notifications_mark_all_read, name='notifications_mark_all_read'),

    path('notifications/unread-count/', views.notifications_unread_count, name='notifications_unread_count'),
    path('notifications/list/', views.notifications_list, name='notifications_list'),
]
