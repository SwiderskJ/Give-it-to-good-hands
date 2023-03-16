from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from user_app.forms import NewUserForm


class LoginView(View):

    def get(self, request):
        if request.user:
            return redirect(reverse('main_site'))
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password,
        )

        if user:
            login(request, user)
            return redirect(reverse('main_site'))
        else:
            messages.success(request, "Niepoprawne dane")
            return redirect(reverse('register'))


class RegisterView(View):

    def get(self, request):
        if request.user:
            return redirect(reverse('main_site'))
        form = NewUserForm()
        return render(request, 'register.html', context={'form': form})

    def post(self, request):

        User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password1'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email')
            )
        messages.success(request, "Registration successful.")
        return redirect(reverse('login'))


class LogoutView(View):
    def get(self, request):
        logout(request)

        return redirect(reverse('main_site'))