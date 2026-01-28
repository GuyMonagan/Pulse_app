from celery import shared_task
from django.utils.timezone import now
from habits.models import Habit
from habits.services import calculate_next_reminder
from telegram_bot.bot import send_telegram_message
import logging

logger = logging.getLogger(__name__)


@shared_task
def check_and_send_reminders():
    """
    Проверяет привычки с активными напоминаниями и отправляет уведомления.

    Алгоритм:
    - находит привычки, для которых пришло время напоминания
    - отправляет сообщение в Telegram
    - рассчитывает и сохраняет следующее напоминание
    """
    sent = 0

    habits = Habit.objects.filter(
        is_reminder_enabled=True,
        next_reminder__lte=now()
    )

    for habit in habits:
        user = habit.user

        if not user.telegram_chat_id:
            continue

        send_telegram_message(
            user.telegram_chat_id,
            f"🔔 Пора: {habit.action} в {habit.place}!"
        )

        # планируем следующее
        habit.next_reminder = calculate_next_reminder(habit)
        habit.save(update_fields=['next_reminder'])

        sent += 1
        logger.info(f"Напоминание отправлено: {habit.id}")

    return f"Отправлено напоминаний: {sent}"
