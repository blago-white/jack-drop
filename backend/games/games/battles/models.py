from django.db import models
from django.core.exceptions import ValidationError


class BattleRequest(models.Model):
    initiator_id = models.PositiveIntegerField(unique=True)
    battle_case_id = models.PositiveIntegerField()
    start_find_time = models.DateTimeField(auto_now=True, blank=True)


class Battle(models.Model):
    winner_id = models.PositiveIntegerField()
    loser_id = models.PositiveIntegerField()

    battle_case_id = models.PositiveIntegerField()

    dropped_item_winner_id = models.PositiveIntegerField()
    dropped_item_loser_id = models.PositiveIntegerField()

    make_at = models.DateTimeField(auto_now=True, blank=True)
