from django.core.exceptions import ValidationError
from django.db import models

from common.models.base import BaseModel


class ApiKey(BaseModel):
    key = models.CharField(verbose_name="Api Key of market", max_length=1000)
    active = models.BooleanField(verbose_name="Can site use this key?",
                                 default=True)

    def __str__(self):
        return self.key

    def clean(self):
        if ApiKey.objects.all().filter(active=True).count() > 1:
            raise ValidationError("There should be only 1 active api key")
