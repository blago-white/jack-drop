from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models.models import Item


@admin.register(Item)
class ItemAdmin(ModelAdmin):
    list_display = ["__str__", "is_edit_manualy"]

    @admin.display(boolean=True)
    def is_edit_manualy(self, instance: Item):
        return instance.manage_manually
