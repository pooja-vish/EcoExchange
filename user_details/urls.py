from django.urls import path
from product import views
from django.conf import settings
from django.conf.urls.static import static
from user_details import views
from .forms import LoginForm, MyPasswordChangedForm, MyPasswordResetForm, MySetPasswordForm
from django.contrib.auth import views as auth_views

from .views import MyPasswordResetConfirmView

app_name = 'user_details'
urlpatterns = [
    path('userdetails/', views.login_view, name='login_details'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('seller/<int:user_id>/', views.seller_desc_view, name='seller_desc'),
    path('buy-coins/', views.buy_coins, name='buy_coins'),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('update-coins-balance/', views.update_coins_balance, name='update_coins_balance'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='user_details/password_change.html',
                                                                   form_class=MyPasswordChangedForm,
                                                                   success_url='/password_change/done/'),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='user_details'
                                                                                          '/password_change_done.html'),
         name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='user_details/password_reset.html',
        form_class=MyPasswordResetForm, success_url='/password_reset/done/',
        email_template_name='user_details/password_reset_email.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='user_details/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='user_details/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('logout/', views.logout, name='logout'),
    path('user_visit_history/', views.user_visit_history_view, name='user_visit_history'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
