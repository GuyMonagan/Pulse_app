from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import pytz


class CustomUserManager(BaseUserManager):
    """
    Менеджер для CustomUser, где email — основной идентификатор.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен для регистрации')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Пользователь приложения.

    Аутентификация по email.
    Поддержка Telegram и часового пояса.
    """

    # Убираем поле username совсем
    username = None
    email = models.EmailField('email address', unique=True)

    # Новое поле для связи с ТГ по никнейму
    telegram_username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    telegram_chat_id = models.CharField(max_length=255, blank=True, null=True)
    timezone = models.CharField(
        max_length=50,
        choices=[(tz, tz) for tz in pytz.common_timezones],
        default='Europe/Moscow'
    )

    # 3. Указываем, что теперь email — это логин
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
