from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models.models import CasesCategory


@admin.register(CasesCategory)
class CasesCategoryAdmin(ModelAdmin):
    list_display = ["__str__", "slug", "count_cases"]

    @admin.display
    def count_cases(self, instance: CasesCategory):
        return instance.case_set.all().count()
