# 引入gevent
from gevent import monkey
monkey.patch_all()

import multiprocessing

debug = True
loglevel = 'debug'
bind = 'localhost:5000'
pidfile = 'log/gunicorn.pid'
logfile = 'log/debug.log'

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'