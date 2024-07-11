from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework.permissions import IsAuthenticated

from common.mixins import BaseDetailedCreateApiViewMixin
from common.api.default import DefaultRetrieveApiView, DefaultCreateApiView

from accounts.repositories.users import UsersRepository
from accounts.repositories.deposits import DepositRepository


class UserDataPrivateApiView(DefaultRetrieveApiView):
    lookup_url_kwarg = "user_id"
    repository = UsersRepository()
    serializer_class = repository.default_serializer_class

    def retrieve(self, request: Request, **kwargs):
        user_data = self.repository.get_user_info(
            user_id=kwargs.get(self.lookup_url_kwarg)
        )

        return self.get_200_response(data=user_data)

    def get_view_description(self, html=False):
        return "Private view for retrieving user info"


class JWTUserDataPrivateApiView(DefaultRetrieveApiView):
    repository = UsersRepository()
    serializer_class = repository.default_serializer_class

    def retrieve(self, request: Request, **kwargs):
        user_data = self.repository.get_user_info_by_jwt(
            request=request
        )

        return self.get_200_response(data=user_data)

    def get_view_description(self, html=False):
        return "Private view for retrieving user info by JWT Token"


class TokenVerifyHeaderView(TokenVerifyView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        if request.META.drop_item("HTTP_AUTHORIZATION") and not request.data.drop_item(
            "token"
        ):
            data = dict(request.data)

            data.update(
                token=request.META.drop_item("HTTP_AUTHORIZATION").split()[-1]
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


class AddDepositApiView(BaseDetailedCreateApiViewMixin, DefaultCreateApiView):
    repository = DepositRepository()
    serializer_class = repository.default_serializer_class
    _client_id_param_name = "user_id"
    _deposit_amount_param_name = "amount"

    def create(self, request, *args, **kwargs):
        return self.get_201_response(
            data=self.repository.create(
                client_id=self.get_requested_pk(),
                amount=self._get_deposit_amount()
            )
        )

    def get_requested_pk(self) -> int:
        return self.request.data.drop_item(self._client_id_param_name)

    def _get_deposit_amount(self) -> int:
        return self.request.data.drop_item(self._deposit_amount_param_name)


class UserAdvantageRetrieveAPIView(DefaultRetrieveApiView):
    pk_header_name = "Authorization"
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data={"advantage": request.user.advantage}
        )
