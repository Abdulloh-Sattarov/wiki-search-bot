import requests
import logging

from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler
from telegram.update import Update
from telegram.ext.filters import Filters

import settings

updater = Updater(token=settings.TELEGRAM_TOKEN)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)


def start(update: Update, context: CallbackContext):
    update.message.reply_text\
        ("Assalomu alaykum! Vikipediadan maʼlumot qidiruvchi"
         " botga hush kelibsiz! Biron nima izlash uchun /search"
         " va so‘rovingizni yozing. Misol uchun /search Elon Musk")


def search(update: Update, context: CallbackContext):
    args = " ".join(context.args)

    if len(args):
        logging.info('sending request to Wikipedia API')
        response = requests.get("https://uz.wikipedia.org/w/api.php", {
            'action': 'opensearch',
            'search': args,
            'limit': 1,
            'namespace': 0,
            'format': 'json',
        })
        logging.info('result from Wikipedia API')
        result = response.json()
        link = result[3]
        if len(link):
            update.message.reply_text('Sizning so‘rovingiz bo‘yicha havola: ' + link[0])
        else:
            update.message.reply_text('Sizning so‘rovingiz bo‘yicha hech nima topilmadi.')
    else:
        update.message.reply_text\
            ("Iltimos /search dan so'ng so'rovni kiriting. "
                                  "Masalan /search Elon Musk")


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('search', search))
dispatcher.add_handler(MessageHandler(Filters.all, start))

updater.start_polling()
updater.idle()