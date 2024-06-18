from django.urls import path

from .views import (main_page_view, account_view, mines_view, battle_view,
                    upgrade_view, contract_view, case_view, inventory_view)


urlpatterns = [
    path("", main_page_view),
    path("account/", account_view, name="account"),
    path("mines/", mines_view, name="mines"),
    path("battle/", battle_view, name="battle"),
    path("upgrade/", upgrade_view, name="upgrade"),
    path("contract/", contract_view, name="contract"),
    path("case/<int:case_id>/", case_view, name="case"),
    path("inventory/", inventory_view, name="inventory"),
]
