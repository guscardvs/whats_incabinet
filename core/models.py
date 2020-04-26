from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()


class UserItem(models.Model):
    item = models.ForeignKey(
        to=Item, on_delete=models.CASCADE, to_field='name')
    amount = models.IntegerField(default=0)

    @staticmethod
    def create_user_item(name: str, amount: int, **kwargs) -> models.Model:
        item = Item.objects.get(name=name)
        return UserItem(item=item, amount=amount)


class Profile(models.Model):
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, to_field='username')
    item = models.ManyToManyField(to=UserItem)
