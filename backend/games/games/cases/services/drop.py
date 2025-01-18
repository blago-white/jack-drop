import random

from common.services.api.transfer import CaseItem
from common.services.base import BaseModelService
from ._results import FundsDeltaResult
from .exceptions import ChancesValuesError
from .wins import WinDropsService
from ..states.request import DropRequest, ResultState
from ..models import Drop


class CaseItemDropService:
    _win_service: WinDropsService

    def __init__(self, win_service: WinDropsService = WinDropsService):
        self._win_service = win_service or self._win_service

    def drop(self, request: DropRequest) -> ResultState:
        print("DROP REQUEST::::", request)

        if request.case_price == 0:
            item = self._drop_free_case(request=request)
        else:
            now_win = self._win_service.add_new_drop()
            is_win = now_win or (random.randint(
                0, min(request.early_drops_rate[0], 4)
            ) == random.randint(
                0, min(request.early_drops_rate[0], 4)
            ))

            advantage = request.state.usr_advantage
            advantage_positive = request.state.usr_advantage > 0

            if not is_win:
                item = self._get_random_loss_item(request=request)
            elif advantage_positive and (advantage > request.case_price):
                if now_win:
                    self._win_service.revert_drop()

                item = self._get_random_loss_item(request=request)
            elif not advantage_positive and advantage < -request.case_price:
                item = self._get_random_winning_item(request=request)

                if ((item.price - request.case_price) * 2 >
                        request.state.site_active_funds):
                    item = self._get_random_loss_item(request=request)
            else:
                self._win_service.revert_drop()
                item = self._get_random_loss_item(request=request)

        funds = self._get_funds_delta(drop_item=item,
                                      request=request)

        return ResultState(
            dropped_item=item,
            site_funds_delta=funds.site_funds_delta,
            user_funds_delta=funds.user_funds_delta
        )

    def _drop_free_case(self, request: DropRequest) -> CaseItem:
        mid_idx = len(request.items) // 3

        items = sorted(request.items, key=lambda i: i.price)

        items = [i for i in items[:max(mid_idx, 2)] if
                 i.price < request.state.site_active_funds]

        print("RANDOM1")

        if not items:
            raise ChancesValuesError()

        print("RANDOM2")

        random_item = self._get_random(items=items)

        print("RANDOM3")

        return random_item

    def _get_random_winning_item(self, request: DropRequest) -> CaseItem:
        items = list(filter(
            lambda item: (
                    request.state.site_active_funds >
                    (item.price - request.case_price) and
                    item.price >= request.case_price
            ), request.items
        ))

        if not items:
            return self._get_random_loss_item(request=request)

        return self._get_random(items=items)

    def _get_random_loss_item(self, request: DropRequest) -> CaseItem:
        items = list(filter(
            lambda item: (
                    item.price <= request.case_price
            ), request.items
        ))

        return self._get_random(items=items)

    @staticmethod
    def _get_random(items: list[CaseItem]) -> CaseItem:
        randoms = []

        print(items, "CASE ITEMS FOR DROP")

        percent = sum([i.rate * 100 for i in items]) / 100
        rates = [((i.rate * 100) / percent) for i in items]

        for item, rate in zip(items, rates):
            randoms.extend([item] * (round(rate) if rate > 0.5 else 1))

        randoms.reverse()

        if (diff := len(randoms) - 100) != 0:
            if abs(diff) > 10:
                raise ChancesValuesError("Not correct chances in case")

            if diff > 0:
                randoms = randoms[len(randoms) - 100:]
            elif diff < 0:
                randoms.extend([randoms[0]] * (100 - len(randoms)))

        return random.choice(randoms)

    @staticmethod
    def _get_funds_delta(
            drop_item: CaseItem,
            request: DropRequest) -> FundsDeltaResult:
        return FundsDeltaResult(
            site_funds_delta=request.case_price - drop_item.price,
            user_funds_delta=drop_item.price - request.case_price
        )


class CaseItemDropModelService(BaseModelService):
    default_model = Drop

    def add(self, user_id: int, result: ResultState):
        drop = self._model(user_id=user_id,
                           dropped_item_id=result.dropped_item.item_id,
                           dropped_case_item_id=result.dropped_item.id,
                           site_funds_delta=result.site_funds_delta)

        drop.save()

        return drop

    def get_early_games_rate(self, user_id: int) -> tuple[int, float]:
        result = self._model.objects.filter(user_id=user_id).values_list(
            "site_funds_delta", flat=True
        )

        last_ten_results = result[:10]

        rate = (sum([i for i in last_ten_results if i > 0]) -
                abs(sum([i for i in last_ten_results if i < 0])))

        return len(result), rate,
