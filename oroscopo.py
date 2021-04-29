from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update
import random

Segni = ['Cancro', 'Toro', 'Acquario', 'Scorpione', 'Vergine', 'Gemelli']

Pianeti = ['Mercurio', 'Venere', 'Luna', 'Marte', 'Giove', 'Saturno', 'Nettuno', 'Urano', 'Plutone']

Costellazioni = ['Orione', 'Bilancia', 'Orsa Maggiore', 'Pleiadi', 'Andromeda', 'Balena', 'Bussola', 'Cane Maggiore',
                'Cane minore', 'Vergine', 'Cassiopea', 'Capricorno', 'Centauro', 'Delfino', 'Tua Mamma']

Effetti = ['in dominazione su', 'calante in', 'in contrapposizione con', 'in favore a', 'in sottomissione a', 'in calore per', 
            'incazzato con', 'ghosta', 'friendzona', 'egobusta', 'incula', 'si scopa', 'ci prova con',
            'picchia', 'fa amicizia con', 'spia', 'spara a', 'insegue', 'fischia a', 'si scaccola davanti a', 
            'è scocciato con', 'organizza una festa in', 'brilla su', 'fa il protagonista in', 'piange con', 'e stanco di',
            'ammira', 'attraversa', 'schiaffeggia']

def oro(update: Update, constext: CallbackContext)-> None:
    #update: Update, constext: CallbackContext
    chat_id = update.message.chat_id
    segno = random.choice(Segni)
    planet_1 = random.choice(Pianeti)
    cost = random.choice(Costellazioni)
    azione = random.choice(Effetti)
    ans = segno + ': ' + planet_1 + ' ' + azione + ' ' + cost+ '\n'


    f = open('frasifatte.txt', 'r')
    frasi_list = f.read().split()
    
    
    frase = random.choice(frasi_list).replace('_', ' ')
    ans += frase
    print(ans)
    f.close()
    update.message.reply_text(ans)
    
    print(update.message.text, reply)



if __name__ == '__main__':
    oro()

