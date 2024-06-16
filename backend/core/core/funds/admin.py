from django.contrib import admin

from .models import DinamicSiteProfit, FrozenSiteProfit


@admin.register(FrozenSiteProfit)
class FrozenProfitAdmin(admin.ModelAdmin):
    pass


@admin.register(DinamicSiteProfit)
class DinamicProfitAdmin(admin.ModelAdmin):
    fields = ["amount", "time_update"]
    readonly_fields = ["time_update"]
    list_display = ["amount", "time_update"]
