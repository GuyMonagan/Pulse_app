from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)

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

    def clean(self):
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
        return f"{self.action} в {self.time} @ {self.place}"
