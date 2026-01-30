from django.test import TestCase
from datetime import time
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from habits.models import Habit

User = get_user_model()


class HabitValidationTest(TestCase):
    """
    Тесты бизнес-валидации модели Habit.
    """
    def setUp(self):
        """Создаёт пользователя и приятную привычку."""
        self.user = User.objects.create(email="testuser@test.com", timezone="Europe/Moscow")
        self.pleasant_habit = Habit.objects.create(
            user=self.user, action="Read book", place="Sofa", time=time(9, 0),
            duration=60, is_pleasant=True
        )

    # Тест 1: Нельзя одновременно награда + связанная привычка
    def test_reward_and_related_habit_validation(self):
        habit = Habit(
            user=self.user, action="Run", place="Park", time=time(7, 0), duration=60,
            reward="Candy",
            related_habit=self.pleasant_habit  # Оба поля заполнены
        )
        with self.assertRaises(ValidationError):
            habit.clean()  # Django должен выбросить ошибку

    # Тест 2: Длительность не больше 120 секунд
    def test_duration_validation(self):
        habit = Habit(
            user=self.user, action="Meditate", place="Home", time=time(8, 0),
            duration=150  # Слишком долго
        )
        with self.assertRaisesMessage(ValidationError, "Время выполнения привычки не должно превышать 120 секунд."):
            habit.clean()

    # Тест 3: Периодичность не реже, чем раз в 7 дней
    def test_periodicity_validation(self):
        habit = Habit(
            user=self.user, action="Walk", place="Street", time=time(17, 0),
            duration=60, periodicity=10  # Слишком редко
        )
        with self.assertRaisesMessage(ValidationError, "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."):
            habit.clean()

    # Тест 4: У приятной привычки нет награды/связанной привычки
    def test_pleasant_habit_no_rewards(self):
        habit = Habit(
            user=self.user, action="Sleep", place="Bed", time=time(23, 0),
            duration=120, is_pleasant=True, reward="Money"  # Приятная + награда
        )
        with self.assertRaisesMessage(
                ValidationError,
                "Приятная привычка не может иметь награду"
        ):
            habit.clean()
