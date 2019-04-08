import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter
import sys
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

lanzaflex=0
ammoniti = list()

class FilterLanza(BaseFilter):
    def filter(self, message):
        return 'Lanza?' in message.text

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    context.message.reply_text('Hi!')
    
def taccuino(update, context):
    listaout= "\n".join(str(x) for x in ammoniti)
    context.message.reply_text("Ecco il taccuino dell'arbitro:\n\n" + listaout)

def isAdministrator(update, context):
    if(update.get_chat_member(context.message.chat_id, context.message.reply_to_message.from_user.id).status == "creator"):
        context.message.reply_text("Il creatore")
    elif(update.get_chat_member(context.message.chat_id, context.message.reply_to_message.from_user.id).status == "administrator"):
        context.message.reply_text("Un amministratore")
    else: context.message.reply_text("Nope, persona inutile")
#    administratorList = update.get_chat_administrators(context.message.chat_id)
#    print(administratorList)
#    administratorListString = list()
#    for item in administratorList:
#        administratorListString.append(administratorList[item.user.last_name])
#    print(administratorList)
    
def ammonito(update, context):
    if(update.get_chat_member(context.message.chat_id, context.message.from_user.id).status == "creator" or update.get_chat_member(context.message.chat_id, context.message.from_user.id).status == "administrator"):
        global ammoniti
        #if(context.message.reply_to_message.from_user.id == 847018555):
        if(context.message.reply_to_message.from_user.is_bot == False):
            if context.message.reply_to_message.from_user.last_name in ammoniti:
                ammoniti.remove(context.message.reply_to_message.from_user.last_name)
                context.message.reply_text("Attenzione, l'arbitro si avvicina a " + context.message.reply_to_message.from_user.first_name + " " + context.message.reply_to_message.from_user.last_name + " ed estrae il secondo cartellino giallo!\nOra " + context.message.reply_to_message.from_user.first_name + " dovra' abbandonare il terreno di gioco lasciando la sua squadra in svantaggio numerico")
                update.kick_chat_member(context.message.chat_id, context.message.reply_to_message.from_user.id)
            else:
                ammoniti.append(context.message.reply_to_message.from_user.last_name)
                context.message.reply_text("L'arbitro si avvicina a " + context.message.reply_to_message.from_user.first_name + " " + context.message.reply_to_message.from_user.last_name + " ed estrae il cartellino giallo!\nAnche oggi " + context.message.reply_to_message.from_user.first_name + " finira' sul taccuino dei cattivi")
    else:
        context.message.reply_text("Non sei amministratore, non ti devi permettere")

def espulso(update, context):
    if(update.get_chat_member(context.message.chat_id, context.message.from_user.id).status == "creator" or update.get_chat_member(context.message.chat_id, context.message.from_user.id).status == "administrator"):
        if(context.message.reply_to_message.from_user.is_bot == False):
            context.message.reply_text("Ma no! Cosa e' preso a " + context.message.reply_to_message.from_user.first_name + " " + context.message.reply_to_message.from_user.last_name + "!\nL'arbitro si e' trovato costretto a sventolare il cartellino rosso!\nOra " + context.message.reply_to_message.from_user.last_name + " sara' costretto ad abbandonare il campo")
            update.kick_chat_member(context.message.chat_id, context.message.reply_to_message.from_user.id)
                    
def grazia(update, context):  
    if(update.get_chat_member(context.message.chat_id, context.message.from_user.id).status == "creator" or update.get_chat_member(context.message.chat_id, context.message.from_user.id).status == "administrator"):
        global ammoniti
        if context.message.reply_to_message.from_user.last_name in ammoniti:
            ammoniti.remove(context.message.reply_to_message.from_user.last_name)
            context.message.reply_text(context.message.reply_to_message.from_user.last_name + " e' stato graziato")
        else:
            context.message.reply_text(context.message.reply_to_message.from_user.last_name + " e' un'anima pia, non ha bisogno della grazia")

def help(update, context):
    """Send a message when the command /help is issued."""
    context.message.reply_text('Fottiti')

def max(update, context):
    """Send a message when the command /help is issued."""
    context.message.reply_text('Se continui Max ti riempie di Bot')
    
def chatID(update, context):
#    context.message.reply_text(context.message.reply_to_message.from_user.id)
    context.message.reply_text("Ciao, " + context.message.from_user.first_name + "!\nIl tuo chat id in questo gruppo e' " +  str(context.message.from_user.id))

def lanza(update, context):
    global lanzaflex
    lanzaflex=lanzaflex+2
    context.message.reply_text("Lanza sta sollevando " + str(lanzaflex) + " kg")

    """def echo(context, update):"""
    """update.message.reply_text(update.message.text)"""


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':
    # Getting mode, so we could define run function for local and Heroku setup
    mode = "dev"
    TOKEN = "847018555:AAHOHfC7Nj7zLMEo5leHE2knXoLZpnoifv4"
    updater = Updater(TOKEN)
    if mode == "dev":
        def run(updater):
            updater.start_polling(clean=True)
    elif mode == "prod":
        def run(updater):
            PORT = int("8443")
            HEROKU_APP_NAME = "doublecheckbot"
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
            updater.start_webhook(listen="0.0.0.0",
                                  port=PORT,
                                  url_path=TOKEN)
            updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
    else:
        logger.error("No MODE specified!")
        sys.exit(1)
    logger.info("Starting bot")
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    filter_lanza= FilterLanza()
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("max", max))
    dp.add_handler(CommandHandler("chatID", chatID))
    dp.add_handler(CommandHandler("ammonito", ammonito))
    dp.add_handler(CommandHandler("taccuino", taccuino))
    dp.add_handler(CommandHandler("isAdministrator", isAdministrator))
    dp.add_handler(CommandHandler("grazia", grazia))
    dp.add_handler(CommandHandler("espulso", espulso))
    #lanzastr="Lanza"
    dp.add_handler(MessageHandler(filter_lanza, lanza))

    #dp.add_handler(CommandHandler("member", member))
    #dp.add_handler(MessageHandler(Filters.text, lanza))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
#    updater.start_polling(clean=True)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    run(updater)