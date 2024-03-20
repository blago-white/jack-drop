from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models.models import Item


@admin.register(Item)
class ItemAdmin(ModelAdmin):
    pass
