from django.urls import path

from .endpoints import MakeGameView


urlpatterns = [
    path("make/", MakeGameView.as_view(), name="make-mines-game"),
    path("next/", MakeGameView.as_view(), name="next-mines-game")
    path("stop/", MakeGameView.as_view(), name="stop-mines-game")
]
