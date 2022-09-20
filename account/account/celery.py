import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'account.settings')

app = Celery('account')
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.config_from_object(settings, namespace='CELERY')

# app.conf.beat_schedule = {
#     'send-mail-specified-time': {
#         'task': 'user.task.send_email_task',
#         'schedule': crontab(minute='*/1'),
#         'args': (['userid'], ['to'], ['username']),
#     },
# }

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
