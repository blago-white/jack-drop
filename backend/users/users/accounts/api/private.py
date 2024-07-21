from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.views import TokenVerifyView

from accounts.repositories.users import PrivateUsersRepository
from common.api.default import DefaultRetrieveApiView


class UserDataPrivateApiView(DefaultRetrieveApiView):
    lookup_url_kwarg = "user_id"
    repository = PrivateUsersRepository()
    serializer_class = repository.default_serializer_class

    def retrieve(self, request: Request, **kwargs):
        user_data = self.repository.get_user_info(
            user_id=kwargs.get(self.lookup_url_kwarg)
        )

        return self.get_200_response(data=user_data)

    def get_view_description(self, html=False):
        return "Private view for retrieving user info"


class JWTUserDataPrivateApiView(DefaultRetrieveApiView):
    repository = PrivateUsersRepository()
    serializer_class = repository.default_serializer_class

    def retrieve(self, request: Request, **kwargs):
        print(request.auth, request, "DDE")

        user_data = self.repository.get_user_info_by_jwt(
            request=request
        )

        return self.get_200_response(data=user_data)

    def get_view_description(self, html=False):
        return "Private view for retrieving user info by JWT Token"


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


class UserAdvantageRetrieveAPIView(DefaultRetrieveApiView):
    pk_header_name = "Authorization"
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data={"advantage": request.user.advantage}
        )
