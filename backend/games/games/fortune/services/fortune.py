import dataclasses
import datetime
import json
import random

from django.db import models

from common.services.api.states import FundsDifference, FundsState
from common.services.api.transfer import CaseData
from common.services.base import BaseModelService
from ..models import (FortuneWheelWinning, WinningTypes, FortuneWheelOpening,
                      FortuneWheelTimeout, FortuneWheelPromocode)
from ..services.transfer import (FortuneWheelGameResult,
                                 FortuneWheelGameRequest,
                                 CaseDiscountResult)


class FortuneWheelModelService(BaseModelService):
    default_model = FortuneWheelWinning

    def save(self, result: FortuneWheelGameResult) -> FortuneWheelWinning:
        instance = self._model.objects.create(
            user_id=result.user_id,
            winning_type=result.winning_type,
            user_funds_diff=result.funds_diff.user_funds_diff,
            site_funds_diff=result.funds_diff.site_funds_diff
        )

        return instance


class FortuneWheelOpeningModelService(BaseModelService):
    default_model = FortuneWheelOpening

    def get_opening_time_delta(self, user_id: int) -> datetime.timedelta:
        try:
            return datetime.datetime.now().replace(
                tzinfo=None
            ).timestamp() - self.get_latest(
                user_id=user_id
            ).date
        except:
            return None

    def init_user(self, user_id: int):
        return self._model.objects.create(user_id=user_id)

    def get_latest(self, user_id: int) -> FortuneWheelOpening:
        user_openings = self._model.objects.filter(user_id=user_id)

        if not user_openings:
            return

        return user_openings.first()

    def add(self, user_id: int, prize_data: dict):
        return self._model.objects.create(
            result=json.dumps(prize_data),
            user_id=user_id
        )


class FortuneWheelPromocodeModelService(BaseModelService):
    default_model = FortuneWheelPromocode

    def use(self, user_id: int, promocode: str):
        promo = self._model.objects.filter(
            models.Q(for_user=user_id) | models.Q(for_user=None),
            pk=promocode
        )

        if promo.count() and promo.first().count_usages > 0:
            return bool(promo.update(count_usages=models.F("count_usages")-1))

        return False


class TimeoutValueService(BaseModelService):
    default_model = FortuneWheelTimeout

    def get(self) -> datetime:
        return self._model.objects.first().timeout


class FortuneWheelService:
    winning_types = WinningTypes
    min_free_item_price = 20
    min_contract_item_price = 30
    min_upgrade_item_price = 10

    max_free_item_price = 60
    max_contract_item_price = 120
    max_upgrade_item_price = 120

    free_skin_random_chance = 5

    def make(self, request: FortuneWheelGameRequest) -> FortuneWheelGameResult:
        winning_item = self._get_win_item(request=request)

        if request.winning_type == self.winning_types.FREE_SKIN:
            user_funds_diff = winning_item.price
            site_funds_diff = -winning_item.price
        else:
            user_funds_diff = site_funds_diff = 0

        if request.winning_type == self.winning_types.CASE_DISCOUNT:
            diff = winning_item.case.price * (
                winning_item.discount / 100
            )

            user_funds_diff = diff
            site_funds_diff = -diff

        return FortuneWheelGameResult(
            funds_diff=FundsDifference(
                user_funds_diff=user_funds_diff,
                site_funds_diff=site_funds_diff
            ),
            user_id=request.user_id,
            winning_type=request.winning_type,
            winning_item=winning_item
        )

    def _get_win_item(
            self, request: FortuneWheelGameRequest
    ) -> dataclasses.dataclass:
        if request.winning_type == self.winning_types.UPGRADE:
            return random.choice(
                sorted(
                    [i for i in request.data.items
                     if i.price < self.max_upgrade_item_price],
                    key=lambda item: item.price
                )
            )

        if request.winning_type == self.winning_types.CONTRACT:
            able_items = [i
                          for i in request.data.items
                          if i.price < self.max_contract_item_price]

            able_items = able_items[:random.randint(1, len(able_items) - 1)]

            return random.choice(able_items)

        if request.winning_type == self.winning_types.FREE_SKIN:
            free_items = [i for i in request.data.items
                          if i.price < self.max_free_item_price]

            if not request.funds_state.usr_advantage:
                return random.choice(free_items)
            else:
                return random.choice(free_items[:3])

        if request.winning_type == self.winning_types.CASE_DISCOUNT:
            result_case: CaseData = self._get_case(cases=request.data.items)

            discount = self._get_case_discount(case=result_case,
                                               funds=request.funds_state)

            return CaseDiscountResult(case=result_case,
                                      discount=discount)

    def get_type(
            self, request: FortuneWheelGameRequest
    ) -> tuple[str, str]:
        if request.funds_state.site_active_funds < self.min_free_item_price*5:
            return self._get_lose_result()

        if request.funds_state.site_active_funds < self.min_contract_item_price*5:
            return self._get_lose_result()

        if request.funds_state.usr_advantage <= 0:
            if (request.funds_state.usr_advantage <
                    -self.min_contract_item_price*3):
                winnint_type = (random.randint(
                        0, 100
                    ) < self.free_skin_random_chance) or (
                        request.funds_state.site_active_funds <
                        request.min_item_price*5 <=
                        request.funds_state.usr_advantage
                    )

                return (
                    self.winning_types.CONTRACT
                    if winnint_type else
                    self.winning_types.FREE_SKIN
                ) if random.randint(0, 1) == 0 else self._get_lose_result()

            if request.funds_state.usr_advantage < -self.min_free_item_price*2.5:
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

        cases = filter(lambda c: c.price < max(300, cases[-1]), cases)

        return random.choice(
            cases+cases[:len(cases)//2 if not count else count]
        )

    @staticmethod
    def _get_case_discount(case: CaseData,
                           funds: FundsState) -> int:
        if not funds.site_active_funds > case.price*5:
            return random.randint(5, 10)

        if funds.usr_advantage > case.price:
            return random.randint(5, 15)

        if funds.usr_advantage >= 0:
            return random.randint(5, 25)

        if funds.usr_advantage < 0:
            return random.randint(5, 35)
