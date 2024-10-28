import aiohttp

from celery import shared_task


@shared_task
async def withdraw_service_balance():
    async with aiohttp.ClientSession() as session:
        async with session.post()
