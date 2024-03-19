#!/bin/sh

# Collect static files into location shared by nginx
echo "Running collectstatic..."
python manage.py collectstatic --noinput

# Create any new DB migrations and apply those in version control.
# Note that running this script for the very first time produces
# Django warnings such as for both makemigrations and migrate:
#
#   makemigrations.py:105: RuntimeWarning: Got an error checking a consistent migration history performed for database connection 'default': connection to server at "postgres" (192.168.128.2), port 5432 failed: Connection refused
#   Is the server running on that host and accepting TCP/IP connections?
#
# This is expected as the app has not been initialized yet so the DB does not
# exist.
echo "Running makemigrations..."
python manage.py makemigrations --noinput
echo "Running migrate..."
python manage.py migrate --noinput

# If running in DEBUG mode add debug logging to gunicorn
if [ -n "${DEBUG}" ]; then
  DEBUG_ARGS="--log-level debug --capture-output"
else
  DEBUG_ARGS=
fi

# Start
gunicorn wsgi:application -w 1 -k "gevent" --max-requests 1000 --max-requests-jitter 100 --timeout 600 --graceful-timeout 600 ${DEBUG_ARGS} -b :8000
