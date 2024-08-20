from rest_framework import serializers


class TransactionCreationPubllicSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=500)
    pay_method = serializers.ChoiceField(choices=[
        ("C", "crypto"),
        ("R", "Rubles")
    ])


class TransactionCreationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField(max_length=300)
    user_ip = serializers.IPAddressField()
    pay_method = serializers.ChoiceField(choices=[
        ("C", "crypto"),
        ("R", "Rubles")
    ])
    amount = serializers.FloatField(min_value=500)
