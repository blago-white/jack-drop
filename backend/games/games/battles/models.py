from django.db import models


class BattleRequest(models.Model):
    initiator_id = models.PositiveIntegerField(unique=True)
    battle_case_id = models.PositiveIntegerField(unique=True)
    start_find_time = models.DateTimeField(auto_now=True, blank=True)


class Battle(models.Model):
    winner_id = models.PositiveIntegerField()
    loser_id = models.PositiveIntegerField()

    battle_case_id = models.PositiveIntegerField()

    dropped_item_winner_id = models.PositiveIntegerField()
    dropped_item_loser_id = models.PositiveIntegerField()

    loser_balance_diff = models.FloatField(default=0)
    winner_balance_diff = models.FloatField(default=0)

    make_at = models.DateTimeField(auto_now=True, blank=True)
