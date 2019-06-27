from __future__ import absolute_import, unicode_literals

# from .celery_app import Celery
from celery import Celery

import os

# set the default Django settings module for the 'celery' program.
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'universal.settings.develop')

app = Celery('universal')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()