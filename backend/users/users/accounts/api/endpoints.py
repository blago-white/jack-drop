from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request

from common.mixins import BaseRetrieveApiViewMixin
from accounts.repositories.users import UsersRepository


class UserDataPrivateApiView(BaseRetrieveApiViewMixin, RetrieveAPIView):
    lookup_url_kwarg = "user_id"
    repository = UsersRepository()
    serializer_class = repository.default_serializer_class

    def retrieve(self, request: Request, **kwargs):
        user_data = self.repository.get_user_info(
            user_id=kwargs.get("user_id")
        )

        return self.get_200_request(data=user_data)

    def get_view_description(self, html=False):
        return "Private view for retrieving user info"
