from django.db import models


class FortuneWheelBan(models.Model):
    user_id = models.IntegerField(unique=True)

    def __str__(self):
        return f"Banned: {self.user_id}"
