# -*- coding: utf-8 -*-
import multiprocessing

pythonpath = '/home/sof15/app'
bind = '0.0.0.0:8000'

workers = multiprocessing.cpu_count() * 2 + 1  # todo: optimize
threads = 1  # todo: optimize

user = None
loglevel = 'debug'
errorlog = '-'  # stderr