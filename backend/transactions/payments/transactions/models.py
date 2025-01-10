from django.core.exceptions import ValidationError
from django.db import models


class PaymentStatus(models.TextChoices):
    SUCCESS = ("S", "SUCCESS")
    FAILED = ("F", "FAILED")


class PaymentCurrency(models.TextChoices):
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"
    UAH = "UAH"
    KZT = "KZT"


class Config(models.Model):
    merchant_id = models.CharField(max_length=512)
    secret_key = models.CharField(max_length=512)
    bank_address = models.CharField(max_length=512)

    def save(self, *args, **kwargs):
        if (not self.pk) and Config.objects.all().exists():
            raise ValidationError("Can add only one config")

        return super().save(*args, **kwargs)


class Payment(models.Model):
    payment_id = models.UUIDField(null=True, blank=True, unique=True)
    user_id = models.IntegerField()
    amount_local = models.IntegerField()
    currency = models.CharField(blank=True,
                                choices=PaymentCurrency.choices,
                                null=True,
                                default=PaymentCurrency.RUB)
    status = models.CharField(choices=PaymentStatus.choices,
                              blank=True,
                              null=True)
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    expired_at = models.DateTimeField(blank=True, null=True)
