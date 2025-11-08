import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

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

user_context = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_context[user.id] = user.username or user.full_name
    await update.message.reply_text(FIRST_MESSAGE)
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"New user started the bot:\n{user.full_name} (@{user.username})\nID: {user.id}"
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This bot is for verification by Grnt Media.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    user_context[user.id] = user.username or user.full_name
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Message from {user.full_name} (@{user.username})\nID: {user.id}\n\n{text}"
    )
    await update.message.reply_text("Your message has been received by admin.")

async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /reply <user_id> <message>")
        return
    try:
        target_id = int(context.args[0])
        reply_text = " ".join(context.args[1:])
        await context.bot.send_message(chat_id=target_id, text=reply_text)
        await update.message.reply_text("Message sent successfully.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("info", info))
app.add_handler(CommandHandler("reply", admin_reply))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
