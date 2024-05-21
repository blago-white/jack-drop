import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'common.settings')

from django import setup

setup()

from cases.serializers import DropCaseRequestSerializer


ser = DropCaseRequestSerializer(data={
    "case_id": 1,
    "items": [
        {"id": 1,
         "rate": 30,
         "price": 10},
        {"id": 2,
         "rate": 10,
         "price": 90},
        {"id": 3,
         "rate": 50,
         "price": 30}
    ],
    "funds": {
        "user_advantage": 100,
        "site_active_funds_per_hour": 1340,
    },
    "price": 150
})

ser.is_valid()

print(ser.errors)

print(ser.validated_data)
