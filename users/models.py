from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name="st", on_delete=models.CASCADE)
    is_driver = models.BooleanField(default=False)
