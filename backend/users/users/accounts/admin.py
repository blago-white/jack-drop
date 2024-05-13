from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Client, ClientDeposit


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ["__str__", "promocode", "is_staff"]


@admin.register(ClientDeposit)
class ClientDepositAdmin(ModelAdmin):
    list_display = ["user", "amount", "datetime"]
