from django.db import models

FUNDATION_TYPE = (
    ('fundacja', 'Fundacja'),
    ('op', 'Organizacja pozarządowa'),
    ('zl', 'Zbiórka lokalna'),
)


class Category(models.Model):
    name = models.CharField(max_length=64)


class Institution(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    type = models.CharField(choices=FUNDATION_TYPE, default='fundacja')
