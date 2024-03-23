from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.html import mark_safe

from .models.cases import Case
from .models.items import CaseItem
from . import actions


@admin.register(Case)
class CaseAdmin(ModelAdmin):
    pass


@admin.register(CaseItem)
class CaseItemAdmin(ModelAdmin):
    list_display = ["__str__", "case", "chance_of_item_drop", "preview_short"]
    exclude = ["chance"]
    ordering = ["case", "-chance"]

    actions = [actions.hide_items,
               actions.make_visible_items,
               actions.prohibit_drop,
               actions.allow_drop]

    @admin.display()
    def chance_of_item_drop(self, instance: CaseItem):
        if instance.chance < 1 / 10:
            hightlight_color = "red"
        elif instance.chance < 1 / 2:
            hightlight_color = "orange"
        else:
            hightlight_color = "green"

        return mark_safe(
            f"<span style=\"color: {hightlight_color};font-weight: bold\">"
            f"{round(instance.chance * 100, 3)}%</span>"
        )
