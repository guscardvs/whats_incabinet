import contextlib
from typing import Any
import profiles.models as profiles_models
import items.models as items_models
from user_items import models


def create_user_item(profile: profiles_models.Profile, item: items_models.Item, amount: Any = 0):
    return models.UserItem.objects.create(profile=profile, item=item, amount=amount)

def delete_user_item(pk: int, profile: profiles_models.Profile):
    with contextlib.suppress(models.UserItem.DoesNotExist):
        user_item: models.UserItem = models.UserItem.objects.get(pk=pk, profile=profile)
        user_item.delete()

def get_user_item(pk: int, profile: profiles_models.Profile) -> models.UserItem:
    return models.UserItem.objects.get(pk=pk, profile=profile)

def update_user_item(pk: int, profile: profiles_models.Profile, amount: Any):
    user_item = get_user_item(pk, profile)
    user_item.amount = amount
    user_item.save()
    return user_item

def list_items(profile: profiles_models.Profile):
    return models.UserItem.objects.filter(profile=profile)

def list_not_user_items(profile: profiles_models.Profile):
    return items_models.Item.objects.exclude(user_items__profile=profile)