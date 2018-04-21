from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
import logging
import config
import datetime
import csv
import os
import time


from text import location_text, faq_text, timetable, text_early, token_text, lineup_text, meet_text

os.environ['TZ'] = 'Europe/Moscow'
time.tzset()

telegram_token = config.telegram_token
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)

PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(telegram_token)
dispatcher = updater.dispatcher

start_keyboard = ('МЕСТО', 'FAQ', 'РАСПИСАНИЕ', 'ХЕДЛАЙНЕРЫ', 'КАНАЛ', 'ЧАТ', 'ССЫЛКИ')
links_keyboard = ('QUANTUM VK','QUANTUM FB','m_VK','m_INSTAGRAM','m_SOUNDCLOUD', '<< в начало')

map_pic = 'map_pic.jpg'

def start(bot, update):
    buttons_list = make_buttons_list(start_keyboard)
    menu = build_menu(buttons_list, 1)
    markup = InlineKeyboardMarkup(menu)
    bot.sendMessage(text = 'Добро пожаловать на Квант. Начало в 22.00. Место — BLANK, Арсенальная набережная, 1.', chat_id = update.message.chat.id, \
                    reply_markup=markup)
    record_user(user_id=update.message.chat.id)
    print(update.message.text)
    #botan.track(botan_token, update.message.chat.id,message=update.message.text)

def send(bot, update):
    print(1)
    print()
    if update.message.chxat.id == 47303188 and update.message.text == '1':
        user_ids = get_users()
        buttons_list = make_buttons_list(start_keyboard)
        menu = build_menu(buttons_list, 1)
        markup = InlineKeyboardMarkup(menu)
        print(user_ids)
        for user in user_ids:
            print(user)
            try:
                bot.sendMessage(text = meet_text, chat_id = int(user), \
                            reply_markup=markup)
            except:
                pass
def get_users():
    with open('users.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        user_ids = set()
        for row in csvreader:
            user_ids.add(row[2])
    return user_ids

def build_menu(buttons,n_cols,):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    return menu

def make_buttons_list(lst):
    buttons_list = []
    for a in lst:
        if a == 'FAQ':
            button = InlineKeyboardButton(a, url='http://telegra.ph/FAQ-Kvant-04-15')
        elif a == 'ХЕДЛАЙНЕРЫ':
            button = InlineKeyboardButton(a, url='http://telegra.ph/Hedlajnery-Kvant-04-15')
        elif a == 'КАНАЛ':
            button = InlineKeyboardButton(a, url='https://t.me/m_division')
        elif a == 'ЧАТ':
            button = InlineKeyboardButton(a, url='https://t.me/m_divisionchat')
        elif a == '<< назад':
            button = InlineKeyboardButton(a, callback_data='back_music')
        elif a == '<< в начало':
            button = InlineKeyboardButton(a, callback_data='back_main')
        elif a == 'QUANTUM VK':
            button = InlineKeyboardButton(a, url='https://vk.com/m_quantum')
        elif a == 'QUANTUM FB':
            button = InlineKeyboardButton(a, url='https://www.facebook.com/events/363814224126602/')
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
    lat = '59.954605'
    lng = '30.372228'
    if data == 'МЕСТО':
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
        bot.sendMessage(chat_id=query.message.chat.id, text=timetable, \
                        parse_mode='HTML', reply_markup=markup)

    elif data == 'ТОКЕНЫ':
        # menu = build_menu(buttons_list, 1)
        # markup = InlineKeyboardMarkup(menu)
        keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
        markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(chat_id=query.message.chat.id, text=token_text, \
                        parse_mode='HTML', reply_markup=markup)


    # elif data == 'FAQ':
    #     keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
    #     markup = InlineKeyboardMarkup(keyboard)
    #     bot.sendMessage(chat_id=query.message.chat.id, text=faq_text, parse_mode='HTML',reply_markup=markup)


    elif data == 'ИГРАЮТ СЕЙЧАС':
            pass

    elif data == 'ССЫЛКИ':
        buttons_list = make_buttons_list(links_keyboard)
        menu = build_menu(buttons_list, 1)
        markup = InlineKeyboardMarkup(menu)
        bot.sendMessage(chat_id=query.message.chat.id, text='Выберите ресурс:', \
                        parse_mode='HTML', reply_markup=markup)


    elif data == 'back_main':
        buttons_list = make_buttons_list(start_keyboard)
        menu = build_menu(buttons_list, 1)
        markup = InlineKeyboardMarkup(menu)
        bot.sendMessage(text='Добро пожаловать на Квант.', chat_id=query.message.chat.id, \
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
text_handler = MessageHandler(Filters.text, send)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(button_handler)
dispatcher.add_handler(text_handler)

if __name__ == '__main__':
    updater.start_polling()
