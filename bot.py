from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
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
import chatbase

from texts import *

os.environ['TZ'] = 'Europe/Moscow'
time.tzset()

telegram_token = config.telegram_token
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# PORT = int(os.environ.get('PORT', '5000'))  # type: int
updater = Updater(telegram_token)
dispatcher = updater.dispatcher

start_keyboard = ('БИЛЕТЫ', 'ОПИСАНИЕ', 'РАСПИСАНИЕ', 'ВЫСТУПАЮТ СЕЙЧАС', 'ЧАТ')
continue_keyboard = ('ПРОДОЛЖИТЬ')
links_keyboard = ('VK EVENT', 'FB EVENT', 'm_VK', 'm_INSTAGRAM', 'm_SOUNDCLOUD', '<< в начало')
links_schedule = ('m_19Jul', 'm_20Jul', 'm_21Jul', 'm_22Jul', '<< в начало')

map_picture = 'map_gamma_pic.jpg'


def chatbase_log(chat_id, message, intent):
    chat_id_key = 18223618210808258664  # type: int # a 64-bit random number
    chat_id ^= chat_id_key
    chatbase_message = chatbase.Message(api_key=config.chatbase_token,
                                        platform="telegram",
                                        user_id=str(chat_id),
                                        message=message,
                                        intent=intent)
    chatbase_message.send()


def start(bot, update):
    chatbase_log(update.message.chat.id, "/start", "START")
    buttons_list = make_buttons_list(start_keyboard)
    menu = build_menu(buttons_list, 1)
    markup = InlineKeyboardMarkup(menu)
    bot.sendMessage(text=meet_text, chat_id=update.message.chat.id,
                    parse_mode='HTML', reply_markup=markup)
    record_user(user_id=update.message.chat.id)
    print(update.message.text)
    # botan.track(botan_token, update.message.chat.id,message=update.message.text)


def push(bot, update):
    print(1)
    print()

    buttons_list = [InlineKeyboardButton('РАСПИСАНИЕ', callback_data='РАСПИСАНИЕ'),
                    InlineKeyboardButton('ПРОДОЛЖИТЬ', callback_data='back_main')]
    markup = InlineKeyboardMarkup(build_menu(buttons_list, n_cols=1))
    push_text = push_text2

    if update.message.chat.id == 47303188 and update.message.text == 'push':
        user_ids = get_users()

        print(user_ids)
        count = 0
        for user in user_ids:
            try:
                bot.sendMessage(chat_id=int(user), text=push_text, parse_mode='HTML', reply_markup=markup,
                                disable_web_page_preview=True)

                # bot.sendMessage(text = push_final_text, chat_id = int(user), parse_mode='HTML', reply_markup=markup, disable_web_page_preview=True)
                count += 1
                print(user)
            except:
                pass
        print('sum')
        print(count)

    elif update.message.chat.id == 47303188 and update.message.text == 'test':
        user_ids = [47303188, ]

        for user in user_ids:
            bot.sendMessage(chat_id=int(user), text=push_text, parse_mode='HTML', reply_markup=markup,
                            disable_web_page_preview=True)


def get_users():
    with open('users.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        user_ids = set()
        for row in csvreader:
            user_ids.add(row[2])
    return user_ids


def build_menu(buttons, n_cols, ):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    return menu


def make_buttons_list(lst):
    buttons_list = []
    for a in lst:
        if a == 'FAQ':
            button = InlineKeyboardButton(a, callback_data='FAQ')
        elif a == 'БИЛЕТЫ':
            button = InlineKeyboardButton(a, url='https://radario.ru/widgets/mobile/549706')
        elif a == 'КАРТА GAMMA_MAIN':
            button = InlineKeyboardButton(a, callback_data='map')
        elif a == 'ЛОКАЦИИ':
            button = InlineKeyboardButton(a, url='https://telegra.ph/Lokacii-Gamma-2019-07-08')
        elif a == 'РАСПИСАНИЕ':
            button = InlineKeyboardButton(a, callback_data='РАСПИСАНИЕ')
        elif a == 'ОПИСАНИЕ':
            button = InlineKeyboardButton(a, url='https://teletype.in/@m_division/HJqLvxFCr')
        elif a == 'ВЕРСИЯ В TELEGRA.PH':
            button = InlineKeyboardButton(a, url='https://telegra.ph/Gamma-2019-07-08')
        elif a == 'ЧАТ':
            button = InlineKeyboardButton(a, url='https://t.me/joinchat/AtHKFEQZJqg0s0rqdoW_tQ')
        elif a == '<< назад':
            button = InlineKeyboardButton(a, callback_data='back_music')
        elif a == '<< в начало':
            button = InlineKeyboardButton(a, callback_data='back_main')
        elif a == 'ПРОДОЛЖИТЬ':
            button = InlineKeyboardButton(a, url='https://t.me/m_divisionbot')
        elif a == 'RSVP':
            button = InlineKeyboardButton(a,
                                          url='https://docs.google.com/forms/d/e/1FAIpQLSckYhvXDxlUiQfzUONzmyXDWuSg50z_R0VG8684PJ9oxgb-Eg/viewform')
        else:
            button = InlineKeyboardButton(a, callback_data=a)
        buttons_list.append(button)

    return buttons_list


def button(bot, update):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat.id
    lat = '59.954688'
    lng = '30.372135'
    if data == 'МЕСТО':
        chatbase_log(chat_id, "МЕСТО", "PLACE")
        keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
        markup = InlineKeyboardMarkup(keyboard)
        bot.sendLocation(chat_id=query.message.chat.id, latitude=lat, longitude=lng)
        bot.sendMessage(chat_id=query.message.chat.id, text=location_text, parse_mode='HTML',
                        reply_markup=markup, disable_web_page_preview=True)

    elif data == 'РАСПИСАНИЕ':
        chatbase_log(chat_id, "РАСПИСАНИЕ", "SCHEDULE")
        buttons_list = [[InlineKeyboardButton('<< в начало', callback_data='back_main'), ]]

        markup = InlineKeyboardMarkup(buttons_list)
        bot.sendMessage(chat_id=query.message.chat.id, text=timetable_text, \
                        parse_mode='HTML', disable_web_page_preview=True, reply_markup=markup)


    elif data == 'БИЛЕТЫ':

        buttons_list = [InlineKeyboardButton('КУПИТЬ БИЛЕТ', url='https://www.gammafestival.ru/delta'),
                        InlineKeyboardButton('МЕНЮ', callback_data='back_main')]
        markup = InlineKeyboardMarkup(build_menu(buttons_list, n_cols=1))
        bot.sendMessage(chat_id=query.message.chat.id, text=tickets_text, \
                        parse_mode='HTML', reply_markup=markup)

    elif data == 'ИНФОРМАЦИЯ':
        buttons_list = [[InlineKeyboardButton('<< в начало', callback_data='back_main'), ]]
        markup = InlineKeyboardMarkup(buttons_list)
        bot.sendPhoto(chat_id=query.message.chat.id, photo=open(inttech_pic, 'rb'))
        bot.sendMessage(chat_id=query.message.chat.id, text=info_text, parse_mode='HTML', reply_markup=markup,
                        disable_web_page_preview=True)

    elif data == 'ТОКЕНЫ':
        chatbase_log(chat_id, "ТОКЕНЫ", "TOKENS")
        # menu = build_menu(buttons_list, 1)
        # markup = InlineKeyboardMarkup(menu)
        keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
        markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(chat_id=query.message.chat.id, text=token_text, \
                        parse_mode='HTML', reply_markup=markup)

    elif data == 'tickets':
        chatbase_log(chat_id, 'tickets', 'TICKETS')
        buttons_list = [[InlineKeyboardButton('<< в начало', callback_data='back_main'),
                         InlineKeyboardButton('КУПИТЬ', url='https://radario.ru/widgets/mobile/385838')]]

        markup = InlineKeyboardMarkup(buttons_list)
        print(markup)
        bot.sendMessage(chat_id=query.message.chat.id, text=tickets_text, parse_mode='HTML', reply_markup=markup)


    elif data == 'FAQ':
        keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
        markup = InlineKeyboardMarkup(keyboard)
        bot.sendMessage(chat_id=query.message.chat.id, text=faq_text, parse_mode=ParseMode.HTML, reply_markup=markup)


    elif data == 'ИГРАЮТ СЕЙЧАС' or data == 'ВЫСТУПАЮТ СЕЙЧАС':
        chatbase_log(chat_id, "ВЫСТУПАЮТ СЕЙЧАС", "PLAYING NOW")
        keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
        markup = InlineKeyboardMarkup(keyboard)
        now_text = playing_now()
        bot.sendMessage(chat_id=query.message.chat.id, text=now_text,
                        parse_mode='HTML', reply_markup=markup)

    elif data == 'ССЫЛКИ':
        chatbase_log(chat_id, "ССЫЛКИ", "LINKS")
        buttons_list = make_buttons_list(links_keyboard)
        menu = build_menu(buttons_list, 1)
        markup = InlineKeyboardMarkup(menu)
        bot.sendMessage(chat_id=query.message.chat.id, text='Выберите ресурс:', \
                        parse_mode='HTML', reply_markup=markup)

    elif data == 'map':
        keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
        markup = InlineKeyboardMarkup(keyboard)
        # bot.sendPhoto(chat_id=query.from_user.id, photo=open(map_picture, 'rb'))
        text = map_text  # type: str
        bot.sendMessage(chat_id=query.from_user.id, text=text, reply_markup=markup)


    elif data == 'back_main':
        chatbase_log(chat_id, "В НАЧАЛО", "START")
        buttons_list = make_buttons_list(start_keyboard)
        menu = build_menu(buttons_list, 1)
        markup = InlineKeyboardMarkup(menu)
        bot.sendMessage(text=meet_text, chat_id=query.message.chat.id, \
                        reply_markup=markup, parse_mode='HTML')


def get_artists(data):
    artists = []

    with open('schedule.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if row[0] == data:
                artists.append(row)
    return artists


def make_text(artists):
    text = ''
    for artist in artists:
        scene = '\n' + '<b>' + artist[1] + '</b>\n'
        if scene not in text:
            text += scene
        text = text + '<b>' + artist[2] + '</b> '
        text = text + artist[3] + '\n'
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
    return file_name.split("+")[2][:-4].strip()


"""
(time, artist, [description])
"""


def format_artist(entry):
    time = entry[0]
    artist = entry[1]
    description = entry[2]

    text = time.strftime("<b>%H:%M - " + artist + "</b>")
    if description != "":
        text += "\n" + description

    return text


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


def stage_order():
    schedule_files = sorted(glob.glob("data/*.csv"))
    stage_order = []
    for file in schedule_files:
        stage = file.split("+")[-1][:-4].strip()
        stage_order.append(stage)

    stage_order = [x for i, x in enumerate(stage_order) if stage_order.index(x) == i]
    return stage_order


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
                event_description = ""
                if len(row) > 2:
                    event_description = row[2]

                schedule[scene].append((event_datetime, event_name, event_description))

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
                # print(row[1])
                event_name = row[1]

                if event_time < previous_time:
                    reached_tomorrow = True

                current_date = tomorrow_date if reached_tomorrow else today_date
                event_datetime = datetime.datetime.combine(current_date, event_time)
                event_description = ""
                if len(row) > 2:
                    event_description = row[2]

                schedule[scene].append((event_datetime, event_name, event_description))

                previous_time = event_time

    # print(schedule)

    DAY_THRESHOLD = datetime.time(14, 0)

    STAGES_ORDER = stage_order()
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
                result += format_artist(first_entry)

        if today_string != "2018.07.19":
            pass
            # result += "\n"
            # result += "\nНа основе официального расписания."
        return result


    else:
        result = playing_now_text
        for stage in STAGES_ORDER:
            if stage in schedule:
                first_entry = schedule[stage][0]
                if first_entry[0] > time:
                    result += "\n\n<b>" + stage + "</b>\n"
                    result += format_artist(first_entry)
                else:
                    current_entry = first_entry
                    for next_entry in schedule[stage][1:]:
                        if next_entry[0] >= time:
                            result += "\n\n<b>" + stage + "</b>\n"
                            result += format_artist(current_entry) + "\n"
                            result += format_artist(next_entry)
                            if next_entry[1] == "перерыв":
                                i = schedule[stage][1:].index(next_entry)
                                after_break_entry = schedule[stage][1:][i + 1]
                                result += "\n" + format_artist(after_break_entry)

                            break

                        current_entry = next_entry

        result += "\n"

        if result == playing_now_text + "\n":  # all the stages have finished
            result = over_text + "\n"

        if today_string != "2018.07.19":
            result += '\n'
        return result


def playing_now():
    return playing_at(datetime.datetime.now())


def help(bot, update):
    keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
    markup = InlineKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id=update.message.chat.id, text=help_text, parse_mode='HTML',
                    reply_markup=markup, disable_web_page_preview=True)


def handle_message(bot, update):
    chat_id = update.message.chat.id

    buttons_list = make_buttons_list()
    menu = build_menu(buttons_list, 1)
    markup = InlineKeyboardMarkup(menu)
    bot.sendMessage(text=test_suite(), chat_id=chat_id, reply_markup=markup)


def now_command(bot, update):
    chat_id = update.message.chat.id
    chatbase_log(chat_id, "/now", "PLAYING NOW")
    keyboard = [[InlineKeyboardButton('<< в начало', callback_data='back_main')]]
    markup = InlineKeyboardMarkup(keyboard)
    now_text = playing_now()
    bot.sendMessage(chat_id=chat_id, text=now_text, \
                    parse_mode='HTML', reply_markup=markup)


start_handler = CommandHandler('start', start)
button_handler = CallbackQueryHandler(button)
text_handler = MessageHandler(Filters.text, push)
now_handler = CommandHandler('now', now_command)
help_handler = CommandHandler('help', help)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(button_handler)
dispatcher.add_handler(text_handler)
dispatcher.add_handler(now_handler)
dispatcher.add_handler(help_handler)

if __name__ == '__main__':
    updater.start_polling()
