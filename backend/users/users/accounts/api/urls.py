from django.urls import path, include

from .private import (UserDataPrivateApiView,
                      UserAdvantageRetrieveAPIView,
                      JWTUserDataPrivateApiView,
                      UserAdvantageUpdateAPIView,
                      UsersDataPrivateListApiView,
                      AddLotteryResultsAPIView)
from .public import UserDataApiView, UserTradeLinkApiView

private_urlpatterns = [
    path("get_user_info/<int:user_id>/", UserDataPrivateApiView.as_view()),
    path("get_user_info_jwt/", JWTUserDataPrivateApiView.as_view()),
    path("advantage/", UserAdvantageRetrieveAPIView.as_view()),
    path("advantage/update/", UserAdvantageUpdateAPIView.as_view()),
    path("advantage/update/<int:user_id>/", UserAdvantageUpdateAPIView.as_view()),
    path("get_users_info/", UsersDataPrivateListApiView.as_view()),
    path("add_lottery_result/", AddLotteryResultsAPIView.as_view())
]

public_urlpatterns = [
    path("user/", UserDataApiView.as_view()),
    path("add-trade/", UserTradeLinkApiView.as_view())
]

urlpatterns = [
    path("api/v1/p/", include((private_urlpatterns, "private-accounts"))),
    path("api/v1/public/", include((public_urlpatterns, "public-accounts"))),
]
