import logging
import os
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, MessageHandler, Updater

TOKEN = os.environ.get('TOKEN')


def help(update, context):
    """Send a message when the command /help is issued."""
    context.message.reply_text('Fottiti')

# Write your handlers here


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    
    updater = Updater(TOKEN)
    bot = updater.bot
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("help", help))
    # Add your handlers here
    
    bot.set_webhook()  # Delete webhook
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    setup()