from django.db import models


class BattleRequest(models.Model):
    initiator_id = models.PositiveIntegerField(unique=True)
    battle_case_id = models.PositiveIntegerField()
    start_find_time = models.TimeField(auto_now=True, blank=True)


class Battle(models.Model):
    winner_id = models.PositiveIntegerField()
    loser_id = models.PositiveIntegerField()
    battle_case_id = models.PositiveIntegerField()
    finished_at = models.DateTimeField(auto_now=True, blank=True)
