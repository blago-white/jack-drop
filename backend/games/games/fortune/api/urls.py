from django.urls import path

from .endpoints import (FortuneWheelPrizeTypeApiView,
                        MakeFortuneWheelPrizeApiView,
                        GameTimeoutApiView,
                        UsePromocodeCreateApiView)

urlpatterns = [
    path('prize-type/',
         FortuneWheelPrizeTypeApiView.as_view(),
         name="fortune-wheel"),
    path('make-prize/',
         MakeFortuneWheelPrizeApiView.as_view(),
         name="fortune-wheel-prize"),
    path('get-timeout/<int:user_id>/',
         GameTimeoutApiView.as_view(),
         name="fortune-wheel-prize"),
    path('use-promo/',
         UsePromocodeCreateApiView.as_view(),
         name="use-promo"),
]
