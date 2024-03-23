from django.contrib.admin import ModelAdmin
from django.contrib import admin

from .models.models import Item


@admin.register(Item)
class ItemAdmin(ModelAdmin):
    list_display = ["__str__", "preview_short", "price_of_item"]
    fields = ["title",
              "image_path",
              "price",
              "market_link",
              "preview"]

    readonly_fields = ['preview',
                       "preview_short",
                       "title",
                       "image_path",
                       "price"]

    search_fields = ["title"]

    ordering = ["-price"]

    @admin.display()
    def price_of_item(self, instance: Item):
        return f"{instance.price // 100} RUB"
