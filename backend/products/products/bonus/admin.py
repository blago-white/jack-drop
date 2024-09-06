from django.contrib import admin

from .models import UserBonusBuyProfile, BonusBuyLevel, UsedDeposit, FreeDepositCase, BonusCase


admin.site.register(UserBonusBuyProfile)
admin.site.register(BonusBuyLevel)
admin.site.register(UsedDeposit)
admin.site.register(FreeDepositCase)
admin.site.register(BonusCase)
