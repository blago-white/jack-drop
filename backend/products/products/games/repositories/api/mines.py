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
    _api_service: MinesGameApiService

    def __init__(
            self, *args,
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

    def init(self, request_data: dict, user_data: dict):
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

        if result:
            self._users_service.update_user_balance_by_id(
                user_id=user_data.get("id"),
                delta_amount=-result.get("deposit")
            )

        return result

    def next(self, user_id: int) -> dict:
        site_active_funds = self._site_funds_service.get()

        result = self._api_service.next(user_id=user_id,
                                        site_funds=site_active_funds)

        if result.get("game_ended"):
            self._commit_result(
                user_id=user_id,
                funds_difference=result.get("funds_difference"),
                deposit=result.get("mines_game").get("deposit"),
                is_win=result.get("mines_game").get("is_win")
            )

            return self._deserialize_result(result_json=result)

        return {"win_amount": result.get("new_amount"),
                "next_win_factor": result.get("next_win_factor"),
                "game_ended": False}

    def stop(self, user_id: int) -> dict:
        result = self._api_service.stop(user_id=user_id)

        self._commit_result(
            user_id=user_id,
            funds_difference=result.get("funds_difference"),
            deposit=result.get("mines_game").get("deposit"),
            is_win=True
        )

        return {
            "win_amount": result.get("mines_game").get("game_amount")
        }

    def _commit_result(
            self, user_id: int,
            funds_difference: dict,
            deposit: float,
            is_win: bool) -> None:
        print("MINES COMMIT METHOD")
        self._game_result_service.save(data=GameResultData(
            user_id=user_id,
            game=Games.MINES,
            is_win=float(funds_difference.get("user_funds_diff")) > 0
        ))

        ok, to_blogger_advantage = self._users_service.update_user_advantage(
            delta_advantage=funds_difference.get("user_funds_diff"),
            user_id=user_id
        )
        print(
            f"MINES GAME COMMIT RESULT USER: {funds_difference.get('user_funds_diff')} + {0 if not is_win else deposit}")
        self._users_service.update_user_balance_by_id(
            delta_amount=funds_difference.get("user_funds_diff") + deposit,
            user_id=user_id
        )

        self._site_funds_service.update(
            amount=funds_difference.get(
                "site_funds_diff") - to_blogger_advantage
        )

    @staticmethod
    def _validate_funds(user_balance: float, deposit: int):
        if float(user_balance) < float(deposit):
            raise ValidationError(
                detail="There are not enough balance funds for action",
                code=400
            )

    @staticmethod
    def _deserialize_result(result_json: dict) -> dict:
        return {
            "is_win": result_json.get("mines_game").get("is_win"),
            "win_amount": (
                float(result_json.get("mines_game").get("game_amount"))
                if result_json.get("mines_game").get("is_win") else
                -result_json.get("mines_game").get("deposit")
            ),
            "next_win_factor": result_json.get("next_win_factor"),
            "game_ended": True
        }

    def _get_serialized(
            self, request_data: dict,
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
