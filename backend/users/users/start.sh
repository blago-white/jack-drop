python manage.py collectstatic --noinput

python manage.py makemigrations
python manage.py migrate --noinput

gunicorn common.wsgi:application --bind 0.0.0.0
