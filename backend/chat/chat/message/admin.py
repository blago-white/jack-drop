from django.contrib import admin

from .models import Chat, ChatMessage


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["username"]
    search_fields = ["username"]
    list_filter = ["username"]

    readonly_fields = ["username", "user_id"]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["view_this", "username", "text", "from_admin"]
    search_fields = ["username"]
    list_filter = ["username", "from_admin"]

    readonly_fields = ["username", "from_admin"]
