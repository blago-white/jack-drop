from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from common.mixins import BaseRetrieveApiViewMixin, BaseDetailedCreateApiViewMixin
from ..repositories.users import PublicUsersRepository


class UserDataApiView(BaseRetrieveApiViewMixin, RetrieveAPIView):
    repository = PublicUsersRepository()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.get_user_info(user_id=request.user.id)
        )


class UserTradeLinkApiView(BaseDetailedCreateApiViewMixin, CreateAPIView):
    repository = PublicUsersRepository()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return self.get_201_response(
            data=self.repository.update_trade_link(
                user_id=request.user.id,
                trade_link=request.data.get("trade_link")
            )
        )
