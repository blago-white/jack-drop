from django.urls import path

from .endpoints import (BonusBuyStatusApiView, BonusBuyNextLevelApiView,
                        GetBonusBuyCaseApiView, HasBonusCaseApiView,
                        AllBonusesCasesApiView)


urlpatterns = [
    path("info/", BonusBuyStatusApiView.as_view(), name="bonus-buy-stats"),
    path("next/", BonusBuyNextLevelApiView.as_view(), name="bonus-buy-next"),
    path("get-case/", GetBonusBuyCaseApiView.as_view(), name="bonus-buy-case"),
    path("bonuse/<int:case_pk>/", HasBonusCaseApiView.as_view(), name="bonuse"),
    path("bonuse/all/", AllBonusesCasesApiView.as_view(), name="bonuse-all"),
    path("deposit-free-case/", GetBonusBuyCaseApiView.as_view(), name="bonus-buy-case"),
]
