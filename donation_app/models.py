from django.db import models

FUNDATION_TYPE = (
    (1, 'Fundacja'),
    (2, 'Organizacja pozarządowa'),
    (3, 'Zbiórka lokalna'),
)


class Category(models.Model):
    name = models.CharField(max_length=64)


class Institution(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    type = models.IntegerField(choices=FUNDATION_TYPE, default=1)
    categories = models.ManyToManyField(Category)
