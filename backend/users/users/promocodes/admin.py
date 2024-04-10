from django.contrib import admin

from .models import Promocode


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    pass
