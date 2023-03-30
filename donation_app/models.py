from django.db import models
from django.contrib.auth.models import User

FUNDATION_TYPE = (
    (1, 'Fundacja'),
    (2, 'Organizacja pozarządowa'),
    (3, 'Zbiórka lokalna'),
)


class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    type = models.IntegerField(choices=FUNDATION_TYPE, default=1)
    categories = models.ManyToManyField(Category)

    class Meta:
        verbose_name_plural = "Institutions"

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    is_taken = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Donations"


