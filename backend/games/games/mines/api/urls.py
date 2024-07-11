from django.urls import path

from .endpoints import MakeGameView

urlpatterns = [
    path("make/", MakeGameView.as_view(), name="make-mines-game")
]
