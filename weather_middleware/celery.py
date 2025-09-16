import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_middleware.settings')

app = Celery('weather_middleware')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "push-message-to-portal-every-5-minutes": {
        "task": "api.tasks.push_message_to_portal",
        "schedule": crontab(minute="0", hour="0"),  # every 5 minutes
    }
}