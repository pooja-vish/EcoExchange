from django.urls import path
from product import views
from django.conf import settings
from django.conf.urls.static import static
from .views import AuctionCreateView, AuctionUpdateView, AuctionDeleteView, AuctionListView, AuctionRealTimeView

urlpatterns = [

    path('product/<int:pk>', views.product_detail,name='product_detail'),
    path('products/', views.products, name='products'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('aboutus/',views.aboutus, name='aboutus'),
    path('', views.homepage, name='homepage'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart_detail/', views.cart_detail,name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_item_to_cart, name='cart_add_item'),
    path('cart/remove/<int:item_id>/', views.remove_item_from_cart, name='cart_remove_item'),
    path('cart/delete/<int:item_id>/', views.delete_item_from_cart, name='cart_delete_item'),
    path('products_list/cart/add/<int:product_id>/', views.addtocart, name='addtocart'),
    path('auction/<int:product_id>/', views.auction_view, name='auction_view'),
    path('auctions/', AuctionListView.as_view(), name='auction_list'),
    path('auction/create/', AuctionCreateView.as_view(), name='auction_create'),
    path('auction/update/<int:pk>/', AuctionUpdateView.as_view(), name='auction_update'),
    path('auction/delete/<int:pk>/', AuctionDeleteView.as_view(), name='auction_delete'),
    path('checkout/', views.checkout, name='checkout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
