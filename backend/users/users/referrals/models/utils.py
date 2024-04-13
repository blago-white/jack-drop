from django.db.models import IntegerChoices


class ReferralLevels(IntegerChoices):
    NULL = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
