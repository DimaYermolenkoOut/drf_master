release: python manage.py migrate
web: gunicorn drfmaster.wsgi:application --bind 0.0.0.0:$PORT