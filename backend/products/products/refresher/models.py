from django.db import models


class RefresherConfig(models.Model):
    frequency = models.IntegerField(
        verbose_name="Frequency of prices refreshing in seconds"
    )

    def __str__(self):
        return f"Refresh per {self.frequency} second"
