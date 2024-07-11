import datetime
import json
from django.core.exceptions import ValidationError

from common.repositories import BaseRepository

from ..services.fortune import (FortuneWheelService,
                                FortuneWheelModelService,
                                FortuneWheelOpeningModelService,
                                TimeoutValueService,
                                FortuneWheelPromocodeModelService)
from ..services.transfer import (FortuneWheelGameRequest,
                                 FortuneWheelGameResult,
                                 FundsState,
                                 FortuneWheelTypeGameRequest,
                                 FortuneWheelCaseData,
                                 FortuneWheelCaseItemData)
from ..serializers import (PrizeTypeSerializer, PrizeTypeRequestSerializer,
                           PrizeRequestSerializer, PrizeSerializer,
                           FortuneWheelTimeoutSerializer,
                           FortuneWheelTimeoutValueSerializer,
                           UsePromocodeSerializer)
from ..models import WinningTypes


class FortuneWheelRepository(BaseRepository):
    default_serializer_class = FortuneWheelTimeoutSerializer
    default_opening_service = FortuneWheelOpeningModelService()
    default_timeout_service = TimeoutValueService()

    default_service = FortuneWheelTimeoutValueSerializer

    def __init__(self,
                 opening_service: FortuneWheelOpeningModelService = None,
                 timeout_service: TimeoutValueService = None,
                 serializer: FortuneWheelTimeoutSerializer = None):
        self._timeout_service = timeout_service or self.default_timeout_service
        self._opening_service = opening_service or self.default_opening_service

        super().__init__(serializer_class=serializer)

    def get_timeout_for_user(self, user_id: int) -> dict[str, int]:
        time_delta_from_opening = self._opening_service.get_opening_time_delta(
            user_id=user_id
        )

        timeout = self._timeout_service.get()

        if time_delta_from_opening:
            timeout = max(0, (
                    self._timeout_service.get() - time_delta_from_opening
            ))
        else:
            self._opening_service.init_user(user_id=user_id)

        return {
            "current": datetime.datetime.now().replace(
                tzinfo=None
            ).timestamp(),
            "timeout": timeout
        }


class WheelPromocodeRepository(BaseRepository):
    default_service = FortuneWheelPromocodeModelService()
    default_serializer_class = UsePromocodeSerializer()

    def use_promocode(self, user_id: int, promocode: str) -> None:
        try:
            used = self.default_service.use(
                user_id=user_id, promocode=promocode
            )

            if not used:
                raise ValueError

        except Exception as e:
            print(e)
            raise ValidationError("Not valid promocode")


class FortuneWheelPrizeTypeRepository(BaseRepository):
    default_service = FortuneWheelService()
    default_serializer_class = PrizeTypeRequestSerializer

    _service: FortuneWheelService

    def get_prize_type(self, request_data: dict) -> dict:
        serialized: PrizeTypeRequestSerializer = self._serializer_class(
            data=request_data
        )

        serialized.is_valid(raise_exception=True)

        result = self._service.get_type(
            request=self._convert_game_request(
                serialized=serialized
            )
        )

        print(result, "RESULT TYPE")

        return PrizeTypeSerializer(instance={"type": result}).data

    @staticmethod
    def _convert_game_request(
            serialized: PrizeTypeRequestSerializer
    ) -> FortuneWheelTypeGameRequest:
        return FortuneWheelTypeGameRequest(
            funds_state=FundsState(
                usr_advantage=serialized.data.get("user_funds").get(
                    "user_advantage"
                ),
                site_active_funds=serialized.data.get(
                    "site_funds"
                ).get("site_active_funds")
            ),
            min_item_price=serialized.data.get("min_item_price")
        )


class FortuneWheelPrizeRepository(BaseRepository):
    default_service = FortuneWheelService()
    default_serializer_class = PrizeRequestSerializer
    default_model_service = FortuneWheelModelService()
    default_opening_service = FortuneWheelOpeningModelService()

    _service: FortuneWheelService

    def __init__(self, *args,
                 model_service: FortuneWheelModelService = None,
                 serializer_class: PrizeRequestSerializer = None,
                 opening_service: FortuneWheelOpeningModelService = None,
                 **kwargs):
        self._model_service = model_service or self.default_model_service
        self._serializer_class = serializer_class or self.default_serializer_class
        self._opening_service = opening_service or self.default_opening_service

        super().__init__(*args, **kwargs)

    def get_prize(self, request_data: dict) -> dict:
        serialized: PrizeRequestSerializer = self._serializer_class(data=request_data)

        serialized.is_valid(raise_exception=True)

        result: FortuneWheelGameResult = self._service.make(
            request=self._convert_game_request(
                serialized=serialized
            )
        )

        self._model_service.save(result=result)
        print("RES SAVE", self._opening_service.add(
            user_id=serialized.data.get("user_funds").get("id"),
            prize_data=result.winning_item.as_json()
        ))

        return PrizeSerializer(instance={
            "prize": result.winning_item.as_json(),
            "user_funds_diff": result.funds_diff.user_funds_diff,
            "site_funds_diff": result.funds_diff.site_funds_diff,
            "type": result.winning_type
        }).data

    @staticmethod
    def _convert_game_request(
        serialized: PrizeRequestSerializer
    ):
        if serialized.data.get("type") == WinningTypes.CASE_DISCOUNT:
            additional = FortuneWheelCaseData(items=json.loads(
                serialized.data.get("additional_data")
            ))
        else:
            additional = FortuneWheelCaseItemData(items=json.loads(
                serialized.data.get("additional_data")
            ))

        return FortuneWheelGameRequest(
            funds_state=FundsState(
                usr_advantage=serialized.data.get("user_funds").get(
                    "user_advantage"
                ),
                site_active_funds=serialized.data.get("site_funds").get(
                    "site_active_funds"
                ),
            ),
            winning_type=serialized.data.get("type"),
            user_id=serialized.data.get("user_funds").get("id"),
            data=additional
        )
