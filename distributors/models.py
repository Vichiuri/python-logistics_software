from django.db import models

# Create your models here.


class Vehicle(models.Model):
    vehicle_name = models.CharField(max_length=100)
    capacity = models.CharField(max_length=50, null=True, blank=True)
    company = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.vehicle_name
