from django.db import models

from django.core.exceptions import ValidationError


class PaymentStatus(models.TextChoices):
    INITED = ("CREATED", "Created")
    PENDING = ("PENDING", "Pending")
    PROGRESS = ("IN_PROGRESS", "Progress")
    PAID = ("PAID", "Payd")
    CONFIRMED = ("CONFIRMED", "Confirmed")

    FAILED = ("FAILED", "Failed")
    CANCELED = ("CANCELED", "Canceled")
    EXPIRED = ("EXPIRED", "Expired")


class Config(models.Model):
    apikey = models.CharField(max_length=512)
    api_user_id = models.CharField(max_length=512)
    bank_address = models.CharField(max_length=512)

    def save(self, *args, **kwargs):
        if (not self.pk) and Config.objects.all().exists():
            raise ValidationError("Can add only one config")

        return super().save(*args, **kwargs)


class Payment(models.Model):
    foreign_id = models.UUIDField(null=True, blank=True, unique=True)
    user_id = models.IntegerField()
    status = models.CharField(choices=PaymentStatus.choices,
                              blank=True,
                              null=True)
    payment_method = models.UUIDField(blank=True, null=True)
    amount_local = models.FloatField()
    currency = models.CharField(blank=True, null=True)
    expired_at = models.DateTimeField(blank=True, null=True)
