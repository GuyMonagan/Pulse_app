from django.test import TestCase
from datetime import time
from habits.services import calculate_next_reminder
from django.contrib.auth import get_user_model
import pytz
from habits.models import Habit

User = get_user_model()


class HabitTimeZoneTest(TestCase):
    """
    Тесты корректного расчёта напоминаний
    с учётом часового пояса пользователя.
    """
    def setUp(self):
        """Создаёт пользователя с часовым поясом Asia/Tashkent."""
        self.user = User.objects.create(
            email="test@example.com",
            timezone="Asia/Tashkent"
        )

    def test_calculate_next_reminder_tashkent(self):
        # Создаем привычку на 10:00 утра
        habit = Habit.objects.create(
            user=self.user,
            action="Drink water",
            place="Kitchen",
            time=time(10, 0),  # 10:00 утра по местному времени
            is_reminder_enabled=True,
            duration=60
        )

        # Считаем напоминание
        reminder = calculate_next_reminder(habit)

        # 10:00 в Ташкенте (UTC+5) должно быть 05:00 в UTC
        self.assertEqual(reminder.hour, 5)
        self.assertEqual(reminder.tzinfo, pytz.UTC)
