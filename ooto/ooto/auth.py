import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

logger = logging.getLogger(__name__)


def login_view(request):
    """Handle user login."""
    if request.method == "POST":
        # Check if this is a signup request
        if "signup" in request.POST:
            return signup_handler(request)

        # Otherwise handle login
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next", "home")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")

    next_url = request.GET.get("next", "home")
    return render(request, "ooto/auth/login.html", {"next": next_url})


def signup_handler(request):
    """Handle user signup."""
    username = request.POST.get("username")
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")

    # Validate signup information
    if not username or not password:
        messages.error(request, "Username and password are required.")
        return redirect("login")

    if password != confirm_password:
        messages.error(request, "Passwords don't match.")
        return redirect("login")

    if len(password) < 8:
        messages.error(request, "Password must be at least 8 characters.")
        return redirect("login")

    # Create new user
    try:
        user = User.objects.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        login(request, user)
        messages.success(request, "Account created successfully!")
        next_url = request.POST.get("next", "home")
        return redirect(next_url)
    except IntegrityError:
        messages.error(request, "Username already exists.")
        return redirect("login")
    except Exception as e:
        logger.error("Error creating user: %s", e)
        messages.error(request, "An error occurred. Please try again.")
        return redirect("login")


def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect("home")
