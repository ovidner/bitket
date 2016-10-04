from __future__ import absolute_import, unicode_literals
from multiprocessing import cpu_count

from environ import Env

env = Env()

bind = ['0.0.0.0:{}'.format(env('GUNICORN_PORT'))]

reload = env.bool('GUNICORN_RELOAD', False)
workers = env.int('GUNICORN_WORKERS', cpu_count()*2+1)

loglevel = env.str('GUNICORN_LOG_LEVEL', 'error')
errorlog = '-'  # stderr
accesslog = '-' if env.bool('GUNICORN_ACCESS_LOG', False) else None
