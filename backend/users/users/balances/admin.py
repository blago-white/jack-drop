from django.contrib import admin

from .models import ClientBalance, ClientDeposit


@admin.register(ClientBalance)
class ClientBalanceAdmin(admin.ModelAdmin):
    list_display = ["client", "real_balance", "displayed_balance"]


@admin.register(ClientDeposit)
class ClientDepositAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "datetime"]
