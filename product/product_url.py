from django.urls import path
from product import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('products_list/', views.products_list, name='product_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)