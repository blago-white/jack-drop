from django.urls import path, include

from .endpoints import UserDataPrivateApiView, AddDepositApiView

private_urlpatterns = [
    path("get_user_info/<int:user_id>/", UserDataPrivateApiView.as_view()),
    path("add_deposit/", AddDepositApiView.as_view())
]

urlpatterns = [
    path("api/v1/p/", include((private_urlpatterns, "private-users")))
]
