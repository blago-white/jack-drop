from django.contrib import admin

from .models import DinamicSiteProfit, FrozenSiteProfit, FreezeFundsPercent


@admin.register(FrozenSiteProfit)
class FrozenProfitAdmin(admin.ModelAdmin):
    pass


@admin.register(DinamicSiteProfit)
class DinamicProfitAdmin(admin.ModelAdmin):
    fields = ["amount", "min_value", "time_update"]
    readonly_fields = ["time_update"]
    list_display = ["amount", "time_update"]


@admin.register(FreezeFundsPercent)
class FreezeFundsPercentAdmin(admin.ModelAdmin):
    pass

