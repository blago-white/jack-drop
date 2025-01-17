import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'common.settings')

from django import setup

setup()

app = Celery('common')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'inflate-advantage': {
        'task': 'inflate_advantage',
        'schedule': 60*60,
    }
}
