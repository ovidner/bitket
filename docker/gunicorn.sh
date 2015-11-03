#!/bin/sh
django-admin collectstatic --noinput
gunicorn config.wsgi -c /app/config/gunicorn.py
