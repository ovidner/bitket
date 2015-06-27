SOF15
=====

## Set the environment in development mode
    touch dev.env

The existence of the dev.env file will tell the application to set certain sane
defaults for development.

## Dumping data to JSON
    manage.py dumpdata -n -e contenttypes -e auth.permission -e sessions > data.json
    manage.py dumpdata --natural-foreign -e contenttypes -e auth.permission > data.YYYY-MM-DD.json
