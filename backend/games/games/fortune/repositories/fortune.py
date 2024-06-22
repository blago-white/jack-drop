import json

from common.repositories import BaseRepository

from ..services.fortune import (FortuneWheelService,
                                FortuneWheelModelService)
from ..services.transfer import (FortuneWheelGameRequest,
                                 FortuneWheelGameResult,
                                 FundsState,
                                 FortuneWheelTypeGameRequest,
                                 FortuneWheelCaseData,
                                 FortuneWheelCaseItemData)
from ..serializers import (PrizeTypeSerializer, PrizeTypeRequestSerializer,
                           PrizeRequestSerializer, PrizeSerializer)
from ..models import WinningTypes


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

    _service: FortuneWheelService

    def __init__(self, *args,
                 model_service: FortuneWheelModelService = None,
                 serializer_class: PrizeSerializer = None,
                 **kwargs):
        self._model_service = model_service or self.default_model_service
        self._serializer_class = serializer_class or self.default_serializer_class

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

        return PrizeSerializer(instance={
            "prize": result.winning_item.as_json(),
            "user_funds_diff": result.funds_diff.user_funds_diff,
            "site_funds_diff": result.funds_diff.site_active_funds_diff,
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
