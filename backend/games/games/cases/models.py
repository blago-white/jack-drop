from django.db import models


class Drop(models.Model):
    user_id = models.PositiveIntegerField()
    dropped_case_item_id = models.IntegerField()
    dropped_item_id = models.IntegerField()
    site_funds_delta = models.FloatField()
