from django.urls import path

from .endpoints.contract import ContractGameApiView
from .endpoints.drop import DropItemGameApiView
from .endpoints.mines import MinesGameApiView
from .endpoints.upgrade import UpgradeGameApiView
from .endpoints.fortune import FortuneWheelGameApiView, FortuneWheelTimeoutApiView
from .endpoints.battle import BattleStatsApiView, BattlesHistoryApiView
from .endpoints.result import GameResultsApiView

urlpatterns = [
    path("drop/<int:case_id>/", DropItemGameApiView.as_view(), name="drop"),
    path("upgrade/", UpgradeGameApiView.as_view(), name="upgrade"),
    path("contract/", ContractGameApiView.as_view(), name="contract"),
    path("mines/", MinesGameApiView.as_view(), name="mines"),
    path("mines/next/", MinesGameApiView.as_view(), name="mines"),
    path("mines/stop/", MinesGameApiView.as_view(), name="mines"),

    path("fortune-wheel/", FortuneWheelGameApiView.as_view(), name="fortune-wheel"),
    path("fortune-wheel/timeout/",
         FortuneWheelTimeoutApiView.as_view(),
         name="fortune-wheel-timeout"),

    path("battle-stats/",
         BattleStatsApiView.as_view(),
         name="battle-stats"),
    path("battle-history/",
         BattlesHistoryApiView.as_view(),
         name="battle-history"),
    path("history/<str:section>/",
         GameResultsApiView.as_view(),
         name="history"),
]
