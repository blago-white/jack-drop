from django.contrib import admin

from .models.results import GameResult
from .models.fortune import FortuneWheelBan


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ["get_game_display", "is_win", "date"]


@admin.register(FortuneWheelBan)
class FortuneWheelBanService(admin.ModelAdmin):
    list_display = ["user_id"]
