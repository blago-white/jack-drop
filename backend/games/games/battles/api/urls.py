from django.urls import path

from .game import MakeBattleApiView
from .request import StartBattleRequestApiView, DropBattleRequestApiView
from .stats import BattlesStatsApiView, BattlesHistoryApiView

urlpatterns = [
    path("make-request/",
         StartBattleRequestApiView.as_view(),
         name="start-request"),
    path("drop-request/<int:initiator_id>/",
         DropBattleRequestApiView.as_view(),
         name="drop-request"),
    path("make-battle/",
         MakeBattleApiView.as_view(),
         name="commit-battle"),
    path("stats/<int:user_id>/",
         BattlesStatsApiView.as_view(),
         name="battle-stats"),
    path("all/<int:user_id>/",
         BattlesHistoryApiView.as_view(),
         name="battle-history")
]
