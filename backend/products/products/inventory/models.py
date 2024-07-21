from django.db import models

from items.models.models import Item


class Lockings(models.TextChoices):
    UNLOCK = "N", "Unlocked"
    UPGRADE = "U", "Locked for upgrade"
    CONTRACT = "C", "Locked for contract"


class InventoryItem(models.Model):
    user_id = models.PositiveIntegerField()
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE)
    locked_for = models.CharField(max_length=1,
                                  choices=Lockings.choices,
                                  default=Lockings.UNLOCK,
                                  blank=True)
    frozen = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"Inventory item: {self.item}"
