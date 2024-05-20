from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, ValidationError


class CleanedSaveModel(models.Model):
    class Meta:
        abstract = True

    def save(
        self, *args, **kwargs
    ):
        self.full_clean()

        return super().save(*args, **kwargs)


class Upgrade(CleanedSaveModel):
    user_id = models.PositiveIntegerField()
    granted = models.PositiveIntegerField(null=True, blank=True)
    received = models.PositiveIntegerField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Upgrade {self.winning_amount}"

    def winning_amount(self):
        return self.received - self.granted

    class Meta:
        ordering = ["-datetime"]


class ChanceShift(CleanedSaveModel):
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
                    "You can add only one active chance shift"
                )
