from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.user_orders, name='user_orders'),
    path('onsale/', views.seller_products, name='ordered_products'),

]
