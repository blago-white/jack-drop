from django.urls import path

from .endpoints.drop import DropItemGameApiView
from .endpoints.upgrade import UpgradeGameApiView
from .endpoints.contract import ContractApiRepository

urlpatterns = [
    path("drop/<int:case_id>/", DropItemGameApiView.as_view(), name="drop"),
    path("upgrade/", UpgradeGameApiView.as_view(), name="upgrade"),
    path("contract/", ContractApiRepository.as_view(), name="upgrade")
]
