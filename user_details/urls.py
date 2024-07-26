from django.urls import path
from product import views
from django.conf import settings
from django.conf.urls.static import static
from user_details import views
from .forms import LoginForm, MyPasswordChangedForm
from django.contrib.auth import views as auth_views

app_name = 'user_details'
urlpatterns = [
   path('userdetails/', views.login_view, name='login_details'),
   path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
   path('seller/<int:user_id>/', views.seller_desc_view, name='seller_desc'),
   path('buy-coins/', views.buy_coins, name='buy_coins'),
   path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
   path('update-coins-balance/', views.update_coins_balance, name='update_coins_balance'),
   path('profile/', views.ProfileView.as_view(), name='profile'),
   path('passwordchange/',
        auth_views.PasswordChangeView.as_view(template_name='changepassword.html'),
        name='password_change'),
   path('passwordchangedone/',
        auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),
        name='password_change_done'),
]
