#!/bin/bash
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Checking for superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'muthupandi.velmurugan@outlook.com', 'cre@v0@dm!n')
END

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn myapp.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
