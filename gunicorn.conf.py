import multiprocessing
import os

wsgi_app = "restaurants.wsgi:application"
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 120
graceful_timeout = 30
keepalive = 5

accesslog = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "gunicorn_access.log")
errorlog = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "gunicorn_error.log")
capture_output = True
loglevel = "info"

pidfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gunicorn.pid")
daemon = False

reload = False

raw_env = [
    f"DJANGO_SETTINGS_MODULE=restaurants.settings",
]

def on_starting(server):
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"), exist_ok=True)

def post_fork(server, worker):
    pass

def worker_int(worker):
    pass
