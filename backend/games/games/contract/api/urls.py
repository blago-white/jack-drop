from django.urls import path

from .endpoints import SaveContractApiView, ShiftedContractAmountApiView


urlpatterns = [
    path("get_shifted_amount/",
         ShiftedContractAmountApiView.as_view(),
         name="get-shifted-amount-contract"),
    path("save/",
         SaveContractApiView.as_view(),
         name="save-contract")
]
