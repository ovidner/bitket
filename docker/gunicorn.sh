#!/bin/sh
django-admin collectstatic --noinput
newrelic-admin run-program gunicorn config.wsgi -c /app/config/gunicorn.py
