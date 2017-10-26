from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
import logging
import config
import datetime
import csv

from text import location_text, faq_text

telegram_token = config.telegram_token

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)

PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(telegram_token)
dispatcher = updater.dispatcher

start_keyboard = ('МЕСТО ПРОВЕДЕНИЯ', 'FAQ', 'РАСПИСАНИЕ', 'ИГРАЮТ СЕЙЧАС', 'КАНАЛ', 'ЧАТ', 'ССЫЛКИ')
links_keyboard = ('MYSTERY VK','MYSTERY FB','m_VK','m_INSTAGRAM','m_SOUNDCLOUD', '<< в начало')

def start(bot, update):
    buttons_list = make_buttons_list(start_keyboard)
    menu = build_menu(buttons_list, 1)
    markup = InlineKeyboardMarkup(menu)
    bot.sendMessage(text = 'Добро пожаловать на Mystery 2017', chat_id = update.message.chat.id, \
                    reply_markup=markup)
    record_user(user_id=update.message.chat.id)
    print(update.message.text)
    #botan.track(botan_token, update.message.chat.id,message=update.message.text)

def build_menu(buttons,n_cols,):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    return menu

def make_buttons_list(lst):
    buttons_list = []
    for a in lst:
        if a == 'FAQ':
            button = InlineKeyboardButton(a, url='http://telegra.ph/FAQ-Mystery-2017-10-26')
        elif a == 'КАНАЛ':
            button = InlineKeyboardButton(a, url='https://t.me/m_division')
        elif a == 'ЧАТ':
            button = InlineKeyboardButton(a, url='https://t.me/m_divisionchat')
        elif a == '<< назад':
            button = InlineKeyboardButton(a, callback_data='back_music')
        elif a == '<< в начало':
            button = InlineKeyboardButton(a, callback_data='back_main')
        elif a == 'MYSTERY VK':
            button = InlineKeyboardButton(a, url='https://vk.com/m_mystery2017')
        elif a == 'MYSTERY FB':
            button = InlineKeyboardButton(a, url='https://www.facebook.com/events/768576016675791/')
        elif a == 'm_VK':
            button = InlineKeyboardButton(a, url='https://vk.com/mdivisiongroup')
        elif a == 'm_INSTAGRAM':
            button = InlineKeyboardButton(a, url='https://www.instagram.com/m_division/')
        elif a == 'm_SOUNDCLOUD':
            button = InlineKeyboardButton(a, url='https://soundcloud.com/mdivision/')
        else:
            button = InlineKeyboardButton(a,callback_data=a)
        buttons_list.append(button)

    return buttons_list


def button(bot, update):
    query = update.callback_query
    data = query.data
    lat = '59.911079'
    lng = '30.267228'
    if data == 'МЕСТО ПРОВЕДЕНИЯ':
        keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
        markup = InlineKeyboardMarkup(keyboard)
        bot.sendLocation(chat_id=query.message.chat.id, latitude=lat, longitude=lng)
        bot.sendMessage(chat_id=query.message.chat.id, text=location_text, parse_mode='HTML',
                        reply_markup=markup)

    elif data == 'РАСПИСАНИЕ':
        #menu = build_menu(buttons_list, 1)
        #markup = InlineKeyboardMarkup(menu)
        keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
        markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(chat_id=query.message.chat.id, text='Информация скоро появится.', \
                        parse_mode='HTML', reply_markup=markup)

    elif data == 'FAQ':
        keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
        markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(chat_id=query.message.chat.id, text=faq_text, parse_mode='HTML',reply_markup=markup)


    elif data == 'ИГРАЮТ СЕЙЧАС':
        keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
        markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(chat_id=query.message.chat.id, text='Информация скоро появится.', parse_mode='HTML',
                        reply_markup=markup)
        #botan.track(botan_token, query.message.chat.id, message=query.message.text)

    elif data == 'КАРТА':
        keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
        markup = InlineKeyboardMarkup(keyboard)
        bot.sendPhoto(chat_id=query.from_user.id, photo=open(map_picture, 'rb'))
        bot.sendPhoto(chat_id=query.from_user.id, photo=open(map_picture2, 'rb'))
        bot.sendPhoto(chat_id=query.from_user.id, photo=open(map_picture3, 'rb'))
        bot.sendMessage(chat_id=query.from_user.id, text='Расположение объектов', reply_markup=markup)

    elif data == 'ССЫЛКИ':
        buttons_list = make_buttons_list(links_keyboard)
        menu = build_menu(buttons_list, 1)
        markup = InlineKeyboardMarkup(menu)
        bot.sendMessage(chat_id=query.message.chat.id, text='Выберите ресурс:', \
                        parse_mode='HTML', reply_markup=markup)


    elif data  == 'back_music':
        buttons_list = make_buttons_list(dates_keyboard)
        menu = build_menu(buttons_list, 1)
        markup = InlineKeyboardMarkup(menu)
        bot.sendMessage(chat_id=query.message.chat.id, text='Выберите день:', \
                        parse_mode='HTML', reply_markup=markup)

    elif data == 'back_main':
        buttons_list = make_buttons_list(start_keyboard)
        menu = build_menu(buttons_list, 1)
        markup = InlineKeyboardMarkup(menu)
        bot.sendMessage(text='Добро пожаловать на Mystery 2017', chat_id=query.message.chat.id, \
                        reply_markup=markup)


def get_artists(data):
    artists = []

    with open('schedule.csv','r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if row[0] == data:
                artists.append(row)
    return artists


def make_text(artists):
    text = ''
    for artist in artists:
        scene = '\n'+'<b>'+artist[1]+'</b>\n'
        if scene not in text:
            text += scene
        text = text + '<b>' + artist[2] + '</b> '
        text = text + artist[3]+'\n'
        # text = text+ '('+artist[4] + ')'
        # text += artist[5] + '\n'
    return text


def record_user(user_id):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open('users.csv', 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['start', now, user_id])


start_handler = CommandHandler('start', start)
button_handler = CallbackQueryHandler(button)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(button_handler)


if __name__ == '__main__':
    updater.start_polling()
