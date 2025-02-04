from django.contrib import admin

from .models import (DinamicSiteProfit,
                     FrozenSiteProfit,
                     FreezeFundsPercent,
                     CasesDropsProfit)


@admin.register(FrozenSiteProfit)
class FrozenProfitAdmin(admin.ModelAdmin):
    pass


@admin.register(DinamicSiteProfit)
class DinamicProfitAdmin(admin.ModelAdmin):
    fields = ["amount", "bottom_dinamic_border", "min_value", "time_update"]
    readonly_fields = ["time_update"]
    list_display = ["amount", "bottom_dinamic_border", "time_update"]


@admin.register(FreezeFundsPercent)
class FreezeFundsPercentAdmin(admin.ModelAdmin):
    pass


@admin.register(CasesDropsProfit)
class CasesDropsProfitAdmin(admin.ModelAdmin):
    pass
