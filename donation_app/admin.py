from django.contrib import admin

from donation_app.models import Category, Institution, Donation


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'type']


class DonationAdmin(admin.ModelAdmin):
    list_display = ['quantity', 'institution', 'address', 'phone_number', 'city', 'zip_code',
                    'pick_up_date', 'pick_up_time', 'pick_up_comment', 'user']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Donation, DonationAdmin)
