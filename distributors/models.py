from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()


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


class Valuer(models.Model):
    valuer_name = models.CharField(max_length=100)
    valuer_email = models.EmailField(null=True, blank=True)
    valuer_number = models.PositiveIntegerField(null=True, blank=True)
    valuer_address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.valuer_name


class ConsignmentNote(models.Model):
    sender_name = models.ForeignKey(
        'users.CustomerRelation', on_delete=models.DO_NOTHING, related_name='sender_name')
    consignee = models.ForeignKey(
        'users.CustomerRelation', on_delete=models.DO_NOTHING, related_name='consignee')
    reference_no = models.CharField(max_length=100, null=True, blank=True)
    route = models.ForeignKey(
        'users.Route', on_delete=models.CASCADE, null=True, blank=True)
    town = models.ForeignKey(
        'main.Town', on_delete=models.DO_NOTHING, null=True, blank=True)
    document = models.ForeignKey('main.Document', on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    bundle = models.PositiveIntegerField()
    rate = models.PositiveIntegerField()
    per = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    tax = models.CharField(max_length=100, null=True, blank=True)
    inclusive = models.CharField(max_length=100, null=True, blank=True)
    tracking_no = models.PositiveIntegerField(default=0)
    is_delivered = models.BooleanField(default=False)
    valuer = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True)
    date_created = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        db_table = 'consignment_note'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # check if date_created is provided and if not, set it to today
        if self.date_created:
            self.date_created = self.date_created
        else:
            self.date_created = datetime.date.today()
