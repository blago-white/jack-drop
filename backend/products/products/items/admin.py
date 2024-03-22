from django.contrib.admin import ModelAdmin
from django.contrib import admin

from .models.models import Item


@admin.register(Item)
class ItemAdmin(ModelAdmin):
    list_display = ["__str__", "is_edit_manualy", "preview_short"]
    fields = ["title",
              "image_path",
              "price",
              "market_link",
              "manage_manually",
              "preview"]

    readonly_fields = ['preview', "preview_short"]

    @admin.display(boolean=True)
    def is_edit_manualy(self, instance: Item):
        return instance.manage_manually
