from django.db import models
from .config import MESSAGE_MAX_LEN, SENDER_USERNAME_MAX_LEN


class Message(models.Model):
    username = models.CharField(
        "Username of sender references Client model in users service",
        max_length=SENDER_USERNAME_MAX_LEN
    )
    text = models.CharField("Text of message",
                            max_length=MESSAGE_MAX_LEN)
    date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f"{self.username}: {self.text[:20]}"
