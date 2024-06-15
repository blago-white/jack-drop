from django.db import models

from items.models.models import Item


class InventoryItem(models.Model):
    user_id = models.PositiveIntegerField()
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"Inventory item: {self.item}"
