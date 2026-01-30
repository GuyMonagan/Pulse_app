from django.contrib.auth.models import AbstractUser
from django.db import models
import pytz


class CustomUser(AbstractUser):
    """
    Пользователь приложения.

    Аутентификация по email.
    Поддержка Telegram и часового пояса.
    """

    username = None  # отключаем username

    email = models.EmailField(
        unique=True,
        verbose_name="Email"
    )

    telegram_chat_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    timezone = models.CharField(
        max_length=50,
        choices=[(tz, tz) for tz in pytz.common_timezones],
        default="Europe/Moscow"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
