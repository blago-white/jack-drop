from django.urls import path

from .endpoints import UserDataPrivateApiView


urlpatterns = [
    path("api/v1/private/get_usr_info/<int:user_id>/",
         UserDataPrivateApiView.as_view()),
]
