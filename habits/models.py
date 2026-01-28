from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Habit(models.Model):
    """
    Модель привычки пользователя.

    Описывает действие, которое пользователь должен выполнять регулярно,
    с возможностью напоминаний, награды или связанной приятной привычки.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_reminder_enabled = models.BooleanField(
        default=False,
        help_text="Включить напоминание через Telegram"
    )
    next_reminder = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Следующее напоминание (UTC)"
    )

    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_pleasant': True},
        related_name='rewarded_habits'
    )
    periodicity = models.PositiveIntegerField(default=1)  # в днях
    reward = models.CharField(max_length=255, blank=True, null=True)
    duration = models.PositiveIntegerField(help_text='время в секундах')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Валидирует бизнес-правила привычки.

        Ограничения:
        - нельзя одновременно указывать награду и связанную привычку
        - приятная привычка не может иметь награду или связанную привычку
        - длительность выполнения не более 120 секунд
        - периодичность не реже одного раза в 7 дней
        """
        # Нельзя одновременно указывать и награду, и связанную привычку
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя одновременно указывать награду и связанную привычку.")

        # Приятная привычка не может иметь ни награду, ни связанную привычку
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("Приятная привычка не может иметь награду или связанную привычку.")

        # Время выполнения не больше 120 секунд
        if self.duration > 120:
            raise ValidationError("Время выполнения привычки не должно превышать 120 секунд.")

        # Периодичность — не реже, чем 1 раз в 7 дней
        if self.periodicity > 7:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")

    def __str__(self):
        """
        Читаемое представление привычки.
        """
        return f"{self.action} в {self.time} @ {self.place}"
