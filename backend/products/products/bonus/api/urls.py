from django.urls import path

from .endpoints import BonusBuyStatusApiView, BonusBuyNextLevelApiView


urlpatterns = [
    path("info/", BonusBuyStatusApiView.as_view(), name="bonus-buy-stats"),
    path("next/", BonusBuyNextLevelApiView.as_view(), name="bonus-buy-next")
]
