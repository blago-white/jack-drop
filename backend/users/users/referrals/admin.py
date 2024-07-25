from django.contrib import admin

from .models.referral import Referral


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    pass
