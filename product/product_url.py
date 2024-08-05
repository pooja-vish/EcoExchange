from django.urls import path
from product import views
from django.conf import settings
from django.conf.urls.static import static
from .views import AuctionCreateView, AuctionUpdateView, AuctionDeleteView, AuctionListView, AuctionRealTimeView, AuctionAllListView

urlpatterns = [

    path('product/<int:pk>', views.product_detail,name='product_detail'),
    path('products/', views.products, name='products'),
    path('dashboard/<str:section>/', views.dashboard, name='dashboard'),
    path('dashboard/edit_profile/', views.dashboard, name='edit_profile'),
    #path('edit_profile/', views.dashboard, name='edit_profile'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('support/', views.support, name='support'),
    path('', views.homepage, name='homepage'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart_detail/', views.cart_detail,name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_item_to_cart, name='cart_add_item'),
    path('cart/remove/<int:item_id>/', views.remove_item_from_cart, name='cart_remove_item'),
    path('cart/delete/<int:item_id>/', views.delete_item_from_cart, name='cart_delete_item'),
    path('products_list/cart/add/<int:product_id>/', views.addtocart, name='addtocart'),
    path('auction_view/<int:product_id>/', views.auction_view, name='auction_view'),
    #path('auctions/', AuctionListView.as_view(), name='auction_list'),
    path('all_auctions/', AuctionAllListView.as_view(), name='all_auctions'),
    path('auction/create/', AuctionCreateView.as_view(), name='auction_list'),
    path('auction/update/<int:pk>/', AuctionUpdateView.as_view(), name='auction_update'),
    path('auction/delete/<int:pk>/', AuctionDeleteView.as_view(), name='auction_delete'),
    path('checkout/', views.checkout, name='checkout'),
    path('realtime/<int:product_id>/', views.AuctionRealTimeView.as_view(), name='auction_realtime'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
