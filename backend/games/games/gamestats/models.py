from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


AVAILABLE_STATS = [
    "online",
    "users",
    "cases",
    "contracts",
    "upgrades",
    "battles"
]


class _StatsField(models.FloatField):
    default_validators = [
        MinValueValidator(0)
    ]


_stats_field = _StatsField(default=0, blank=True)


class SingletonModel:
    _model: models.Model

    def save(
        self, *args, **kwargs
    ):
        if not self.pk:
            if self._model.objects.all().exists():
                raise ValidationError("Can add only one instance")

        return super().save(*args, **kwargs)


class Stats(SingletonModel, models.Model):
    online = _StatsField(default=0, blank=True)
    users = _StatsField(default=0, blank=True)
    cases = _StatsField(default=0, blank=True)
    contracts = _StatsField(default=0, blank=True)
    upgrades = _StatsField(default=0, blank=True)
    battles = _StatsField(default=0, blank=True)

    def __init__(self, *args, **kwargs):
        self._model = Stats

        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"Stats [online: {self.online}]"


class StatsDelta(SingletonModel, models.Model):
    online = models.IntegerField()
    users = models.IntegerField()
    cases = models.IntegerField()
    contracts = models.IntegerField()
    upgrades = models.IntegerField()
    battles = models.IntegerField()

    def __init__(self, *args, **kwargs):
        self._model = StatsDelta

        super().__init__(*args, **kwargs)

    class Meta:
        verbose_name = "Stats Increasing / Hour"
