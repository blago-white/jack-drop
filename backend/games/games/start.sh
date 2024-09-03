python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate --noinput
daphne common.asgi:application --bind 0.0.0.0