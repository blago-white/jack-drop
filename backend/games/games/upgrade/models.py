from django.db import models


class Upgrade(models.Model):
    user_id = models.PositiveIntegerField()
    granted_item = models.PositiveIntegerField(null=True, blank=True)
    received_item = models.PositiveIntegerField(null=True, blank=True)
    winning_amount = models.FloatField()
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Upgrade {self.winning_amount}"

    class Meta:
        ordering = ["-datetime"]
