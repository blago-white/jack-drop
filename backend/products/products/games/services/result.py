from common.services.base import BaseModelService
from .transfer import GameResultData
from ..models import GameResult


class GameResultService(BaseModelService):
    default_model = GameResult

    def save(self, data: GameResultData) -> GameResult:
        args = dict(
            user_id=data.user_id,
            game=data.game,
            is_win=data.is_win,
        )

        if data.case_id:
            if (type(data.case_id) is list) and all(data.case_id):
                args.update(related_case_id=data.case_id)
            elif type(data.case_id) is int:
                args.update(related_case_id=data.case_id)

        if data.first_item_id:
            args.update(related_item_first_id=data.first_item_id)

        if data.second_item_id:
            args.update(related_item_second_id=data.second_item_id)

        return self._model.objects.create(**args)

    def get_for_user(self, user_id: int) -> GameResult:
        return self._model.objects.filter(user_id=user_id)