from multiprocessing import cpu_count

# Socket Path
bind = 'unix:/home/julpiguet/CloudSys/testapp/backend/python/gunicorn.sock'

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/julpiguet/CloudSys/testapp/backend/python/access_log'
errorlog =  '/home/julpiguet/CloudSys/testapp/backend/python/error_log'