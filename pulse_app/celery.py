import os
from celery import Celery
from decouple import config

# Указываем Django, какие настройки использовать
os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('DJANGO_SETTINGS_MODULE'))

# Создаём объект Celery
app = Celery('pulse_app')

# Говорим Celery, где искать конфиг — в Django settings по префиксу CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находит таски во всех установленных приложениях
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'🧪 Celery работает. Задача ID: {self.request.id}')
