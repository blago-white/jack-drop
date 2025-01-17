from celery import shared_task

from accounts.services.users import UsersService
from accounts.models.client import Client


@shared_task(name="inflate_advantage")
def inflate_advantage():
    users_service = UsersService()

    users_service.bulk_inflate_advantages()
