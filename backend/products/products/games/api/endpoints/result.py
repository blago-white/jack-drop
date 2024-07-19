from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import ValidationError

from common.views.api import DetailedApiViewMixin

from games.repositories.result import GameResultsRepository
from games.repositories.api.users import UsersApiRepository


class BonusesRepository:
    def get_for_user(self, user_id: int):
        return []


class GameResultsApiView(DetailedApiViewMixin, RetrieveAPIView):
    pk_url_kwarg = "section"
    repository = GameResultsRepository()
    bonuses_repository = BonusesRepository()
    users_repository = UsersApiRepository()

    def retrieve(self, request, *args, **kwargs):
        user_id = self.users_repository.get(
            user_request=request
        ).get("id")

        section = self.get_requested_pk()

        try:
            return self.get_200_response(data=self.repository.get_for_user(
                user_id=user_id,
                game=section
            ))
        except ValidationError:
            return self.get_200_response(data=self.bonuses_repository.get_for_user(
                user_id=user_id
            ))
