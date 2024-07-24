# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.views import View
from user_details.forms import CustomerRegistrationForm
from django.contrib import messages
from .models import Member, Transaction
import json
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from product.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

def login_view(request):
    error_message = None
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print("ello")
        print(form.is_valid())
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')  # Replace 'index' with your desired URL name
            else:
                error_message = "Invalid email or password."

        else:
            print(form.errors)

    return render(request, 'user_details/login.html', {'form': form, 'error_message': error_message})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'registration/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Your account has been created!')
            return redirect('login_details')  # Redirect to login page after successful registration
        # If form is not valid, render the registration page again with the form and errors
        else:
            messages.warning(request, 'Please correct the error below.')
        return render(request, 'registration/customerregistration.html', {'form': form})


def seller_desc_view(request, user_id):
    seller = get_object_or_404(Member, id=user_id)
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
    return render(request, 'user_details/payment.html',{'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLISHABLE_KEY })

