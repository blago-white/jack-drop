# import os
#
# from celery import Celery
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'common.settings')
#
# from django import setup
#
# setup()
#
# from executor.services import config
#
# app = Celery('common')
#
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# app.autodiscover_tasks()
#
# config_service = config.ConfigModelService()
#
# app.conf.beat_schedule = {
#     'withdraw-items': {
#         'task': 'withdraw',
#         'schedule': config_service.get_interval(),
#     }
# }
