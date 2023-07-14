from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from .open_json import get_orders_data, check_if_logined, get_login, get_orders_msg
from .keyboards import get_orders_kb, back_inline_kb


async def cmd_start(update : Update, context : ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привіт! Це бот інтернет магазину розетка. У цьому боті ви можете зайти в свій акаунт розетки, і подивитися інформацію про своє замовлення.')


async def help(update : Update, context : ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''
Ось список команд, які вам можуть бути потробні:
1) /register <логін> <пароль> - зареєструвати свій акаунт;
2) /login <логін> <пароль> - увійти в свій акаунт;
3) Мої замовлення - це кнопка знизу, під клавіатурою щоб подивитися інформацію про свої замовлення.''')


async def send_order_data(update : Update, context : ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    login = get_login(user_id)
    order_id = update.callback_query.data.split()[1]

    order_data = get_orders_data(login)[str(order_id)]

    item_name = order_data['item_name']
    arrival_time = order_data['arrival_time']
    price = order_data['price']
    delivery_price = order_data['delivery_price']


    msg = f'Назва товару - {item_name}, ціна(з доставкою) - {price + delivery_price}, орієнтовна дата прибуття - {arrival_time}'
    query = update.callback_query
    inline_kb = back_inline_kb()

    await query.edit_message_text(text = msg, reply_markup=inline_kb)



async def send_orders(update : Update, context : ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if get_orders_msg(user_id) != False:
        msg = get_orders_msg(user_id)[0]

    else:
        await update.message.reply_text('Ви ще не ввійшли в акаунт')
        return ...

    orders = get_orders_msg(user_id)[1]
    reply_kb_markup = get_orders_kb(orders, user_id)
    query = update.callback_query

    if query == None:
        await update.message.reply_text(msg, reply_markup= reply_kb_markup)
    
    else:
        await query.edit_message_text(msg, reply_markup= reply_kb_markup)


def get_handlers():

    return [
        CommandHandler('start', cmd_start),
        CommandHandler('help', help),
        MessageHandler(filters.Text('Подивитися свої замовлення'), send_orders),
        CallbackQueryHandler(callback= send_orders, pattern='back'),
        CallbackQueryHandler(callback= send_order_data)

    ]
