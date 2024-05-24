import multiprocessing

worker_class = 'sync' # or gthread, gevent, tornado, eventlet, etc.
bind = '0.0.0.0:8080'
timeout = '600'
workers = 2 * multiprocessing.cpu_count() + 1