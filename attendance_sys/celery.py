import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_sys.settings')

app = Celery('attendance_sys')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.update(timezone = 'Asia/Kolkata')


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# celery beat
app.conf.beat_schedule = {
        'AutoCheckOut': {
            'task': 'att_sys.tasks.auto_checkout',
            'schedule': crontab(minute="0", hour="0", day_of_week="mon-fri"),
            # 'schedule':crontab(minute='*/1'),
        },

        'AutoReload': {
            'task': 'att_sys.tasks.auto_reload',
            'schedule': crontab ()

        },
        'ReloadAutoChout': {
            'task': 'att_sys.tasks.reload_autochout',
            'schedule':crontab(0, 0, day_of_month='1'),
            # 'schedule': crontab (minute = '*/5'),

        }, 

}
