from django.contrib.auth.models import AbstractUser
from django.db import models
import pytz


class CustomUser(AbstractUser):
    """
    Пользователь приложения.

    Расширяет стандартного пользователя Django
    поддержкой Telegram и часового пояса.
    """
    telegram_chat_id = models.CharField(max_length=255, blank=True, null=True)

    timezone = models.CharField(
        max_length=50,
        choices=[(tz, tz) for tz in pytz.common_timezones],
        default='Europe/Moscow'
    )

    def __str__(self):
        """
        Возвращает имя пользователя.
        """
        return self.username
