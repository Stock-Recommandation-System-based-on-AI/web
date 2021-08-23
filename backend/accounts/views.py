from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

def signup(request):
    if request.user.is_authenticated:
        return redirect('stock:main_page')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form = form.save()
            auth_login(request, form, backend="django.contrib.auth.backends.ModelBackend",)
            return redirect('stock:main_page')
    else:
        form = CustomUserCreationForm()
    context ={
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('stock:main_page')
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('stock:main_page')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('stock:main_page')


@login_required
def profile(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    context = {
        'user': user
    }
    return render(request, 'accounts/profile.html', context)