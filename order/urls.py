from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.user_orders, name='user_orders'),
    path('onsale/', views.seller_products, name='ordered_products'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),


]
