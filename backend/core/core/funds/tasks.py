from celery import shared_task

from .services.convert import convert_dinamic_to_frozen


@shared_task(name="update_funds")
def update_funds():
    convert_dinamic_to_frozen()
