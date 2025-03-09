from django.urls import path

from .endpoints import (GetCurrentLotteryApiView,
                        ParticipateLotteryApiView)


urlpatterns = [
    path("current/",
         GetCurrentLotteryApiView.as_view(),
         name="view-current-lottery"),
    path("participate/",
         ParticipateLotteryApiView.as_view(),
         name="participate-lottery")
]
