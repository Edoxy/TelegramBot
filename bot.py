import random
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update
from get_token import get_token, get_key_alpha, get_key_yahoo
from stocks import InfoStock, DateCheck, GetData

from questions import answer, who, dove
from oroscopo import oro

import logging
import pandas as pd
import yfinance as yf
import time


# Inserisce i token e le API keys nelle costanti
TOKEN = get_token()
API_Y = get_key_yahoo()
API_A = get_key_alpha()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Ciao sono un bot inutile :). Per usare i miei comandi scrivi "/" e un comando. Per aiuto scrivi /help')

def _help(update: Update, constext: CallbackContext) -> None:

    text = "I possibili comandi sono:\n"
    text += "/set + #secondi : per settare un timer della durata speificata;\n\n"
    text += "/unset : per interrompere il timer prima del termine\n\n"
    text += "/stocks : per avere informazioni live sul mercato azionario\n\n"
    text += "/nostocks : per interrompere le informazioni\n\n"
    text += "/ans + 'una domanda' : per ricevere una risposta ad una domanda (si o no)\n\n"
    text += "/chi + 'una domanda' : per ricevere la risposta (persona)\n\n"

    update.message.reply_text(text)

def alarm(context):
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text='Beep... Beep!')
    context.bot.send_message(job.context, text='...')
    context.bot.send_message(job.context, text='BEEP BEEP!!')


def remove_job_if_exists(name, context):
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(
            alarm, due, context=chat_id, name=str(chat_id))

        text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)

# Returns message with stocks information
def Stock(context):
    job = context.job
    # calls the method that will process and create the message content
    textinfo = InfoStock()
    # sends the message only if the message is not empty
    if textinfo != 'info:\n':
        context.bot.send_message(job.context, text=textinfo)

#schedueler
def stocks(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    data = GetData('AAPL')
    if DateCheck(data):
        update.message.reply_text('This market is open and up to date')
        context.job_queue.run_repeating(
            Stock, 60, context=chat_id, name='stocks')
    else:
        update.message.reply_text(
            'Sorry, Market closed or the dataset is not up to date')


def stop_stocks(update: Update, context: CallbackContext) -> None:
    """Remove the job: Stocks updating"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists('stocks', context)
    text = 'Market updating stopped' if job_removed else 'Stock was not started'
    update.message.reply_text(text)

def main():
    upd = Updater(TOKEN, use_context=True)
    disp = upd.dispatcher

    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("help", _help))

    ##Timer commands
    disp.add_handler(CommandHandler("set", set_timer))
    disp.add_handler(CommandHandler("unset", unset))

    #Stocks commands
    disp.add_handler(CommandHandler("stocks", stocks))
    disp.add_handler(CommandHandler("nostocks", stop_stocks))

    #New Command
    disp.add_handler(CommandHandler("ans", answer))
    disp.add_handler(CommandHandler("chi", who))
    disp.add_handler(CommandHandler("dove", dove))
    disp.add_handler(CommandHandler("come", who))
    disp.add_handler(CommandHandler("hm", who))
    disp.add_handler(CommandHandler("oro", oro))

    upd.start_polling()

    upd.idle()


if __name__ == '__main__':
    main()
