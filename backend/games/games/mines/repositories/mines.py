from common.repositories import BaseRepository

from ..services.mines import MinesService, MinesModelService
from ..services.transfer import MinesGameRequest, MinesGameResult
from ..serializers import MinesGameRequestSerializer, MinesGameResultSerializer


class MinesGameRepository(BaseRepository):
    default_service = MinesService()
    default_serializer_class = MinesGameRequestSerializer
    default_model_service = MinesModelService()

    _serializer_class: MinesGameRequestSerializer
    _service: MinesService
    _model_service: MinesModelService

    def __init__(self, *args,
                 model_service: MinesModelService = None,
                 **kwargs):
        self._model_service = model_service or self.default_model_service

        super().__init__()

    def make(self, request_data: dict) -> dict:
        serialized: MinesGameRequestSerializer = self._serializer_class(
            data=request_data
        )

        serialized.is_valid(raise_exception=True)

        game_request = self._serialize_game_request(
            serialized=serialized
        )

        result: MinesGameResult = self._service.get_result(
            game_request=game_request
        )

        instance = self._model_service.save(
            count_mines=game_request.count_mines,
            is_win=result.is_win,
            loss_step=result.loss_step
        )

        return MinesGameResultSerializer(
            instance={
                "mines_game": instance,
                "funds_difference": result.funds_diffirence
            }
        ).data

    @staticmethod
    def _serialize_game_request(
            serialized: MinesGameRequestSerializer
    ) -> MinesGameRequest:
        return MinesGameRequest(
            count_mines=serialized.data.get("count_mines"),
            user_advantage=serialized.data.get("user_advantage"),
            user_deposit=serialized.data.get("user_deposit"),
            site_active_funds_per_hour=serialized.data.get(
                "site_funds"
            ).get("site_active_funds_per_hour"),
        )
