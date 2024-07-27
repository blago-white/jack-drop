from django.contrib import admin

from .models import UserBonusBuyProfile, BonusBuyLevel, UsedDeposit, FreeCase


admin.site.register(UserBonusBuyProfile)
admin.site.register(BonusBuyLevel)
admin.site.register(UsedDeposit)
admin.site.register(FreeCase)
