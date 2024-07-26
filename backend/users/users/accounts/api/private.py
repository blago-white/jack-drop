from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.views import TokenVerifyView

from accounts.repositories.users import PrivateUsersRepository
from accounts.repositories.advantage import AdvantageRepository
from common.api.default import DefaultRetrieveApiView, DefaultUpdateApiView
from common.mixins import DetailedApiViewMixin


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
        print("TOKEN", self.get_serializer_class())

        print(request.data, request.headers)

        if request.headers.get("Authorization") and not request.data.get(
            "token"
        ):
            print("EEDDD")
            serializer = self.get_serializer_class()(
                data={"token": request.headers.get("Authorization").split()[-1]}
            )

        else:
            serializer = self.get_serializer_class()(data=request.data)

        try:
            print("EEERO1")
            serializer.is_valid(raise_exception=False)
            print("EEERO2", serializer.errors, serializer.data)
        except TokenError as e:
            print("ERROR TOKEN ")
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserAdvantageRetrieveAPIView(DefaultRetrieveApiView):
    pk_header_name = "Authorization"
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data={"advantage": request.user.advantage}
        )


class UserAdvantageUpdateAPIView(DefaultUpdateApiView):
    pk_url_kwarg = "user_id"
    repository = AdvantageRepository()

    def update(self, request, *args, **kwargs):
        updated = self.repository.update(
            user_id=self.get_requested_pk() or request.user.id,
            delta_amount=request.data.get("delta_advantage")
        )

        return self.get_201_response(
            data=updated
        )
