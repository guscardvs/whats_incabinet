from items import models

def create_item(name: str, description: str = '') -> models.Item:
    return models.Item.objects.create(name=name, description=description)

def get_or_create(name: str, description: str = '') -> models.Item:
    try:
        item = models.Item.objects.get(name=name)
    except models.Item.DoesNotExist:
        item = create_item(name, description)
    return item