from django.db import models


class MinesGame(models.Model):
    user_id = models.PositiveIntegerField()
    count_mines = models.PositiveIntegerField()
    is_win = models.BooleanField()
    loss_step = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(count_mines__gte=1) & models.Q(
                    count_mines__lte=24
                ),
                name="count_mines_gte_1_lte_24"
            ),
        ]

    def get_multiplier(self):
        return self.count_mines / 24
