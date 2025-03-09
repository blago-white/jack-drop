from django.db import models


class LotteryEvent(models.Model):
    is_active = models.BooleanField(default=False)
    end_date = models.DateTimeField(
        verbose_name="Дата определения победителя"
    )
    start_date = models.DateTimeField(
        verbose_name="Дата создания"
    )
    prize_secondary = models.ForeignKey(to="items.Item",
                                        verbose_name="Дешевый приз",
                                        on_delete=models.CASCADE)
    prize_main = models.ForeignKey(to="items.Item",
                                   verbose_name="Дорогой приз",
                                   on_delete=models.CASCADE)

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

    def __str__(self):
        return f"Lottery [{self.display_participants_count} users]"


class LotteryParticipant(models.Model):
    user_id = models.IntegerField()
    lottery = models.ForeignKey(to=LotteryEvent,
                                on_delete=models.CASCADE,
                                related_name="participants")
    to_main_lottery = models.BooleanField(default=False)

    def __str__(self):
        return f"Participant [{self.user_id}]"
