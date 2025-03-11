import datetime
import threading

import time

from django.db.models.signals import post_save

from ..services.model import LotteryModelService
from .lottery import LotteryEvent
from ..tasks import implement_lottery


def _apply_lottery(lottery_id: int, delay: int):
    time.sleep(delay)

    print("START LOTTERY")

    related_lottery = LotteryModelService().get_by_id(lottery_id=lottery_id)

    if related_lottery.is_active:
        implement_lottery()


def implement_lottery_post_save(
    sender: LotteryEvent,
    instance: LotteryEvent,
    **kwargs
) -> None:
    print("START LOTTERY SIGNAL")

    delay = (instance.created_at + instance.start_after - instance.created_at) + instance.duration

    print(f"DELAY {delay}")

    threading.Thread(target=_apply_lottery, args=(instance.id, delay)).start()

    print("START THREAD")


post_save.connect(implement_lottery_post_save,
                  sender=LotteryEvent,
                  dispatch_uid="implement_lottery")
