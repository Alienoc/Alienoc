from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os

# Get the bot token from the environment
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text('Hi, welcome to Siekevitz\'s CC generator Bot!')

async def gen(update: Update, context: CallbackContext) -> None:
    """Handle the /gen command to generate card details"""
    # Implement your CC generation logic here
    pass

async def bin_info(update: Update, context: CallbackContext) -> None:
    """Handle the /bin command to fetch bin info"""
    # Implement bin info logic here using the API
    pass

def main():
    """Start the bot."""
    # Create the Application and pass the bot token
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("gen", gen))
    application.add_handler(CommandHandler("bin", bin_info))

    # Run the bot until you stop it
    application.run_polling()

if __name__ == '__main__':
    main()
