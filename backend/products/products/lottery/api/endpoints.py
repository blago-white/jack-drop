from rest_framework.generics import RetrieveAPIView, CreateAPIView

from games.api.services.users import UsersApiService
from common.mixins.api import ApiViewMixin, CreateAPIViewMixin

from ..repositories.lottery import LotteryRepository


class GetCurrentLotteryApiView(RetrieveAPIView, ApiViewMixin):
    repository = LotteryRepository()

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.get_current()
        )


class ParticipateLotteryApiView(CreateAPIViewMixin, CreateAPIView):
    repository = LotteryRepository()
    users_repository = UsersApiService()

    def create(self, request, *args, **kwargs):
        user_data = self.users_repository.get_user_info(
            user_request=request
        )

        return self.get_201_response(
            data=self.repository.partipicate(
                user_id=user_data.get("id"),
                to_main=request.data.get("to_main", False)
            )
        )
