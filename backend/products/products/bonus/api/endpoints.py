from rest_framework.generics import CreateAPIView

from common.views.api import BaseRetreiveAPIView
from common.mixins.api import CreateAPIViewMixin

from ..repositories.bonus import BonusBuyRepository
from ..repositories.free import FreeCasesRepository
from games.repositories.api.users import UsersApiRepository


class BonusBuyStatusApiView(BaseRetreiveAPIView):
    repository = BonusBuyRepository()
    users_repository = UsersApiRepository()

    def retrieve(self, request, *args, **kwargs):
        user_id = self.users_repository.get(user_request=request).get("id")

        return self.get_200_response(
            data=self.repository.get(user_id=user_id)
        )


class BonusBuyNextLevelApiView(CreateAPIViewMixin, CreateAPIView):
    _repository = BonusBuyRepository()
    users_repository = UsersApiRepository()

    def create(self, request, *args, **kwargs):
        user_id = self.users_repository.get(user_request=request).get("id")

        return self.get_201_response(
            data=self._repository.next_level(user_id=user_id)
        )


class GetBonusBuyCaseApiView(CreateAPIViewMixin, CreateAPIView):
    _repository = BonusBuyRepository()
    users_repository = UsersApiRepository()

    def create(self, request, *args, **kwargs):
        user_id = self.users_repository.get(user_request=request).get("id")

        return self.get_201_response(
            data=self._repository.get_case(user_id=user_id)
        )


class HasBonusCaseApiView(BaseRetreiveAPIView):
    _repository = BonusBuyRepository()
    users_repository = UsersApiRepository()
    pk_url_kwarg = "case_pk"

    def retrieve(self, request, *args, **kwargs):
        user_id = self.users_repository.get(user_request=request).get("id")

        return self.get_200_response(
            data={
                "free": self._repository.has_withdrawed_case(
                    user_id=user_id,
                    case_id=self.get_requested_pk()
                ).get("ok"),
                "discount": self._repository.get_discount(
                    user_id=user_id,
                    case_id=self.get_requested_pk()
                ).get("discount")
            }
        )


class AddFreeCaseForDeposit(CreateAPIViewMixin, CreateAPIView):
    _repository = FreeCasesRepository()
    users_repository = UsersApiRepository()
    serializer_class = _repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        user_data = self.users_repository.get(user_request=request)

        result = self._repository.add(request_data=request.data,
                                      user_data=user_data)

        return self.get_201_response(data=result)
