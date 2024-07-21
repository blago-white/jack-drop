from rest_framework.generics import RetrieveAPIView

from common.mixins import BaseRetrieveApiViewMixin
from ..repositories.users import PublicUsersRepository


class UserDataApiView(BaseRetrieveApiViewMixin, RetrieveAPIView):
    repository = PublicUsersRepository()

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.get_user_info(user_id=request.user.id)
        )
