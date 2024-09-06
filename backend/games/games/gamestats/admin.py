from django.contrib import admin

from .models import Stats, StatsDelta


@admin.register(Stats)
class StatsAdmin(admin.ModelAdmin):
    list_display = [
        "online", "users", "cases", "contracts", "upgrades", "battles"
    ]


@admin.register(StatsDelta)
class StatsDeltaAdmin(admin.ModelAdmin):
    list_display = [
        "online", "users", "cases", "contracts", "upgrades", "battles"
    ]
