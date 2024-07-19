from django.urls import path
from product_crud import views

urlpatterns = [
    path('', views.product_details, name='product_details'),
    path('product_update', views.product_update, name='product_update'),
    path('product_delete/<int:product_id>/', views.product_delete, name='product_delete'),
]