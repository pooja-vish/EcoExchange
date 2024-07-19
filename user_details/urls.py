from django.urls import path
from product import views
from django.conf import settings
from django.conf.urls.static import static
from user_details import views
from .forms import LoginForm

urlpatterns = [
   path('userdetails/', views.login_view, name='login_details'),
   path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
]