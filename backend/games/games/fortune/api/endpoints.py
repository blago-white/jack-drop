from common.views.api import DefaultRetrieveApiView, DefaultCreateApiView

from ..repositories.fortune import (FortuneWheelPrizeTypeRepository,
                                    FortuneWheelPrizeRepository,
                                    FortuneWheelRepository,
                                    WheelPromocodeRepository)
from ..serializers import FortuneWheelTimeoutSerializer


class FortuneWheelPrizeTypeApiView(DefaultRetrieveApiView):
    repository = FortuneWheelPrizeTypeRepository()
    serializer_class = repository.default_serializer_class

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(self.repository.get_prize_type(
            request_data=request.data
        ))


class MakeFortuneWheelPrizeApiView(DefaultCreateApiView):
    repository = FortuneWheelPrizeRepository()
    serializer_class = repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        return self.get_201_response(
            data=self.repository.get_prize(request_data=request.data)
        )


class GameTimeoutApiView(DefaultRetrieveApiView):
    repository = FortuneWheelRepository()
    pk_url_kwarg = "user_id"

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            self.repository.get_timeout_for_user(
                user_id=int(self.get_requested_pk())
            )
        )


class UsePromocodeCreateApiView(DefaultCreateApiView):
    repository = WheelPromocodeRepository()
    serializer_class = repository.default_serializer_class

    def get_204_response(self):
        return self._response_class(status=204)

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        promocode = request.data.get("promocode")

        self.repository.use_promocode(user_id=user_id, promocode=promocode)

        return self.get_204_response()
