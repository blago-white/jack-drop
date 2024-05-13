from rest_framework import serializers

from .models import Promocode


class DiscountSerializer(serializers.ModelSerializer):
    discount = serializers.IntegerField(default=0, initial=0)

    class Meta:
        fields = ["discount"]
        model = Promocode
