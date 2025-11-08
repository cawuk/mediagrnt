import os
import asyncio
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 5536891599

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Hello, {user.first_name}! 👋\nThe bot is active and ready ✅")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a simple verification bot. Type anything and I'll reply 😉")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")
    msg = f"📩 From @{user.username or user.first_name} (ID: {user.id}):\n{text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

async def set_commands(application):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Show help message"),
    ]
    await application.bot.set_my_commands(commands)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.post_init = set_commands
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
