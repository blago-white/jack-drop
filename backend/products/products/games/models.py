from django.core.exceptions import ValidationError
from django.db import models


class Games(models.TextChoices):
    UPGRADE = "U", "Upgrade"
    CONTRACT = "C", "Contract"
    BATTLE = "B", "Battle"
    MINES = "M", "Mines"


class GameResult(models.Model):
    user_id = models.IntegerField()
    game = models.CharField(max_length=20, choices=Games.choices)

    is_win = models.BooleanField(default=False, blank=True)

    related_case = models.ForeignKey("cases.Case",
                                     on_delete=models.CASCADE,
                                     null=True)
    related_item_first = models.ForeignKey("items.Item",
                                           on_delete=models.CASCADE,
                                           null=True,
                                           related_name="result_items_first")
    related_item_second = models.ForeignKey("items.Item",
                                            on_delete=models.CASCADE,
                                            null=True,
                                            related_name="result_items_second")

    date = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"{self.get_game_display()} game {'win' if self.is_win else 'lose'}"

    def clean(self):
        if self.related_case and self.related_item_second:
            raise ValidationError("Can add related case or related item second")
