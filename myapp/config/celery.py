import os
import sys

import environ
from celery import Celery

env = environ.Env()

BASE_DIR = environ.Path(__file__) - 3
sys.path.append(f"{BASE_DIR}/myapp")

env_file = f"{BASE_DIR}/.env"

if os.path.isfile(env_file):
    environ.Env.read_env(env_file)

app = Celery("myapp")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
