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
import logging
import datetime
import time
import os
import csv
import glob


from text import *

os.environ['TZ'] = 'Europe/Moscow'
time.tzset()

telegram_token = config.telegram_token
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level= logging.INFO)

PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(telegram_token)
dispatcher = updater.dispatcher

start_keyboard = ('МЕСТО', 'FAQ', 'РАСПИСАНИЕ', 'ИГРАЮТ СЕЙЧАС', 'АРТИСТЫ', 'КАНАЛ', 'ЧАТ')
links_keyboard = ('GAMMA VK','GAMMA FB','m_VK','m_INSTAGRAM','m_SOUNDCLOUD', '<< в начало')

map_pic = 'map_pic.jpg'

def start(bot, update):
    buttons_list = make_buttons_list(start_keyboard)
    menu = build_menu(buttons_list, 1)
    markup = InlineKeyboardMarkup(menu)
    bot.sendMessage(text = 'Добро пожаловать на Gamma 2018', chat_id = update.message.chat.id, \
                    reply_markup=markup)
    record_user(user_id=update.message.chat.id)
    print(update.message.text)
    #botan.track(botan_token, update.message.chat.id,message=update.message.text)

def send(bot, update):
    print(1)
    print()
    if update.message.chat.id == 47303188 and update.message.text == '1':
        user_ids = get_users()
        buttons_list = make_buttons_list(start_keyboard)
        menu = build_menu(buttons_list, 1)
        markup = InlineKeyboardMarkup(menu)
        print(user_ids)
        for user in user_ids:
            print(user)
            try:
                bot.sendMessage(text = meet_text, chat_id = int(user), reply_markup=markup)
            except:
                pass
    elif update.message.chat.id == 47303188 and update.message.text == '2':
        user_ids = get_users()
        buttons_list = make_buttons_list(start_keyboard)
        menu = build_menu(buttons_list, 1)
        markup = InlineKeyboardMarkup(menu)
        print(user_ids)
        for user in user_ids:
            print(user)
            try:
                bot.sendMessage(text='Если «FAQ» и «Артисты» не открываются, нажмите снова /start', chat_id=int(user), reply_markup=markup)
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
            button = InlineKeyboardButton(a, url='https://zen.yandex.ru/media/id/5b473690bbc36f00a8b583b7/faq-gamma-2018-5b47369d3d0e9500a9a83328')
        elif a == 'АРТИСТЫ':
            button = InlineKeyboardButton(a, url='https://zen.yandex.ru/media/id/5b473690bbc36f00a8b583b7/artisty-gamma-2018-5b473824a4dd5400a75237e9')
        elif a == 'КАНАЛ':
            button = InlineKeyboardButton(a, url='https://t.me/m_division')
        elif a == 'ЧАТ':
            button = InlineKeyboardButton(a, url='https://t.me/m_divisionchat')
        elif a == '<< назад':
            button = InlineKeyboardButton(a, callback_data='back_music')
        elif a == '<< в начало':
            button = InlineKeyboardButton(a, callback_data='back_main')
        elif a == 'GAMMA VK':
            button = InlineKeyboardButton(a, url='https://vk.com/gammafestival2018')
        elif a == 'GAMMA FB':
            button = InlineKeyboardButton(a, url='https://www.facebook.com/gammaspb/')
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
    lat = '59.911202'
    lng = '30.266454'
    if data == 'МЕСТО':
        keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
        markup = InlineKeyboardMarkup(keyboard)
        #bot.sendLocation(chat_id=query.message.chat.id, latitude=lat, longitude=lng)
        bot.sendMessage(chat_id=query.message.chat.id, text=location_text, parse_mode='HTML',
                        reply_markup=markup, disable_web_page_preview=True)

    elif data == 'РАСПИСАНИЕ':
        #menu = build_menu(buttons_list, 1)
        #markup = InlineKeyboardMarkup(menu)
        keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
        markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(chat_id=query.message.chat.id, text=timetable_text, \
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

        keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
        markup = InlineKeyboardMarkup(keyboard)
        now_text = playing_now()
        bot.sendMessage(chat_id=query.message.chat.id, text=now_text, \
                        parse_mode='HTML', reply_markup=markup)

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
        bot.sendMessage(text='Добро пожаловать на Gamma 2018.', chat_id=query.message.chat.id, \
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


def format_date(datetime):
    return datetime.strftime("%Y.%m.%d")


def format_datetime(datetime):
    return datetime.strftime("%Y.%m.%d %H:%M")


def parse_time(time_string):
    try:
        return datetime.datetime.strptime(time_string, "%H:%M").time()
    except:
        print("parse_time: wrond time " + time_string)

def parse_datetime(datetime_string):
    return datetime.datetime.strptime(datetime_string, "%Y.%m.%d %H:%M")


def scene_name(file_name):
    return file_name.split("-")[2][:-4].strip()


def format_artist(time, artist):
    return time.strftime("<b>%H:%M</b> - " + artist)


def test_suite():
    report = ""

    time = datetime.datetime(2018, 5, 25, 18, 00)
    expected = no_event_text
    report += test_case(time, expected)

    time = datetime.datetime(2018, 5, 26, 11, 00)
    expected = starting_soon_text + """

beta stage:
16:00 - Galich

gamma stage:
22:00 - Eye Que b2b naya

omega stage:
22:00 - Lluck
"""

    report += test_case(time, expected)

    time = datetime.datetime(2018, 5, 26, 15, 00)
    # same expected value
    report += test_case(time, expected)

    time = datetime.datetime(2018, 5, 26, 16, 00)
    expected = playing_now_text + """

beta stage:
16:00 - Galich
17:30 - ArkadyAir

gamma stage:
22:00 - Eye Que b2b naya

omega stage:
22:00 - Lluck
"""

    report += test_case(time, expected)

    time = datetime.datetime(2018, 5, 26, 16, 5)
    # same expected value
    report += test_case(time, expected)

    time = datetime.datetime(2018, 5, 27, 8, 40)
    expected = playing_now_text + """

beta stage:
08:30 - Anrilov b2b Bvoice
12:00 - окончание

gamma stage:
07:00 - Kobba
09:00 - окончание

omega stage:
07:30 - Lena Popova
09:00 - Cultkitchen
"""

    report += test_case(time, expected)

    time = datetime.datetime(2018, 5, 27, 9, 10)
    expected = playing_now_text + """

beta stage:
08:30 - Anrilov b2b Bvoice
12:00 - окончание

omega stage:
09:00 - Cultkitchen
12:00 - окончание
"""
    report += test_case(time, expected)

    time = datetime.datetime(2018, 5, 27, 12, 00)
    # same expected value
    report += test_case(time, expected)

    time = datetime.datetime(2018, 5, 27, 12, 20)
    expected = over_text + "\n"
    report += test_case(time, expected)

    time = datetime.datetime(2018, 5, 27, 19, 20)
    # same expected value
    report += test_case(time, expected)

    return report


def test_case(time, expected):
    report = time.strftime("\n\n%Y.%m.%d %H:%M:\n")
    actual = playing_at(time)
    if actual == expected:
        report += "Test passed\n\n" + actual
    else:
        report += "Test failed\n\nActaul result:\n" + actual + "\nExpected result:\n" + expected
        print(actual)
        print(expected)
        import difflib
        expected = expected.splitlines(1)
        actual = actual.splitlines(1)
        diff = difflib.unified_diff(expected, actual)
        print(''.join(diff))

    return report


def test(bot, update, args):
    chat_id = update.message.chat.id
    if len(args) == 0:
        bot.sendMessage(text=test_suite(), chat_id=chat_id)
    else:
        time = ' '.join(args)
        report = "Playing at " + time + "\n"
        report += playing_at(parse_datetime(time))
        bot.sendMessage(text=report, chat_id=chat_id, parse_mode='HTML')


def playing_at(time):
    today_string = format_date(time)
    today_files = glob.glob("data/*" + today_string + "*.csv")

    yesterday = time - datetime.timedelta(days=1)
    tomorrow = time + datetime.timedelta(days=1)

    today_date = time.date()
    yesterday_date = yesterday.date()
    tomorrow_date = tomorrow.date()

    yesterday_string = format_date(yesterday)
    yesterday_files = glob.glob("data/*" + yesterday_string + "*.csv")

    if len(today_files) == len(yesterday_files) == 0:
        return no_event_text

    schedule = {}

    for file in yesterday_files:
        scene = scene_name(file)
        if not scene in schedule:
            schedule[scene] = []

        reached_today = False

        with open(file, newline='') as csvfile:
            previous_time = datetime.time(0, 0)
            scene_reader = csv.reader(csvfile)
            for row in scene_reader:
                # print(row)
                event_time = parse_time(row[0])
                event_name = row[1]

                if event_time < previous_time:
                    reached_today = True

                current_date = today_date if reached_today else yesterday_date
                event_datetime = datetime.datetime.combine(current_date, event_time)
                schedule[scene].append((event_datetime, event_name))

                previous_time = event_time

    for file in today_files:
        scene = scene_name(file)
        if not scene in schedule:
            schedule[scene] = []

        reached_tomorrow = False

        with open(file, newline='') as csvfile:
            previous_time = datetime.time(0, 0)
            scene_reader = csv.reader(csvfile)
            for row in scene_reader:
                # print(row)
                event_time = parse_time(row[0])
                event_name = row[1]

                if event_time < previous_time:
                    reached_tomorrow = True

                current_date = tomorrow_date if reached_tomorrow else today_date
                event_datetime = datetime.datetime.combine(current_date, event_time)
                schedule[scene].append((event_datetime, event_name))

                previous_time = event_time

    # print(schedule)


    DAY_THRESHOLD = datetime.time(14, 0)

    # TODO: find out dynamically
    STAGES_ORDER = ["ОТКРЫТИЕ", "GAMMA_PRO", "MAIN", "TERRACE"]

    started = False
    for scene in schedule:
        if time >= schedule[scene][0][0]:
            started = True
            break

    if not started:
        result = starting_soon_text
        for stage in STAGES_ORDER:
            if stage in schedule:
                first_entry = schedule[stage][0]
                result += "\n\n<b>" + stage + "</b>\n"
                result += format_artist(first_entry[0], first_entry[1])

        if today_string != "2018.07.19":
            result += "\n"
            result += "\nНа основе официального расписания."
        return result


    else:
        result = playing_now_text
        for stage in STAGES_ORDER:
            if stage in schedule:
                first_entry = schedule[stage][0]
                if first_entry[0] > time:
                    result += "\n\n<b>" + stage + "</b>\n"
                    result += format_artist(first_entry[0], first_entry[1])
                else:
                    current_entry = first_entry
                    for next_entry in schedule[stage][1:]:
                        if next_entry[0] >= time:
                            result += "\n\n<b>" + stage + "</b>\n"
                            result += format_artist(current_entry[0], current_entry[1]) + "\n"
                            result += format_artist(next_entry[0], next_entry[1])
                            if next_entry[1] == "перерыв":
                                i = schedule[stage][1:].index(next_entry)
                                after_break_entry = schedule[stage][1:][i+1]
                                result += "\n" + format_artist(after_break_entry[0], after_break_entry[1])

                            break

                        current_entry = next_entry

        result += "\n"

        if result == playing_now_text + "\n":  # all the stages have finished
            result = over_text + "\n"

        if today_string != "2018.07.19":
            result += '\nНа основе официального расписания.'
        return result


def playing_now():
    return playing_at(datetime.datetime.now())





def handle_message(bot, update):
    chat_id = update.message.chat.id

    buttons_list = make_buttons_list()
    menu = build_menu(buttons_list, 1)
    markup = InlineKeyboardMarkup(menu)
    bot.sendMessage(text=test_suite(), chat_id=chat_id, reply_markup=markup)


def play_command(bot, update):
    keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
    markup = InlineKeyboardMarkup(keyboard)
    now_text = playing_now()
    bot.sendMessage(chat_id=update.message.chat.id, text=now_text, \
                    parse_mode='HTML', reply_markup=markup)


start_handler = CommandHandler('start', start)
button_handler = CallbackQueryHandler(button)
text_handler = MessageHandler(Filters.text, send)
now_handler = CommandHandler('now', play_command)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(button_handler)
dispatcher.add_handler(text_handler)
dispatcher.add_handler(now_handler)

if __name__ == '__main__':
    updater.start_polling()
