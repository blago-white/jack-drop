from common.mixins.api import CreateApiViewMixin
from games.repositories.api.contract import ContractApiRepository
from games.repositories.api.users import UsersApiRepository

from .base import BaseGameProxyCreateApiView


class ContractGameApiView(CreateApiViewMixin, BaseGameProxyCreateApiView):
    users_api_repository = UsersApiRepository()
    contract_repository = ContractApiRepository()
    serializer_class = contract_repository.default_api_service.default_endpoint_serializer_class

    def create(self, request, *args, **kwargs):
        user_data = self.users_api_repository.get(
            user_request=request
        )

        result = self.contract_repository.make_contract(
            request_data=request.data,
            user_data=user_data
        )

        return self.get_201_response(
            data=result
        )
