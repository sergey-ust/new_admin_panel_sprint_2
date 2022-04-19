#!/bin/sh

echo "Waiting for DB..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "DB started"


echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply DB migrations"
python manage.py migrate

echo "Starting server"
gunicorn --bind 0.0.0.0:8000 config.wsgi

exec "$@"