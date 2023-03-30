from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model

from donation_app.models import Donation
from user_app.forms import NewUserForm
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
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
        if request.user.is_authenticated:
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


class ProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        last_name = request.user.last_name
        email = User.objects.get(username=request.user).email
        donations = Donation.objects.filter(user=request.user.id, is_taken=False)
        archives = Donation.objects.filter(user=request.user.id, is_taken=True)
        return render(request, 'profile.html', context={
            'surname': last_name,
            'email': email,
            'donations': donations,
            'archives': archives,
        })


class ArchiveDonationView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, donation_id):
        donation = Donation.objects.get(id=donation_id)
        donation.is_taken = True
        donation.save()
        return redirect(reverse('profile'))
