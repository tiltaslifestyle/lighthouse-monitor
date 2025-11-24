#!/bin/sh

# Apply database migrations
python manage.py migrate --no-input

# Collect all static files to the root directory
python manage.py collectstatic --no-input

exec "$@"