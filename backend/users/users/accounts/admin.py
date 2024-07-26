from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Client
from .models.api import SteamApiKey


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ["__str__", "promocode", "is_staff"]


@admin.register(SteamApiKey)
class ClientAdmin(ModelAdmin):
    list_display = ["apikey"]
