import os

from django.conf import settings

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "core.settings")

app = Celery("core")

app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks(packages=("near_cars", "service"))
