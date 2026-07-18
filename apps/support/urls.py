from django.urls import path

from . import views

app_name = 'support'

urlpatterns = [
    path('support/', views.ticket_list, name='ticket_list'),
    path('support/new/', views.ticket_create, name='ticket_create'),
    path('support/<int:pk>/', views.ticket_detail, name='ticket_detail'),

    path('chat/unread-count/', views.chat_unread_count, name='chat_unread_count'),
    path('chat/messages/', views.chat_messages, name='chat_messages'),
    path('chat/send/', views.chat_send, name='chat_send'),
]
