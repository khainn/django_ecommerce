import multiprocessing

# Gunicorn configuration file
bind = "0.0.0.0:8000"
worker_class = "gevent"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 1  # Since we're using gevent, we set threads to 1
worker_connections = 1000
timeout = 300
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# SSL (if needed)
# keyfile = "path/to/keyfile"
# certfile = "path/to/certfile"

# Process naming
proc_name = "django_ecommerce"

# Preload app for better performance
preload_app = True

def post_fork(server, worker):
    """
    Called just after a worker has been forked.
    """
    from gevent import monkey
    monkey.patch_all()

def when_ready(server):
    """
    Called just before the master process is initialized.
    """
    pass 