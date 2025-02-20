from common.repositories import BaseRepository
from ..serializers import MinesGameInitSerializer, MinesGameNextStepSerializer, \
    GameResultSerializer, FundsDifferenceSerializer
from ..services.mines import MinesService, MinesModelService
from ..services.transfer import MinesGameNextStepRequest, MinesGameStepResult, \
    MinesGameInitParams


class MinesGameRepository(BaseRepository):
    default_service = MinesService()
    default_model_service = MinesModelService()

    default_serializer_class = GameResultSerializer
    default_init_serializer_class = MinesGameInitSerializer
    default_mines_game_init_params = MinesGameInitParams
    default_next_serializer_class = MinesGameNextStepSerializer

    _init_serializer_class: MinesGameInitSerializer
    _service: MinesService
    _model_service: MinesModelService

    def __init__(
            self, *args,
            model_service: MinesModelService = None,
            init_serializer_class: MinesGameInitSerializer = None,
            mines_game_init_params: MinesGameInitParams = None,
            **kwargs):
        self._model_service = model_service or self.default_model_service
        self._init_serializer_class = init_serializer_class or self.default_init_serializer_class
        self._mines_game_init_params = mines_game_init_params or self.default_mines_game_init_params

        super().__init__(*args, **kwargs)

    def next(self, request_data: dict) -> dict:
        serialized: MinesGameNextStepSerializer = self.default_next_serializer_class(
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
            print("LOSSEE LOSEEE", result.funds_diffirence)

            user_id = serialized.data.get("user_id")

            commited = self._model_service.commit(
                user_id=user_id,
                is_win=False
            )

            return {
                "mines_game": self._serializer_class(instance=commited).data,
                "funds_difference": FundsDifferenceSerializer(
                    instance=result.funds_diffirence
                ).data,
                "game_ended": True
            }

        print("NEXT NEXT", result.funds_diffirence, "|", game_request)

        instance = self._model_service.next_win_step(
            user_id=serialized.data.get("user_id"),
            new_game_amount=game_request.user_current_ammount + result.funds_diffirence.user_funds_diff,
            step=game_request.step + 1
        )

        return {"new_amount": instance.game_amount,
                "game_ended": False}

    def init(self, data: dict) -> dict:
        serialized: MinesGameInitSerializer = self._init_serializer_class(
            data=data
        )

        serialized.is_valid(raise_exception=True)

        created, obj = self._model_service.init(
            data=self._mines_game_init_params(
                user_id=serialized.data.get("user_funds").get("id"),
                advantage=serialized.data.get("user_funds").get("id"),
                count_mines=serialized.data.get("count_mines"),
                deposit=serialized.data.get("user_deposit"),
            )
        )

        return self._serializer_class(instance=obj).data

    def stop(self, user_id: int) -> dict:
        commited = self._model_service.commit(user_id=user_id, is_win=True)

        print("STOP STOP", commited, commited.game_amount, commited.deposit)

        return {
            "mines_game": self._serializer_class(
                instance=commited
            ).data,
            "funds_difference": FundsDifferenceSerializer(
                instance={
                    "user_funds_diff": commited.game_amount - commited.deposit,
                    "site_funds_diff": -(commited.game_amount - commited.deposit),
                    "game_ended": True
                }
            ).data,
            "game_ended": True
        }

    def _serialize_game_request(
            self, serialized: MinesGameInitSerializer
    ) -> MinesGameNextStepRequest:
        game = self._model_service.get_active(
            user_id=serialized.data.get(
                "user_id"
            ),
            raise_exception=True
        )

        return MinesGameNextStepRequest(
            count_mines=game.count_mines,
            user_advantage=game.user_advantage,
            user_deposit=game.deposit,
            site_active_funds=serialized.data.get(
                "site_funds"
            ).get("site_active_funds"),
            user_current_ammount=game.game_amount,
            step=game.step
        )
