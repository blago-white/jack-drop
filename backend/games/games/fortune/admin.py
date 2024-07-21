from django.contrib import admin

from .models import (FortuneWheelWinning, FortuneWheelOpening,
                     FortuneWheelTimeout, FortuneWheelPromocode)

admin.site.register(FortuneWheelWinning)
admin.site.register(FortuneWheelOpening)
admin.site.register(FortuneWheelPromocode)


@admin.register(FortuneWheelTimeout)
class FortuneWheelTimeoutAdmin(admin.ModelAdmin):
    fields = []
