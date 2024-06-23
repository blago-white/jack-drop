import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'common.settings')

from django import setup

setup()

from fortune.services.fortune import FortuneWheelService
from fortune.services.transfer import (FortuneWheelGameRequest, FundsState,
                                       FortuneWheelCaseData,
                                       CaseData, CaseItem)

serv = FortuneWheelService()

res = serv.get_win_item(request=FortuneWheelGameRequest(
    funds_state=FundsState(usr_advantage=100, site_active_funds=1000),
    winning_type="4",
    data=FortuneWheelCaseData(
        items=[
            CaseData(id=1,
                     items=[
                         CaseItem(id=1, rate=1, price=100),
                         CaseItem(id=2, rate=1, price=125),
                         CaseItem(id=3, rate=1, price=150),
                         CaseItem(id=4, rate=1, price=177),
                         CaseItem(id=5, rate=1, price=199),
                         CaseItem(id=6, rate=1, price=400),
                         CaseItem(id=7, rate=1, price=300)
                     ],
                     price=199),
            CaseData(id=2,
                     items=[
                         CaseItem(id=1, rate=1, price=115),
                         CaseItem(id=2, rate=1, price=115),
                         CaseItem(id=3, rate=1, price=130),
                         CaseItem(id=4, rate=1, price=150),
                         CaseItem(id=5, rate=1, price=160),
                         CaseItem(id=6, rate=1, price=200),
                         CaseItem(id=7, rate=1, price=300)
                     ],
                     price=155),
            CaseData(id=3,
                     items=[
                         CaseItem(id=1, rate=1, price=100),
                         CaseItem(id=2, rate=1, price=115),
                         CaseItem(id=3, rate=1, price=130),
                         CaseItem(id=4, rate=1, price=150),
                         CaseItem(id=5, rate=1, price=200),
                         CaseItem(id=6, rate=1, price=290),
                         CaseItem(id=7, rate=1, price=300),
                         CaseItem(id=8, rate=1, price=350),
                         CaseItem(id=9, rate=1, price=500)
                     ],
                     price=290)
        ]
    )
))

print(res)
