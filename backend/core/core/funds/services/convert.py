from .frozen import FrozenFundsService
from .percent import FreezeFundsPercent
from .dinamic import DinamicFundsService


def convert_dinamic_to_frozen(
        frozen_funds_service: FrozenFundsService = FrozenFundsService(),
        percent_funds_service: FreezeFundsPercent = FreezeFundsPercent(),
        dinamic_funds_service: DinamicFundsService = DinamicFundsService()
) -> None:
    if (dinamic_funds := dinamic_funds_service.get()) <= 1:
        return False

    frozen_funds = int(dinamic_funds * (percent_funds_service.get()/100))

    if not dinamic_funds_service.update(delta_funds=-frozen_funds):
        return False

    frozen_funds_service.update(delta_funds=frozen_funds)

    return True
