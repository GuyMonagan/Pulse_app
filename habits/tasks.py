from celery import shared_task
import time

@shared_task
def remind_user(username):
    time.sleep(2)  # симулируем задержку
    print(f"🔔 Напоминание для пользователя {username} отправлено.")
    return f"Ping {username}"
