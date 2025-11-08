from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_ID = 5536891599

users_seen = set()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "No username"

    if user_id not in users_seen:
        users_seen.add(user_id)
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

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"User started bot:\nID: {user_id}\nUsername: @{username}"
    )

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "No username"
    text = update.message.text

    if user_id not in users_seen:
        users_seen.add(user_id)
        await update.message.reply_text(
            "I'm a Telegram bot for verification by Grnt Media! ✅"
        )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Message from user:\nID: {user_id}\nUsername: @{username}\nMessage: {text}"
    )

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not update.message.reply_to_message:
        return  # адміністратор не відповідає на повідомлення користувача

    original_text = update.message.reply_to_message.text

    # шукаємо ID користувача в оригінальному повідомленні
    import re
    match = re.search(r"ID: (\d+)", original_text)
    if not match:
        await update.message.reply_text("Cannot find user ID in original message.")
        return

    target_id = int(match.group(1))
    reply_text = update.message.text

    await context.bot.send_message(chat_id=target_id, text=reply_text)
    await update.message.reply_text(f"Message sent to {target_id}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.Chat(ADMIN_ID) & filters.REPLY, handle_admin_reply))

    app.run_polling()
