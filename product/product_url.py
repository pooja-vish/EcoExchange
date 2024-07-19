from django.urls import path
from product import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.homepage, name='homepage'),
    path('products_list/', views.products_list, name='product_list'),
    path('product/<int:pk>', views.product_detail, name='product_detail'),
    path('cart_detail/',views.cart_detail,name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_item_to_cart, name='cart_add_item'),
    path('cart/remove/<int:item_id>/', views.remove_item_from_cart, name='cart_remove_item'),
    path('cart/delete/<int:item_id>/', views.delete_item_from_cart, name='cart_delete_item'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


