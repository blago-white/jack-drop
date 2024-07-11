import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'common.settings')

from django import setup

setup()

from battles.services.battle import BattleModelService


serv = BattleModelService()

print(serv.get_stats(user_id=1))
