# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

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
