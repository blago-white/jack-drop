from django.contrib import admin

from .models import ClientBalance


@admin.register(ClientBalance)
class ClientBalanceAdmin(admin.ModelAdmin):
    list_display = ["client", "real_balance", "displayed_balance"]
