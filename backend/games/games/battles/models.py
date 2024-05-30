from django.db import models
from django.core.exceptions import ValidationError


class BattleRequest(models.Model):
    initiator_id = models.PositiveIntegerField(unique=True)
    battle_case_id = models.PositiveIntegerField()
    start_find_time = models.DateTimeField(auto_now=True, blank=True)
    participant_id = models.PositiveIntegerField(unique=True)
    commited = models.BooleanField(default=False)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.commited:
            raise ValidationError("Cannot edit commited instace")

        if self.initiator_id and self.participant_id:
            self.commited = True

        super().save(

            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )


class Battle(models.Model):
    winner_id = models.PositiveIntegerField()
    loser_id = models.PositiveIntegerField()
    battle_case_id = models.PositiveIntegerField()
    finished_at = models.DateTimeField(auto_now=True, blank=True)
