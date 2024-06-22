import dataclasses
import random

from common.services.base import BaseModelService
from common.services.api.transfer import CaseData
from common.services.api.states import FundsDifference

from ..models import FortuneWheelWinning, WinningTypes
from ..services.transfer import FortuneWheelGameResult, FortuneWheelGameRequest


class FortuneWheelModelService(BaseModelService):
    default_model = FortuneWheelWinning

    def save(self, result: FortuneWheelGameResult) -> FortuneWheelWinning:
        instance = self._model.objects.create(
            user_id=result.user_id,
            winning_type=result.winning_type,
            user_funds_diff=result.funds_diff.user_funds_diff,
            site_funds_diff=result.funds_diff.site_active_funds_diff
        )

        return instance


class FortuneWheelService:
    winning_types = WinningTypes
    min_free_item_price = 20
    min_contract_item_price = 100

    free_skin_random_chance = 5

    def make(self, request: FortuneWheelGameRequest) -> FortuneWheelGameResult:
        winning_item = self._get_win_item(request=request)

        if request.winning_type == self.winning_types.FREE_SKIN:
            user_funds_diff = winning_item.price
            site_funds_diff = -winning_item.price
        else:
            user_funds_diff = 0
            site_funds_diff = 0

        return FortuneWheelGameResult(
            funds_diff=FundsDifference(
                user_funds_diff=user_funds_diff,
                site_active_funds_diff=site_funds_diff
            ),
            user_id=request.user_id,
            winning_type=request.winning_type,
            winning_item=winning_item
        )

    def _get_win_item(
            self, request: FortuneWheelGameRequest) -> dataclasses.dataclass:
        print(request.data.items)
        print(request.data)

        if request.winning_type == self.winning_types.UPGRADE:
            return random.choice(
                sorted(
                    request.data.items, key=lambda item: item.price
                )[:len(request.data.items) // 2]
            )

        if request.winning_type == self.winning_types.CONTRACT:
            able_items = [i
                          for i in request.data.items
                          if i.price < request.funds_state.site_active_funds]

            if not able_items:
                able_items = sorted(
                    request.data.items, key=lambda item: item.price
                )

            able_items = able_items[:random.randint(1, len(able_items) - 1)]

            return random.choice(
                    able_items
                    if (request.funds_state.usr_advantage <
                        able_items[0].price)
                    else able_items[:2]
            )

        if request.winning_type == self.winning_types.FREE_SKIN:
            if not request.funds_state.usr_advantage:
                return random.choice(
                    request.data.items[:len(request.data.items) // 2]
                )
            else:
                return random.choice(
                    request.data.items[:3]
                )

        if request.winning_type == self.winning_types.CASE_DISCOUNT:
            return self._get_case(cases=request.data.items)

    def get_type(
            self, request: FortuneWheelGameRequest
    ) -> tuple[str, str]:
        if (
                request.funds_state.site_active_funds < self.min_free_item_price
        ):
            return self._get_lose_result()

        if (request.funds_state.site_active_funds <
                self.min_contract_item_price):
            return self._get_lose_result()

        if request.funds_state.usr_advantage <= 0:
            if (request.funds_state.usr_advantage <
                    -self.min_contract_item_price):
                return (
                    self.winning_types.CONTRACT
                    if random.randint(
                        0, 100
                    ) < self.free_skin_random_chance or (
                            request.funds_state.site_active_funds < request.min_item_price <= request.funds_state.usr_advantage
                    ) else
                    self.winning_types.FREE_SKIN
                )

            if request.funds_state.usr_advantage < -self.min_free_item_price:
                return (
                    self.winning_types.FREE_SKIN
                    if random.randint(
                        0, 100
                    ) < self.free_skin_random_chance else
                    self._get_lose_result()
                )

        return self._get_lose_result()

    def _get_lose_result(self) -> str:
        return (self.winning_types.CASE_DISCOUNT
                if random.randint(0, 100) >= 50 else
                self.winning_types.UPGRADE)

    @staticmethod
    def _get_case(cases: list[CaseData], count: int = None) -> CaseData:
        cases = sorted(cases, key=lambda case: case.price, reverse=True)

        return random.choice(
            cases+cases[:len(cases)//2 if not count else count]
        )
