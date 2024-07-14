from django.urls import path, include

from .private import (UserDataPrivateApiView, AddDepositApiView,
                      UserAdvantageRetrieveAPIView, JWTUserDataPrivateApiView)
from .public import UserDataApiView

private_urlpatterns = [
    path("get_user_info/<int:user_id>/", UserDataPrivateApiView.as_view()),
    path("get_user_info_jwt/", JWTUserDataPrivateApiView.as_view()),
    path("add_deposit/", AddDepositApiView.as_view()),
    path("advantage/", UserAdvantageRetrieveAPIView.as_view()),
]

public_urlpatterns = [
    path("user/", UserDataApiView.as_view()),
]

urlpatterns = [
    path("api/v1/p/", include((private_urlpatterns, "private-accounts"))),
    path("api/v1/public/", include((public_urlpatterns, "private-accounts"))),
]
