from rest_framework import serializers

from .models import Promocode


class DiscountSerializer(serializers.ModelSerializer):
    discount = serializers.IntegerField(default=0, initial=0)

    class Meta:
        fields = ["discount"]
        model = Promocode


class PromocodeSerializer(serializers.ModelSerializer):
    discount = serializers.IntegerField(default=0, initial=0)

    class Meta:
        fields = ["code", "discount"]
        model = Promocode


class PersonalOfferSerializer(serializers.Serializer):
    available = serializers.BooleanField(default=False)

    promocode = PromocodeSerializer(required=False, allow_null=True)

    class Meta:
        fields = ["available", "promocode"]
