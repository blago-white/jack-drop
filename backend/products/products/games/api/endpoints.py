from django.conf import settings
from rest_framework.generics import RetrieveAPIView

from cases.repositories.case import CasesRepository
from common.mixins.api import DetailedApiViewMixin
from games.repositories.api.drop import CaseDropApiRepository
from games.repositories.api.users import UsersApiRepository
from games.serializers.drop import DropItemGameApiViewSerializer


class BaseGameProxyApiView(RetrieveAPIView):
    _routes: dict[str, str] = settings.GAMES_SERVICE_ROUTES


class DropItemGameApiView(DetailedApiViewMixin, BaseGameProxyApiView):
    users_api_repository = UsersApiRepository()
    cases_repository = CasesRepository()
    drop_api_repository = CaseDropApiRepository()

    serializer_class = DropItemGameApiViewSerializer

    pk_url_kwarg = "case_id"

    def retrieve(self, request, *args, **kwargs):
        user_funds = self.users_api_repository.get(
            user_request=request
        )

        case_data = self.cases_repository.get(
            case_id=self.get_requested_pk()
        )

        return self.get_200_response(
            data=self.drop_api_repository.drop(
                data=user_funds | case_data
            )
        )


class UpgradeGameApiView(DetailedApiViewMixin, BaseGameProxyApiView):
    pass


class ContractGameApiView(DetailedApiViewMixin, BaseGameProxyApiView):
    pass
