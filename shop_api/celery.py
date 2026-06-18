import os

from celery import Celery
from celery.beat import crontab
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')

app = Celery('shop_api')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.schedule = {
    "delete inactive users": {
        "task": "users.tasks.delete_inactive_users",
        "schedule": crontab(minute="*"),
    }
}
