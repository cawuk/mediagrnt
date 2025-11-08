from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_ID = 5536891599  # замініть на ваш Telegram ID

FIRST_MESSAGE_TEXT = (
    "I'm a Telegram bot for verification by Grnt Media! ✅\n"
    "My job is to confirm that you're a real Telegram user.\n"
    "I will connect with you in the future.\n\n"
    "Website: grnt.media\n"
    "Telegram: @gruntmedia\n"
    "YouTube: youtube.com/@grntmedia\n"
    "Twitter: twitter.com/grntmedia 🌱\n\n"
    "If you have any questions, feel free to contact the tech admin: @megrunt"
)

users_seen = set()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "No username"

    if user_id not in users_seen:
        users_seen.add(user_id)
        await update.message.reply_text(FIRST_MESSAGE_TEXT)

    # Відправляємо адміну інформацію про всі повідомлення
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Message from user:\nID: {user_id}\nUsername: @{username}\nMessage: {update.message.text}"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
