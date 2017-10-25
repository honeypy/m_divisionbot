from telegram import InlineKeyboardButton, InlineKeyboardMarkup

start_keyboard = ('Location','Music','Art', 'Channel', 'Community Chat','Help')

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def make_buttons_list(lst):
    buttons_list = []
    for a in lst:
        button = InlineKeyboardButton(a,callback_data=a)
        buttons_list.append(button)
    return buttons_list

buttons_list = make_buttons_list(start_keyboard)
menu = build_menu(buttons_list,1)
