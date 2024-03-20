from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models.models import CasesCategory


@admin.register(CasesCategory)
class CasesCategoryAdmin(ModelAdmin):
    pass
