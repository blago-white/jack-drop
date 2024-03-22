from django.contrib.admin import ModelAdmin
from django.contrib import admin

from .models.apikey import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(ModelAdmin):
    list_display = ["__str__", "active"]
