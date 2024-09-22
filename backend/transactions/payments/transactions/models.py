from django.db import models

from django.core.exceptions import ValidationError


class PaymentStatus(models.TextChoices):
    INITED = ("I", "Created")
    PENDING = ("D", "Pending")
    PROGRESS = ("P", "Progress")
    PAID = ("Y", "Payd")
    CONFIRMED = ("C", "Confirmed")

    FAILED = ("F", "Failed")
    CANCELED = ("L", "Canceled")
    EXPIRED = ("E", "Expired")


class Config(models.Model):
    apikey = models.CharField(max_length=512)
    api_user_id = models.CharField(max_length=512)
    bank_address = models.CharField(max_length=512)

    def save(self, *args, **kwargs):
        if (not self.pk) and Config.objects.all().exists():
            raise ValidationError("Can add only one config")

        return super().save(*args, **kwargs)


class Payment(models.Model):
    user_id = models.IntegerField()
    user_ip = models.GenericIPAddressField()
    status = models.CharField(choices=PaymentStatus.choices,
                              default=PaymentStatus.PROGRESS,
                              blank=True)
    payment_method = models.UUIDField()
    amount_local = models.FloatField()
    currency = models.CharField()
    expired_at = models.DateTimeField()


