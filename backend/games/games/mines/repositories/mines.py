from common.repositories import BaseRepository
from ..serializers import MinesGameInitSerializer, MinesGameNextStepSerializer, MinesGameResultSerializer, GameResultSerializer
from ..services.mines import MinesService, MinesModelService
from ..services.transfer import MinesGameNextStepRequest, MinesGameStepResult, MinesGameInitParams


class MinesGameRepository(BaseRepository):
    default_service = MinesService()
    default_model_service = MinesModelService()

    default_serializer_class = GameResultSerializer
    default_init_serializer_class = MinesGameRequestSerializer
    default_mines_game_init_params = MinesGameInitParams

    _init_serializer_class: MinesGameRequestSerializer
    _service: MinesService
    _model_service: MinesModelService

    def __init__(self, *args,
                 model_service: MinesModelService = None,
                 init_serializer_class: MinesGameInitSerializer = None,
                 mines_game_init_params: MinesGameInitParams = None,
                 **kwargs):
        self._model_service = model_service or self.default_model_service
        self._init_serializer_class = init_serializer_class or self.default_init_serializer_class
        self._mines_game_init_params = mines_game_init_params or self.default_mines_game_init_params

        super().__init__(*args, **kwargs)

    def next(self, request_data: dict) -> dict:
        serialized: MinesGameNextStepSerializer = self._init_serializer_class(
            data=request_data
        )

        serialized.is_valid(raise_exception=True)

        game_request = self._serialize_game_request(
            serialized=serialized
        )

        result: MinesGameStepResult = self._service.next_step(
            game_request=game_request
        )

        if not result.is_win:
            user_id = serialized.data.get("user_funds").get("id")

            commited = self._model_service.commit(
                user_id=user_id,
                mines_game_result=result
            )

            return MinesGameResultSerializer(
                instance={
                    "mines_game": commited,
                    "funds_difference": result.funds_diffirence
                }
            ).data

        instance = self._model_service.next_win_step(
            user_id=serialized.data.get("user_funds").get("id"),
            new_game_amount=result.funds_diffirence.user_funds_diff,
            step=game_request.step+1
        )

        return {"new_amount": instance.game_amount,
                "game_ended": False}

    def init(self, data: dict) -> dict:
        serialized: MinesGameInitSerializer = self._init_serializer_class(data=data)

        serialized.is_valid(raise_exception=True)

        created, obj = self._model_service.init(
            data=self._mines_game_init_params(
                user_id=serialized.data.get("user_funds").get("id"),
                count_mines=serialized.data.get("count_mines"),
                deposit=serialized.data.get("user_deposit"),
            )
        )

        return self._serializer_class(instance=obj).data

    def stop(self, user_id: int) -> dict:
        commited = self._model_service.commit(user_id=user_id)

        return self._serializer_class(
            instance=commited
        ).data

    def _serialize_game_request(
            self, serialized: MinesGameRequestSerializer
    ) -> MinesGameNextStepRequest:
        game = self._model_service.get_active(
            user_id=serialized.data.get("user_funds").get(
                "id"
            ),
            raise_exception=True
        )

        return MinesGameNextStepRequest(
            count_mines=serialized.data.get("count_mines"),
            user_advantage=serialized.data.get("user_funds").get(
                "user_advantage"
            ),
            user_deposit=game.deposit,
            site_active_funds=serialized.data.get(
                "site_funds"
            ).get("site_active_funds"),
            user_current_ammount=game.game_amount,
            step=game.step
        )
