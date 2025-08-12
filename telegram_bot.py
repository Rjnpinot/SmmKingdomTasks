# telegram_bot.py
from telegram.ext import Updater, CommandHandler
from config import TELEGRAM_BOT_TOKEN, ADMIN_TELEGRAM_ID
from task_handler import TaskHandler
from utils_session import append_log

task_handler = TaskHandler()

def start_command(update, context):
    update.message.reply_text("SMMKingdomTask Bot: ready. Use /run to fetch tasks once.")

def run_command(update, context):
    update.message.reply_text("Fetching and running tasks...")
    task_handler.run_once()
    update.message.reply_text("Run completed.")
    append_log("Tasks run via Telegram command")

def start_telegram_bot():
    if TELEGRAM_BOT_TOKEN == "PUT_YOUR_TOKEN_HERE" or not TELEGRAM_BOT_TOKEN:
        print("Please set TELEGRAM_BOT_TOKEN in config.py or environment.")
        return
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("run", run_command))
    print("Starting Telegram bot...")
    updater.start_polling()
    updater.idle()
