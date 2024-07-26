from rest_framework import serializers

from .models import ChatMessage
from .config import SENDER_USERNAME_MAX_LEN, MESSAGE_MAX_LEN


class MessageSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        max_length=MESSAGE_MAX_LEN
    )

    class Meta:
        model = ChatMessage
        fields = "__all__"
