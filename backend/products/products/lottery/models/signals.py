import datetime
import threading

import time

from django.db.models.signals import post_save

from .lottery import LotteryEvent
from ..tasks import implement_lottery


def _apply_lottery(delay: int):
    time.sleep(delay)

    print("START LOTTERY")

    implement_lottery()


def implement_lottery_post_save(
    sender: LotteryEvent,
    instance: LotteryEvent,
    **kwargs
) -> None:
    print("START LOTTERY SIGNAL")

    delay = (instance.created_at + instance.start_after - instance.created_at) + instance.duration

    print(f"DELAY {delay}")

    threading.Thread(target=_apply_lottery, args=(delay, )).start()

    print("START THREAD")


post_save.connect(implement_lottery_post_save,
                  sender=LotteryEvent,
                  dispatch_uid="implement_lottery")
