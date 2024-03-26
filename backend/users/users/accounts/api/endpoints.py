from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.exceptions import InvalidToken

from common.mixins import BaseRetrieveApiViewMixin
from accounts.repositories.users import UsersRepository


class UserDataPrivateApiView(BaseRetrieveApiViewMixin, RetrieveAPIView):
    lookup_url_kwarg = "user_id"
    repository = UsersRepository()
    serializer_class = repository.default_serializer_class

    def retrieve(self, request: Request, **kwargs):
        user_data = self.repository.get_user_info(
            user_id=kwargs.get(self.lookup_url_kwarg)
        )

        return self.get_200_request(data=user_data)

    def get_view_description(self, html=False):
        return "Private view for retrieving user info"


class TokenVerifyHeaderView(TokenVerifyView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        if request.META.get("HTTP_AUTHORIZATION") and not request.data.get(
            "token"
        ):
            data = dict(request.data)

            data.update(
                token=request.META.get("HTTP_AUTHORIZATION").split()[-1]
            )

            serializer = self.get_serializer(
                data=data
            )

        else:
            serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

