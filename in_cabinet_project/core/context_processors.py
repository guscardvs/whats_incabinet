from django.http import HttpRequest

from items.models import Item


def get_item(request: HttpRequest) -> dict:
    return {"global_items": Item.objects.all()}
