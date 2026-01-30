import logging
import os
import sys

import django
import httpx
from asgiref.sync import sync_to_async
from decouple import config
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

"""
Telegram-бот для интеграции с Django-приложением.

Бот предназначен для:
- привязки Telegram-пользователя к аккаунту в Django
- отправки сообщений пользователям Telegram
- работы как отдельный процесс вне Django runserver

Инициализация Django производится вручную, так как бот
запускается как standalone-скрипт.
"""
# 1. Настройка путей и окружения для доступа к Django-проекту
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    config('DJANGO_SETTINGS_MODULE')
)

# 2. Инициализируем Django
django.setup()

# 3. Импорты моделей ТОЛЬКО после django.setup()
logging.basicConfig(level=logging.INFO)
TOKEN = config('TELEGRAM_TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start.

    Назначение:
    - связывает Telegram-аккаунт пользователя с учетной записью в Django
    - сохраняет telegram_chat_id в модели CustomUser

    Алгоритм работы:
    1. Получает Telegram user ID
    2. Пытается найти пользователя в Django
    3. Сохраняет chat_id в профиле пользователя
    4. Отправляет пользователю результат операции

    Использует sync_to_async для корректной работы с Django ORM
    в асинхронном окружении.
    """
    # Локальный импорт модели внутри функции
    from users.models import CustomUser

    user = update.effective_user
    telegram_id = user.id
    tg_nick = user.username  # Никнейм пользователя в ТГ

    if not tg_nick:
        await update.message.reply_text("❌ У вас не установлен Username в настройках Telegram.")
        return

    try:
        # Ищем по новому полю telegram_username
        custom_user = await sync_to_async(CustomUser.objects.get)(
            telegram_username=str(tg_nick)
        )
        custom_user.telegram_chat_id = str(telegram_id)
        await sync_to_async(custom_user.save)()
        await update.message.reply_text(f"✅ Аккаунт {custom_user.email} привязан!")
    except CustomUser.DoesNotExist:
        await update.message.reply_text(
            f"❌ Пользователь с ником @{tg_nick} не найден.\n"
            f"Убедитесь, что вы указали этот ник в профиле на сайте."
        )


def send_telegram_message(chat_id, text):
    """
    Отправляет сообщение пользователю Telegram через HTTP API.

    Используется для:
    - фоновых уведомлений
    - интеграции с Celery или Django задачами
    - отправки сообщений вне контекста Telegram handlers

    :param chat_id: Telegram chat ID получателя
    :param text: Текст сообщения
    """
    url = f"https://api.telegram.org{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    httpx.post(url, data=payload)


def run_bot():
    """
    Точка входа для запуска Telegram-бота.

    Функция:
    - создает приложение python-telegram-bot
    - регистрирует обработчики команд
    - запускает polling

    Должна вызываться как отдельный процесс
    (не внутри Django runserver).
    """
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == "__main__":
    run_bot()
