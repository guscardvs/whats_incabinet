from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager

_User = get_user_model()

class User(_User):
    objects: UserManager
    profile: 'Profile'

    class Meta:
        proxy = True

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')