# -*- coding: utf-8 -*-
import multiprocessing
from os import getenv

pythonpath = '/home/sof15/app'
bind = '0.0.0.0:8080'

workers = int(getenv('GUNICORN_WORKERS', multiprocessing.cpu_count()))
threads = int(getenv('GUNICORN_THREADS', 1))

user = None
loglevel = getenv('GUNICORN_LOG_LEVEL', 'error')
errorlog = '-'  # stderr
