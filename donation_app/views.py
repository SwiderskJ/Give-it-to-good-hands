from django.shortcuts import render
from django.views import View
from donation_app.models import Donation, Institution
from django.core.paginator import Paginator
import random


class LandingPageView(View):

    def get(self, request):
        num_of_donations = 0
        donations = Donation.objects.all()

        for donation in donations:
            donation.quantity += num_of_donations
        num_of_institutions = Institution.objects.all().count()

        if num_of_institutions is None:
            num_of_institutions = 0

        fundations = []
        fundations_list = Institution.objects.filter(type=1)
        for item in fundations_list:
    
        print(fundations)
        page_number = request.GET.get('page')


        return render(request, 'index.html', context={
            'donations': num_of_donations,
            'institutions': num_of_institutions,
            'fundations': fundations,

        })


class AddDonationView(View):

    def get(self, request):
        return render(request, 'form.html')

