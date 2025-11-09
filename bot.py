import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I'm a Telegram bot for verification by Grnt Media! ✅\n"
        "My job is to confirm that you're a real Telegram user.\n"
        "I will connect with you in the future.\n\n"
        "Website: grnt.media\n"
        "Telegram: @gruntmedia\n"
        "YouTube: youtube.com/@grntmedia\n"
        "Twitter: twitter.com/grntmedia 🌱\n\n"
        "If you have any questions, feel free to contact the tech admin: @megrunt"
    )

# Повідомлення користувача ➜ адміну
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # Надсилаємо адміну
    admin_msg = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 Message from {user.first_name} (@{user.username or 'no_username'})\n"
             f"User ID: {user.id}\n\n{text}"
    )

    # Зберігаємо мапу повідомлень
    context.chat_data[admin_msg.message_id] = user.id

    # Відповідь користувачу
    await update.message.reply_text(
        "Hi! Your message has been received, we will reply soon. "
        "If you want to contact the admin immediately, write to @megrunt."
    )

# Відповідь адміна ➜ користувачу
async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return

    original_msg = update.message.reply_to_message
    # Дивимось, чи це реплай на повідомлення, що було від користувача
    if original_msg.message_id in context.chat_data:
        user_id = context.chat_data[original_msg.message_id]
        await context.bot.send_message(
            chat_id=user_id,
            text=f"💬 Reply from admin:\n\n{update.message.text}"
        )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Адмін реплай
    app.add_handler(MessageHandler(filters.TEXT & filters.Chat(chat_id=ADMIN_ID), handle_admin_reply))

    # Повідомлення користувачів
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    app.run_polling()

if __name__ == "__main__":
    main()
