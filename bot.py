import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Get Bot Token ---
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ TELEGRAM_BOT_TOKEN environment variable not found!")
    exit(1)

# --- Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Flask server for health check ---
app = Flask(__name__)
@app.route('/')
def index():
    return "Bot is alive!"
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# --- Telegram Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(f"Hi {user.first_name}, I'm your echo bot!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

def main():
    threading.Thread(target=run_flask).start()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    logger.info("🤖 Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()