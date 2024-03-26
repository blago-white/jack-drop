from django.urls import path

from .endpoints import UserDataPrivateApiView


urlpatterns = [
    path("api/v1/p/get_user_info/<int:user_id>/",
         UserDataPrivateApiView.as_view()),
]
