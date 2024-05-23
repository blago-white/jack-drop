from django.db import models


class BattleRequest(models.Model):
    initiator_id = models.PositiveIntegerField()
    battle_case_id = models.PositiveIntegerField()
