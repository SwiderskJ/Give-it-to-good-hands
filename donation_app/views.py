from django.shortcuts import render
from django.views import View
from donation_app.models import Donation, Institution, Category
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class LandingPageView(View):

    def get(self, request):
        num_of_donations = 0
        donations = Donation.objects.all()

        for donation in donations:
            num_of_donations += donation.quantity
        num_of_institutions = Institution.objects.all().count()
        if num_of_institutions is None:
            num_of_institutions = 0

        page = request.GET.get('page')
        foundations = Institution.objects.filter(type=1).order_by('name')
        paginator_foundations = Paginator(foundations, 5)
        foundations = paginator_foundations.get_page(page)
        organizations = Institution.objects.filter(type=2).order_by('name')
        paginator_organizations = Paginator(organizations, 5)
        organizations = paginator_organizations.get_page(page)
        local_collection = Institution.objects.filter(type=3).order_by('name')
        paginator_local_collections = Paginator(local_collection, 5)
        local_collection = paginator_local_collections.get_page(page)

        return render(request, 'index.html', context={
            'donations': num_of_donations,
            'institutions': num_of_institutions,
            "foundations": foundations,
            "organizations": organizations,
            "collections": local_collection,
        })


class AddDonationView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()

        return render(request, 'form.html', context={
            'categories': categories,
            'institutions': institutions,
        })

