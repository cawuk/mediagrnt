import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 5536891599

FIRST_MESSAGE = """I'm a Telegram bot for verification by Grnt Media! ✅
My job is to confirm that you're a real Telegram user.
I will connect with you in the future.

Website: grnt.media
Telegram: @gruntmedia
YouTube: youtube.com/@grntmedia
Twitter: twitter.com/grntmedia 🌱

If you have any questions, feel free to contact the tech admin: @megrunt"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    # Відправляємо користувачу перше повідомлення
    await update.message.reply_text(FIRST_MESSAGE)
    # Сповіщаємо адміна про нового користувача
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"New user started bot: {user.full_name} ({user_id})")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This bot is for user verification by Grnt Media!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.message.from_user.id
    # Відправляємо адміну текст від користувача
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"User {user_id} wrote: {user_text}")
    # Відповідаємо користувачу
    await update.message.reply_text(f"You wrote: {user_text}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("info", info))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()
