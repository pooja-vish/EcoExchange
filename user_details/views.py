# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.views import View
from user_details.forms import CustomerRegistrationForm
from django.contrib import messages
from .models import Member


def login_view(request):
    error_message = None
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')  # Replace 'index' with your desired URL name
            else:
                error_message = "Invalid email or password."

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
    seller = get_object_or_404(Member, user_id=user_id)
    return render(request, 'user_details/seller_desc.html', {'seller': seller})
