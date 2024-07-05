from rest_framework.generics import RetrieveAPIView

from common.views.api import DetailedApiViewMixin

from games.repositories.result import GameResultsRepository


class GameResultsApiView(DetailedApiViewMixin, RetrieveAPIView):
    pk_url_kwarg = "user_id"
    repository = GameResultsRepository()

    def retrieve(self, request, *args, **kwargs):
        user_id = self.get_requested_pk()

        return self.get_200_response(data=self.repository.get_for_user(
            user_id=user_id
        ))
