import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I'm a Telegram bot for verification by Grnt Media! ✅\n"
        "My job is to confirm that you're a real Telegram user.\n"
        "I will connect with you in the future.\n\n"
        "🌐 Website: grnt.media\n"
        "💬 Telegram: @gruntmedia\n"
        "▶️ YouTube: youtube.com/@grntmedia\n"
        "🐦 Twitter: twitter.com/grntmedia\n\n"
        "If you have any questions, feel free to contact the tech admin: @megrunt"
    )

# Повідомлення користувача ➜ адміну
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # Створюємо повідомлення для адміна
    admin_msg = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"📩 *New message from user:*\n"
            f"👤 {user.first_name} (@{user.username or 'no_username'})\n"
            f"🆔 User ID: `{user.id}`\n\n"
            f"{text}"
        ),
        parse_mode="Markdown"
    )

    # Зберігаємо у глобальне сховище user_id для message_id
    if "message_map" not in context.bot_data:
        context.bot_data["message_map"] = {}
    context.bot_data["message_map"][admin_msg.message_id] = user.id

    # Відповідаємо користувачу
    await update.message.reply_text(
        "✅ Hi! Your message has been received, we will reply soon.\n"
        "If you want to contact the admin immediately, write to @megrunt."
    )

# Відповідь адміна ➜ користувачу
async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message is None:
        return

    original_msg = update.message.reply_to_message

    # Перевіряємо, чи є це реплаєм на повідомлення користувача
    message_map = context.bot_data.get("message_map", {})
    user_id = message_map.get(original_msg.message_id)

    if user_id:
        await context.bot.send_message(
            chat_id=user_id,
            text=f"💬 Reply from admin:\n\n{update.message.text}"
        )
        await update.message.reply_text("✅ Reply sent to user.")
    else:
        await update.message.reply_text("⚠️ Could not find user to reply to.")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Якщо пише адмін (реплай)
    app.add_handler(MessageHandler(filters.TEXT & filters.Chat(chat_id=ADMIN_ID), handle_admin_reply))

    # Якщо пише будь-який користувач
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    print("🚀 Bot started successfully!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
