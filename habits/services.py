import pytz
from datetime import timedelta
from django.utils import timezone


def calculate_next_reminder(habit):
    """
    Рассчитывает дату и время следующего напоминания в UTC.

    Логика:
    - берёт текущее или последнее напоминание как точку отсчёта
    - учитывает часовой пояс пользователя
    - подставляет время привычки
    - сдвигает дату с учётом периодичности
    """

    user_tz = pytz.timezone(habit.user.timezone)
    now_utc = timezone.now()

    # Берём точку отсчёта
    if habit.next_reminder:
        base_utc = habit.next_reminder
    else:
        base_utc = habit.created_at or now_utc

    # Переводим в локальное время пользователя
    base_local = base_utc.astimezone(user_tz)

    # Собираем локальный datetime с временем привычки
    candidate_local = base_local.replace(
        hour=habit.time.hour,
        minute=habit.time.minute,
        second=0,
        microsecond=0
    )

    # Если время уже прошло — двигаем вперёд
    if candidate_local <= base_local:
        candidate_local += timedelta(days=habit.periodicity)

    # Возвращаем в UTC для хранения
    return candidate_local.astimezone(pytz.UTC)
