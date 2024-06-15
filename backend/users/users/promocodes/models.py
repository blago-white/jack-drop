from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .config import MAX_PROMOCODE_LENGTH


class Promocode(models.Model):
    code = models.CharField(max_length=MAX_PROMOCODE_LENGTH,
                            verbose_name="Promo code")
    discount = models.IntegerField(verbose_name="Discount percent",
                                   validators=[
                                       MinValueValidator(0),
                                       MaxValueValidator(100)
                                   ])

    class Meta:
        ordering = ["-discount"]

    def __str__(self):
        return f"Promocode: {self.code[:10]} ({self.discount}%)"
