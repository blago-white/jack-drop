import datetime
import time

from django.db.models.signals import post_save

from .lottery import LotteryEvent
from ..tasks import implement_lottery


def implement_lottery_post_save(
    sender: LotteryEvent,
    instance: LotteryEvent,
    **kwargs
) -> None:
    print("START LOTTERY SIGNAL")

    time.sleep(
        int((
            instance.end_date - instance.start_date
        ) / datetime.timedelta(seconds=1))
    )

    print("START LOTTERY")

    implement_lottery()


post_save.connect(implement_lottery_post_save,
                  sender=LotteryEvent,
                  dispatch_uid="implement_lottery")
