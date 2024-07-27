from django.urls import path

from .endpoints import (BonusBuyStatusApiView, BonusBuyNextLevelApiView,
                        GetBonusBuyCaseApiView, HasBonusCaseApiView,
                        AddFreeCaseForDeposit)


urlpatterns = [
    path("info/", BonusBuyStatusApiView.as_view(), name="bonus-buy-stats"),
    path("next/", BonusBuyNextLevelApiView.as_view(), name="bonus-buy-next"),
    path("get-case/", GetBonusBuyCaseApiView.as_view(), name="bonus-buy-case"),
    path("has-case/<int:case_pk>/", HasBonusCaseApiView.as_view(), name="has-case"),
    path("add-for-deposit/", AddFreeCaseForDeposit.as_view(), name="add-for-dep")
]
