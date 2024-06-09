from django.urls import path

from .views import (main_page_view, account_view, mines_view, battle_view,
                    upgrade_view)


urlpatterns = [
    path("", main_page_view),
    path("account/", account_view, name="account"),
    path("mines/", mines_view, name="mines"),
    path("battle/", battle_view, name="battle"),
    path("upgrade/", upgrade_view, name="upgrade"),
]
