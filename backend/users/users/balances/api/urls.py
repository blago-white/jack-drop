from django.urls import path

from .displayed import (DisplayedBalanceRetrieveApiView,
                        DisplayedBalanceUpdateJWTApiView,
                        DisplayedBalanceUpdateApiView)


urlpatterns = [
    path("api/v1/p/displayed_balance_jwt/",
         DisplayedBalanceRetrieveApiView.as_view(),
         "displayed-balance"),
    path("api/v1/p/displayed_balance_jwt/update/",
         DisplayedBalanceUpdateJWTApiView.as_view(),
         "update-displayed-balance"),
    path("api/v1/p/displayed_balance/<int:client_id>/update/",
         DisplayedBalanceUpdateApiView.as_view()),
    path("api/v1/p/hidden_balance/<int:client_id>/update/",
         DisplayedBalanceUpdateApiView.as_view())
]
