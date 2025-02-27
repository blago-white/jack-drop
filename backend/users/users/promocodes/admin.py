from django.contrib import admin

from .models import Promocode, PersonalDepositOffer


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ["code", "discount", "for_personal_offers"]


@admin.register(PersonalDepositOffer)
class PersonalDepositOfferAdmin(admin.ModelAdmin):
    list_display = ["recipient", "activated", "blocked"]
