from django.db import models


class ScheduledItem(models.Model):
    inventory_item_id = models.IntegerField()
    item_market_hash_name = models.CharField()
    price = models.IntegerField()
    trade_link = models.CharField()
