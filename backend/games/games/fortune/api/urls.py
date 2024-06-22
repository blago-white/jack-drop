from django.urls import path

from .endpoints import FortuneWheelPrizeTypeApiView, MakeFortuneWheelPrizeApiView

urlpatterns = [
    path('prize-type/',
         FortuneWheelPrizeTypeApiView.as_view(),
         name="fortune-wheel"),
    path('make-prize/',
         MakeFortuneWheelPrizeApiView.as_view(),
         name="fortune-wheel-prize")
]
