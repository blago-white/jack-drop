from django.db.models.signals import post_save, post_delete

from ..services.items import ItemService
from .models import Item


def update_set_price(
        *args,
        instance: Item,
        item_service: ItemService = None,
        **kwargs):
    print(instance.sets.all())


post_save.connect(update_set_price, sender=Item)
post_delete.connect(update_set_price, sender=Item)
