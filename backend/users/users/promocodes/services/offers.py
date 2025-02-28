import datetime

from ..models import PersonalDepositOffer

from common.services import BaseService


class PersonalOffersService(BaseService):
    default_model = PersonalDepositOffer

    def can_receive(self, client_id: int) -> tuple[PersonalDepositOffer, bool]:
        try:
            offer: PersonalDepositOffer = self._model.objects.get(
                recipient_id=client_id
            )
        except:
            return None, False

        if (not offer.activated and
                not offer.blocked and
                (datetime.datetime.now(tz=datetime.UTC) - offer.date) <= datetime.timedelta(days=3)):
            return offer, True

        return None, False

    def activate(self, client_id: int) -> PersonalDepositOffer:
        offer: PersonalDepositOffer = self._model.objects.get(
            recipient_id=client_id,
            activated=False,
            blocked=False
        )

        if (datetime.datetime.now() - offer.date) > datetime.timedelta(days=3):
            raise ValueError()

        offer.activated = True

        offer.save()

        return offer

    def block(self, client_id: int):
        offer: PersonalDepositOffer = self._model.objects.get(
            recipient_id=client_id
        )

        offer.blocked = True

        offer.save()
