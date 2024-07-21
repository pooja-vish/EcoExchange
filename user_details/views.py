# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.views import View
from user_details.forms import CustomerRegistrationForm
from django.contrib import messages


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
