python manage.py collectstatic

python manage.py makemigrations --noinput

python manage.py migrate

gunicorn common.wsgi:application --bind 0.0.0.0 && celery -A common worker -l info
