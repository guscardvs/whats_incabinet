from django.db import models
import items.models as item_models
import profiles.models as profiles_models

# Create your models here.
class UserItem(models.Model):
    item = models.ForeignKey(
        to=item_models.Item, on_delete=models.CASCADE, related_name='user_items')
    profile = models.ForeignKey(to=profiles_models.Profile, on_delete=models.CASCADE, related_name='items')
    amount = models.IntegerField()

    