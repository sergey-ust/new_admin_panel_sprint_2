#!/bin/sh

echo "Waiting for DB..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "DB started"


echo "Apply DB migrations"
python manage.py migrate


exec "$@"
