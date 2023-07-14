from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler

def send_order_data():
    ...

def get_orders_kb(orders, user_id):
    inline_kb_buttons = [
        
    ]
    
    handlers = []
    new_kb = []
    num = 0


    for order_id, order_data in orders.items():
        item_name = order_data['item_name']

        new_kb.append(InlineKeyboardButton(text=item_name, callback_data=f'{user_id} {order_id}'))
        
        if len(new_kb) == 3:
            inline_kb_buttons.append(new_kb)
            new_kb = []


    if new_kb not in inline_kb_buttons:
        inline_kb_buttons.append(new_kb)
    

    return InlineKeyboardMarkup(inline_kb_buttons)


def back_inline_kb():
    inline_kb = [[InlineKeyboardButton(text='Назад', callback_data='back')]]

    return InlineKeyboardMarkup(inline_kb)


def start_reply_kb():
    reply_kb = [['/help']]

    return ReplyKeyboardMarkup(reply_kb, resize_keyboard=True)


def login_reply_kb():
    reply_kb = [['/help', 'Вийти з акаунту'], ['Подивитися свої замовлення']]

    return ReplyKeyboardMarkup(reply_kb, resize_keyboard=True)