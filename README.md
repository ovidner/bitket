SOF15
=====

## Dumping data to JSON
    manage.py dumpdata -n -e contenttypes -e auth.permission -e sessions > data.json
    manage.py dumpdata --natural-foreign -e contenttypes -e auth.permission > data.YYYY-MM-DD.json
