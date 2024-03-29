from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Client


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ["__str__", "is_staff"]
