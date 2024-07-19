from django.urls import path
from product import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', views.index, name='index'),
    path('product/<int:pk>',views.product_detail,name='product_detail'),
    path('products_list/', views.products_list, name='product_list'),
    path('aboutus/',views.aboutus,name='aboutus'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
