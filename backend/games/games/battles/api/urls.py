from django.urls import path

from .request import StartBattleRequestApiView, DropBattleRequestApiView
from .game import MakeBattleApiView


urlpatterns = [
    path("make-request/",
         StartBattleRequestApiView.as_view(),
         name="start-request"),
    path("drop-request/<int:initiator_id>/",
         DropBattleRequestApiView.as_view(),
         name="drop-request"),
    path("make-battle/",
         MakeBattleApiView.as_view(),
         name="commit-battle")
]
