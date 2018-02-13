#!/bin/sh

# Initialize the database layers
python manage.py collectstatic --noinput
chmod 755 -R /usr/src/app/static
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# If running in DEBUG mode add debug logging to gunicorn
if [ -n "${DEBUG}" ]; then
  DEBUG_ARGS="--log-level debug --capture-output"
else
  DEBUG_ARGS=
fi

# Start
gunicorn wsgi:application -w 4 -k "gevent" --max-requests 1000 --max-requests-jitter 100 --timeout 600 --graceful-timeout 600 ${DEBUG_ARGS} -b :8000
