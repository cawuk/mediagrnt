import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = 5536891599

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot.")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm a Telegram bot for verification by Grnt Media!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # Відповідь користувачу
    await update.message.reply_text(
        "Hello! Your message has been received, we will reply soon. "
        "If you want to contact the admin immediately, write to @megrunt."
    )

    # Пересилання адміну
    admin_text = f"Message from {user.full_name} (@{user.username}, id={user.id}):\n{text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
