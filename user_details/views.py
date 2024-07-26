# views.py
from django.contrib.auth.models import Permission, User
from django.contrib.auth.views import PasswordResetConfirmView
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, CustomerProfileForm
from django.views import View
from user_details.forms import CustomerRegistrationForm
from django.contrib import messages
from .models import Member, Transaction
import json
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from product.models import Product
from .models import Member

stripe.api_key = settings.STRIPE_SECRET_KEY


def login_view(request):
    error_message = None
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_details:profile')  # Replace 'index' with your desired URL name
            else:
                error_message = "Invalid email or password."

        else:
            print(form.errors)

    return render(request, 'user_details/login.html', {'form': form, 'error_message': error_message})


@receiver(post_save, sender=Member)
def assign_default_permissions(sender, instance, created, **kwargs):
    if created:
        # Define the permissions you want to assign
        permissions = [
            'add_product',
            'change_product',
            'delete_product',
            'view_product',
            'add_order',
            'view_order',
            'add_review',
            'view_review',
            'delete_review',
            'view_auction',
            'participate_auction',
            'add_bid',
            'view_bid',
            'add_cartitem',
            'view_cartitem',
            'change_cartitem',
            'delete_cartitem'
        ]

        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                instance.user_permissions.add(permission)
            except Permission.DoesNotExist:
                print(f"Permission {perm} does not exist.")


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'registration/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the form data to the database
            # Authenticate the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Adjust according to your form fields
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Log in the user
                messages.success(request, 'Your account has been created and you are now logged in!')
                return redirect('user_details:profile')  # Redirect to the profile page after successful login
        else:
            # If form is not valid, render the registration page again with the form and errors
            messages.warning(request, 'Please correct the error below.')
        return render(request, 'registration/customerregistration.html', {'form': form})

def seller_desc_view(request, user_id):
    seller = get_object_or_404(Member, user_id=user_id)
    products = Product.objects.filter(user=seller)
    return render(request, 'user_details/seller_desc.html', {'seller': seller, 'products': products})


@login_required
def create_payment_intent(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        quantity = int(data.get('quantity'))

        # Define prices
        COIN_PRICES = {
            50: 500,  # 50 coins for $5.00
            100: 1000,  # 100 coins for $10.00
        }

        if quantity not in COIN_PRICES:
            return JsonResponse({'error': 'Invalid quantity'}, status=400)

        price = COIN_PRICES[quantity]

        # Create a Payment Intent
        intent = stripe.PaymentIntent.create(
            amount=price,
            currency='usd',
            payment_method_types=['card'],
        )

        return JsonResponse({'clientSecret': intent.client_secret})


@login_required
def update_coins_balance(request):
    try:
        member = Member.objects.get(username=request.user.username)
    except Member.DoesNotExist:
        member = None
    if request.method == 'POST':
        data = json.loads(request.body)
        quantity = int(data.get('quantity'))
        transaction_id = data.get('transaction_id')

        if quantity <= 0:
            return JsonResponse({'success': False}, status=400)

        # Add coins to the user's balance

        member.coin_balance += quantity
        member.save()
        Transaction.objects.create(
            user=member,
            transaction_id=transaction_id,
            quantity=quantity,
            amount=quantity * 5.00  # Assuming $5.00 for 50 coins or $10.00 for 100 coins
        )

        return JsonResponse({'success': True})


@login_required
def buy_coins(request):
    return render(request, 'user_details/payment.html', {'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLISHABLE_KEY})


class ProfileView(View):
    def get(self, request):
        user = request.user
        try:
            member = Member.objects.get(id=user.id)
        except Member.DoesNotExist:
            member = None

        form = CustomerProfileForm(instance=member)
        return render(request, 'user_details/profile.html', {'form': form})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            mobile_no = form.cleaned_data['mobile_no']
            country = form.cleaned_data['country']

            # Update the Member profile linked to the current user
            Member.objects.filter(id=user.id).update(
                address=address,
                city=city,
                mobile_no=mobile_no,
                country=country
            )

            messages.success(request, 'Your profile has been updated!')
            return redirect('homepage')  # Redirect to profile page or any other appropriate page
        else:
            messages.warning(request, 'Please correct the error below.')
        return render(request, 'user_details/profile.html', {'form': form})


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user_details/password_reset_confirm.html'
    form_class = MySetPasswordForm

    def get(self, request, *args, **kwargs):
        print(f"UID: {kwargs['uidb64']}, Token: {kwargs['token']}")
        return super().get(request, *args, **kwargs)


def admin_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

@admin_required(login_url='/login/')
def user_visit_history_view(request):
    visits = request.COOKIES.get('visits', '[]')
    visits = json.loads(visits) if visits else []
    return render(request, 'user_details/user_visit_history.html', {'visits': visits})

