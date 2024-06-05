from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", primary_key=True
    )
    registeras = models.CharField(max_length=2, null=True)
    profile_image = models.ImageField(
        upload_to="user_profile", null=True, blank=True)
    emotion = models.CharField(null=True, max_length=100)
