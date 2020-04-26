from django.http import HttpRequest

from core import models


def get_item(request: HttpRequest) -> dict:
    return {'global_items': models.Item.objects.all()}
