from django.db import models
from django.conf import settings
# Create your models here.


class Vehicle(models.Model):
    vehicle_name = models.CharField(max_length=100)
    capacity = models.CharField(max_length=50, null=True, blank=True)
    company = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.vehicle_name


class Driver(models.Model):
    name = models.CharField(max_length=100)
    national_id = models.PositiveIntegerField('ID', unique=True)
    users = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    mobile_number = models.PositiveIntegerField(
        'Mobile Number', unique=True, null=True, blank=True)
    email = models.EmailField(verbose_name="Email",
                              max_length=100, unique=True)

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(max_length=100)
    created = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'town'
        verbose_name = 'Town'
        verbose_name_plural = 'Towns'


class Route(models.Model):
    route_name = models.CharField(max_length=100, null=True, blank=True)
    cities = models.CharField(max_length=100, null=True, blank=True)
    created = models.BooleanField(default=False)

    def __str__(self):
        return self.route_name


class CustomerRelation(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_address = models.TextField(null=True, blank=True)
    town = models.ForeignKey(
        'Town', on_delete=models.DO_NOTHING, null=True, blank=True)
    Customer_pin = models.CharField(
        max_length=100, unique=True, null=True, blank=True)
    contact_person_number = models.PositiveIntegerField(null=True, blank=True)
    contact_person_name = models.CharField(
        max_length=100, null=True, blank=True)
    account = models.CharField(max_length=100, null=True, blank=True)
    created = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_name
