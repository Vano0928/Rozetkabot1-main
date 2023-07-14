from telegram import InlineKeyboardButton, InlineKeyboardMarkup
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
        num += 1
        
        if num == 2:
            inline_kb_buttons.append(new_kb)
            num = 0

    if new_kb not in inline_kb_buttons:
        inline_kb_buttons.append(new_kb)
    

    return InlineKeyboardMarkup(inline_kb_buttons)


def back_inline_kb():
    inline_kb = [[InlineKeyboardButton(text='Назад', callback_data='back')]]

    return InlineKeyboardMarkup(inline_kb)
