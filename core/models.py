from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.IntegerField(default=0)

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, to_field='username')
    item = models.ManyToManyField(to=Item)