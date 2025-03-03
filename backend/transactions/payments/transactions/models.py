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


class PaymentSystem(models.TextChoices):
    NICEPAY = ("N", "Nicepay")
    SKINIFY = ("S", "Skinify")


class Config(models.Model):
    merchant_id = models.CharField(max_length=512)
    secret_key = models.CharField(max_length=512)
    skinify_key = models.CharField(max_length=255, default="")
    bank_address = models.CharField(max_length=512)

    def __str__(self):
        return (f"merchant_id={self.merchant_id} | "
                f"secret_key={self.secret_key}")

    def save(self, *args, **kwargs):
        if (not self.pk) and Config.objects.all().exists():
            raise ValidationError("Can add only one config")

        return super().save(*args, **kwargs)


class Payment(models.Model):
    payment_id = models.UUIDField(null=True, blank=True, unique=True)
    user_id = models.IntegerField()
    provider = models.CharField(choices=PaymentSystem.choices)

    amount_local = models.IntegerField(blank=True, null=True)
    currency = models.CharField(blank=True,
                                choices=PaymentCurrency.choices,
                                null=True,
                                default=PaymentCurrency.RUB)
    status = models.CharField(choices=PaymentStatus.choices,
                              blank=True,
                              null=True)
    promocode = models.CharField(max_length=16,
                                 null=True,
                                 blank=True)
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    expired_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, auto_now=True)

    def __str__(self):
        return f"Payment of {self.user_id} for {self.amount_local} {self.currency}"
