import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'common.settings')

from django import setup

setup()


from funds.services.dinamic import DinamicFundsService


s = DinamicFundsService()

print(s.update(delta_funds=1200))
