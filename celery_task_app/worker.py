import os
from celery import Celery

BROKER_URI = 'redis://localhost:6379'
BACKEND_URI = 'redis'

app = Celery(
    'celery_app',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['celery_task_app.tasks']
)
