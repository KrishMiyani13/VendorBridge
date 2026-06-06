from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import re
from .models import UserProfile

def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            messages.success(request, "Login Successful!")
            return redirect('dashboard')

        else:
            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(
        request,
        'accounts/login.html'
    )




def signup_view(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        username = request.POST.get('username')
        email = request.POST.get('email')

        phone = request.POST.get('phone')
        role = request.POST.get('role')
        country = request.POST.get('country')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation

        if len(username) < 4:

            messages.error(
                request,
                "Username must contain at least 4 characters"
            )

            return redirect('signup')

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Username already exists"
            )

            return redirect('signup')

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(email_pattern, email):

            messages.error(
                request,
                "Invalid email address"
            )

            return redirect('signup')

        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                "Email already registered"
            )

            return redirect('signup')

        if not phone.isdigit():

            messages.error(
                request,
                "Phone number must contain only digits"
            )

            return redirect('signup')

        if len(phone) != 10:

            messages.error(
                request,
                "Phone number must be exactly 10 digits"
            )

            return redirect('signup')

        if len(password) < 8:

            messages.error(
                request,
                "Password must be at least 8 characters"
            )

            return redirect('signup')

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match"
            )

            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            role=role,
            country=country,
            password=password,
            photo=request.FILES.get('photo')
        )

        messages.success(
            request,
            "Registration Successful"
        )

        return redirect('login')

    return render(
        request,
        'accounts/signup.html'
    )

def dashboard_view(request):

    if not request.user.is_authenticated:
        return redirect('login')

    return render(
        request,
        'accounts/dashboard.html'
    )


def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged Out Successfully"
    )

    return redirect('login')