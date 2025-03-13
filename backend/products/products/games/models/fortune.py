from django.db import models


class FortuneWheelBan(models.Model):
    user_id = models.IntegerField()
