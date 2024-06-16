from rest_framework.exceptions import ValidationError

from .base import BaseApiRepository

from games.api.services.mines import MinesGameApiService
from games.serializers.mines import MinesGameRequestViewSerializer


class MinesGameApiRepository(BaseApiRepository):
    default_api_service = MinesGameApiService()
    default_serializer_class = MinesGameRequestViewSerializer

    def __init__(self, *args,
                 serializer_class: MinesGameRequestViewSerializer = None,
                 **kwargs):
        self._serializer_class = serializer_class or self.default_serializer_class

        super().__init__(*args, **kwargs)

    def make(self, request_data: dict, user_data: dict):
        serialized = self._get_serialized(
            request_data=request_data,
            user_data=user_data
        )

        serialized.is_valid(raise_exception=True)

        self._validate_funds(
            user_balance=user_data.get("displayed_balance"),
            deposit=serialized.data.get("user_deposit")
        )

        result = self._api_service.make(
            serialized=serialized
        )

        return result

    @staticmethod
    def _validate_funds(user_balance: float, deposit: int):
        if float(user_balance) < float(deposit):
            raise ValidationError(
                "There are not enough balance funds for action"
            )

    def _get_serialized(self, request_data: dict,
                        user_data: dict):
        return self._api_service.default_endpoint_serializer_class(
            data={
                "count_mines": request_data.get("count_mines"),
                "user_funds": {
                    "user_advantage": user_data.get("user_advantage"),
                    "id": user_data.get("id")
                },
                "user_deposit": request_data.get("user_deposit"),
                "site_funds": {
                    "site_active_funds_per_hour": 1000, # TODO: Call service
                }
            }
        )
