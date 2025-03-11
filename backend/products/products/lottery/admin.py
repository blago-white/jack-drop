import time

from django.contrib import admin
from .models.lottery import LotteryEvent, LotteryParticipant


@admin.register(LotteryEvent)
class LotteryEventAdmin(admin.ModelAdmin):
    list_display = ["is_active", "to_start", "to_implementation", "is_dummy"]

    @admin.display()
    def to_start(self, instance: LotteryEvent):
        start_after = max((instance.start_after + instance.created_at) - time.time(), 0)

        if start_after:
            return f"{start_after//3600}ч. {int(start_after%3600)}мин. {start_after%60}"
        else:
            return f"Started"

    @admin.display()
    def to_implementation(self, instance: LotteryEvent):
        started = (instance.created_at + instance.start_after) < time.time()

        if started:
            to_implementation = max((instance.created_at + instance.start_after + instance.duration) - time.time(), 0)

            if to_implementation:
                return f"{to_implementation//3600}ч. {int(to_implementation%3600)}мин. {to_implementation%60}"
            else:
                return "Implemented!"
        else:
            return f"Acceptance now"


@admin.register(LotteryParticipant)
class LotteryParticipantAdmin(admin.ModelAdmin):
    list_display = ["user_id", "lottery"]
