from ..models import PersonalDepositOffer

from common.services import BaseService


class PersonalOffersService(BaseService):
    default_model = PersonalDepositOffer

    def can_receive(self, client_id: int) -> bool:
        try:
            offer: PersonalDepositOffer = self._model.objects.get(
                recipient_id=client_id
            )
        except:
            return False

        if not offer.activated and not offer.blocked:
            return True

        return False

    def activate(self, client_id: int) -> PersonalDepositOffer:
        offer: PersonalDepositOffer = self._model.objects.get(
            recipient_id=client_id,
            activated=False,
            blocked=False
        )

        offer.activated = True

        offer.save()

        return offer

    def block(self, client_id: int):
        offer: PersonalDepositOffer = self._model.objects.get(
            recipient_id=client_id
        )

        offer.blocked = True

        offer.save()
