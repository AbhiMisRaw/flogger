#!/bin/sh

# If any command fails, the whole script stops
set -e


# New: Wait for Postgres to be ready
echo "Waiting for postgres..."
echo "PostgreSQL started"

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# This tells the script to run whatever was passed as the CMD (Gunicorn/Runserver)
exec "$@"