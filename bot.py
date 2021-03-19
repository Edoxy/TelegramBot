
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update
from get_token import Get_token
from stocks import InfoStock, DateCheck, GetData

import logging
import exchange
import pandas as pd
import yfinance as yf
import time


# IMPORTANTE: inserire il token fornito dal BotFather nella seguente stringa
TOKEN, api_key = Get_token()


def extract_number(text):
    return text.split()[1].strip()


def convert_usd(update, context):
    usd = float(extract_number(update.message.text))
    eur = exchange.from_usd_to_eur(usd)
    print(f'Eseguita conversione da {usd} USD a {eur} EUR')
    update.message.reply_text(f'{eur} EUR')


def convert_eur(update, context):
    eur = float(extract_number(update.message.text))
    usd = exchange.from_eur_to_usd(eur)
    print(f'Eseguita conversione da {eur} EUR a {usd} USD')
    update.message.reply_text(f'{usd} USD')


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Use /set <seconds> to set a timer\n/stocks to see market status')


def alarm(context):
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text='Beep Cazzo!')
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

    disp.add_handler(CommandHandler("usd", convert_usd))
    disp.add_handler(CommandHandler("eur", convert_eur))

    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("help", start))
    disp.add_handler(CommandHandler("set", set_timer))
    disp.add_handler(CommandHandler("unset", unset))

    #stocks commands
    disp.add_handler(CommandHandler("stocks", stocks))
    disp.add_handler(CommandHandler("nostocks", stop_stocks))

    upd.start_polling()

    upd.idle()


if __name__ == '__main__':
    main()
