from django.urls import path

from .endpoints import UserDataPrivateApiView


urlpatterns = [
    path("private/accounts/api/v1/get_user_info/<int:user_id>/",
         UserDataPrivateApiView.as_view()),
]
