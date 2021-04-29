from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update
import random

def who(update: Update, constext: CallbackContext)-> None:
    f = open('person.txt', 'r')
    who_list = f.read().split()
    
    chat_id = update.message.chat_id
    
    reply = random.choice(who_list).replace('_', ' ')
    update.message.reply_text(reply)
    f.close()
    print(update.message.text, reply)

def answer(update: Update, constext: CallbackContext)-> None:
    f = open('answer.txt', 'r')
    ans_list = f.read().split()
    
    chat_id = update.message.chat_id
    
    reply = random.choice(ans_list).replace('_', ' ')
    update.message.reply_text(reply)
    f.close()
    print(update.message.text, reply)

def dove(update: Update, constext: CallbackContext)-> None:
    f = open('luoghi.txt', 'r')
    ans_list = f.read().split()
    
    chat_id = update.message.chat_id
    
    reply = random.choice(ans_list).replace('_', ' ')
    update.message.reply_text(reply)
    f.close()
    print(update.message.text, reply)
