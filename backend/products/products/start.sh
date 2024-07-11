python manage.py collectstatic --no-input
python manage.py makemigrations --noinput
python manage.py migrate
daphne common.asgi:application --bind 0.0.0.0