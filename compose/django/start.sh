#!/bin/bash
function manage_app () {
    python manage.py migrate
    python manage.py collectstatic --no-input
}

function start_development() {
    # use django runserver as development server here.
    manage_app
    python manage.py runserver 0.0.0.0:8000
}

function start_production() {
    # use gunicorn for production server here
    manage_app
    gunicorn config.wsgi -w 4 -b 0.0.0.0:8000 --chdir=/app --log-file -
}

if [ "$DEBUG" = "True" ]
then
    # use development server
    start_development
else
    # use production server
    start_production
fi