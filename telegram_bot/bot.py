import logging
import os
import sys

import django
import httpx
from asgiref.sync import sync_to_async
from decouple import config
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1. Сначала настраиваем пути и окружение
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    config('DJANGO_SETTINGS_MODULE')
)

# 2. Инициализируем Django
django.setup()

# 3. Импорты моделей ТОЛЬКО после django.setup()
# Чтобы Flake8 не ругался на E402 (импорт не в начале файла),
# мы используем локальный импорт внутри функций.
# Это официально разрешенный костыль для скриптов инициализации.

logging.basicConfig(level=logging.INFO)
TOKEN = config('TELEGRAM_TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает команду /start в Telegram."""
    # Локальный импорт модели внутри функции
    from users.models import CustomUser

    user = update.effective_user
    telegram_id = user.id

    try:
        custom_user = await sync_to_async(CustomUser.objects.get)(
            username=str(user.username)
        )
        custom_user.telegram_chat_id = str(telegram_id)
        await sync_to_async(custom_user.save)()
        await update.message.reply_text("✅ Chat ID привязан к вашему аккаунту!")
    except CustomUser.DoesNotExist:
        await update.message.reply_text("❌ Пользователь не найден в системе.")


def send_telegram_message(chat_id, text):
    """Отправляет сообщение пользователю в Telegram."""
    url = f"https://api.telegram.org{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    httpx.post(url, data=payload)


def run_bot():
    """Запускает Telegram-бота."""
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == "__main__":
    run_bot()
