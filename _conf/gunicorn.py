# -*- coding: utf-8 -*-
import multiprocessing
import os

pythonpath = '/home/sof15/app'
bind = '0.0.0.0:8080'

workers = multiprocessing.cpu_count() * 2 + 1  # todo: optimize
threads = 1  # todo: optimize

user = None
loglevel = 'debug'
errorlog = '-'  # stderr

debug = os.getenv('DEBUG', False)
