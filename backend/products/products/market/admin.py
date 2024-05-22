from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models.apikey import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(ModelAdmin):
    list_display = ["__str__", "active"]
    list_editable = ["active"]
