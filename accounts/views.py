from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from vendors.models import Vendor
from rfq.models import RFQ
from procurement.models import PurchaseOrder, Invoice
from quotations.models import Quotation
from approvals.models import Approval

import re


# ---------------- LOGIN ----------------

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

            # Remember Me
            if request.POST.get('remember_me'):
                request.session.set_expiry(1209600)  # 14 Days

            else:
                request.session.set_expiry(0)

            messages.success(
                request,
                "Login Successful!"
            )

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


# ---------------- SIGNUP ----------------

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

        photo = request.FILES.get('photo')

        # Username Validation

        if len(username) < 4:

            messages.error(
                request,
                "Username must contain at least 4 characters"
            )

            return redirect('signup')

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists"
            )

            return redirect('signup')

        # Email Validation

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(
            email_pattern,
            email
        ):

            messages.error(
                request,
                "Invalid Email Address"
            )

            return redirect('signup')

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email already registered"
            )

            return redirect('signup')

        # Mobile Validation

        if not phone.isdigit():

            messages.error(
                request,
                "Phone number must contain digits only"
            )

            return redirect('signup')

        if len(phone) != 10:

            messages.error(
                request,
                "Phone number must be exactly 10 digits"
            )

            return redirect('signup')

        # Password Validation

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

        # Create User

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create Profile

        UserProfile.objects.create(
            user=user,
            phone=phone,
            role=role,
            country=country,
            photo=photo
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


# ---------------- DASHBOARD ----------------

def dashboard_view(request):

    if not request.user.is_authenticated:
        return redirect('login')

    profile = UserProfile.objects.get(
        user=request.user
    )

    context = {
        'profile': profile,
        'role': profile.role,
        'vendors_count': Vendor.objects.count(),
        'rfq_count': RFQ.objects.count(),
        'po_count': PurchaseOrder.objects.count(),
        'invoice_count': Invoice.objects.count(),
        'quotations_count': Quotation.objects.count(),
        'approvals_count': Approval.objects.count(),
    }

    return render(
        request,
        'accounts/dashboard.html',
        context
    )


# ---------------- FORGOT PASSWORD ----------------

def forgot_password_view(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:

            user = User.objects.get(
                email=email
            )

            messages.success(
                request,
                f"Account Found: {user.username}"
            )

            return redirect('reset_password')

        except User.DoesNotExist:

            messages.error(
                request,
                "Email Not Registered"
            )

    return render(
        request,
        'accounts/forgot_password.html'
    )


# ---------------- RESET PASSWORD ----------------

def reset_password_view(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        new_password = request.POST.get(
            "new_password"
        )

        confirm_password = request.POST.get(
            "confirm_password"
        )

        if new_password != confirm_password:

            messages.error(
                request,
                "Passwords Do Not Match"
            )

            return redirect(
                'reset_password'
            )

        try:

            user = User.objects.get(
                username=username
            )

            user.set_password(
                new_password
            )

            user.save()

            messages.success(
                request,
                "Password Updated Successfully"
            )

            return redirect('login')

        except User.DoesNotExist:

            messages.error(
                request,
                "User Not Found"
            )

    return render(
        request,
        'accounts/reset_password.html'
    )


# ---------------- LOGOUT ----------------

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged Out Successfully"
    )

    return redirect('login')