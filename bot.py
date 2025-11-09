import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot.")


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This bot is running successfully!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # Повідомлення адміну
    admin_msg = (
        f"📩 New message from {user.full_name} (@{user.username or 'no username'})\n"
        f"🆔 User ID: {user.id}\n\n"
        f"{text}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg)

    # Відповідь користувачу
    await update.message.reply_text(
        "Hi! Your message has been received, we will reply soon. "
        "If you want to contact the admin immediately, write to @megrunt."
    )


async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Команда: /reply <user_id> текст відповіді
    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /reply <user_id> <message>")
        return

    try:
        user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("User ID must be a number.")
        return

    reply_text = " ".join(context.args[1:])
    await context.bot.send_message(chat_id=user_id, text=reply_text)
    await update.message.reply_text("✅ Reply sent.")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("reply", reply_to_user))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
