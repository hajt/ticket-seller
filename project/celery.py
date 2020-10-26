from __future__ import absolute_import, unicode_literals

import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'every-15-seconds': {
        'task': 'api.tasks.release_expired_reservations',
        'schedule': 15
    }
}

app.conf.timezone = 'UTC'

app.autodiscover_tasks()