from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.

class Regions(models.Model):
    region = models.CharField(max_length=255, null=False, blank=False, unique=True, verbose_name='Region')
    code = models.CharField(max_length=255, null=False, blank=False, unique=True, verbose_name='Code')
    status = models.BooleanField(verbose_name='Status', default=True)
    dateRegistered = models.DateTimeField(default=timezone.now)

    def __str__(self):  # __unicode__ for Python 2
        region_name = str(self.region)
        return region_name


class Towns(models.Model):
    town = models.CharField(max_length=255, null=False, blank=False, verbose_name='Ville')
    region = models.ForeignKey(Regions, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, null=False, blank=False, unique=True, verbose_name='Code')
    status = models.BooleanField(verbose_name='Status', default=True)
    dateRegistered = models.DateTimeField(default=timezone.now)

    def __str__(self):  # __unicode__ for Python 2
        town_name = str(self.town)
        return town_name

    @property
    def name_region(self):
        return self.region.region


class Agencies(models.Model):
    agency = models.CharField(max_length=255, null=False, blank=False, unique=True, verbose_name='Agence')
    code = models.CharField(max_length=255, null=False, blank=False, unique=False, verbose_name='Code')
    town = models.ForeignKey(Towns, on_delete=models.CASCADE, verbose_name='Ville')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='address')
    telephone = models.CharField(max_length=255, null=True, blank=True, verbose_name='telephone')
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name='email')
    status = models.BooleanField(verbose_name='Status', default=True)
    dateRegistered = models.DateTimeField(default=timezone.now)

    def __str__(self):  # __unicode__ for Python 2
        agency_name = str(self.agency)
        return agency_name

    @property
    def name_town(self):
        return self.town.town
