import logging
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter
import sys
import os
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

lanzaflex = os.environ.get('lanzaflex')
random.seed(a=None, version=2)
ammoniti = {}

class FilterLanza(BaseFilter):
    def filter(self, message):
        return 'Lanza?' in message.text

class FilterPrato(BaseFilter):
    def filter(self, message):
        return 'Prato' in message.text


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    if(context.message.reply_to_message.from_user.last_name != "Lanzarini"):
    	context.message.reply_text('Sono tornato merde!')
    else:
    	update.promote_chat_member(context.message.chat_id, context.message.from_user.id, can_restrict_members=True, can_promote_members=True )
    	context.message.reply_text('A RIOT!!!!')
    	
def taccuino(update, context):
    listaoutSTR = list()
    for item in ammoniti:
        if(ammoniti[item] == None):
            listaoutSTR.append(str(item))
        else:
            listaoutSTR.append(str(ammoniti[item]))
    listaoutSTR= "\n".join(str(x) for x in ammoniti)
    context.message.reply_text("Ecco il taccuino dell'arbitro:\n\n" + listaoutSTR)

def isAdministrator(update, context):
    if(update.get_chat_member(context.message.chat_id, context.message.reply_to_message.from_user.id).status == "creator"):
        context.message.reply_text("Il creatore")
    elif(update.get_chat_member(context.message.chat_id, context.message.reply_to_message.from_user.id).status == "administrator"):
        context.message.reply_text("Un amministratore")
    else: context.message.reply_text("Nope, persona inutile")


def ammonito(update, context):
    if(update.get_chat_member(context.message.chat_id, context.message.from_user.id).status == "creator" or update.get_chat_member(context.message.chat_id, context.message.from_user.id).status == "administrator"):
        global ammoniti
        #if(context.message.reply_to_message.from_user.id == 847018555):
        if(context.message.reply_to_message.from_user.is_bot == False):
            if context.message.reply_to_message.from_user.id in ammoniti:
                del ammoniti[context.message.reply_to_message.from_user.id]
                if(context.message.reply_to_message.from_user.last_name):
                    context.message.reply_to_message.reply_text("Attenzione, l'arbitro si avvicina a " + context.message.reply_to_message.from_user.last_name + " ed estrae il secondo cartellino giallo!\nOra " + context.message.reply_to_message.from_user.last_name + " dovra' abbandonare il terreno di gioco lasciando la sua squadra in svantaggio numerico")
                else:
                    context.message.reply_to_message.reply_text(str(context.message.reply_to_message.from_user.id) + " Pensava di fare il furbetto cancellando una parte delle sue informazioni, invece verra'  ammonito comunque! GIALLO!")
                if(context.message.reply_to_message.from_user.last_name != "Lanzarini"):
                	update.kick_chat_member(context.message.chat_id, context.message.reply_to_message.from_user.id)
            else:
                if(context.message.reply_to_message.from_user.last_name):
                    context.message.reply_to_message.reply_text("L'arbitro si avvicina a " + context.message.reply_to_message.from_user.last_name + " ed estrae il cartellino giallo!\nAnche oggi " + context.message.reply_to_message.from_user.last_name + " finira' sul taccuino dei cattivi")
                    ammoniti[context.message.reply_to_message.from_user.id] = context.message.reply_to_message.from_user.last_name
                else:
                    context.message.reply_text(str(context.message.reply_to_message.from_user.id) + " Pensava di fare il furbetto cancellando una parte delle sue informazioni, invece verra'  ammonito comunque! GIALLO!")
                ammoniti[context.message.reply_to_message.from_user.id] = "Furbetto"
    else:
        context.message.reply_text("Non sei amministratore, non ti devi permettere")

def espulso(update, context):
    if(update.get_chat_member(context.message.chat_id, context.message.from_user.id).status == "creator" or update.get_chat_member(context.message.chat_id, context.message.from_user.id).status == "administrator"):
        if(context.message.reply_to_message.from_user.is_bot == False or context.message.reply_to_message.from_user.last_name != "Lanzarini"):
            if(not context.message.reply_to_message.from_user.last_name):
                context.message.reply_to_message.reply_text(str(context.message.reply_to_message.from_user.id) + " voleva fare il furbetto, invece verrà espulso comunque")
            else:
                context.message.reply_to_message.reply_text("Ma no! Cosa e' preso a " + context.message.reply_to_message.from_user.last_name + "!\nL'arbitro si e' trovato costretto a sventolare il cartellino rosso!\nOra " + context.message.reply_to_message.from_user.last_name + " sara' costretto ad abbandonare il campo")
        update.kick_chat_member(context.message.chat_id, context.message.reply_to_message.from_user.id)

def grazia(update, context):
    if(update.get_chat_member(context.message.chat_id, context.message.from_user.id).status == "creator" or update.get_chat_member(context.message.chat_id, context.message.from_user.id).status == "administrator"):
        global ammoniti
        if context.message.reply_to_message.from_user.id in ammoniti.keys:
            del ammoniti[context.message.reply_to_message.from_user.id]
            if(context.message.reply_to_message.from_user.last_name):
                context.message.reply_to_message.reply_text(context.message.reply_to_message.from_user.last_name + " e' stato graziato")
            else:
                context.message.reply_to_message.reply_text(str(context.message.reply_to_message.from_user.id) + " e' stato graziato")
        else:
            if(context.message.reply_to_message.from_user.last_name)):
                context.message.reply_to_message.reply_text(context.message.reply_to_message.from_user.last_name + " e' un'anima pia, non ha bisogno della grazia")
            else:
                context.message.reply_to_message.reply_text(str(context.message.reply_to_message.from_user.id) + " e' un'anima pia, non ha bisogno della grazia") 

def help(update,context):
    """Send a message when the command /help is issued."""
    context.message.reply_text('Fottiti')

def max(update, context):
    """Send a message when the command /help is issued."""
    context.message.reply_to_message.reply_text('Se continui Max ti riempie di Bot')

def chatID(update, context):
#    context.message.reply_text(context.message.reply_to_message.from_user.id)
    context.message.reply_text("Ciao, " + context.message.from_user.first_name + "!\nIl tuo chat id in questo gruppo e' " +  str(context.message.from_user.id))

def lanza(update, context):
    global lanzaflex
    lanzaflex=lanzaflex + random.randint(0,20)
    context.message.reply_text("Lanza sta sollevando " + str(lanzaflex) + " kg")

def prato(update, context):
    context.message.reply_text("Forse volevi dire Verbano-Cusio-Ossola")

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':
    # Getting mode, so we could define run function for local and Heroku setup
    TOKEN = "847018555:AAHOHfC7Nj7zLMEo5leHE2knXoLZpnoifv4"
#    TOKEN = "612053408:AAFc6c6DZ_80zmFZ2YIy8pnXr0nzBjocXHU" #TilliBot
    updater = Updater(TOKEN)

    def run(updater):
            updater.start_polling(clean=True)
    logger.info("Starting bot")
    """Start the bot."""


    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    filter_lanza= FilterLanza()
    filter_prato=FilterPrato()
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

    dp.add_handler(MessageHandler(filter_lanza, lanza))
    dp.add_handler(MessageHandler(filter_prato, prato))


    # log all errors
    dp.add_error_handler(error)


    run(updater)