from rest_framework.request import Request

from games.api.services.users import UsersApiService
from games.serializers.users import UserFundsSerializer
from .base import BaseApiRepository


class UsersApiRepository(BaseApiRepository):
    default_api_service = UsersApiService()
    default_serializer_class = UserFundsSerializer
    _api_service: UsersApiService

    def get(self, user_request: Request) -> dict:
        data: float = self._api_service.get_user_info(
            user_request=user_request
        )

        return UserFundsSerializer(instance=data).data

    def get_by_jwt(self, jwt_token: str) -> dict:
        data: float = self._api_service.get_user_info(
            jwt=jwt_token
        )

        return UserFundsSerializer(instance=data).data

    def get_balance(self, user_request: Request) -> float:
        return self.get(user_request=user_request).get("desplayed_balance")

    def get_advantage(self, user_request: Request) -> float:
        return self.get(user_request=user_request).get("advantage")

    def update_balance(self, user_request: Request, delta_amount: float):
        self._api_service.update_user_balance(
            user_request=user_request,
            delta_amount=delta_amount
        )
