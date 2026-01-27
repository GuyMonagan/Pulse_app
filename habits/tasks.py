from celery import shared_task
from datetime import datetime
from django.utils.timezone import now
from .models import Habit
from telegram_bot.bot import send_telegram_message
import logging

logger = logging.getLogger(__name__)

@shared_task
def check_and_send_reminders():
    now_time = now().time()
    today = now().date()
    sent = 0

    for habit in Habit.objects.filter(is_reminder_enabled=True):
        if not habit.created_at:
            continue

        # Проверка дня по периодичности
        days_since_start = (today - habit.created_at.date()).days
        if days_since_start % habit.periodicity != 0:
            continue

        # Проверка времени
        if now_time.hour != habit.time.hour or now_time.minute != habit.time.minute:
            continue

        # Проверка наличия чата
        if not habit.user.telegram_chat_id:
            continue

        message = f"🔔 Пора: {habit.action} в {habit.place}!"
        send_telegram_message(habit.user.telegram_chat_id, message)
        sent += 1
        logger.info(f"Напоминание отправлено пользователю {habit.user.username}")

    return f"✅ Отправлено напоминаний: {sent} | {now()}"
