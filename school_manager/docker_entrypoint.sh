#!/bin/bash
export DJANGO_SETTINGS_MODULE=school_manager.settings

python manage.py makemigrations 
python manage.py migrate 
python manage.py createsuperuser --no-input
python manage.py collectstatic --no-input
gunicorn school_manager.asgi:application -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000