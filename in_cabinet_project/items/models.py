from typing import Optional
from django.db import models, transaction

# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()


class UserItem(models.Model):
    item = models.ForeignKey(
        to=Item, on_delete=models.CASCADE, related_name="user_items"
    )
    amount = models.IntegerField(default=0)
    profile = models.ForeignKey(
        to="users.Profile", on_delete=models.CASCADE, related_name="user_items"
    )
