from django.db import models


class ScheduledItem(models.Model):
    inventory_item_id = models.IntegerField()
    item_market_hash_name = models.CharField()
    item_market_link = models.URLField()
    price = models.IntegerField()
    trade_link = models.CharField()
