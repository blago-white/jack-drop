from rest_framework.exceptions import ValidationError

from games.api.services.mines import MinesGameApiService
from games.api.services.site import SiteFundsApiService
from games.api.services.users import UsersApiService
from games.models import Games
from games.serializers.mines import MinesGameRequestViewSerializer
from games.services.result import GameResultService
from games.services.transfer import GameResultData
from .base import BaseApiRepository


class MinesGameApiRepository(BaseApiRepository):
    default_api_service = MinesGameApiService()
    default_serializer_class = MinesGameRequestViewSerializer
    default_site_funds_service = SiteFundsApiService()
    default_users_service = UsersApiService()
    default_game_result_service = GameResultService()

    _site_funds_service: SiteFundsApiService

    def __init__(self, *args,
                 site_funds_service: SiteFundsApiService = None,
                 users_service: SiteFundsApiService = None,
                 serializer_class: MinesGameRequestViewSerializer = None,
                 game_result_service: GameResultService = None,
                 **kwargs):
        self._serializer_class = serializer_class or self.default_serializer_class
        self._site_funds_service = site_funds_service or self.default_site_funds_service
        self._users_service = users_service or self.default_users_service
        self._game_result_service = game_result_service or self.default_game_result_service

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

        self._commit_result(
            funds_difference=result.get("funds_difference"),
            user_id=user_data.get("id")
        )

        return result

    def _commit_result(self, user_id: int, funds_difference: dict) -> None:
        self._site_funds_service.update(
            amount=funds_difference.get("site_funds_diff")
        )

        self._game_result_service.save(data=GameResultData(
            user_id=user_id,
            game=Games.MINES,
            is_win=float(funds_difference.get("user_funds_diff")) > 0
        ))

        self._users_service.update_user_balance_by_id(
            delta_amount=funds_difference.get("user_funds_diff"),
            user_id=user_id
        )

    @staticmethod
    def _validate_funds(user_balance: float, deposit: int):
        if float(user_balance) < float(deposit):
            raise ValidationError(
                detail="There are not enough balance funds for action",
                code=400
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
                    "site_active_funds": self._site_funds_service.get()
                }
            }
        )
