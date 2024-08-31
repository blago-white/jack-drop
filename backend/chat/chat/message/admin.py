from django.contrib import admin

from .models import Chat, ChatMessage


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["username", "has_new_messages"]
    search_fields = ["username"]
    list_filter = ["username"]

    readonly_fields = ["username", "user_id"]

    @admin.display(boolean=True)
    def has_new_messages(self, instance: Chat):
        return instance.messages.filter(view_this=False).exists()


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["view_this", "username", "text", "from_admin"]
    search_fields = ["username"]
    list_filter = ["username", "from_admin"]

    readonly_fields = ["from_admin"]
