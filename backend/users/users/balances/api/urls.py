from django.urls import path

from .endpoints import DisplayedBalanceRetrieveApiView


urlpatterns = [
    path("api/v1/p/real_balance/<int:client_id>/",
         DisplayedBalanceRetrieveApiView.as_view(),
         "displayed-balance")
]
