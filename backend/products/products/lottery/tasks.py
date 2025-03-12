from celery import shared_task

from inventory.services.inventory import InventoryService
from .repositories.users import UsersLotteryResultsApiRepository
from .repositories.transfer import LotteryResult, LotteryPrize
from .services.transfer import LotteryWinners
from .services.executor import LotteryGameService


def implement_lottery():
    print("APPLY LOTTERY")

    service = LotteryGameService()
    users_repository = UsersLotteryResultsApiRepository()
    inventory_service = InventoryService()

    ok, lottery = service.implement_lottery()

    if not ok:
        raise ValueError("Lottery implementation error!")

    prizes = []

    if lottery.winner_main > 0:
        prizes.append(
            LotteryPrize(
                winner_id=lottery.winner_main,
                prize_item_id=lottery.prize_main
            )
        )

        inventory_service.add_item(owner_id=lottery.winner_main,
                                   item_id=lottery.prize_main.id)

    if lottery.winner_secondary > 0:
        prizes.append(
            LotteryPrize(
                winner_id=lottery.winner_secondary,
                prize_item_id=lottery.prize_secondary
            )
        )

        inventory_service.add_item(owner_id=lottery.winner_secondary,
                                   item_id=lottery.prize_secondary.id)

    print("LOTTERY IMPLEMENTED")

    if not prizes:
        return

    users_repository.send_results(
        results=LotteryResult(prizes=prizes)
    )
