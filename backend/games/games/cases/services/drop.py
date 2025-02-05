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
            is_win = self._win_service.add_new_drop()

            print(f"DROP IS WIN: {is_win}")

            advantage_positive = request.state.usr_advantage > 0

            if request.state.site_active_funds_for_cases < 50:
                is_win = random.randint(0, 8) == 0
                print(f"SITE ACTIVE FUNDS < 50 {is_win=}")
            elif request.state.site_active_funds_for_cases > request.case_price*.5 and not is_win:
                if not advantage_positive:
                    is_win = is_win or (random.randint(0, 3) == 0)
                    print(f"IS WIN NEXT TRY ADV NOT POS {is_win=}")
                if request.early_drops_rate[0] <= 3:
                    is_win = is_win or (random.randint(0, 2) == 0)
                    print(f"IS WIN NEXT TRY DROPS RATE {is_win=}")

            if not is_win:
                item = self._get_random_loss_item(request=request)
                print(f"RECEIVE LOSE ITEM {item}")
            elif request.state.site_active_funds > request.case_price:
                item = self._get_random_winning_item(
                    request=request,
                    strict=True
                )
                print(f"RECEIVE WIN ITEM {item}")
            else:
                item = self._get_random_loss_item(
                    request=request,
                    strict=random.randint(0, 3) == random.randint(0, 3) != 0
                )

                print(f"RECEIVE LOSE ITEM 2 {item}")

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

        if not items:
            raise ChancesValuesError()

        random_item = self._get_random(items=items)

        return random_item

    def _get_random_winning_item(
            self, request: DropRequest,
            strict: bool = False) -> CaseItem:
        items = list(filter(
            lambda item: (
                    request.state.site_active_funds >
                    (item.price - request.case_price)*2 and
                    item.price >= (
                        request.case_price
                        if strict else
                        min(request.case_price * 0.9, request.case_price - 100)
                    )
            ), request.items
        ))

        if not items:
            return self._get_random_loss_item(request=request,
                                              strict=True)

        return self._get_random(items=items)

    def _get_random_loss_item(
            self, request: DropRequest,
            strict: bool = False) -> CaseItem:
        items = list(filter(
            lambda item: (
                item.price <= (
                    request.case_price
                    if strict else
                    min(request.case_price * 1.1, request.case_price + 100))
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
