from django.urls import path

from .displayed import (DisplayedBalanceRetrieveApiView,
                        DisplayedBalanceUpdateJWTApiView)
from .hidden import (DisplayedBalanceUpdateApiView, AddDepositApiView)

urlpatterns = [
    path("api/v1/p/displayed_balance_jwt/",
         DisplayedBalanceRetrieveApiView.as_view(),
         name="displayed-balance"),
    path("api/v1/p/displayed_balance_jwt/update/",
         DisplayedBalanceUpdateJWTApiView.as_view(),
         name="update-displayed-balance"),
    path("api/v1/p/displayed_balance/<int:client_id>/update/",
         DisplayedBalanceUpdateApiView.as_view()),
    path("api/v1/public/add_deposit/", AddDepositApiView.as_view()),
]
