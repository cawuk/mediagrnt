import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_ID = 5536891599

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

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
    if update.message.from_user.id != ADMIN_ID:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"New user started bot:\nID: {update.message.from_user.id}\nUsername: @{update.message.from_user.username}"
        )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "This bot allows you to communicate directly with the admin."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_text = update.message.text

    if user_id != ADMIN_ID:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"Message from {user_id} (@{update.message.from_user.username}):\n{message_text}"
        )
    else:
        await update.message.reply_text("Admin messages must use /reply <user_id> <message>")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /reply <user_id> <message>")
        return

    try:
        user_id = int(context.args[0])
        reply_text = " ".join(context.args[1:])
        await context.bot.send_message(chat_id=user_id, text=reply_text)
        await update.message.reply_text(f"Message sent to {user_id}.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("reply", reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
