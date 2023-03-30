from django.shortcuts import render
from django.views import View
from donation_app.models import Donation, Institution, Category
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User


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

    def post(self, request):

        donation = Donation.objects.create(
            quantity=request.POST.get('bags'),
            address=request.POST.get('address'),
            institution=Institution.objects.get(name=request.POST.get('organization')),
            phone_number=request.POST.get('phone'),
            city=request.POST.get('city'),
            zip_code=request.POST.get('postcode'),
            pick_up_date=request.POST.get('date'),
            pick_up_time=request.POST.get('time'),
            pick_up_comment=request.POST.get('more_info'),
            user=User.objects.get(username=request.user)
        )
        categories = request.POST.getlist('categories')
        for category in categories:
            donation.categories.add(Category.objects.get(id=int(category)))

        return redirect(reverse('confirm'))


class FormConfirmView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        return render(request, 'form-confirmation.html')
