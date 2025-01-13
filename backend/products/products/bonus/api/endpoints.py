from rest_framework.generics import CreateAPIView
from rest_framework.request import Request

from common.views.api import BaseRetreiveAPIView, BaseListAPIView
from common.mixins.api import CreateAPIViewMixin

from ..repositories.bonus import BonusBuyRepository, UserBonusesRepository
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
    _user_bonuses_repository = UserBonusesRepository()
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
                "discount": self._user_bonuses_repository.get_discount(
                    user_id=user_id,
                    case_id=self.get_requested_pk()
                ).get("discount")
            }
        )


class AllBonusesCasesApiView(BaseListAPIView):
    _repository = BonusBuyRepository()
    _user_bonuses_repository = UserBonusesRepository()
    users_repository = UsersApiRepository()

    def retrieve(self, request, *args, **kwargs):
        user_id = self.users_repository.get(user_request=request).get("id")

        free_cases = self._repository.get_withdrawed_cases(user_id=user_id)
        discounted = self._user_bonuses_repository.get_all_discounts(
            user_id=user_id
        )

        discounted_dict = {
            i.get("case"): i.get("discount") for i in discounted.get("discounts")
        }

        return self.get_200_response(
            data={
                "free": free_cases,
                "discounted": discounted_dict
            }
        )

    def list(self, request, *args, **kwargs):
        return self.retrieve(*args, request=request, **kwargs)


class GetFreeCaseForDeposit(BaseRetreiveAPIView):
    _free_cases_repository = FreeCasesRepository()

    def retrieve(self, request: Request, *args, **kwargs):
        deposit = float(request.query_params.get("deposit")[0])

        return self.get_200_response(
            data=self._free_cases_repository.get_for_deposit(deposit=deposit)
        )
