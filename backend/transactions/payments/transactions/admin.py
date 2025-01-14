from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Config, Payment


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ["__str__", "created_at"]


admin.site.register(Config)
