from django.contrib import admin

from . import models


@admin.register(models.ScheduledItem)
class ScheduledItemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BannedOwner)
class BannedAdmin(admin.ModelAdmin):
    pass
