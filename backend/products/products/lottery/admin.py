from django.contrib import admin
from .models.lottery import LotteryEvent, LotteryParticipant


@admin.register(LotteryEvent)
class LotteryEventAdmin(admin.ModelAdmin):
    list_display = ["is_active", "prize_main", "prize_secondary", "is_dummy"]


@admin.register(LotteryParticipant)
class LotteryParticipantAdmin(admin.ModelAdmin):
    list_display = ["user_id", "lottery"]
