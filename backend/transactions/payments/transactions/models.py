from django.db import models

from django.core.exceptions import ValidationError


class PaymentStatus(models.TextChoices):
    SUCCESS = ("S", "Success")
    FAIL = ("F", "Fail")
    PROGRESS = ("P", "Progress")


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
    payin_amount = models.FloatField()
    payin_currency = models.CharField()
    start_at = models.DateTimeField(auto_now=True,
                                    editable=False)
    ended_at = models.DateTimeField(null=True, blank=True)
