from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update
import random

who_list = ['Edo', 'Ginalu', 'Jack', 'Andre', 'Lara', 'Gio', 'Samu',
            'Edoraptor', 'Il bruco', 'il Gay', 'Tua mamma', 'Laura', 'Signores Oscuros',
            'una puttana', 'sto cazzo', 'joe mama', 'Trump', 'Britney Bitch',
            'Lillo']

ans_list = ['Si', 'No', 'Ma figurati', 'Fatti furbo', 'Certo', 'Certamente', 'ehmm...', 'Fai un po te...', 'Col cazzo', 'Sicuro', 'Stanne certo',
            'La vedo dura', 'Mai dire mai', 'AHAHAHAHA', 'mmmm', 'Non rispondo', 'Mi astengo', 'Chiedi a tua madre', 'Ovvio', 'Ovvio che no', 'Sicuramente',
            'Certo che no', 'N\nO', 'SI SI...', 'Tu credici...', 'Vedrai ;)', 'Sono Positivo', 'Negativo', 'Damn Daniel...', 'Ti sei visto?',
            'Prova a richiedere', 'ahahaha emmm', 'Sei scemo?', 'Mi sa di si', 'Mi sa di no', 'Aspetta e spera', 'sni?', 'Due lettere:\nS\nI',
            'fatti un esame di coscienza', 'Chiedi a papino', 'Allora sei forte', 'Datti una sveglia', 'Sono Lillo!']

def who(update: Update, constext: CallbackContext)-> None:
    f = open('person.txt', 'r')
    who_list = f.read().split()
    
    chat_id = update.message.chat_id
    
    reply = random.choice(who_list).replace('_', ' ')
    update.message.reply_text(reply)
    
    print(update.message.text, reply)

def answer(update: Update, constext: CallbackContext)-> None:
    f = open('answer.txt', 'r')
    ans_list = f.read().split()
    
    chat_id = update.message.chat_id
    
    reply = random.choice(ans_list).replace('_', ' ')
    update.message.reply_text(reply)
    
    print(update.message.text, reply)