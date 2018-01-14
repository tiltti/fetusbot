#!/usr/bin/env python
""" Python Telegram Module """
# -*- coding: utf-8 -*-

import logging
import random
import json
import time
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# global vars
QUOTES = ""
TELEGRAM_BOT_TOKEN = ''

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def menu(bot, update):
    """ Display virtual buttons as menu """
    keyboard = [[InlineKeyboardButton("Add", callback_data='1'),
                 InlineKeyboardButton("Delete", callback_data='2')],

                [InlineKeyboardButton("Random Quote", callback_data='random_quote')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def log_menu_choice(query, choice):
    """ Log entry to screen, todo: file """
    log_entry(str(query.message.chat.username) + " executed menu item: " + choice)

def log_command_choice(choice):
    """ Log entry to screen, todo: file """
    log_entry("Unknown executed menu item: " + choice)

def log_entry(choice):
    """ Log entry to screen, todo: file """
    time_stamp = time.time()
    formatted_time_stamp = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    print("[" + formatted_time_stamp + "] " + choice)

def button(bot, update):
    """ Handler for 'button' presses """
    query = update.callback_query

    respi = ''
    choice = ''

    if query.data == 'random_quote':
        choice = 'Random Quote'
        respi = random_quote(bot, update, False)
    elif query.data == 'Temperature':
        choice = 'Temperature'
        respi = temps(bot, update, False)
    else:
        choice = 'Invalid choice!'

    log_menu_choice(query, choice)
    #print(query)

    bot.edit_message_text(text="{}".format(respi),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def help(bot, update):
    """ Help for bot """
    update.message.reply_text("Use /menu to see the options.")

def error(bot, update, error):
    """ Log Errors caused by Updates. """
    LOGGER.warning('Update "%s" caused error "%s"', update, error)

def random_quote(bot, update, status=True):
    """ Return random quote """
    rnd_q = random.choice(QUOTES)
    # debug
    #print(rnd_q)
    if status:
        update.message.reply_text(text=rnd_q)
        log_command_choice("Random Quote")
        return None
    return rnd_q

def init_config():
    """ Initialize configruation (e.g. Telegram bot token) from config.json """
    with open('config.json') as json_cfg_file:
        config = json.load(json_cfg_file)
    return config

def init_quotes(file):
    """ Load quotes from a file to memory """
    log_entry("Opening " + file)
    with open(file, 'r') as quote_file:
        quotes = quote_file.readlines()

    with open(file, 'r') as filu:
        num_lines = 0
        for line in filu:
            num_lines += 1
    log_entry("Read " + str(num_lines) + " quotes into memory.")

    return quotes

def main():
    """ Main Function """
    # init configure
    config = init_config()
    telegram_bot_token = config['telegram']['token']
    quotes_file = config['quote']['file']

    # read quotes
    global QUOTES
    QUOTES = init_quotes(quotes_file)

    # Create the Updater and pass it your bot's token.
    updater = Updater(telegram_bot_token)

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
