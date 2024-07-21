from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from common.mixins.api import CreateAPIViewMixin, ApiViewMixin, \
    DetailedApiViewMixin
from common.views.api import BaseListAPIView
from games.repositories.api.users import UsersApiRepository
from ..repositories.inventory import InventoryRepository


class InventoryItemsListApiView(BaseListAPIView):
    _repository = InventoryRepository()
    _users_repository = UsersApiRepository()

    def list(self, request, *args, **kwargs):
        user_id = self._users_repository.get(
            user_request=request
        ).get("id")

        return self.get_200_response(
            data=self._repository.get_all(user_id=user_id)
        )


class UnlockInventoryItemsListApiView(BaseListAPIView):
    _repository = InventoryRepository()
    _users_repository = UsersApiRepository()

    def list(self, request, *args, **kwargs):
        user_id = self._users_repository.get(user_request=request).get("id")

        return self.get_200_response(
            data=self._repository.get_all_unlock(user_id=user_id)
        )


class UpgradeInventoryItemsListApiView(BaseListAPIView):
    _repository = InventoryRepository()
    _users_repository = UsersApiRepository()

    def list(self, request, *args, **kwargs):
        user_id = self._users_repository.get(user_request=request).get("id")

        return self.get_200_response(
            data=self._repository.get_all_for_upgrade(user_id=user_id)
        )


class ContractInventoryItemsListApiView(BaseListAPIView):
    _repository = InventoryRepository()
    _users_repository = UsersApiRepository()

    def list(self, request, *args, **kwargs):
        user_id = self._users_repository.get(user_request=request).get("id")

        return self.get_200_response(
            data=self._repository.get_all_for_contract(user_id=user_id)
        )


class SellInventoryItemApiView(CreateAPIViewMixin, CreateAPIView):
    _repository = InventoryRepository()
    _users_repository = UsersApiRepository()

    def create(self, request, *args, **kwargs):
        user_id = self._users_repository.get(user_request=request).get("id")

        return self.get_200_response(
            data=self._repository.sell(user_id=user_id,
                                       item_id=request.data.get("item_id"))
        )


class CountInventoryItemsApiView(ApiViewMixin, APIView):
    _repository = InventoryRepository()
    _users_repository = UsersApiRepository()

    def get(self, request, *args, **kwargs):
        user_id = self._users_repository.get(user_request=request).get("id")

        return self.get_200_response(
            data=self._repository.get_count(user_id=user_id)
        )


class WithdrawInventoryItemApiView(DetailedApiViewMixin, CreateAPIViewMixin,
                                   CreateAPIView):
    users_repository = UsersApiRepository()
    repository = InventoryRepository()
    pk_url_kwarg = "item_id"

    def create(self, request, *args, **kwargs):
        user_data = self.users_repository.get(user_request=request)

        result = self.repository.withdraw(user_data=user_data,
                                          item_id=self.get_requested_pk())

        return self.get_201_response(
            data=result
        )


class WithdrawedItemsApiView(CreateAPIViewMixin, CreateAPIView):
    _repository = InventoryRepository()

    def create(self, request, *args, **kwargs):
        return self.get_201_response(
            data=self._repository.commit_withdraw_results(
                results=request.data
            )
        )
