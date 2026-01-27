import logging
import os
import sys
import django
from decouple import config

# 1. Добавляем КОРЕНЬ ПРОЕКТА (там где manage.py)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

# 2. Указываем Django settings
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    config('DJANGO_SETTINGS_MODULE')
)

# 3. Инициализируем Django ОДИН РАЗ
django.setup()

# 4. ТОЛЬКО ПОСЛЕ ЭТОГО — любые Django-импорты
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from users.models import CustomUser
import httpx

logging.basicConfig(level=logging.INFO)

TOKEN = config('TELEGRAM_TOKEN')

from asgiref.sync import sync_to_async

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    telegram_id = user.id

    try:
        custom_user = await sync_to_async(CustomUser.objects.get)(username=str(user.username))
        custom_user.telegram_chat_id = str(telegram_id)
        await sync_to_async(custom_user.save)()
        await update.message.reply_text("✅ Chat ID привязан к вашему аккаунту!")
    except CustomUser.DoesNotExist:
        await update.message.reply_text("❌ Пользователь с таким username не найден в системе.")


def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == "__main__":
    run_bot()

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    httpx.post(url, data=payload)
