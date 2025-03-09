from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models.client import Client, ClientAdvantage, LotteryWin
from .models.api import SteamApiKey


@admin.register(LotteryWin)
class LotteryWin(ModelAdmin):
    list_display = ["__str__", "viewed"]
    list_filter = ["winner", "viewed"]


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ["__str__", "is_staff"]


@admin.register(SteamApiKey)
class SteamApiKeyAdmin(ModelAdmin):
    list_display = ["apikey"]


@admin.register(ClientAdvantage)
class ClientAdvantageAdmin(ModelAdmin):
    list_display = ["value", "client"]
    list_filter = ["client"]
