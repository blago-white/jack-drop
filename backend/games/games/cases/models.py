from django.db import models


class Drop(models.Model):
    user_id = models.PositiveIntegerField()
    case_id = models.IntegerField()
    dropped_item_id = models.IntegerField()
