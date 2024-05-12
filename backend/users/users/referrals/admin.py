from django.contrib import admin

from .models.referral import ReferralBenefit, Referral


@admin.register(ReferralBenefit)
class ReferralBenefitAdmin(admin.ModelAdmin):
    pass


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    pass
