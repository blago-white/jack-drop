import time

from django.db import models


def get_current_unix_time():
    return int(time.time())


class LotteryEvent(models.Model):
    is_active = models.BooleanField(default=False)
    duration = models.IntegerField(
        verbose_name="Продолжительность набора участников (в сек.)",
        default=60*60*24
    )
    start_after = models.IntegerField(
        verbose_name="Через сколько сек. начинаем прием заявок",
        default=60
    )
    prize_secondary = models.ForeignKey(to="items.Item",
                                        verbose_name="Дешевый приз",
                                        on_delete=models.CASCADE,
                                        related_name="lottery_secondary_results")
    prize_main = models.ForeignKey(to="items.Item",
                                   verbose_name="Дорогой приз",
                                   on_delete=models.CASCADE,
                                   related_name="lottery_primary_results")

    winner_main = models.IntegerField(null=True, blank=True)
    winner_secondary = models.IntegerField(null=True, blank=True)

    deposit_amount_require = models.IntegerField(
        default=30,
        verbose_name="Сумма депозитов [Участ. в глав. розыгр.]"
    )
    display_participants_count = models.IntegerField(default=0)
    is_dummy = models.BooleanField(
        verbose_name="Победитель не определяется",
        default=True
    )

    created_at = models.IntegerField(blank=True)

    def __str__(self):
        return f"Lottery [{self.display_participants_count} users]"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.id:
            self.created_at = get_current_unix_time()

        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )


class LotteryParticipant(models.Model):
    user_id = models.IntegerField()
    lottery = models.ForeignKey(to=LotteryEvent,
                                on_delete=models.CASCADE,
                                related_name="participants")
    to_main_lottery = models.BooleanField(default=False)

    def __str__(self):
        return f"Participant [{self.user_id}]"
