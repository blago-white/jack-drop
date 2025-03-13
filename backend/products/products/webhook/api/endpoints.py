from rest_framework.generics import CreateAPIView

from common.mixins.api import CreateAPIViewMixin

from bonus.repositories.free import FreeCasesRepository
from games.repositories.fortune import FortuneWheelModelRepository


class DepositWebHookApiView(CreateAPIViewMixin, CreateAPIView):
    free_cases_repository = FreeCasesRepository()
    fortune_wheel_repository = FortuneWheelModelRepository()
    serializer_class = free_cases_repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        print("DEPOSIT WEBHOOK", request.data)

        self.fortune_wheel_repository.drop_ban(
            user_id=request.data.get("user_id")
        )

        return self.get_201_response(
            data=self.free_cases_repository.add(request_data=request.data)
        )
