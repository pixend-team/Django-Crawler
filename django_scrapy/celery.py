import os
from celery import Celery
from django.conf import settings

# Ensure the settings module is set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_scrapy.settings')

# Create the Celery application
app = Celery('django_scrapy')

# Load settings from the Django settings file
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from installed apps
app.autodiscover_tasks(settings.INSTALLED_APPS)

# Optional: You can add a basic task for testing
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
