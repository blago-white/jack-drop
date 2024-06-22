python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate
daphne common.asgi:application --bind 0.0.0.0 && celery -A common worker -l info