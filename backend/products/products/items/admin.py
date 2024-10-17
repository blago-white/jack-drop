import django.db.models
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.html import mark_safe

from .models.models import Item, ItemsSet


@admin.register(Item)
class ItemAdmin(ModelAdmin):
    list_display = ["__str__", "preview_short", "price_of_item"]

    fields = ["title",
              "image_path",
              "price",
              "market_link",
              "preview",
              "market_hash_name"]

    readonly_fields = ['preview',
                       "preview_short",
                       "title",
                       "image_path",
                       "price",
                       "market_hash_name"]

    search_fields = ["title"]

    ordering = ["-price"]

    @admin.display()
    def price_of_item(self, instance: Item):
        return mark_safe(
            f"<b>{instance.price} RUB</b>"
        )


@admin.register(ItemsSet)
class ItemAdmin(ModelAdmin):
    list_display = ["title", "price"]

    fields = ["title",
              "image_path",
              "items",
              "description",
              "price"]

    search_fields = ["title"]
