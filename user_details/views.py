from django.shortcuts import render

# Create your views here.

def login_view(request):
    error_message = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:

            login(request, user)  # Ensure this line has `request` and `user`
            return redirect('index')  # Replace 'home' with your desired URL name
        else:
            error_message = "Invalid email or password."
    return render(request, 'user_details/login.html')