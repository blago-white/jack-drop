from django.contrib import admin


__all__ = ["hide_items",
           "make_visible_items",
           "prohibit_drop",
           "allow_drop"]


@admin.action(description="Скрыть предметы, их не увидят")
def hide_items(self, request, queryset):
    queryset.update(view=False)


@admin.action(
    description="Сделать предметы видимыми"
)
def make_visible_items(self, request, queryset):
    queryset.update(view=True)


@admin.action(description="Запретить предметам выпадать из кейсов")
def prohibit_drop(self, request, queryset):
    queryset.update(can_drop=False)


@admin.action(
    description="Разрешить предметам выпадать из кейсов"
)
def allow_drop(self, request, queryset):
    queryset.update(can_drop=True)
