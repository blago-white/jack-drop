from django.contrib import admin


from . import models


@admin.register(models.ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.WithdrawedItem)
class WithdrawedItemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Withdraw)
class WithdrawAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BotBalanceReplenish)
class BotBalanceReplenishAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):
    pass
