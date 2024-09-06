from rest_framework.serializers import ModelSerializer, IntegerField

from .models import Stats


class StatsSerializer(ModelSerializer):
    online = IntegerField()
    users = IntegerField()
    cases = IntegerField()
    contracts = IntegerField()
    upgrades = IntegerField()
    battles = IntegerField()

    class Meta:
        model = Stats
        exclude = ["id"]
