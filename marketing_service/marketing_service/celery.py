from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketing_service.settings')
app = Celery('marketing_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
