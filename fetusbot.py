#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import random
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# global vars
QUOTES = ""
NUM_LINES = 0

quotesFile = "quotes.txt"
TOKEN = 'xxx'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def menu(bot, update):
    keyboard = [[InlineKeyboardButton("Add", callback_data='1'),
                 InlineKeyboardButton("Delete", callback_data='2')],

                [InlineKeyboardButton("Random Quote", callback_data='random_quote')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query

    respi = ''
    choice = ''

    if query.data == 'random_quote':
        choice = 'Random Quote'
        respi = random_quote(bot, update, False)
    elif query.data == 'Temperature':
        choice = 'Temperature'
        respi = temps(bot, update, False)
    elif query.data == 'poolaccount':
        # call with False status to allow response overdrive
        respi = money(bot, update, False)
    elif query.data == 'recentrounds':
        data = json.loads(json_url_reader(SP_STATS_URL))
        respi = data
        pprint(respi)
    elif query.data == 'RpiTemp':
        data = subprocess.Popen('/opt/vc/bin/vcgencmd measure_temp', \
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in data.stdout.readlines():
            respi = line
            print(line)
        data = check_output(['/opt/vc/bin/vcgencmd', 'measure_temp'])
        respi = data
        print(respi)
    elif query.data == 'Ant1':
        choice = miners[0]
        respi = getstatus(miners[0])
    elif query.data == 'AllMiners':
        respi = getstatus(query.data)
        print(respi)
    else:
        choice = 'Invalid choice!'

    print("Executed: " + choice)

    bot.edit_message_text(text="{}".format(respi),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          parse_mode="Markdown")


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """ Log Errors caused by Updates. """
    LOGGER.warning('Update "%s" caused error "%s"', update, error)

def random_quote(bot, update, status=True):
    """ Return random quote """
    rnd_q = random.choice(QUOTES)
    # debug
    print(rnd_q)
    if status:
        update.message.reply_text(text=rnd_q, parse_mode="Markdown")
        return None
    return rnd_q

def init_config():
    """ Initialize configruation (e.g. Telegram bot token) from config.json """
    with open('config.json') as json_cfg_file:
        config = json.load(json_cfg_file)
        print(config)
    return config

def init_quotes(file):
    """ Load quotes from a file to memory """
    with open(file, 'r') as quote_file:
        quotes = quote_file.readlines()

    global NUM_LINES

    with open(file, 'r') as f:
        for line in f:
            NUM_LINES += 1
    print("Read " + str(NUM_LINES) + " quotes into memory.")

    return quotes

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # init configure
    config = init_config()

    # read quotes
    global QUOTES
    QUOTES = init_quotes(quotesFile)

    updater.dispatcher.add_handler(CommandHandler('menu', menu))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('quote', random_quote))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
