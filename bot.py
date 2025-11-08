import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

ADMIN_ID = 5536891599
BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I'm a Telegram bot for verification by Grnt Media! ✅\n"
        "I will connect with you in the future.\n\n"
        "Website: grnt.media\n"
        "Telegram: @gruntmedia\n"
        "YouTube: youtube.com/@grntmedia\n"
        "Twitter: twitter.com/grntmedia 🌱\n\n"
        "If you have any questions, feel free to contact the tech admin: @megrunt"
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "This bot confirms you're a real Telegram user.\n"
        "It forwards your messages to admin and replies automatically."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Message from {user.first_name} (@{user.username}, id={user.id}):\n{text}"
    )
    await update.message.reply_text(
        "Hello! Your message has been received. We will reply soon.\n"
        "If you want to contact the admin immediately, write to @megrunt"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("info", info))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
