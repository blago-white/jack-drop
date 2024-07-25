from django.core.exceptions import ValidationError
from django.db import models


class MinesGame(models.Model):
    user_id = models.PositiveIntegerField()
    user_advantage = models.IntegerField()

    count_mines = models.PositiveIntegerField()
    is_win = models.BooleanField(null=True, blank=True)
    step = models.IntegerField(blank=True, default=0)

    game_amount = models.IntegerField(default=1)
    deposit = models.FloatField(default=1)
    commited = models.BooleanField(blank=True, default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(count_mines__gte=1) & models.Q(
                    count_mines__lte=24
                ),
                name="count_mines_gte_1_lte_24"
            ),
            models.CheckConstraint(
                check=models.Q(step__gte=0) & models.Q(step__lte=23),
                name="step_gte_0_lte_23"
            ),
            models.CheckConstraint(
                check=models.Q(deposit__gt=0),
                name="deposit_positive"
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.game_amount = self.deposit

        print(f"CREATED: {self.user_id} - {self.count_mines} - {self.game_amount}")

        return super().save(*args, **kwargs)
