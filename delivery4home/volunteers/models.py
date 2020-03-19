from django.db import models
from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField


class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='volunteer')
    name = models.CharField(max_length=100)
    location = PlainLocationField(default='-1.0, -1.0')

