bind = "0.0.0.0:8080"  # The socket to bind
workers = 3            # Number of worker processes
timeout = 1001         # Workers silent for more than this many seconds are killed and restarted
worker_class = 'gevent' # The type of workers to use
