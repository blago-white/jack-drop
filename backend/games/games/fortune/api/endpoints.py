from common.views.api import DefaultRetrieveApiView, DefaultCreateApiView

from ..repositories.fortune import FortuneWheelPrizeTypeRepository, FortuneWheelPrizeRepository


class FortuneWheelPrizeTypeApiView(DefaultRetrieveApiView):
    repository = FortuneWheelPrizeTypeRepository()
    serializer_class = repository.default_serializer_class

    def retrieve(self, request, *args, **kwargs):
        print(request.data, "REQUEST")

        return self.get_200_response(self.repository.get_prize_type(
            request_data=request.data
        ))


class MakeFortuneWheelPrizeApiView(DefaultCreateApiView):
    repository = FortuneWheelPrizeRepository()
    serializer_class = repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        print(request.data, "REQUEST")

        return self.get_201_response(
            data=self.repository.get_prize(request_data=request.data)
        )
