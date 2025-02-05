from celery import shared_task

from .services.convert import convert_dinamic_to_frozen
from .services.cases import CasesProfitService


@shared_task(name="update_funds")
def update_funds():
    convert_dinamic_to_frozen()


@shared_task(name="drop_cases_funds")
def drop_cases_funds():
    print("START CASES FUNDS DROPPING")
    CasesProfitService().drop_profit()
