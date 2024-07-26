from django.db import models
from django.core.exceptions import ValidationError


class SteamApiKey(models.Model):
    apikey = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.apikey}"

    def save(self, *args, **kwargs):
        if not self.pk and SteamApiKey.objects.all().exists():
            raise ValidationError("Can add only one steam apikey")

        return super().save(*args, **kwargs)
