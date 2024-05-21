from django.db import models


class Contract(models.Model):
    granted_amount = models.FloatField()
    result_item = models.IntegerField()
    datetime = models.DateTimeField(auto_now=True)


class ContractShift(models.Model):
    shift = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    active = models.BooleanField(default=False)

    def clean(self):
        if self.active:
            if ChanceShift.objects.filter(active=True).exists():
                raise ValidationError(
                    "You can add only one active contract shift"
                )

