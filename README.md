# Pulse App — Трекер привычек с Telegram-ботом и напоминаниями

## 📋 Описание

Сервис позволяет создавать, отслеживать и управлять привычками.  
Интеграция с Telegram используется для отправки напоминаний пользователям.  
Фоновая логика реализована через Celery + Redis.

---

## 🚀 Стек технологий

- Python 3.11
- Django / DRF
- PostgreSQL
- Celery + Redis
- Telegram Bot API
- DRF SimpleJWT (аутентификация)
- Pytest / Coverage
- Poetry (управление зависимостями)
- drf-yasg (автогенерация Swagger-документации)

---

## ⚙️ Установка и запуск

### 1. Клонируем проект

```
git clone https://github.com/your-username/pulse_app.git
cd pulse_app
```

### 2. Установка зависимостей

```
poetry install
```

### 3. Переменные окружения

Создайте файл .env или используйте .env.example:

```commandline
SECRET_KEY=django-insecure-here_goes_some_dumb_but_long_key
DB_NAME=pulse_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
TELEGRAM_TOKEN=put_your_token_here_later
ALLOWED_HOSTS=127.0.0.1,localhost

#заменить на 'pulse_app.settings.prod' на проде
DJANGO_SETTINGS_MODULE=pulse_app.settings.dev

# Указать домены, разрешённые для CORS (frontend-домены)
CORS_ALLOWED_ORIGINS=https://frontend.example.com

# Доверенные домены для CSRF (обычно те же самые)
CSRF_TRUSTED_ORIGINS=https://frontend.example.com

```
---
## 💽 Миграции и суперюзер

```
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
```
---
## 🐍 Запуск

Django сервер

```
poetry run python manage.py runserver --settings=pulse_app.settings.dev
```

Telegram-бот

```
poetry run python telegram_bot/bot.py
```

Celery + Beat

- Запуск воркера
```
poetry run celery -A pulse_app worker -l info
```
- Запуск планировщика задач
```
poetry run celery -A pulse_app beat -l info
```
---
## ✅ Покрытие тестами

```
poetry run coverage run manage.py test
```

Покрытие: 93%
Проверены модели, сериализаторы, API, Celery-таски
---

## 🐾 Основной функционал

🔐 JWT авторизация

🧑‍💼 Привязка Telegram-чата

🕑 Напоминания через Celery + Telegram

📃 Валидация привычек по правилам (вознаграждения, периодичность и т.д.)

🌐 Публичные и приватные привычки

📑 Пагинация

✅ Покрытие тестами

---


