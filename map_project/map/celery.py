import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "map.settings")

app = Celery("map")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check_event_status_every_min": {
        "task": "map_apps.events.tasks.check_status_events",
        "schedule": crontab(minute="*/1"),
    },
    "get_top_users": {
        "task": "map_apps.users.tasks.get_top_users",
        "schedule": crontab(hour="*/1"),
    },
}
