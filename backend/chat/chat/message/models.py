from django.db import models
from .config import MESSAGE_MAX_LEN, SENDER_USERNAME_MAX_LEN


class ChatMessage(models.Model):
    text = models.CharField("Text of message",
                            max_length=MESSAGE_MAX_LEN,
                            null=True)
    username = models.CharField(default="test")
    date = models.DateTimeField(auto_now=True, blank=True)

    view_this = models.BooleanField(default=False, blank=True)
    from_admin = models.BooleanField(default=True)

    class Meta:
        ordering = ["view_this", "date"]

    def __str__(self):
        return f"{'✅' if self.view_this else '🚩'} {'admin' if self.from_admin else self.username} | {self.text}"

    def save(self, *args, **kwargs):
        if self.from_admin:
            self.view_this = True

        return super().save(*args, **kwargs)


class Chat(models.Model):
    user_id = models.IntegerField(
        unique=True
    )
    username = models.CharField(
        "Username of sender",
        max_length=SENDER_USERNAME_MAX_LEN,
        unique=True
    )
    messages = models.ManyToManyField(to=ChatMessage,
                                      related_name="chat",
                                      blank=True)

    def __str__(self):
        return f"Chat with {self.username}"
