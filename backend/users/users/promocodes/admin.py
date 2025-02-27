from django.contrib import admin

from .models import Promocode


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ["code", "discount", "for_personal_offers"]
