from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models.cases import Case
from .models.items import CaseItem


@admin.register(Case)
class CaseAdmin(ModelAdmin):
    pass


@admin.register(CaseItem)
class CaseItemAdmin(ModelAdmin):
    pass
