from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('acdpay/', views.acdpay, name='acdpay'),
    path('acdballoons/', views.acdballoons, name='acdballoons'),
    path('buy/<int:product_id>/', views.buy_product, name='buy'),
    path('my-products/', views.my_products, name='my_products'),
    path('my-products/<int:pk>/', views.order_detail, name='order_detail'),
    path('my-products/<int:pk>/delete/', views.order_delete, name='order_delete'),
]
