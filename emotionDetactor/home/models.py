from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

# Create your models here.


class Appointments(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True,
                            unique=True, null=False, blank=False)
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="doctor"
    )
    patient = models.CharField(null=True, max_length=100)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    description = models.TextField(null=True)
    phone_number = models.IntegerField(null=True)
