import logging
import os
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, MessageHandler, Updater

TOKEN = os.environ.get('TOKEN')


def example_handler(bot, update):
    # Remove this handler
    bot.send_message(
        update.message.chat_id,
        text='Hello from openshift'
    )

# Write your handlers here


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
    dp.add_handler(MessageHandler([], example_handler))  # Remove this line
    # Add your handlers here
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()