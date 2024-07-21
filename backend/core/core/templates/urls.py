from django.urls import path

from .views import (main_page_view, account_view, mines_view, battle_view,
                    upgrade_view, contract_view, case_view, inventory_view,
                    replenish_view, fortune_wheel_view, privacy_policy_view,
                    user_agreement_view, about_view, tos_view, case_drop_view,
                    bonus_buy_view, game_history_view, withdraws_view)

urlpatterns = [
    path("", main_page_view),
    path("account/", account_view, name="account"),
    path("mines/", mines_view, name="mines"),
    path("battle/", battle_view, name="battle"),
    path("upgrade/", upgrade_view, name="upgrade"),
    path("contract/", contract_view, name="contract"),
    path("case/<int:case_id>/", case_view, name="case"),
    path("case/<int:case_id>/drop/", case_drop_view, name="case-drop"),
    path("inventory/", inventory_view, name="inventory"),
    path("replenish/", replenish_view, name="replenish"),
    path("fortune/", fortune_wheel_view, name="fortune"),
    path("privacy/", privacy_policy_view, name="privacy"),
    path("agreement/", user_agreement_view, name="agreement"),
    path("about/", about_view, name="about"),
    path("ToS/", tos_view, name="ToS"),
    path("bonus-buy/", bonus_buy_view, name="bonus-buy"),
    path("account/games/", game_history_view, name="game-history"),
    path("account/withdraws/", withdraws_view, name="withdraw-history"),
]
