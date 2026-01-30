from rest_framework.test import APITestCase
from users.models import CustomUser
from unittest.mock import patch
from habits.tasks import check_and_send_reminders
from habits.models import Habit
from django.utils import timezone


class CeleryTaskTest(APITestCase):
    """
    Тест логики отправки напоминаний Celery-задачей.
    """
    def test_reminder_logic(self):
        """Проверяет отправку напоминания и пересчёт следующего времени."""
        user = CustomUser.objects.create(email='bot_user@test.com', telegram_chat_id='12345')
        habit = Habit.objects.create(
            user=user, action="Test Task", place="Lab",
            time=timezone.now().time(),
            is_reminder_enabled=True,
            next_reminder=timezone.now() - timezone.timedelta(minutes=1),  # Время уже прошло
            duration=60
        )

        # "Подсматриваем" за функцией отправки сообщения
        with patch('habits.tasks.send_telegram_message') as mocked_send:
            check_and_send_reminders()
            # Проверяем: вызывалась ли функция отправки?
            self.assertTrue(mocked_send.called)
            # Проверяем: обновилось ли время на следующее?
            habit.refresh_from_db()
            self.assertGreater(habit.next_reminder, timezone.now())
