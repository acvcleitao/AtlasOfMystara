# gunicorn_config.py
import multiprocessing
import os

# "0.0.0.0" makes the server accessible from any network interface, allowing external access.
# "127.0.0.1" limits access to the localhost.
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")
# Dynamically adjust the number of workers
# maximize concurrency without overwhelming the system
workers = multiprocessing.cpu_count() * 2 + 1
# LOG_LEVEL:
# "debug": Maximum detail, useful for debugging
# "info": Standard level, provides important information about the application.
# "warning": Highlights potential issues.
# "error": Logs only errors.
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
