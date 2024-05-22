from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.filters import RelatedFieldListFilter
from django.utils.html import mark_safe

from . import actions
from .models.cases import Case
from .models.items import CaseItem


class CaseFilter(RelatedFieldListFilter):
    title = "Filter For Name Of Case"

    def queryset(self, request, queryset):
        return Case.objects.all()


@admin.register(Case)
class CaseAdmin(ModelAdmin):
    list_display = ["__str__", "preview_short", "count_items"]
    fields = ["title", "category", "image_path", "preview"]
    readonly_fields = ["preview"]

    @admin.display
    def count_items(self, instance: Case):
        return instance.items.all().count()


@admin.register(CaseItem)
class CaseItemAdmin(ModelAdmin):
    list_display = ["__str__",
                    "case",
                    "preview_case",
                    "can_drop",
                    "view",
                    "chance_of_item_drop",
                    "preview_short"]
    list_editable = ("can_drop", "view")
    list_filter = ["case", "can_drop", "view"]

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
