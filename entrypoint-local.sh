#!/bin/sh

if [ "$DATABASE" = "postgresql" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations --no-input
python manage.py migrate --no-input

if [ "$DEBUG" == "0" ]; then
python manage.py collectstatic --no-input --clear
fi

exec "$@"