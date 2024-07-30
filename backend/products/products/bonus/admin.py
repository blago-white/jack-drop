from django.contrib import admin

from .models import UserBonusBuyProfile, BonusBuyLevel, UsedDeposit, FreeCase, CaseDiscount


admin.site.register(UserBonusBuyProfile)
admin.site.register(BonusBuyLevel)
admin.site.register(UsedDeposit)
admin.site.register(FreeCase)
admin.site.register(CaseDiscount)
