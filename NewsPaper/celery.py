import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace = 'CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_mail_every_monday_at_8am' : {
        'task': 'news.tasks.send_week_digest',
        'schedule': crontab('*/2'),
    },
}