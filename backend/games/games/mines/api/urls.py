from django.urls import path

from .endpoints import MakeGameView, NextStepMinesGameView, StopMinesGameView

urlpatterns = [
    path("make/", MakeGameView.as_view(), name="make-mines-game"),
    path("next/", NextStepMinesGameView.as_view(), name="next-mines-game"),
    path("stop/", StopMinesGameView.as_view(), name="stop-mines-game")
]
