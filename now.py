
import logging
import datetime
import time
import os
import csv
import glob

from texts import *

os.environ['TZ'] = 'Europe/Moscow'
time.tzset()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def format_date(datetime):
    return datetime.strftime("%Y.%m.%d")


def format_datetime(datetime):
    return datetime.strftime("%Y.%m.%d %H:%M")


def parse_time(time_string):
    return datetime.datetime.strptime(time_string, "%H:%M").time()


def parse_datetime(datetime_string):
    return datetime.datetime.strptime(datetime_string, "%Y.%m.%d %H:%M")


def scene_name(file_name):
    return file_name.split("-")[2][:-4].strip()


def format_artist(time, artist):
    return time.strftime("%H:%M - " + artist)


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
        bot.sendMessage(text=report, chat_id=chat_id)


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
    STAGES_ORDER = ["MAIN", "SANCTUM"]

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
                result += "\n\n" + stage + ":\n"
                result += format_artist(first_entry[0], first_entry[1])

        result += "\n"
        return result


    else:
        result = playing_now_text
        for stage in STAGES_ORDER:
            if stage in schedule:
                first_entry = schedule[stage][0]
                if first_entry[0] > time:
                    result += "\n\n" + stage + ":\n"
                    result += format_artist(first_entry[0], first_entry[1])
                else:
                    current_entry = first_entry
                    for next_entry in schedule[stage][1:]:
                        if next_entry[0] >= time:
                            result += "\n\n" + stage + ":\n"
                            result += format_artist(current_entry[0], current_entry[1]) + "\n"
                            result += format_artist(next_entry[0], next_entry[1])

                            break

                        current_entry = next_entry

        result += "\n"

        if result == playing_now_text + "\n":  # all the stages have finished
            result = over_text + "\n"

        return result


def playing_now():
    return playing_at(datetime.datetime.now())


def start(bot, update):
    chat_id = update.message.chat.id

    buttons_list = make_buttons_list()
    menu = build_menu(buttons_list, 1)
    markup = InlineKeyboardMarkup(menu)
    bot.sendMessage(text=playing_now(), chat_id=chat_id, reply_markup=markup)


def build_menu(buttons, n_cols):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    return menu


def make_buttons_list():
    buttons_list = [InlineKeyboardButton("Обновить", callback_data='update')]

    return buttons_list


def button(bot, update):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat.id

    if data == 'update':
        buttons_list = make_buttons_list()
        menu = build_menu(buttons_list, 1)
        markup = InlineKeyboardMarkup(menu)
        bot.sendMessage(text=playing_now(), chat_id=query.message.chat.id, reply_markup=markup)


def handle_message(bot, update):
    chat_id = update.message.chat.id

    buttons_list = make_buttons_list()
    menu = build_menu(buttons_list, 1)
    markup = InlineKeyboardMarkup(menu)
    bot.sendMessage(text=test_suite(), chat_id=chat_id, reply_markup=markup)


start_handler = CommandHandler('start', start)
button_handler = CallbackQueryHandler(button)
text_handler = MessageHandler(Filters.text, handle_message)
test_handler = CommandHandler('test', test, pass_args=True)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(button_handler)
dispatcher.add_handler(text_handler)
dispatcher.add_handler(test_handler)

if __name__ == '__main__':
    updater.start_polling()