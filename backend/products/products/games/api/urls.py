from django.urls import path

from .endpoints.contract import ContractGameApiView
from .endpoints.drop import DropItemGameApiView
from .endpoints.mines import MinesGameApiView
from .endpoints.upgrade import UpgradeGameApiView

urlpatterns = [
    path("drop/<int:case_id>/", DropItemGameApiView.as_view(), name="drop"),
    path("upgrade/", UpgradeGameApiView.as_view(), name="upgrade"),
    path("contract/", ContractGameApiView.as_view(), name="contract"),
    path("mines/", MinesGameApiView.as_view(), name="mines"),
]
